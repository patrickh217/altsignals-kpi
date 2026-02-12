"""
High-performance bulk data generation using CSV files
Generates realistic data for hundreds of thousands of records per user
"""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
OUTPUT_DIR = Path("bulk_data")
USERS_TO_GENERATE = list(range(12, 57))  # Users 12-56 (45 users)
RECORDS_PER_USER = 100000  # 100k records per user (adjustable)

# Sample company names
COMPANIES = [
    "microsoft", "apple", "google", "amazon", "meta", "netflix", "tesla",
    "nvidia", "adobe", "salesforce", "oracle", "ibm", "intel", "cisco",
    "paypal", "uber", "airbnb", "spotify", "zoom", "slack", "shopify",
    "square", "stripe", "coinbase", "robinhood", "doordash", "instacart",
    "lyft", "snapchat", "pinterest", "reddit", "twitter", "linkedin",
    "github", "gitlab", "atlassian", "notion", "figma", "canva", "miro",
    "dropbox", "box", "asana", "monday", "zendesk", "hubspot", "mailchimp",
    "twilio", "datadog", "snowflake", "palantir", "cloudflare", "okta"
]

STATUSES = ["done", "pending", "error", "processing", "queued"]
SCRAPER_STATUSES = ["success", "failed", "timeout", "rate_limited", "blocked", "partial"]


def random_datetime(start_days_ago=365):
    """Generate random datetime within the last N days"""
    start = datetime.now() - timedelta(days=start_days_ago)
    random_seconds = random.randint(0, start_days_ago * 24 * 3600)
    return start + timedelta(seconds=random_seconds)


def generate_csv_for_user(user_id, num_records):
    """Generate CSV file with data for a specific user"""
    filename = OUTPUT_DIR / f"user_{user_id}_data.csv"

    print(f"Generating {num_records:,} records for User {user_id}...")

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'compute_datetime', 'linkedin_url', 'status', 'last_update',
            'user_id', 'emergency', 'scraper_status', 'ticker_eod',
            'recycled_datetime_task'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(num_records):
            # Status with 75% success rate
            if random.random() < 0.75:
                status = "done"
                scraper_status = "success"
            else:
                status = random.choice(STATUSES)
                scraper_status = random.choice(SCRAPER_STATUSES)

            compute_datetime = random_datetime(365)
            processing_hours = random.uniform(0.5, 5.5)
            last_update = compute_datetime + timedelta(hours=processing_hours)

            # Vary company URLs to ensure uniqueness
            company = random.choice(COMPANIES)
            linkedin_url = f"https://www.linkedin.com/company/{company}-{random.randint(1, 99999)}"

            emergency = 1 if random.random() < 0.20 else 0  # 20% emergency
            ticker_eod = 1 if random.random() < 0.5 else 0

            # 25% chance of recycled datetime
            recycled_datetime = ""
            if random.random() < 0.25:
                recycled_datetime = random_datetime(180).strftime('%Y-%m-%d %H:%M:%S')

            writer.writerow({
                'compute_datetime': compute_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                'linkedin_url': linkedin_url,
                'status': status,
                'last_update': last_update.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': user_id,
                'emergency': emergency,
                'scraper_status': scraper_status,
                'ticker_eod': ticker_eod,
                'recycled_datetime_task': recycled_datetime
            })

            # Progress indicator
            if (i + 1) % 10000 == 0:
                print(f"  Progress: {i + 1:,} / {num_records:,} records")

    print(f"[OK] User {user_id} CSV created: {filename}")
    return filename


def load_csv_to_sqlite(csv_file, db_path="sample_users.db"):
    """Load CSV data into SQLite database"""
    import sqlite3
    import pandas as pd

    print(f"Loading {csv_file} into database...")

    # Read CSV
    df = pd.read_csv(csv_file)

    # Connect to database
    conn = sqlite3.connect(db_path)

    # Append to table
    df.to_sql('url_status_company', conn, if_exists='append', index=False)

    conn.close()
    print(f"[OK] Loaded {len(df):,} records")


def main():
    """Generate bulk data for all users"""
    print("=" * 60)
    print("BULK DATA GENERATION")
    print("=" * 60)
    print(f"Users: {USERS_TO_GENERATE[0]}-{USERS_TO_GENERATE[-1]} ({len(USERS_TO_GENERATE)} users)")
    print(f"Records per user: {RECORDS_PER_USER:,}")
    print(f"Total records: {RECORDS_PER_USER * len(USERS_TO_GENERATE):,}")
    print()

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Generate CSV files
    csv_files = []
    for user_id in USERS_TO_GENERATE:
        csv_file = generate_csv_for_user(user_id, RECORDS_PER_USER)
        csv_files.append(csv_file)
        print()

    print("=" * 60)
    print("CSV GENERATION COMPLETE")
    print("=" * 60)
    print(f"Total CSV files created: {len(csv_files)}")
    print(f"Location: {OUTPUT_DIR.absolute()}")
    print()

    # Ask if user wants to load into SQLite
    print("Next steps:")
    print("1. Review CSV files in the 'bulk_data' directory")
    print("2. Run load_bulk_data.py to import into SQLite database")
    print()


if __name__ == "__main__":
    main()
