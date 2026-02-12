# LinkedIn KPI Dashboard (FastHTML Version)

This dashboard visualizes the Key Performance Indicators (KPIs) for the LinkedIn Scraper, specifically for Client ID 11.
It is built using **FastHTML** and **Plotly**.

## Prerequisites

You need to have Python installed. The following packages are required:

- python-fasthtml
- pandas
- psycopg2-binary
- plotly
- uvicorn

## Installation

You can install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Running the Dashboard

To run the dashboard, execute the following command in your terminal:

```bash
python main.py
```

Or simply double-click `run_dashboard.bat`.

The dashboard will be available at `http://localhost:5001` (or the port displayed in the terminal).

## Features

- **Client Overview**: Displays total companies tracked, successful scrapes, and success rate.
- **Status Distribution**: A pie chart showing the distribution of scrape statuses.
- **Scraper Status Breakdown**: A bar chart showing the status of the scraper.
- **Timeline**: A line chart showing scraping activity over time.
- **Detailed Data**: A table view of the latest entries.
