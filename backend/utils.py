import math
import httpx
import logging
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


async def clarify_address(address: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"Fix and standardize this address: '{address}'"}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.warning(f"OpenAI fallback: {e}")
        return address


async def geocode(address: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": address, "format": "json", "limit": 1},
            headers={"User-Agent": "AI-Distance-Calc/1.0"}
        )
        if res.status_code == 200:
            data = res.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
    return None


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))
