import streamlit as st
from api_fetch import process_weather_data
from visualization import create_visualizations
from database import query_data, get_summary_stats
import pandas as pd
import os

st.title("Weather Forecast Dashboard")

# Nhập thành phố
cities = st.text_input("Enter city names (comma-separated, e.g., Hanoi,Ho Chi Minh):", "Hanoi")
output_dir = "../outputs"

# Lấy dữ liệu mới
if st.button("Get Weather Forecast"):
    for city in cities.split(","):
        city = city.strip()
        df = process_weather_data(city)
        if df is not None:
            create_visualizations(df, output_dir, city)
            st.success(f"Visualizations for {city} created!")
            st.write(f"Check the report at: {os.path.join(output_dir, f'{city}_weather_report.html')}")
            st.dataframe(df.head())
        else:
            st.error(f"Failed to fetch data for {city}")

# Xem dữ liệu lịch sử
st.subheader("Historical Data")
selected_city = st.selectbox("Select city to view historical data:", cities.split(",") if cities else ["Hanoi"])
start_date = st.date_input("Start date", value=pd.to_datetime("today") - pd.Timedelta(days=7))
end_date = st.date_input("End date", value=pd.to_datetime("today"))

if st.button("View Historical Data"):
    historical_df = query_data(selected_city, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    if historical_df is not None:
        st.dataframe(historical_df)
        create_visualizations(historical_df, output_dir, f"{selected_city}_historical")
        st.write(f"Historical report at: {os.path.join(output_dir, f'{selected_city}_historical_weather_report.html')}")
    else:
        st.error(f"No historical data found for {selected_city}")

# Xem thống kê
st.subheader("Summary Statistics")
if st.button("View Summary Stats"):
    stats = get_summary_stats(selected_city)
    if stats:
        st.write(f"**Average Temperature**: {stats['avg_temp']:.2f} °C")
        st.write(f"**Min Temperature**: {stats['min_temp']:.2f} °C")
        st.write(f"**Max Temperature**: {stats['max_temp']:.2f} °C")
        st.write(f"**Average Precipitation**: {stats['avg_precip']:.2f} mm")
        st.write(f"**Max Precipitation**: {stats['max_precip']:.2f} mm")
    else:
        st.error(f"No stats available for {selected_city}")