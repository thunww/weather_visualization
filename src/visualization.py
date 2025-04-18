import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_line_chart(df, output_dir, city):
    """Vẽ biểu đồ đường cho nhiệt độ."""
    plt.figure(figsize=(10, 6))
    plt.plot(df["date"], df["temperature"], marker="o", color="blue")
    plt.title(f"Temperature in {city}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)
    plt.xticks(rotation=45)
    output_path = os.path.join(output_dir, f"{city}_temperature_line.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

def plot_histogram(df, output_dir, city):
    """Vẽ histogram cho phân bố lượng mưa."""
    plt.figure(figsize=(10, 6))
    sns.histplot(df["precipitation"], bins=20, kde=True, color="green")
    plt.title(f"Precipitation Distribution in {city}")
    plt.xlabel("Precipitation (mm)")
    plt.ylabel("Frequency")
    output_path = os.path.join(output_dir, f"{city}_precipitation_histogram.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

def plot_scatter(df, output_dir, city):
    """Vẽ scatter plot cho nhiệt độ và độ ẩm."""
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="temperature", y="humidity", data=df, hue="precipitation", size="precipitation")
    plt.title(f"Temperature vs. Humidity in {city}")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Humidity (%)")
    output_path = os.path.join(output_dir, f"{city}_temp_humidity_scatter.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

def create_visualizations(df, output_dir, city):
    """Tạo tất cả biểu đồ."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    plot_line_chart(df, output_dir, city)
    plot_histogram(df, output_dir, city)
    plot_scatter(df, output_dir, city)