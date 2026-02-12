"""
Database connection management
"""
import psycopg2
from db_access import postgre_access_aws_external


def get_db_connection():
    """Create and return a PostgreSQL database connection"""
    host, port, database, user, password = postgre_access_aws_external()
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    return conn
