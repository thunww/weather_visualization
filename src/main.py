from api_fetch import process_weather_data
from visualization import create_visualizations

def main():
    # Nhập tên thành phố
    city = input("Enter city name (e.g., Hanoi): ").strip()
    output_dir = "../outputs"

    # Xử lý dữ liệu từ API
    df = process_weather_data(city)

    if df is not None:
        # Tạo biểu đồ
        create_visualizations(df, output_dir, city)
        print(f"Visualizations for {city} created successfully! Check the 'outputs' folder.")
    else:
        print("Failed to process data.")

if __name__ == "__main__":
    main()