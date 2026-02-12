"""
SQLite query functions for demo/testing with sample data
"""
import sqlite3
import pandas as pd
from pathlib import Path

# Path to the sample SQLite database
SAMPLE_DB_PATH = Path(__file__).parent.parent / "sample_users.db"


def fetch_user_data_sqlite(user_id: int) -> pd.DataFrame:
    """Fetch user data from SQLite sample database"""
    if not SAMPLE_DB_PATH.exists():
        return pd.DataFrame()

    conn = sqlite3.connect(str(SAMPLE_DB_PATH))
    query = """
        SELECT
            compute_datetime,
            linkedin_url,
            status,
            last_update,
            user_id,
            emergency,
            scraper_status,
            ticker_eod,
            recycled_datetime_task,
            id
        FROM url_status_company
        WHERE user_id = ?
    """
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df


def fetch_health_check_data_sqlite() -> pd.DataFrame:
    """Fetch health check data from SQLite (User ID 2)"""
    if not SAMPLE_DB_PATH.exists():
        return pd.DataFrame()

    conn = sqlite3.connect(str(SAMPLE_DB_PATH))
    query = """
        SELECT
            compute_datetime,
            linkedin_url,
            status,
            last_update,
            scraper_status
        FROM url_status_company
        WHERE user_id = 2
        ORDER BY compute_datetime DESC
        LIMIT 30
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
