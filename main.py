from fasthtml.common import *
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.io as pio
from db_access import postgre_access_aws_external
import json
from datetime import datetime, timedelta
import numpy as np

# Initialize FastHTML app
app, rt = fast_app(
    hdrs=(
        Script(src="https://cdn.plot.ly/plotly-2.32.0.min.js"),
        Style("""
            .metric-card {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin: 10px;
                flex: 1;
            }
            .metric-value {
                font-size: 2em;
                font-weight: bold;
                color: #007bff;
            }
            .metric-label {
                color: #6c757d;
                font-size: 0.9em;
                text-transform: uppercase;
            }
            .chart-container {
                margin-top: 30px;
                margin-bottom: 30px;
                padding: 20px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            .grid-row {
                display: flex;
                flex-wrap: wrap;
                margin: 0 -10px;
            }
            .col-half {
                flex: 0 0 50%;
                max-width: 50%;
                padding: 0 10px;
                box-sizing: border-box;
            }
            .col-third {
                flex: 0 0 33.333%;
                max-width: 33.333%;
                padding: 0 10px;
                box-sizing: border-box;
            }
            @media (max-width: 768px) {
                .col-half, .col-third {
                    flex: 0 0 100%;
                    max-width: 100%;
                }
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #f8f9fa;
            }
            tr:hover {
                background-color: #f5f5f5;
            }
            .filter-buttons {
                display: flex;
                gap: 10px;
                margin: 20px 0;
                flex-wrap: wrap;
            }
            .filter-btn {
                padding: 10px 20px;
                border: 2px solid #007bff;
                background: white;
                color: #007bff;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                font-weight: 500;
                transition: all 0.3s;
            }
            .filter-btn:hover {
                background: #007bff;
                color: white;
            }
            .filter-btn.active {
                background: #007bff;
                color: white;
            }
            .version-badge {
                display: inline-block;
                background: #28a745;
                color: white;
                padding: 5px 12px;
                border-radius: 15px;
                font-size: 0.85em;
                font-weight: bold;
                margin-left: 10px;
            }
            .header-info {
                color: #666;
                margin-bottom: 20px;
            }
            .health-check-section {
                background: #f0f8ff;
                border-left: 4px solid #17a2b8;
                padding: 15px;
                margin-top: 20px;
            }
            .health-check-title {
                color: #17a2b8;
                margin-bottom: 10px;
            }
        """)
    )
)

def get_db_connection():
    host, port, database, user, password = postgre_access_aws_external()
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    return conn

def fetch_data(target_user_id):
    conn = get_db_connection()
    query = """
        SELECT
            compute_datetime,
            linkedin_url,
            status,
            last_update,
            user_id,
            emergency,
            scraper_status,
            ticker_eod,
            recycled_datetime_task,
            id
        FROM url_status_company
        WHERE user_id = %s
    """
    df = pd.read_sql_query(query, conn, params=(target_user_id,))
    conn.close()
    return df

