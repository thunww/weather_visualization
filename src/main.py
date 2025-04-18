import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def create_temperature_line(df: pd.DataFrame, city: str) -> go.Figure:
    """Tạo biểu đồ đường nhiệt độ tương tác."""
    fig = px.line(df, x="date", y="temperature", color="source", title=f"Temperature in {city}",
                  labels={"temperature": "Temperature (°C)", "date": "Date"})
    fig.update_layout(xaxis_tickangle=45, showlegend=True)
    return fig

def create_precipitation_histogram(df: pd.DataFrame, city: str) -> go.Figure:
    """Tạo histogram lượng mưa."""
    fig = px.histogram(df, x="precipitation", color="source", nbins=20, histnorm="probability density",
                       title=f"Precipitation Distribution in {city}",
                       labels={"precipitation": "Precipitation (mm)", "count": "Density"})
    mean_precip = df["precipitation"].mean()
    fig.add_vline(x=mean_precip, line_dash="dash", line_color="red", annotation_text=f"Mean: {mean_precip:.2f} mm")
    return fig

def create_scatter_temp_humidity(df: pd.DataFrame, city: str) -> go.Figure:
    """Tạo scatter plot nhiệt độ và độ ẩm."""
    fig = px.scatter(df, x="temperature", y="humidity", color="precipitation", size="precipitation",
                     title=f"Temperature vs. Humidity in {city}", hover_data=["date", "weather_description"],
                     labels={"temperature": "Temperature (°C)", "humidity": "Humidity (%)"})
    return fig

def create_pressure_wind_plot(df: pd.DataFrame, city: str) -> go.Figure:
    """Tạo biểu đồ áp suất và tốc độ gió."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df["date"], y=df["pressure"], name="Pressure", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=df["date"], y=df["wind_speed"], name="Wind Speed", line=dict(color="green")), secondary_y=True)
    fig.update_layout(title=f"Pressure and Wind Speed in {city}", xaxis_title="Date",
                      yaxis_title="Pressure (hPa)", yaxis2_title="Wind Speed (m/s)")
    return fig

def create_visualizations(df: pd.DataFrame, output_dir: str, city: str) -> None:
    """Tạo và lưu tất cả biểu đồ dưới dạng HTML."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Tạo các biểu đồ
    temp_fig = create_temperature_line(df, city)
    precip_fig = create_precipitation_histogram(df, city)
    scatter_fig = create_scatter_temp_humidity(df, city)
    pressure_wind_fig = create_pressure_wind_plot(df, city)

    # Lưu các biểu đồ
    temp_fig.write_html(os.path.join(output_dir, f"{city}_temperature_line.html"))
    precip_fig.write_html(os.path.join(output_dir, f"{city}_precipitation_histogram.html"))
    scatter_fig.write_html(os.path.join(output_dir, f"{city}_temp_humidity_scatter.html"))
    pressure_wind_fig.write_html(os.path.join(output_dir, f"{city}_pressure_wind.html"))

    # Tạo báo cáo HTML tổng hợp
    report_html = f"""
    <html>
    <head><title>Weather Report for {city}</title></head>
    <body>
        <h1>Weather Forecast for {city}</h1>
        <h2>Temperature</h2><iframe src="{city}_temperature_line.html" width="100%" height="500"></iframe>
        <h2>Precipitation</h2><iframe src="{city}_precipitation_histogram.html" width="100%" height="500"></iframe>
        <h2>Temperature vs. Humidity</h2><iframe src="{city}_temp_humidity_scatter.html" width="100%" height="500"></iframe>
        <h2>Pressure and Wind Speed</h2><iframe src="{city}_pressure_wind.html" width="100%" height="500"></iframe>
    </body>
    </html>
    """
    with open(os.path.join(output_dir, f"{city}_weather_report.html"), "w") as f:
        f.write(report_html)

    logger.info(f"Visualizations and report for {city} created in {output_dir}")