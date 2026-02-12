"""
System health and monitoring routes
"""
from fasthtml.common import *
from auth import require_auth
from db.queries import get_system_stats
from config import ACTIVE_ACCOUNTS, ACCOUNTS_ON_HOLD, ACTIVE_WORKERS, APP_VERSION


def setup_system_routes(rt):
    """Setup system health routes"""

    @rt("/system-health")
    def system_health(sess: dict = None):
        """System Health Dashboard"""
        redirect = require_auth(sess)
        if redirect:
            return redirect

        try:
            stats = get_system_stats()

            # Calculate health status
            success_count = sum(s['count'] for s in stats['status_distribution'] if s['status'] == 'done')
            total_count = sum(s['count'] for s in stats['status_distribution'])
            success_rate = (success_count / total_count * 100) if total_count > 0 else 0

            if success_rate >= 80:
                overall_status = "healthy"
                status_text = "Healthy"
                status_icon = "✅"
            elif success_rate >= 60:
                overall_status = "warning"
                status_text = "Warning"
                status_icon = "⚠️"
            else:
                overall_status = "error"
                status_text = "Critical"
                status_icon = "❌"

            # System Metrics
            metrics_row = Div(
                Div(
                    Div("Total Records", cls="metric-label"),
                    Div(f"{stats['total_records']:,}", cls="metric-value"),
                    cls="metric-card"
                ),
                Div(
                    Div("Recent Activity (24h)", cls="metric-label"),
                    Div(f"{stats['recent_activity']:,}", cls="metric-value"),
                    cls="metric-card"
                ),
                Div(
                    Div("Unique Users", cls="metric-label"),
                    Div(f"{stats['unique_users']:,}", cls="metric-value"),
                    cls="metric-card"
                ),
                Div(
                    Div("Success Rate", cls="metric-label"),
                    Div(f"{success_rate:.1f}%", cls="metric-value"),
                    cls="metric-card"
                ),
                cls="grid-row"
            )

            # Infrastructure Status
            infra_metrics = Div(
                Div(
                    Div("Active Accounts", cls="metric-label"),
                    Div(str(ACTIVE_ACCOUNTS), cls="metric-value"),
                    cls="metric-card"
                ),
                Div(
                    Div("Accounts On Hold", cls="metric-label"),
                    Div(str(ACCOUNTS_ON_HOLD), cls="metric-value"),
                    cls="metric-card"
                ),
                Div(
                    Div("Active Workers", cls="metric-label"),
                    Div(str(ACTIVE_WORKERS), cls="metric-value"),
                    cls="metric-card"
                ),
                cls="grid-row"
            )

            # Status Distribution Table
            status_rows = []
            for item in stats['status_distribution']:
                status_rows.append(
                    Tr(
                        Td(item['status']),
                        Td(f"{item['count']:,}"),
                        Td(f"{(item['count'] / total_count * 100):.1f}%" if total_count > 0 else "0%")
                    )
                )

            status_table = Div(
                H3("Status Distribution"),
                Table(
                    Thead(
                        Tr(
                            Th("Status"),
                            Th("Count"),
                            Th("Percentage")
                        )
                    ),
                    Tbody(*status_rows)
                ),
                cls="chart-container"
            )

            # Overall Health Status
            health_banner = Div(
                H2(f"{status_icon} System Status: ", Span(status_text, cls=f"status-badge {overall_status}")),
                P(f"Overall success rate: {success_rate:.1f}%"),
                style="text-align: center; padding: 30px; background: white; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
            )

            return Titled("KPI - Altsignals | System Health",
                Div(
                    A("← Back to Platforms", href="/platforms", cls="logout-btn",
                      style="top: 20px; right: 180px; background: #6c757d;"),
                    A("Logout", href="/logout", cls="logout-btn"),
                    H1("🏥 System Health Dashboard", Span(APP_VERSION, cls="version-badge")),
                    Div(
                        P("Real-time system monitoring and statistics"),
                        cls="header-info"
                    ),
                    health_banner,
                    H2("Database Metrics"),
                    metrics_row,
                    H2("Infrastructure Status", style="margin-top: 40px;"),
                    infra_metrics,
                    status_table,
                    cls="system-container"
                )
            )

        except Exception as e:
            return Titled("KPI - Altsignals | Error", Div(f"An error occurred: {e}", style="color: red; padding: 20px;"))
