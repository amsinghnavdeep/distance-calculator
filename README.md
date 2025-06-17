
# Distance Calculator App
![2a7864e7-9609-4928-a2df-9b936f9c593f](https://github.com/user-attachments/assets/f87f02e6-e623-44b8-b554-0e4a6e177ab1)
## System Design Overview
This project is a distance calculator web application designed using a clean, modular architecture. The frontend is built with HTML, CSS, and JavaScript to provide a responsive and interactive user interface for entering addresses and viewing results. The backend uses FastAPI, a modern and efficient Python web framework, to handle requests, perform geolocation via the OpenStreetMap Geocoding API, calculate the distance using the Haversine formula, and store historical queries. All past calculations are saved in a PostgreSQL database, providing persistent storage for user query history. This design separates concerns across layers, making it scalable, maintainable, and easy to extend with features like authentication, logging, or alternative map APIs in the future.

This is a simple web application that calculates the distance between two addresses using the Nominatim API.

## Features

- Enter a source and destination address
- Calculate distance between them
- View history of past queries
- Error handling for invalid inputs or API failures

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (FastAPI)
- **Database**: PostgreSQL
- **Optional**: OpenAI for address correction

## How to Run
2. **Locally Run**:
   docker-compose up --build
2. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/distance-calculator.git
   cd distance-calculator

   
