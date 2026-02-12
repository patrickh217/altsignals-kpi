"""
Generate mock statistics for demo users (no database needed)
Shows realistic big numbers without storing actual data
"""
import random
from datetime import datetime, timedelta
import pandas as pd


def generate_mock_stats(user_id, period="overall"):
    """
    Generate realistic mock statistics for a user
    Returns fake numbers that look impressive for demos
    """
    # Base multiplier increases with user_id for variety
    base = (user_id - 10) * 10000

    # Total companies varies by user (100k to 500k)
    total_companies = random.randint(100000, 500000) + base

    # Success rate >95%
    success_rate = random.uniform(95.5, 98.5)
    successful_scrapes = int(total_companies * (success_rate / 100))

    # Emergency tasks (10-20% of total)
    emergency_count = int(total_companies * random.uniform(0.10, 0.20))

    # Average processing time (~0.35h, max 1h)
    avg_processing_time = random.uniform(0.25, 0.45)

    # Variable infrastructure per user
    active_accounts = random.randint(30, 50)
    accounts_on_hold = random.randint(40, 70)
    active_workers = random.randint(4, 5)  # Mock users have fewer workers

    # Recent activity based on period
    if period == "daily":
        recent_activity = random.randint(5000, 15000)
    elif period == "weekly":
        recent_activity = random.randint(25000, 50000)
    elif period == "monthly":
        recent_activity = random.randint(80000, 150000)
    else:
        recent_activity = total_companies

    return {
        'total_companies': total_companies,
        'successful_scrapes': successful_scrapes,
        'success_rate': success_rate,
        'emergency_count': emergency_count,
        'avg_processing_time': avg_processing_time,
        'recent_activity': recent_activity,
        'active_accounts': active_accounts,
        'accounts_on_hold': accounts_on_hold,
        'active_workers': active_workers
    }


def generate_mock_dataframe(user_id, num_records=20):
    """
    Generate a small DataFrame with mock data for table display
    Just enough to show in the "Latest Entries" table
    """
    companies = [
        "microsoft", "apple", "google", "amazon", "meta", "netflix", "tesla",
        "nvidia", "adobe", "salesforce", "oracle", "ibm", "intel", "cisco",
        "paypal", "uber", "airbnb", "spotify", "zoom", "slack"
    ]

    statuses = ["todo", "pending", "done", "not_existant", "error"]
    scraper_statuses = ["done", "not_existant", "error"]

    data = []
    now = datetime.now()

    for i in range(num_records):
        # Random datetime in the past 30 days
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        compute_datetime = now - timedelta(days=days_ago, hours=hours_ago)

        processing_hours = random.uniform(0.1, 1.0)
        last_update = compute_datetime + timedelta(hours=processing_hours)

        # >95% success rate
        rand = random.random()
        if rand < 0.955:  # 95.5% done
            status = "done"
            scraper_status = "done"
        elif rand < 0.98:  # ~2.5% not_existant
            status = "not_existant"
            scraper_status = "not_existant"
        elif rand < 0.995:  # ~1.5% error
            status = "error"
            scraper_status = "error"
        else:  # remaining todo/pending
            status = random.choice(["todo", "pending"])
            scraper_status = random.choice(statuses)

        data.append({
            'compute_datetime': compute_datetime,
            'linkedin_url': f"https://www.linkedin.com/company/{random.choice(companies)}",
            'status': status,
            'last_update': last_update,
            'emergency': random.choice([True, False, False, False]),
            'scraper_status': scraper_status
        })

    return pd.DataFrame(data)


def generate_mock_status_distribution(user_id):
    """Generate mock status distribution for pie chart"""
    total = generate_mock_stats(user_id)['total_companies']

    # >95% success, >5% not_existant, >1% error (ensure percentages don't exceed 100%)
    done = int(total * random.uniform(0.955, 0.965))  # 95.5-96.5%
    not_existant = int(total * random.uniform(0.05, 0.06))  # 5-6%
    error = int(total * random.uniform(0.01, 0.015))  # 1-1.5%
    pending = int(total * random.uniform(0.005, 0.01))  # 0.5-1%
    todo = max(0, total - (done + not_existant + error + pending))  # Ensure no negatives

    return pd.DataFrame({
        'Status': ['done', 'not_existant', 'error', 'pending', 'todo'],
        'Count': [done, not_existant, error, pending, todo]
    })


def generate_mock_scraper_status(user_id):
    """Generate mock scraper status for bar chart"""
    total = generate_mock_stats(user_id)['total_companies']

    # Match status distribution: >95% done, >5% not_existant, >1% error (ensure no negatives)
    done = int(total * random.uniform(0.955, 0.965))
    not_existant = int(total * random.uniform(0.05, 0.06))
    error = int(total * random.uniform(0.01, 0.015))
    pending = int(total * random.uniform(0.005, 0.01))
    todo = max(0, total - (done + not_existant + error + pending))  # Ensure no negatives

    return pd.DataFrame({
        'Scraper Status': ['done', 'not_existant', 'error', 'pending', 'todo'],
        'Count': [done, not_existant, error, pending, todo]
    })


def generate_mock_timeline(user_id, period="overall"):
    """Generate mock timeline data for line chart"""
    # Determine number of days based on period
    if period == "daily":
        days = 1
        num_points = 24  # Hourly
    elif period == "weekly":
        days = 7
        num_points = 7
    elif period == "monthly":
        days = 30
        num_points = 30
    elif period == "quarterly":
        days = 90
        num_points = 90
    elif period == "yearly":
        days = 365
        num_points = 365  # Daily for yearly
    else:
        # Overall: Historical data back to June 2024 (about 620 days)
        days = 620
        num_points = 620

    dates = []
    counts = []
    now = datetime.now()

    # Ensure minimum 1000 companies per day
    if period == "daily":
        base_count = random.randint(1000, 3000)  # Per hour for daily view
    else:
        base_count = random.randint(1000, 5000)  # Per day

    for i in range(num_points):
        if period == "daily":
            date = now - timedelta(hours=num_points-i-1)
        else:
            date = now - timedelta(days=num_points-i-1)

        # Vary the count with some randomness
        count = base_count + random.randint(-500, 1000)
        dates.append(date.date())
        counts.append(max(count, 0))

    return pd.DataFrame({
        'date': dates,
        'Count': counts
    })


def generate_mock_processing_time(user_id):
    """Generate mock processing time distribution - skewed left, max ~3h"""
    # Generate distribution of processing times (skewed left like user 11)
    times = []
    for _ in range(1000):
        # Skewed left: most values concentrated around 0.3-0.5h, fewer as it goes up
        # Use power distribution to create left skew
        base = random.uniform(0.1, 0.5)  # 70% of values here
        if random.random() < 0.3:  # 30% chance of higher value
            base = random.uniform(0.5, 1.5)
        if random.random() < 0.1:  # 10% chance of even higher value
            extra = random.uniform(0, 1.5) * (random.random() ** 2)  # Squared for more skew
            base = base + extra

        # Cap at 3h max
        time = min(base, 3.0)
        times.append(time)

    return pd.DataFrame({
        'processing_time': times
    })
