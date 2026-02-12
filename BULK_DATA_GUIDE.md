# Bulk Data Generation Guide

## Overview

Generate realistic sample data for **hundreds of thousands** or **millions** of records efficiently using CSV files.

## Quick Start

### Step 1: Generate CSV Files

```bash
python generate_bulk_data.py
```

**Default settings:**
- Users: 12-56 (45 users)
- Records per user: 100,000
- **Total: 4,500,000 records**

### Step 2: Load into Database

```bash
python load_bulk_data.py
```

This loads all CSV files into the SQLite database with optimized indexes.

## Customization

### Change Number of Records

Edit `generate_bulk_data.py`:

```python
# For 500k records per user
RECORDS_PER_USER = 500000

# For 1 million records per user
RECORDS_PER_USER = 1000000

# For testing (smaller dataset)
RECORDS_PER_USER = 10000
```

### Change User Range

Edit `generate_bulk_data.py`:

```python
# Generate for users 12-20 only (9 users)
USERS_TO_GENERATE = list(range(12, 21))

# Generate for users 12-56 (45 users)
USERS_TO_GENERATE = list(range(12, 57))

# Generate for users 12-100 (89 users)
USERS_TO_GENERATE = list(range(12, 101))
```

## Performance

### Generation Speed
- ~50,000-100,000 records/second (CSV writing)
- Depends on disk I/O speed

### Loading Speed
- ~100,000-200,000 records/second (SQLite insertion)
- Chunked loading for memory efficiency

### Example Benchmarks

| Records per User | Total Users | Total Records | Gen Time | Load Time | DB Size |
|-----------------|-------------|---------------|----------|-----------|---------|
| 10,000 | 45 | 450,000 | ~5 sec | ~3 sec | ~50 MB |
| 100,000 | 45 | 4,500,000 | ~45 sec | ~30 sec | ~500 MB |
| 500,000 | 45 | 22,500,000 | ~4 min | ~2 min | ~2.5 GB |
| 1,000,000 | 45 | 45,000,000 | ~8 min | ~4 min | ~5 GB |

## Important Notes

### User ID 11 - Real Data
- User ID 11 **always** uses real PostgreSQL data
- Only users 12+ use the SQLite sample data
- This ensures your production data stays intact

### Data Characteristics
- **Status Distribution**: 75% success rate
- **Processing Time**: 0.5-5.5 hours
- **Emergency Rate**: 20% of records
- **Time Range**: Last 365 days
- **Companies**: 50+ unique company names
- **URLs**: Unique per record

### Database Indexes
The loader automatically creates indexes on:
- `user_id` - For fast user filtering
- `compute_datetime` - For fast date queries

## File Structure

```
linkedin_kpi/
├── bulk_data/                    # Generated CSV files
│   ├── user_12_data.csv
│   ├── user_13_data.csv
│   └── ...
├── sample_users.db              # SQLite database
├── generate_bulk_data.py        # Step 1: Generate CSVs
├── load_bulk_data.py           # Step 2: Load to DB
└── BULK_DATA_GUIDE.md          # This file
```

## Incremental Updates

### Add More Users

1. Edit `USERS_TO_GENERATE` in `generate_bulk_data.py`
2. Run generation script
3. Run load script (appends to existing data)

### Replace Existing User Data

1. Delete specific CSV file from `bulk_data/`
2. Re-generate that user's data
3. **Delete from database first:**
   ```sql
   DELETE FROM url_status_company WHERE user_id = 12;
   ```
4. Run load script

## Memory Management

For very large datasets:

1. **Generate in batches:**
   ```python
   # Batch 1: Users 12-30
   USERS_TO_GENERATE = list(range(12, 31))

   # Batch 2: Users 31-56
   USERS_TO_GENERATE = list(range(31, 57))
   ```

2. **Load in batches:**
   - Move processed CSV files to another folder
   - Load remaining files

## Updating Dashboard

After generating data, update the user range in `routes/linkedin_routes.py`:

```python
# Line 100
available_users = list(range(11, 57))  # Match your user range
```

## Troubleshooting

### "No CSV files found"
- Make sure you ran `generate_bulk_data.py` first
- Check the `bulk_data/` directory exists

### Database locked error
- Close the application
- Close any database browsers
- Try again

### Out of memory
- Reduce `RECORDS_PER_USER`
- Generate in smaller batches
- Increase system RAM or page file

## Clean Slate

To start fresh:

```bash
# Delete database
rm sample_users.db

# Delete CSV files
rm -rf bulk_data/

# Regenerate everything
python generate_bulk_data.py
python load_bulk_data.py
```

## Production Deployment

For production with millions of records:

1. Generate CSVs on development machine
2. Transfer `sample_users.db` file to server
3. Set `USE_DEMO_DATA_FOR_PRIVATE_POOL = True` in config
4. Users 12+ will use sample data
5. User 11 continues using real PostgreSQL data
