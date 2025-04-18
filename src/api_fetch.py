import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_weather_data(city, api_key):
    """Gọi API OpenWeatherMap để lấy dữ liệu thời tiết."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return None

def process_weather_data(city):
    """Xử lý dữ liệu từ API thành DataFrame."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("Error: API Key not found in .env file!")
        return None

    data = fetch_weather_data(city, api_key)
    if data and data.get("cod") == 200:
        # Trích xuất dữ liệu cần thiết
        weather_info = {
            "date": [datetime.now().strftime("%Y-%m-%d")],
            "temperature": [data["main"]["temp"]],
            "humidity": [data["main"]["humidity"]],
            "precipitation": [data.get("rain", {}).get("1h", 0.0)]  # Lượng mưa trong 1 giờ, mặc định 0 nếu không có
        }
        return pd.DataFrame(weather_info)
    else:
        print(f"Failed to fetch data for {city}. Check city name or API key.")
        return None