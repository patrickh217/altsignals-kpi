"""
Load bulk CSV data into SQLite database
"""
import sqlite3
import pandas as pd
from pathlib import Path
import time

DB_FILE = "sample_users.db"
CSV_DIR = Path("bulk_data")


def create_database_if_needed():
    """Create database and table if they don't exist"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS url_status_company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            compute_datetime TEXT NOT NULL,
            linkedin_url TEXT NOT NULL,
            status TEXT NOT NULL,
            last_update TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            emergency INTEGER NOT NULL,
            scraper_status TEXT NOT NULL,
            ticker_eod INTEGER,
            recycled_datetime_task TEXT
        )
    """)

    # Create index on user_id for faster queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_id
        ON url_status_company(user_id)
    """)

    # Create index on compute_datetime for faster date queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_compute_datetime
        ON url_status_company(compute_datetime)
    """)

    conn.commit()
    conn.close()


def load_csv_files():
    """Load all CSV files from bulk_data directory"""
    csv_files = sorted(CSV_DIR.glob("user_*_data.csv"))

    if not csv_files:
        print("No CSV files found in bulk_data directory!")
        print("Run generate_bulk_data.py first to create CSV files.")
        return

    print(f"Found {len(csv_files)} CSV files to load")
    print()

    total_records = 0
    start_time = time.time()

    conn = sqlite3.connect(DB_FILE)

    for i, csv_file in enumerate(csv_files, 1):
        print(f"[{i}/{len(csv_files)}] Loading {csv_file.name}...")

        # Read CSV in chunks for memory efficiency
        chunk_size = 50000
        chunks_loaded = 0

        for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
            chunk.to_sql('url_status_company', conn, if_exists='append', index=False)
            chunks_loaded += 1
            total_records += len(chunk)

            if chunks_loaded % 2 == 0:  # Progress every 100k records
                print(f"  Loaded {chunks_loaded * chunk_size:,} records...")

        print(f"[OK] {csv_file.name} loaded")

    conn.close()

    elapsed = time.time() - start_time
    print()
    print("=" * 60)
    print("LOADING COMPLETE")
    print("=" * 60)
    print(f"Total records loaded: {total_records:,}")
    print(f"Time elapsed: {elapsed:.1f} seconds")
    print(f"Load speed: {total_records / elapsed:,.0f} records/second")


def show_database_stats():
    """Display database statistics"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Total records
    cursor.execute("SELECT COUNT(*) FROM url_status_company")
    total = cursor.fetchone()[0]

    # Records by user
    cursor.execute("""
        SELECT user_id, COUNT(*) as count
        FROM url_status_company
        GROUP BY user_id
        ORDER BY user_id
    """)
    user_stats = cursor.fetchall()

    # Database size
    db_path = Path(DB_FILE)
    db_size_mb = db_path.stat().st_size / (1024 * 1024)

    print()
    print("=" * 60)
    print("DATABASE STATISTICS")
    print("=" * 60)
    print(f"Database file: {DB_FILE}")
    print(f"Database size: {db_size_mb:.2f} MB")
    print(f"Total records: {total:,}")
    print(f"Total users: {len(user_stats)}")
    print()
    print("Records by user:")
    for user_id, count in user_stats:
        print(f"  User {user_id}: {count:,} records")

    conn.close()


def main():
    """Main execution"""
    print("=" * 60)
    print("BULK DATA LOADER")
    print("=" * 60)
    print()

    # Create database
    print("Creating database and indexes...")
    create_database_if_needed()
    print("[OK] Database ready")
    print()

    # Load CSV files
    load_csv_files()

    # Show stats
    show_database_stats()


if __name__ == "__main__":
    main()
