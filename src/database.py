import sqlite3
import pandas as pd
import logging
from datetime import datetime, timedelta
from typing import Optional, List

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def init_database() -> None:
    """Khởi tạo cơ sở dữ liệu và bảng với chỉ mục."""
    with sqlite3.connect("weather_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_forecast (
                date TEXT,
                temperature REAL,
                humidity INTEGER,
                precipitation REAL,
                wind_speed REAL,
                pressure REAL,
                weather_description TEXT,
                source TEXT,
                city TEXT,
                UNIQUE(city, date, source) ON CONFLICT REPLACE
            )
        """)
        # Tạo chỉ mục để tăng tốc truy vấn
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_city_date ON weather_forecast (city, date)")
        conn.commit()
    logger.info("Database initialized")

def save_to_database(df: pd.DataFrame, city: str) -> None:
    """Lưu dữ liệu vào SQLite, thay thế nếu trùng lặp."""
    try:
        init_database()
        with sqlite3.connect("weather_data.db") as conn:
            df.to_sql("weather_forecast", conn, if_exists="append", index=False)
        logger.info(f"Saved {len(df)} records for {city} to database")
    except sqlite3.Error as e:
        logger.error(f"Error saving data for {city}: {e}")

def query_data(city: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Optional[pd.DataFrame]:
    """Truy vấn dữ liệu theo thành phố và khoảng thời gian."""
    try:
        with sqlite3.connect("weather_data.db") as conn:
            query = "SELECT * FROM weather_forecast WHERE city = ?"
            params = [city]
            
            if start_date:
                query += " AND date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND date <= ?"
                params.append(end_date)
                
            df = pd.read_sql_query(query, conn, params=params)
            if not df.empty:
                logger.info(f"Retrieved {len(df)} records for {city}")
                return df
            else:
                logger.warning(f"No data found for {city}")
                return None
    except sqlite3.Error as e:
        logger.error(f"Error querying data for {city}: {e}")
        return None

def delete_old_data(days: int = 30) -> None:
    """Xóa dữ liệu cũ hơn số ngày quy định."""
    try:
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect("weather_data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM weather_forecast WHERE date < ?", (cutoff_date,))
            conn.commit()
            logger.info(f"Deleted {cursor.rowcount} old records before {cutoff_date}")
    except sqlite3.Error as e:
        logger.error(f"Error deleting old data: {e}")

def get_summary_stats(city: str) -> Optional[dict]:
    """Tính toán thống kê cơ bản cho thành phố."""
    try:
        with sqlite3.connect("weather_data.db") as conn:
            query = """
                SELECT 
                    AVG(temperature) as avg_temp,
                    MIN(temperature) as min_temp,
                    MAX(temperature) as max_temp,
                    AVG(precipitation) as avg_precip,
                    MAX(precipitation) as max_precip
                FROM weather_forecast
                WHERE city = ?
            """
            df = pd.read_sql_query(query, conn, params=[city])
            if not df.empty:
                stats = df.iloc[0].to_dict()
                logger.info(f"Generated summary stats for {city}")
                return stats
            else:
                logger.warning(f"No data for summary stats for {city}")
                return None
    except sqlite3.Error as e:
        logger.error(f"Error generating summary stats for {city}: {e}")
        return None

def backup_database(backup_path: str) -> None:
    """Sao lưu cơ sở dữ liệu."""
    try:
        with sqlite3.connect("weather_data.db") as src_conn:
            with sqlite3.connect(backup_path) as dst_conn:
                src_conn.backup(dst_conn)
        logger.info(f"Database backed up to {backup_path}")
    except sqlite3.Error as e:
        logger.error(f"Error backing up database: {e}")