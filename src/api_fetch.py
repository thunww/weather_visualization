import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_weather_data(city, api_key):
    """Gọi API OpenWeatherMap để lấy dữ liệu thời tiết."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return None

def process_weather_data(city):
    """Xử lý dữ liệu từ API thành DataFrame cho nhiều ngày với nhiều thông tin chi tiết."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("Error: API Key not found in .env file!")
        return None

    data = fetch_weather_data(city, api_key)
    if data and data.get("cod") == "200":
        weather_info = {
            "date": [],
            "temperature": [],
            "humidity": [],
            "precipitation": [],
            "wind_speed": [],  # Thêm tốc độ gió
            "pressure": []     # Thêm áp suất khí quyển
        }

        # Lặp qua dữ liệu dự báo 5 ngày (mỗi 3 giờ 1 lần)
        for entry in data["list"]:
            weather_info["date"].append(entry["dt_txt"])  # Thêm thời gian (Ngày và giờ)
            weather_info["temperature"].append(entry["main"]["temp"])  # Nhiệt độ
            weather_info["humidity"].append(entry["main"]["humidity"])  # Độ ẩm
            weather_info["precipitation"].append(entry.get("rain", {}).get("3h", 0.0))  # Lượng mưa trong 3 giờ
            weather_info["wind_speed"].append(entry["wind"]["speed"])  # Tốc độ gió
            weather_info["pressure"].append(entry["main"]["pressure"])  # Áp suất khí quyển

        # Trả về DataFrame từ dữ liệu
        return pd.DataFrame(weather_info)
    else:
        print(f"Failed to fetch data for {city}. Check city name or API key.")
        return None
