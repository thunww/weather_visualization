import requests
import pandas as pd
import logging
from datetime import datetime
from dotenv import load_dotenv
import os
from typing import Optional, Dict
from database import save_to_database

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Tải biến môi trường
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")

def validate_inputs(city: str, api_key: str) -> bool:
    """Kiểm tra đầu vào hợp lệ."""
    if not city or not isinstance(city, str):
        logger.error("City name must be a non-empty string.")
        return False
    if not api_key:
        logger.error("API Key not found.")
        return False
    return True

def fetch_openweather_data(city: str, api_key: str) -> Optional[Dict]:
    """Gọi API OpenWeatherMap để lấy dữ liệu thời tiết."""
    if not validate_inputs(city, api_key):
        return None
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logger.info(f"Successfully fetched OpenWeatherMap data for {city}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching OpenWeatherMap data for {city}: {e}")
        return None

def fetch_weatherapi_data(city: str, api_key: str) -> Optional[Dict]:
    """Gọi WeatherAPI để lấy dữ liệu thời tiết."""
    if not validate_inputs(city, api_key):
        return None
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=5&aqi=no&alerts=no"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logger.info(f"Successfully fetched WeatherAPI data for {city}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching WeatherAPI data for {city}: {e}")
        return None

def process_weather_data(city: str) -> Optional[pd.DataFrame]:
    """Xử lý dữ liệu từ cả hai API và hợp nhất."""
    weather_info = {
        "date": [],
        "temperature": [],
        "humidity": [],
        "precipitation": [],
        "wind_speed": [],
        "pressure": [],
        "weather_description": [],
        "source": []
    }

    # Lấy dữ liệu từ OpenWeatherMap
    ow_data = fetch_openweather_data(city, OPENWEATHER_API_KEY)
    if ow_data and ow_data.get("cod") == "200":
        for entry in ow_data["list"]:
            weather_info["date"].append(entry["dt_txt"])
            weather_info["temperature"].append(entry["main"]["temp"])
            weather_info["humidity"].append(entry["main"]["humidity"])
            weather_info["precipitation"].append(entry.get("rain", {}).get("3h", 0.0))
            weather_info["wind_speed"].append(entry["wind"]["speed"])
            weather_info["pressure"].append(entry["main"]["pressure"])
            weather_info["weather_description"].append(entry["weather"][0]["description"])
            weather_info["source"].append("OpenWeatherMap")

    # Lấy dữ liệu từ WeatherAPI
    wa_data = fetch_weatherapi_data(city, WEATHERAPI_KEY)
    if wa_data and "forecast" in wa_data:
        for day in wa_data["forecast"]["forecastday"]:
            for hour in day["hour"]:
                weather_info["date"].append(hour["time"])
                weather_info["temperature"].append(hour["temp_c"])
                weather_info["humidity"].append(hour["humidity"])
                weather_info["precipitation"].append(hour.get("precip_mm", 0.0))
                weather_info["wind_speed"].append(hour["wind_kph"] / 3.6)  # Chuyển km/h sang m/s
                weather_info["pressure"].append(hour["pressure_mb"])
                weather_info["weather_description"].append(hour["condition"]["text"])
                weather_info["source"].append("WeatherAPI")

    if weather_info["date"]:
        df = pd.DataFrame(weather_info)
        df["city"] = city
        save_to_database(df, city)
        logger.info(f"Processed data for {city} with {len(df)} records")
        return df
    else:
        logger.warning(f"Failed to fetch data for {city} from both APIs.")
        return None