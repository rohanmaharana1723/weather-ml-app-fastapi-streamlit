import streamlit as st
import requests
import pandas as pd

# OpenWeatherMap API setup
API_KEY = '2cd887781e28691cabbbffe5546bda84'  # Replace with your actual key
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Function to fetch weather data
def get_weather(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            'city': city.title(),
            'description': data['weather'][0]['description'].title(),
            'icon': data['weather'][0]['icon'],
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'wind': data['wind']['speed'],
            'wind_deg': data['wind'].get('deg', 0),
            'precip': data.get('rain', {}).get('1h', 0)
        }
    else:
        return None

# Format rich description
def format_description(data):
    temp = round(data['temp'])
    feels = round(data['feels_like'])
    desc = data['description']
    wind = data['wind']
    humidity = data['humidity']
    precip = data['precip']

    wind_desc = "breezy" if wind > 4 else "calm"
    humidity_desc = "humid" if humidity > 70 else "dry"
    rain_desc = f"{precip} mm rain" if precip > 0 else "no rain"

    return f"{desc} with {wind_desc} winds and {humidity_desc} air. Feels like {feels}°C with {rain_desc}."

# Generate placeholder temperature trend
def generate_temp_trend(current_temp):
    return [round(current_temp + i * 0.5 - 1.5, 1) for i in range(6)]

# Streamlit UI
def main():
    st.set_page_config(page_title="BBC Weather Dashboard", layout="wide", page_icon="🌦️")
    st.title("🌍Weather Dashboard")
    st.markdown("Type city names to view live weather cards with rich descriptions and temperature charts.")

    # Sidebar input
    city_input = st.sidebar.text_input("Enter city names (comma-separated)", "Leeds, Watford, Aberfoyle")
    cities = [c.strip() for c in city_input.split(",") if c.strip()]

    if not cities:
        st.warning("Please enter at least one city.")
        return

    cols = st.columns(len(cities))

    for col, city in zip(cols, cities):
        data = get_weather(city)
        if data:
            with col:
                st.markdown(f"### 📍 {data['city']}")
                st.image(f"http://openweathermap.org/img/wn/{data['icon']}@2x.png", width=80)
                st.markdown(f"**{format_description(data)}**")
                st.metric(label="🌡️ Temperature", value=f"{data['temp']} °C")
                st.metric(label="💧 Humidity", value=f"{data['humidity']}%")
                st.metric(label="🌬️ Wind Speed", value=f"{data['wind']} m/s")

                # Line chart for temperature trend
                st.markdown("#### 📈 Temperature Trend (Next 6 Hours)")
                hours = ['Now', '1hr', '2hr', '3hr', '4hr', '5hr']
                temps = generate_temp_trend(data['temp'])
                chart_df = pd.DataFrame({'Hour': hours, 'Temperature (°C)': temps})
                st.line_chart(chart_df.set_index('Hour'))
        else:
            col.error(f"Could not load weather for {city}")

if __name__ == "__main__":
    main()