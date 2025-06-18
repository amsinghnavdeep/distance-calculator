# AI-Powered Distance Calculator Web Application

![App Screenshot](https://github.com/user-attachments/assets/f87f02e6-e623-44b8-b554-0e4a6e177ab1)

A modern, AI-enhanced web application to calculate the distance between two addresses. It uses the Haversine formula to compute accurate distances, geocodes addresses using OpenStreetMap, and optionally corrects/standardizes inputs with OpenAI's ChatGPT API. Users can view a searchable history of previous queries stored in a PostgreSQL database.

---

## System Design Overview

This application is designed using a clean and modular architecture:

- **Frontend (HTML, CSS, JavaScript):** Handles user interactions and displays results.
- **Backend (FastAPI):** Processes inputs, performs geocoding, applies the Haversine formula, and interacts with the database.
- **Database (PostgreSQL):** Stores query history with timestamps and computed distances.
- **External Services:**
  - **OpenStreetMap Nominatim API** for geocoding (converting addresses to coordinates).
  - **OpenAI GPT API (optional)** to intelligently suggest valid address formats or correct input errors.

---

##  Features

- Enter a source and destination address  
- Choose distance unit: kilometers, miles, or both  
- Calculate distance in real-time  
- Stores historical data of previous queries  
- Fetch and display the last 10 distance calculations  
- Friendly error messages for invalid inputs or API issues  
- Optional AI enhancement for validating/correcting unclear addresses  
- Fully Dockerized for local or cloud deployment  
- **Testable backend with unit and API tests** 

---

##  Tech Stack

| Layer         | Technology                     |
|---------------|--------------------------------|
| Frontend      | HTML, CSS, JavaScript          |
| Backend       | Python (FastAPI)               |
| API Calls     | OpenStreetMap (Nominatim API)  |
| AI (Optional) | OpenAI ChatGPT (for address fix) |
| Database      | PostgreSQL                     |
| Infrastructure| Docker, Docker Compose         |

---

##  How It Works

1. **User Input**  
   The user enters two address fields (source and destination) via a web form.

2. **Address Correction (optional)**  
   If enabled, the backend uses OpenAI GPT API to suggest corrected versions of input addresses.

3. **Geocoding**  
   The backend calls the Nominatim API to retrieve latitude and longitude for each address.

4. **Distance Calculation**  
   The Haversine formula is applied to the geocoordinates to calculate distance (in km or miles).

5. **Persistence**  
   The query is saved to PostgreSQL with source, destination, distance, and timestamp.

6. **Response**  
   The calculated result is returned to the frontend and displayed to the user.

7. **History Retrieval**  
   Users can view a list of the 10 most recent queries in a formatted table.

---

##  Project Structure


distance-calculator/
 backend/
    app.py              # FastAPI application
    utils.py            # Geocoding, distance, AI logic
    test.py             # Test suite (unit + integration)
    requirements.txt    # Python dependencies
    Dockerfile          # Backend Docker build
 frontend/
    index.html          # Main UI page
    style.css           # Styling
    script.js           # Client-side logic
    nginx.conf          # Nginx proxy config
    Dockerfile          # Frontend Docker build
 docker-compose.yml      # Orchestrates services
 README.md               # This file


---

##  Running Tests

###  Run tests locally:

1. Install dependencies:
   bash
   cd backend
   pip install -r requirements.txt
   pip install pytest
   

2. Run the tests:
   bash
   pytest test.py
   

This runs unit tests (e.g., Haversine function) and API endpoint tests (/calculate, /history).

###  Run tests inside Docker:

If desired, modify your backend/Dockerfile to include:
dockerfile
RUN pip install pytest


Then:

bash
docker-compose run backend pytest test.py


 **Expected output:**

test.py .....   [100%]


---

##  How to Run the App

> Make sure Docker and Docker Compose are installed on your machine.

### 1. Clone the Repository

bash
git clone https://github.com/amsinghnavdeep/distance-calculator
cd distance-calculator


### 2. Set Environment Variables

Create a .env file or update your docker-compose.yml:

env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://user:password@db:5432/geo


### 3. Start the App

bash
docker-compose up --build


Then open: [http://localhost](http://localhost)

---

##  API Endpoints

| Endpoint     | Method | Description                          |
|--------------|--------|--------------------------------------|
| /calculate | POST   | Calculates distance between addresses |
| /history   | GET    | Returns last 10 stored queries       |

### Example Request:
json
{
  "source": "Toronto",
  "destination": "Montreal",
  "unit": "km"
}


---

##  Optional: OpenAI Address Correction

To use AI-enhanced location input:

1. Add OPENAI_API_KEY to your environment.
2. The app will automatically clarify vague inputs before geocoding.

---

##  UI Preview

![image](https://github.com/user-attachments/assets/88dbb766-2a1d-4aca-ad6b-6fb5b192d8be)

---

##  Future Enhancements

-  Map visualization (Leaflet/Google Maps)
-  Authenticated user query history
-  Export queries to CSV
-  Public rate limiting
-  Mobile-first UI layout

---