"""
Create a SQLite database with sample data for testing the user selector
This creates data for users 11-19 (8 sample users + the original user 11)
"""
import sqlite3
import random
from datetime import datetime, timedelta

# Database file
DB_FILE = "sample_users.db"

# Sample company names for LinkedIn URLs
COMPANIES = [
    "microsoft", "apple", "google", "amazon", "meta", "netflix", "tesla",
    "nvidia", "adobe", "salesforce", "oracle", "ibm", "intel", "cisco",
    "paypal", "uber", "airbnb", "spotify", "zoom", "slack", "shopify",
    "square", "stripe", "coinbase", "robinhood", "doordash", "instacart",
    "lyft", "snapchat", "pinterest", "reddit", "twitter", "linkedin",
    "github", "gitlab", "atlassian", "notion", "figma", "canva", "miro",
    "dropbox", "box", "asana", "monday", "zendesk", "hubspot", "mailchimp"
]

STATUSES = ["done", "pending", "error", "processing", "queued"]
SCRAPER_STATUSES = ["success", "failed", "timeout", "rate_limited", "blocked", "partial"]

def random_datetime(start_days_ago=90):
    """Generate random datetime within the last N days"""
    start = datetime.now() - timedelta(days=start_days_ago)
    random_days = random.randint(0, start_days_ago)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    return start + timedelta(days=random_days, hours=random_hours, minutes=random_minutes)

def create_database():
    """Create SQLite database and table"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create table matching PostgreSQL schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS url_status_company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            compute_datetime TEXT NOT NULL,
            linkedin_url TEXT NOT NULL,
            status TEXT NOT NULL,
            last_update TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            emergency BOOLEAN NOT NULL,
            scraper_status TEXT NOT NULL,
            ticker_eod BOOLEAN,
            recycled_datetime_task TEXT
        )
    """)

    conn.commit()
    return conn

def generate_user_data(conn, user_id, num_records=150):
    """Generate and insert sample data for a user"""
    cursor = conn.cursor()

    print(f"Generating {num_records} records for User {user_id}...")

    for i in range(num_records):
        # Vary the company selection to ensure diversity
        company = random.choice(COMPANIES)
        linkedin_url = f"https://www.linkedin.com/company/{company}-{user_id}-{i}"

        status = random.choice(STATUSES)
        scraper_status = random.choice(SCRAPER_STATUSES)

        # Bias towards 'done' status (70% success rate)
        if random.random() < 0.7:
            status = "done"
            scraper_status = "success"

        compute_datetime = random_datetime(90)

        # last_update is compute_datetime + processing time (0.5 to 5 hours)
        processing_hours = random.uniform(0.5, 5.0)
        last_update = compute_datetime + timedelta(hours=processing_hours)

        emergency = random.choice([True, False, False, False])  # 25% emergency
        ticker_eod = random.choice([True, False])

        # recycled_datetime_task - some records have it, some don't
        if random.random() < 0.3:  # 30% have recycled datetime
            recycled_datetime = random_datetime(60).strftime('%Y-%m-%d %H:%M:%S')
        else:
            recycled_datetime = None

        cursor.execute("""
            INSERT INTO url_status_company
            (compute_datetime, linkedin_url, status, last_update, user_id, emergency,
             scraper_status, ticker_eod, recycled_datetime_task)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            compute_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            linkedin_url,
            status,
            last_update.strftime('%Y-%m-%d %H:%M:%S'),
            user_id,
            emergency,
            scraper_status,
            ticker_eod,
            recycled_datetime
        ))

    conn.commit()
    print(f"[OK] Completed User {user_id}")

def main():
    """Generate the complete sample database"""
    print("Creating sample SQLite database...")
    print(f"Database file: {DB_FILE}")
    print()

    # Create database and table
    conn = create_database()

    # Generate data for users 11-19
    user_ids = list(range(11, 20))

    for user_id in user_ids:
        generate_user_data(conn, user_id, num_records=150)

    # Show statistics
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM url_status_company")
    total_records = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM url_status_company")
    total_users = cursor.fetchone()[0]

    print()
    print("=" * 50)
    print("Database created successfully!")
    print(f"Total records: {total_records:,}")
    print(f"Total users: {total_users}")
    print(f"Average records per user: {total_records // total_users}")
    print()
    print("Records by user:")
    cursor.execute("""
        SELECT user_id, COUNT(*) as count
        FROM url_status_company
        GROUP BY user_id
        ORDER BY user_id
    """)
    for row in cursor.fetchall():
        print(f"  User {row[0]}: {row[1]:,} records")

    conn.close()
    print()
    print(f"Database saved to: {DB_FILE}")

if __name__ == "__main__":
    main()
