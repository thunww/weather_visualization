from apscheduler.schedulers.background import BackgroundScheduler
from api_fetch import process_weather_data
from visualization import create_visualizations
from database import delete_old_data
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def update_weather_data(cities, output_dir):
    """Cập nhật dữ liệu thời tiết và bảo trì cơ sở dữ liệu."""
    for city in cities:
        df = process_weather_data(city)
        if df is not None:
            create_visualizations(df, output_dir, city)
            logger.info(f"Scheduled update completed for {city}")
    # Xóa dữ liệu cũ hơn 30 ngày
    delete_old_data(days=30)

def schedule_weather_updates(cities, output_dir):
    """Lên lịch cập nhật dữ liệu mỗi 6 giờ."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_weather_data, "interval", hours=6, args=[cities, output_dir])
    scheduler.start()
    logger.info("Scheduled weather updates every 6 hours")