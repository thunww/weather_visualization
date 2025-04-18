import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_line_chart(df, output_dir, city):
    """Vẽ biểu đồ đường cho nhiệt độ."""
    plt.figure(figsize=(10, 6))
    plt.plot(df["date"], df["temperature"], marker="o", color="blue", label="Temperature")
    plt.title(f"Temperature in {city}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()  # Đảm bảo các nhãn không bị cắt
    plt.legend()
    output_path = os.path.join(output_dir, f"{city}_temperature_line.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


def plot_histogram(df, output_dir, city):
    """Vẽ histogram cho phân bố lượng mưa."""
    plt.figure(figsize=(10, 6))
    sns.histplot(df["precipitation"], bins=20, kde=True, color="green", stat="density")
    plt.title(f"Precipitation Distribution in {city}")
    plt.xlabel("Precipitation (mm)")
    plt.ylabel("Density")
    # Hiển thị trung bình và độ lệch chuẩn
    mean_precip = df["precipitation"].mean()
    std_precip = df["precipitation"].std()
    plt.axvline(mean_precip, color='red', linestyle='--', label=f'Mean: {mean_precip:.2f} mm')
    plt.axvline(mean_precip + std_precip, color='orange', linestyle='--', label=f"+1 Std Dev: {mean_precip + std_precip:.2f} mm")
    plt.axvline(mean_precip - std_precip, color='orange', linestyle='--', label=f"-1 Std Dev: {mean_precip - std_precip:.2f} mm")
    plt.legend()
    output_path = os.path.join(output_dir, f"{city}_precipitation_histogram.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


def plot_scatter(df, output_dir, city):
    """Vẽ scatter plot cho nhiệt độ và độ ẩm."""
    plt.figure(figsize=(10, 6))
    scatter = sns.scatterplot(x="temperature", y="humidity", data=df, hue="precipitation", size="precipitation", palette="coolwarm", sizes=(20, 200))
    plt.title(f"Temperature vs. Humidity in {city}")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Humidity (%)")
    # Điều chỉnh độ trong suốt để dễ nhìn khi dữ liệu dày đặc
    plt.legend(title="Precipitation (mm)", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    output_path = os.path.join(output_dir, f"{city}_temp_humidity_scatter.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


def create_visualizations(df, output_dir, city):
    """Tạo tất cả biểu đồ và lưu chúng vào thư mục đầu ra."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plot_line_chart(df, output_dir, city)
    plot_histogram(df, output_dir, city)
    plot_scatter(df, output_dir, city)
    print(f"Visualizations for {city} created successfully! Check the '{output_dir}' folder.")
