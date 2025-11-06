from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import requests
import pickle
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load your model
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    print("❌ Model loading failed:", e)

# Your OpenWeatherMap API key
OPENWEATHER_API_KEY = "2cd887781e28691cabbbffe5546bda84"

# Input schema for prediction
class WeatherInput(BaseModel):
    Humidity: float
    Pressure: float
    Temp: float
    MaxTemp: float
    MinTemp: float
    WindGustSpeed: float
    WindGustDir: float

# Get live weather data from OpenWeatherMap
@app.get("/weather")
def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found or API error")
    
    data = response.json()
    weather = {
        "Humidity": data["main"]["humidity"],
        "Pressure": data["main"]["pressure"],
        "Temp": data["main"]["temp"],
        "MaxTemp": data["main"]["temp_max"],
        "MinTemp": data["main"]["temp_min"],
        "WindGustSpeed": data["wind"].get("gust", 0),
        "WindGustDir": data["wind"].get("deg", 0)
    }
    return weather

@app.get("/predict_weather")
def predict_weather(city: str):
    # Your ML prediction logic here
    return {"city": city, "prediction": "sunny"}  # Example response
