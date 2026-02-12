# Sample Data Generation Guide

This guide explains how to generate and use sample data for testing the user selector feature.

## Overview

- **Sample Database**: SQLite file (`sample_users.db`)
- **Users Generated**: 11-19 (9 users total)
- **Records per User**: ~150 records
- **Total Records**: ~1,350 records

## Generate Sample Data

Run the following command to create the sample database:

```bash
python create_sample_db.py
```

This will:
1. Create `sample_users.db` file
2. Generate realistic sample data for users 11-19
3. Display statistics about the generated data

## How It Works

### Configuration

In `config.py`:
```python
USE_DEMO_DATA_FOR_PRIVATE_POOL = True  # Uses SQLite for private pool
```

- **True**: Private pool users (11-19) use SQLite sample data
- **False**: All users use real PostgreSQL database

### Data Source by Pool

| Pool | Data Source |
|------|-------------|
| Private Pool (users 11-19) | SQLite sample database |
| Shared Pool | PostgreSQL (real data) |

## User Selector

When viewing the Private Pool dashboard:
1. A dropdown appears below the header
2. Select from User 11-19
3. Dashboard updates automatically
4. All filters maintain the selected user

## Sample Data Characteristics

- **Status Distribution**: ~70% success rate (realistic)
- **Processing Time**: 0.5-5 hours per task
- **Emergency Flags**: ~25% of records
- **Time Range**: Last 90 days
- **Companies**: 40+ different company URLs

## Expanding to 45 Users

To add more users (20-56):

### Option 1: Modify and Re-run Script

Edit `create_sample_db.py`:
```python
user_ids = list(range(11, 57))  # Change from 20 to 57
```

Then re-run:
```bash
python create_sample_db.py
```

### Option 2: Add Users Incrementally

Modify the script to append new users without recreating the database.

### Update User Range in Dashboard

Edit `routes/linkedin_routes.py`:
```python
available_users = list(range(11, 57))  # Update from 20 to 57
```

## File Structure

```
linkedin_kpi/
├── sample_users.db              # SQLite database (generated)
├── create_sample_db.py          # Generation script
├── db/
│   └── sqlite_queries.py        # SQLite query functions
└── SAMPLE_DATA_README.md        # This file
```

## Switching Between Real and Demo Data

### Use Demo Data (Default)
```python
# config.py
USE_DEMO_DATA_FOR_PRIVATE_POOL = True
```

### Use Real PostgreSQL Data
```python
# config.py
USE_DEMO_DATA_FOR_PRIVATE_POOL = False
```

No other changes needed - the app automatically switches data sources!

## Notes

- Shared pool always uses PostgreSQL (real data)
- Sample data is completely separate from production database
- Safe to delete `sample_users.db` and regenerate anytime
- User 11 exists in both databases (can compare real vs demo)
