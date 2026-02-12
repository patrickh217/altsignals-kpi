"""
Configuration settings for the Company Scraper Dashboard
"""

# Authentication
VALID_CREDENTIALS = {
    "patrickh217@gmail.com": "Tada1234!!",
}

# Dashboard Settings
DEFAULT_USER_ID = 11
HEALTH_CHECK_USER_ID = 2

# Infrastructure Metrics (static for now)
ACTIVE_ACCOUNTS = 37
ACCOUNTS_ON_HOLD = 55
ACTIVE_WORKERS = 10

# Processing Time Limits (in hours)
MAX_PROCESSING_TIME = 6  # Scrapers work during business hours only

# Pagination
LATEST_ENTRIES_LIMIT = 20
HEALTH_CHECK_ENTRIES_LIMIT = 30

# Platform Configuration
PLATFORMS = [
    ("linkedin", "LinkedIn", "💼", True),  # (id, name, icon, is_active)
    ("system-health", "System Health", "🏥", True),
    ("similarweb", "Similar Web", "📊", False),
    ("trends", "Google Trends", "📈", False),
    ("capterra", "Capterra", "⭐", False),
    ("twitter", "Twitter", "🐦", False),
    ("appstore", "App Store", "📱", False),
    ("amazon", "Amazon", "📦", False),
    ("crunchbase", "Crunchbase", "🚀", False),
    ("meta", "Meta", "👥", False),
    ("glassdoor", "Glassdoor", "🏢", False),
    ("producthunt", "Product Hunt", "🎯", False),
]

# Version (User 11 uses v2, mock users 12-56 use v3)
APP_VERSION = "v2"  # Default for real data (User 11)

# Demo Mode (generates mock data for private pool users 6-10 & 12-56)
USE_DEMO_DATA_FOR_PRIVATE_POOL = True  # Set to False to use real PostgreSQL data
