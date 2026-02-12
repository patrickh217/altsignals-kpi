"""
LinkedIn dashboard routes
"""
from fasthtml.common import *
from datetime import datetime, timedelta
import pandas as pd
from auth import require_auth
from db.queries import fetch_user_data, fetch_health_check_data
from utils.mock_data import (
    generate_mock_stats, generate_mock_dataframe, generate_mock_status_distribution,
    generate_mock_scraper_status, generate_mock_timeline, generate_mock_processing_time
)
from components.charts import (
    generate_plot_html, create_status_pie_chart, create_scraper_status_bar_chart,
    create_infrastructure_chart, create_timeline_chart, create_processing_time_histogram
)
from config import (
    DEFAULT_USER_ID, ACTIVE_ACCOUNTS, ACCOUNTS_ON_HOLD, ACTIVE_WORKERS,
    MAX_PROCESSING_TIME, LATEST_ENTRIES_LIMIT, APP_VERSION, USE_DEMO_DATA_FOR_PRIVATE_POOL
)


def setup_linkedin_routes(rt):
    """Setup LinkedIn dashboard routes"""

    @rt("/linkedin")
    def linkedin_pool_selection(sess: dict = None):
        """LinkedIn Pool Selection Page"""
        redirect = require_auth(sess)
        if redirect:
            return redirect

        return Titled("KPI - Altsignals | LinkedIn",
            Div(
                A("← Back to Platforms", href="/platforms", cls="logout-btn",
                  style="top: 20px; right: 180px; background: #6c757d;"),
                A("Logout", href="/logout", cls="logout-btn"),
                Div(
                    H1("LinkedIn Analytics"),
                    P("Select a data pool to view analytics"),
                    cls="platform-header"
                ),
                Div(
                    A(
                        Div("🔒", cls="platform-icon"),
                        Div("Private Pool", cls="platform-name"),
                        P("Private client data", style="color: #666; margin-top: 10px;"),
                        href="/linkedin/dashboard?pool=private",
                        cls="platform-box linkedin"
                    ),
                    A(
                        Div("🌐", cls="platform-icon"),
                        Div("Shared Pool", cls="platform-name"),
                        P("Shared data pool", style="color: #666; margin-top: 10px;"),
                        href="/linkedin/dashboard?pool=shared",
                        cls="platform-box linkedin"
                    ),
                    style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 25px; max-width: 800px; margin: 0 auto;"
                ),
                cls="platform-container"
            )
        )

    @rt("/linkedin/dashboard")
    def linkedin_dashboard(period: str = "overall", pool: str = "private", user_id: int = 11, sess: dict = None):
        """LinkedIn KPI Dashboard"""
        redirect = require_auth(sess)
        if redirect:
            return redirect

        try:
            # Use selected user_id for private pool, DEFAULT_USER_ID for shared
            selected_user_id = user_id if pool == "private" else DEFAULT_USER_ID

            # Use MOCK data for demo users (12-56), REAL data for user 11
            use_mock_data = (pool == "private" and USE_DEMO_DATA_FOR_PRIVATE_POOL and selected_user_id != 11)

            # Version: v2 for user 11 (real data), v3 for mock users
            app_version = "v2" if selected_user_id == 11 else "v3"

            if use_mock_data:
                # Generate mock statistics (no database needed!)
                mock_stats = generate_mock_stats(selected_user_id, period)
                total_companies = mock_stats['total_companies']
                successful_scrapes = mock_stats['successful_scrapes']
                success_rate = mock_stats['success_rate']
                emergency_count = mock_stats['emergency_count']
                avg_processing_time = mock_stats['avg_processing_time']

                # Variable infrastructure metrics per user
                active_accounts = mock_stats['active_accounts']
                accounts_on_hold = mock_stats['accounts_on_hold']
                active_workers = mock_stats['active_workers']

                # Generate mock data for charts
                df_status = generate_mock_status_distribution(selected_user_id)
                df_scraper = generate_mock_scraper_status(selected_user_id)
                df_timeline = generate_mock_timeline(selected_user_id, period)
                df_processing = generate_mock_processing_time(selected_user_id)

                # Generate small dataframe for table display
                latest_df = generate_mock_dataframe(selected_user_id, num_records=20)

            else:
                # Use REAL data from PostgreSQL for user 11
                df = fetch_user_data(selected_user_id)

                if df.empty:
                    return Titled("KPI - Altsignals | Dashboard",
                        Div(P(f"No data found for User ID {selected_user_id}."), cls="container")
                    )

                # Use default infrastructure values for real data
                active_accounts = ACTIVE_ACCOUNTS
                accounts_on_hold = ACCOUNTS_ON_HOLD
                active_workers = ACTIVE_WORKERS

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

                # Calculate metrics from REAL data
                total_companies = len(df_filtered)
                successful_scrapes = len(df_filtered[df_filtered['status'] == 'done'])
                success_rate = (successful_scrapes / total_companies * 100) if total_companies > 0 else 0
                emergency_count = len(df_filtered[df_filtered['emergency'] == True])

                # Calculate average processing time
                df_filtered['processing_time'] = (df_filtered['last_update'] - df_filtered['compute_datetime']).dt.total_seconds() / 3600
                df_valid_time = df_filtered[(df_filtered['processing_time'] > 0) & (df_filtered['processing_time'] <= MAX_PROCESSING_TIME)]
                avg_processing_time = df_valid_time['processing_time'].mean() if len(df_valid_time) > 0 else 0

                # Generate chart data from REAL data
                df_status = df_filtered['status'].value_counts().reset_index()
                df_status.columns = ['Status', 'Count']

                df_scraper = df_filtered['scraper_status'].value_counts().reset_index()
                df_scraper.columns = ['Scraper Status', 'Count']

                df_filtered['date'] = df_filtered['compute_datetime'].dt.date
                df_timeline = df_filtered.groupby('date').size().reset_index(name='Count')

                df_processing = df_valid_time[['processing_time']].copy() if len(df_valid_time) > 0 else pd.DataFrame()

                # Table data from REAL data
                latest_df = df_filtered.sort_values(by='compute_datetime', ascending=False).head(LATEST_ENTRIES_LIMIT)
                columns_to_drop = ['date', 'processing_time', 'ticker_eod', 'recycled_datetime_task', 'user_id', 'id']
                latest_df = latest_df.drop(columns=[col for col in columns_to_drop if col in latest_df.columns])

            # Period label for mock data
            if use_mock_data:
                if period == "daily":
                    period_label = "Last 24 Hours"
                elif period == "weekly":
                    period_label = "Last Week"
                elif period == "monthly":
                    period_label = "Last 30 Days"
                elif period == "quarterly":
                    period_label = "Last Quarter"
                elif period == "yearly":
                    period_label = "Last Year"
                else:
                    period_label = "All Time"

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
                    href=f"/linkedin/dashboard?pool={pool}&period={p}&user_id={selected_user_id}",
                    cls=f"filter-btn {'active' if p == period else ''}")
                  for p, label in periods],
                cls="filter-buttons"
            )

            # User selector (only for private pool)
            if pool == "private":
                # Available user IDs (6-56 = 51 users total)
                available_users = list(range(6, 57))  # Users 6-10 + User 11 + 45 demo users

                user_selector = Div(
                    Div(
                        Label("Select User:", style="margin-right: 10px; font-weight: 600; color: #333;"),
                        Select(
                            *[Option(f"User {uid}", value=str(uid), selected=(uid == selected_user_id))
                              for uid in available_users],
                            name="user_selector",
                            id="user_selector",
                            onchange=f"window.location.href='/linkedin/dashboard?pool={pool}&period={period}&user_id=' + this.value",
                            style="padding: 8px 12px; border: 2px solid #007bff; border-radius: 5px; font-size: 14px; cursor: pointer;"
                        ),
                        style="display: flex; align-items: center; margin-bottom: 20px;"
                    ),
                    style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px;"
                )
            else:
                user_selector = Div()  # No selector for shared pool

            # Build Metrics
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
                    Div(str(active_accounts), cls="metric-value"),
                    cls="metric-card"
                ),
                Div(
                    Div("Accounts On Hold", cls="metric-label"),
                    Div(str(accounts_on_hold), cls="metric-value"),
                    cls="metric-card"
                ),
                Div(
                    Div("Active Workers", cls="metric-label"),
                    Div(str(active_workers), cls="metric-value"),
                    cls="metric-card"
                ),
                cls="grid-row"
            )

            # Create Charts (using pre-generated dataframes)
            import plotly.express as px

            fig_status = px.pie(df_status, values='Count', names='Status', hole=0.4,
                               color_discrete_sequence=px.colors.qualitative.Pastel,
                               title="Status Distribution")
            fig_status.update_layout(margin=dict(t=40, b=0, l=0, r=0))

            fig_scraper = px.bar(df_scraper, x='Scraper Status', y='Count',
                                color='Scraper Status', text='Count',
                                title="Scraper Status Breakdown")
            fig_scraper.update_layout(margin=dict(t=40, b=0, l=0, r=0))

            fig_infra = create_infrastructure_chart(active_accounts, accounts_on_hold, active_workers)

            fig_timeline = px.line(df_timeline, x='date', y='Count', markers=True,
                                  title=f"Scraped Companies Over Time ({period_label})")
            fig_timeline.update_layout(margin=dict(t=40, b=0, l=0, r=0))

            # Processing Time Distribution
            if len(df_processing) > 0:
                fig_processing = px.histogram(df_processing, x='processing_time',
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

            # Table headers and rows
            headers = [Th(col) for col in latest_df.columns]
            rows = []
            for _, row in latest_df.iterrows():
                cells = [Td(str(val)) for val in row]
                rows.append(Tr(*cells))

            data_table = Div(
                H3("Latest Entries"),
                Div(
                    Table(
                        Thead(Tr(*headers)),
                        Tbody(*rows)
                    ),
                    style="overflow-x: auto;"
                ),
                cls="chart-container"
            )

            # Health Check Data
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
                            H3("Infrastructure Health Check - Latest Entries", cls="health-check-title"),
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

            # Pool display name
            pool_name = "Private Pool" if pool == "private" else "Shared Pool"

            return Titled("KPI - Altsignals | Dashboard",
                Div(
                    A("← Back to Pool Selection", href="/linkedin", cls="logout-btn",
                      style="top: 20px; right: 180px; background: #6c757d;"),
                    A("Logout", href="/logout", cls="logout-btn"),
                    H1("📊 Company Scraper KPI Dashboard",
                       Span(app_version, cls="version-badge")),
                    Div(
                        P(f"{pool_name} - Client Overview (User ID: {selected_user_id}) - {period_label}"),
                        cls="header-info"
                    ),
                    user_selector,
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
            return Titled("KPI - Altsignals | Error", Div(f"An error occurred: {e}", style="color: red; padding: 20px;"))
