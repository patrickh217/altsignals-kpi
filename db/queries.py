"""
Database query functions
"""
import pandas as pd
from db.connection import get_db_connection
from config import HEALTH_CHECK_USER_ID, HEALTH_CHECK_ENTRIES_LIMIT


def fetch_user_data(user_id: int) -> pd.DataFrame:
    """Fetch all data for a specific user"""
    conn = get_db_connection()
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
        WHERE user_id = %s
    """
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df


def fetch_health_check_data() -> pd.DataFrame:
    """Fetch health check data from monitoring user"""
    conn = get_db_connection()
    query = """
        SELECT
            compute_datetime,
            linkedin_url,
            status,
            last_update,
            scraper_status
        FROM url_status_company
        WHERE user_id = %s
        ORDER BY compute_datetime DESC
        LIMIT %s
    """
    df = pd.read_sql_query(query, conn, params=(HEALTH_CHECK_USER_ID, HEALTH_CHECK_ENTRIES_LIMIT))
    conn.close()
    return df


def get_system_stats() -> dict:
    """Get overall system statistics"""
    conn = get_db_connection()

    # Total records
    total_query = "SELECT COUNT(*) as total FROM url_status_company"
    total_df = pd.read_sql_query(total_query, conn)
    total_records = total_df['total'].iloc[0]

    # Status distribution
    status_query = """
        SELECT status, COUNT(*) as count
        FROM url_status_company
        GROUP BY status
    """
    status_df = pd.read_sql_query(status_query, conn)

    # Recent activity (last 24 hours)
    recent_query = """
        SELECT COUNT(*) as recent
        FROM url_status_company
        WHERE compute_datetime >= NOW() - INTERVAL '24 hours'
    """
    recent_df = pd.read_sql_query(recent_query, conn)
    recent_count = recent_df['recent'].iloc[0]

    # Unique users
    users_query = "SELECT COUNT(DISTINCT user_id) as users FROM url_status_company"
    users_df = pd.read_sql_query(users_query, conn)
    unique_users = users_df['users'].iloc[0]

    conn.close()

    return {
        'total_records': total_records,
        'status_distribution': status_df.to_dict('records'),
        'recent_activity': recent_count,
        'unique_users': unique_users
    }
