# Company Scraper Dashboard

A multi-platform analytics dashboard for monitoring web scraping operations across various platforms.

## Features

- 🔐 Secure authentication system
- 📊 Real-time KPI monitoring
- 🏥 System health dashboard
- 💼 LinkedIn analytics (active)
- 🚀 Multi-platform support (coming soon)
- 📈 Time-based filtering (Daily, Weekly, Monthly, Quarterly, Yearly)
- 📉 Interactive charts and visualizations
- 🔍 Infrastructure monitoring

## Project Structure

```
linkedin_kpi/
├── main.py                     # Application entry point
├── config.py                   # Configuration settings
├── auth.py                     # Authentication utilities
├── db/
│   ├── __init__.py
│   ├── connection.py          # Database connection
│   └── queries.py             # Database queries
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py         # Login/logout routes
│   ├── platform_routes.py     # Platform selection
│   ├── linkedin_routes.py     # LinkedIn dashboard
│   └── system_routes.py       # System health monitoring
├── components/
│   ├── __init__.py
│   ├── charts.py              # Chart generation
│   └── styles.py              # CSS styles
├── utils/
│   └── __init__.py
├── db_access.py               # Database credentials
└── main_old.py                # Original monolithic version (backup)
```

## Installation

1. Install dependencies:
```bash
pip install fasthtml pandas psycopg2 plotly numpy
```

2. Ensure database credentials are configured in `db_access.py`

3. Run the application:
```bash
python main.py
```

## Usage

1. **Login**
   - Navigate to http://localhost:5001
   - Email: patrickh217@gmail.com
   - Password: Tada1234!!

2. **Platform Selection**
   - Choose from available platforms
   - Currently active: LinkedIn, System Health

3. **LinkedIn Dashboard**
   - View KPIs and metrics
   - Filter by time period
   - Monitor infrastructure status

4. **System Health**
   - Overall system status
   - Database metrics
   - Infrastructure monitoring

## Version

Current version: **v2**
