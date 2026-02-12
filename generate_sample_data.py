"""
Generate sample data for additional users in the private pool
Run this script to generate SQL INSERT statements
"""
import random
from datetime import datetime, timedelta

# User IDs to generate data for (8 users: 12-19)
USER_IDS = [12, 13, 14, 15, 16, 17, 18, 19]

# Sample company names for LinkedIn URLs
COMPANIES = [
    "microsoft", "apple", "google", "amazon", "meta", "netflix", "tesla",
    "nvidia", "adobe", "salesforce", "oracle", "ibm", "intel", "cisco",
    "paypal", "uber", "airbnb", "spotify", "zoom", "slack", "shopify",
    "square", "stripe", "coinbase", "robinhood", "doordash", "instacart",
    "lyft", "snapchat", "pinterest", "reddit", "twitter", "linkedin",
    "github", "gitlab", "atlassian", "notion", "figma", "canva", "miro"
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

def generate_user_data(user_id, num_records=150):
    """Generate sample data for a user"""
    sql_statements = []

    for i in range(num_records):
        company = random.choice(COMPANIES)
        linkedin_url = f"https://www.linkedin.com/company/{company}"
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
            recycled_datetime = random_datetime(60)
            recycled_str = f"'{recycled_datetime.strftime('%Y-%m-%d %H:%M:%S')}'"
        else:
            recycled_str = "NULL"

        sql = f"""INSERT INTO url_status_company
    (compute_datetime, linkedin_url, status, last_update, user_id, emergency, scraper_status, ticker_eod, recycled_datetime_task)
VALUES
    ('{compute_datetime.strftime('%Y-%m-%d %H:%M:%S')}', '{linkedin_url}', '{status}', '{last_update.strftime('%Y-%m-%d %H:%M:%S')}', {user_id}, {emergency}, '{scraper_status}', {ticker_eod}, {recycled_str});"""

        sql_statements.append(sql)

    return sql_statements

def main():
    """Generate SQL for all users"""
    print("-- Generated Sample Data for Private Pool Users")
    print("-- Run this SQL in your PostgreSQL database")
    print("-- Generated on:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print()

    for user_id in USER_IDS:
        print(f"\n-- User ID: {user_id}")
        print(f"-- Generating {150} records for user {user_id}")

        statements = generate_user_data(user_id, num_records=150)

        for stmt in statements:
            print(stmt)

        print(f"\n-- Completed user {user_id}")
        print()

if __name__ == "__main__":
    main()
