from utils import haversine, geocode, clarify_address
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from functools import lru_cache
import math, os, logging
import asyncpg, httpx, openai

openai.api_key = os.getenv("openApi-key")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/geo")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
logging.basicConfig(level=logging.INFO)

@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.create_pool(DATABASE_URL)
    async with app.state.db.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id SERIAL PRIMARY KEY,
                source TEXT,
                destination TEXT,
                distance_km DOUBLE PRECISION,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

class DistanceRequest(BaseModel):
    source: str
    destination: str
    unit: str = "km"

@lru_cache(maxsize=1000)
async def geocode(address: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": address, "format": "json", "limit": 1},
            headers={"User-Agent": "AI-Distance-Calc/1.0"}
        )
        if r.status_code == 200:
            data = r.json()
            if data: return float(data[0]["lat"]), float(data[0]["lon"])
    return None

async def correct_address(prompt: str):
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"Fix and standardize this address: '{prompt}'"}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.warning(f"OpenAI fallback: {e}")
        return prompt

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in KM
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

@app.post("/calculate")
async def calculate_distance(req: DistanceRequest):
    src = await correct_address(req.source)
    dst = await correct_address(req.destination)
    src_coords = await geocode(src)
    dst_coords = await geocode(dst)

    if not src_coords or not dst_coords:
        raise HTTPException(status_code=400, detail="Could not geocode address(es)")

    dist_km = haversine(*src_coords, *dst_coords)
    async with app.state.db.acquire() as conn:
        await conn.execute(
            "INSERT INTO queries (source, destination, distance_km) VALUES ($1, $2, $3)",
            src, dst, dist_km
        )
    return {
        "source": src,
        "destination": dst,
        "distance_km": round(dist_km, 2),
        "distance_miles": round(dist_km * 0.621371, 2)
    }

@app.get("/history")
async def get_history():
    async with app.state.db.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM queries ORDER BY created_at DESC LIMIT 10")
    return [{"source": r["source"], "destination": r["destination"], "distance_km": r["distance_km"]} for r in rows]