def fetch_health_check_data():
    conn = get_db_connection()
    query = """
        SELECT
            compute_datetime,
            linkedin_url,
            status,
            last_update,
            scraper_status
        FROM url_status_company
        WHERE user_id = 2
        ORDER BY compute_datetime DESC
        LIMIT 30
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def generate_plot_html(fig):
    return NotStr(pio.to_html(fig, full_html=False, include_plotlyjs=False, config={'responsive': True}))

@rt("/")
def get(period: str = "overall"):
    try:
        df = fetch_data(11)

        if df.empty:
            return Titled("Company Scraper KPI Dashboard",
                Div(P("No data found for User ID 11."), cls="container")
            )

        # Process Data
        df['compute_datetime'] = pd.to_datetime(df['compute_datetime'])
        df['last_update'] = pd.to_datetime(df['last_update'])

        # Apply period filter
        now = datetime.now()
        df_filtered = df.copy()

        if period == "daily":
            cutoff = now - timedelta(days=1)
            df_filtered = df_filtered[df_filtered['compute_datetime'] >= cutoff]
            period_label = "Last 24 Hours"
        elif period == "weekly":
            cutoff = now - timedelta(weeks=1)
            df_filtered = df_filtered[df_filtered['compute_datetime'] >= cutoff]
            period_label = "Last Week"
        elif period == "monthly":
            cutoff = now - timedelta(days=30)
            df_filtered = df_filtered[df_filtered['compute_datetime'] >= cutoff]
            period_label = "Last 30 Days"
        elif period == "quarterly":
            cutoff = now - timedelta(days=90)
            df_filtered = df_filtered[df_filtered['compute_datetime'] >= cutoff]
            period_label = "Last Quarter"
        elif period == "yearly":
            cutoff = now - timedelta(days=365)
            df_filtered = df_filtered[df_filtered['compute_datetime'] >= cutoff]
            period_label = "Last Year"
        else:
            period_label = "All Time"

        # Calculate metrics
        total_companies = len(df_filtered)
        successful_scrapes = len(df_filtered[df_filtered['status'] == 'done'])
        success_rate = (successful_scrapes / total_companies * 100) if total_companies > 0 else 0
        emergency_count = len(df_filtered[df_filtered['emergency'] == True])

        # Calculate average processing time (excluding >6h as scrapers work only during business hours)
        df_filtered['processing_time'] = (df_filtered['last_update'] - df_filtered['compute_datetime']).dt.total_seconds() / 3600
        df_valid_time = df_filtered[(df_filtered['processing_time'] > 0) & (df_filtered['processing_time'] <= 6)]
        avg_processing_time = df_valid_time['processing_time'].mean() if len(df_valid_time) > 0 else 0

        # Create Filter Buttons
        periods = [
            ("overall", "All Time"),
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
            ("yearly", "Yearly")
        ]

        filter_buttons = Div(
            *[A(label,
                href=f"/?period={p}",
                cls=f"filter-btn {'active' if p == period else ''}")
              for p, label in periods],
            cls="filter-buttons"
        )

        # Build HTML Components
        metrics_row_1 = Div(
            Div(
                Div("Total Companies", cls="metric-label"),
                Div(f"{total_companies:,}", cls="metric-value"),
                cls="metric-card"
            ),
            Div(
                Div("Successfully Scraped", cls="metric-label"),
                Div(f"{successful_scrapes:,}", cls="metric-value"),
                cls="metric-card"
            ),
            Div(
                Div("Success Rate", cls="metric-label"),
                Div(f"{success_rate:.1f}%", cls="metric-value"),
                cls="metric-card"
            ),
            Div(
                Div("Emergency Tasks", cls="metric-label"),
                Div(f"{emergency_count:,}", cls="metric-value"),
                cls="metric-card"
            ),
            cls="grid-row"
        )

        metrics_row_2 = Div(
            Div(
                Div("Avg Processing Time", cls="metric-label"),
                Div(f"{avg_processing_time:.2f}h", cls="metric-value"),
                cls="metric-card"
            ),
            Div(
                Div("Active Accounts", cls="metric-label"),
                Div("37", cls="metric-value"),
                cls="metric-card"
            ),
            Div(
                Div("Accounts On Hold", cls="metric-label"),
                Div("55", cls="metric-value"),
                cls="metric-card"
            ),
            Div(
                Div("Active Workers", cls="metric-label"),
                Div("10", cls="metric-value"),
                cls="metric-card"
            ),
            cls="grid-row"
        )

        # Create Charts
        # 1. Status Distribution
        status_counts = df_filtered['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig_status = px.pie(status_counts, values='Count', names='Status', hole=0.4,
                           color_discrete_sequence=px.colors.qualitative.Pastel,
                           title="Status Distribution")
        fig_status.update_layout(margin=dict(t=40, b=0, l=0, r=0))

        # 2. Scraper Status
        scraper_status_counts = df_filtered['scraper_status'].value_counts().reset_index()
        scraper_status_counts.columns = ['Scraper Status', 'Count']
        fig_scraper = px.bar(scraper_status_counts, x='Scraper Status', y='Count',
                            color='Scraper Status', text='Count',
                            title="Scraper Status Breakdown")
        fig_scraper.update_layout(margin=dict(t=40, b=0, l=0, r=0))

        # 3. Infrastructure Overview
        infra_data = pd.DataFrame({
            'Category': ['Active Accounts', 'Accounts On Hold', 'Active Workers'],
            'Count': [37, 55, 10]
        })
        fig_infra = px.bar(infra_data, x='Category', y='Count',
                          color='Category', text='Count',
                          title="Infrastructure Overview",
                          color_discrete_sequence=['#28a745', '#ffc107', '#007bff'])
        fig_infra.update_layout(margin=dict(t=40, b=0, l=0, r=0), showlegend=False)

        # 4. Timeline
        df_filtered['date'] = df_filtered['compute_datetime'].dt.date
        daily_activity = df_filtered.groupby('date').size().reset_index(name='Count')
        fig_timeline = px.line(daily_activity, x='date', y='Count', markers=True,
                              title=f"Scraped Companies Over Time ({period_label})")
        fig_timeline.update_layout(margin=dict(t=40, b=0, l=0, r=0))

        # 5. Processing Time Distribution
        if len(df_valid_time) > 0:
            fig_processing = px.histogram(df_valid_time, x='processing_time',
                                         nbins=30,
                                         title="Processing Time Distribution (Hours)",
                                         labels={'processing_time': 'Hours'})
            fig_processing.update_layout(margin=dict(t=40, b=0, l=0, r=0))
            processing_chart = Div(
                Div(Div(generate_plot_html(fig_processing)), cls="col-half chart-container"),
                Div(Div(generate_plot_html(fig_infra)), cls="col-half chart-container"),
                cls="grid-row"
            )
        else:
            processing_chart = Div(
                Div(Div(generate_plot_html(fig_infra)), cls="col-half chart-container"),
                cls="grid-row"
            )

        charts_row = Div(
            Div(Div(generate_plot_html(fig_status)), cls="col-half chart-container"),
            Div(Div(generate_plot_html(fig_scraper)), cls="col-half chart-container"),
            cls="grid-row"
        )

        timeline_row = Div(
            Div(generate_plot_html(fig_timeline)),
            cls="chart-container"
        )

        # Table Data (Latest 20)
        latest_df = df_filtered.sort_values(by='compute_datetime', ascending=False).head(20)
        # Remove unnecessary columns
        columns_to_drop = ['date', 'processing_time', 'ticker_eod', 'recycled_datetime_task', 'user_id', 'id']
        latest_df = latest_df.drop(columns=[col for col in columns_to_drop if col in latest_df.columns])

        # Create Table
        headers = [Th(col) for col in latest_df.columns]
        rows = []
        for _, row in latest_df.iterrows():
            cells = [Td(str(val)) for val in row]
            rows.append(Tr(*cells))

        data_table = Div(
            H3("Latest Entries (User ID 11)"),
            Div(
                Table(
                    Thead(Tr(*headers)),
                    Tbody(*rows)
                ),
                style="overflow-x: auto;"
            ),
            cls="chart-container"
        )

        # Health Check Data (User ID 2)
        try:
            health_check_df = fetch_health_check_data()
            if not health_check_df.empty:
                health_check_df['compute_datetime'] = pd.to_datetime(health_check_df['compute_datetime'])
                health_check_df['last_update'] = pd.to_datetime(health_check_df['last_update'])

                health_headers = [Th(col) for col in health_check_df.columns]
                health_rows = []
                for _, row in health_check_df.iterrows():
                    cells = [Td(str(val)) for val in row]
                    health_rows.append(Tr(*cells))

                health_check_table = Div(
                    Div(
                        H3("Infrastructure Health Check - Latest Entries (User ID 2)", cls="health-check-title"),
                        P("Verification scrapes to monitor infrastructure status", style="color: #666; font-size: 0.9em;"),
                        Div(
                            Table(
                                Thead(Tr(*health_headers)),
                                Tbody(*health_rows)
                            ),
                            style="overflow-x: auto;"
                        ),
                        cls="health-check-section"
                    ),
                    cls="chart-container"
                )
            else:
                health_check_table = Div()
        except Exception as e:
            health_check_table = Div(
                P(f"Unable to load health check data: {e}", style="color: #ff6b6b; padding: 10px;"),
                cls="chart-container"
            )

        return Titled("Company Scraper KPI Dashboard",
            Div(
                H1("📊 Company Scraper KPI Dashboard",
                   Span("v2", cls="version-badge")),
                Div(
                    P(f"Client Overview (User ID: 11) - {period_label}"),
                    cls="header-info"
                ),
                filter_buttons,
                metrics_row_1,
                metrics_row_2,
                charts_row,
                processing_chart,
                timeline_row,
                data_table,
                health_check_table,
                style="max-width: 1400px; margin: 0 auto; padding: 20px; font-family: sans-serif;"
            )
        )

    except Exception as e:
        return Titled("Error", Div(f"An error occurred: {e}", style="color: red; padding: 20px;"))

serve()
