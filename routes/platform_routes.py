"""
Platform selection and coming soon routes
"""
from fasthtml.common import *
from auth import require_auth
from config import PLATFORMS


def setup_platform_routes(rt):
    """Setup platform selection routes"""

    @rt("/platforms")
    def platforms(sess: dict = None):
        """Platform selection page"""
        redirect = require_auth(sess)
        if redirect:
            return redirect

        platform_boxes = []
        for platform_id, platform_name, icon, is_active in PLATFORMS:
            href = f"/{platform_id}" if is_active else "/coming-soon"
            platform_boxes.append(
                A(
                    Div(icon, cls="platform-icon"),
                    Div(platform_name, cls="platform-name"),
                    href=href,
                    cls=f"platform-box {platform_id}"
                )
            )

        return Titled("KPI - Altsignals | Platforms",
            Div(
                A("Logout", href="/logout", cls="logout-btn"),
                Div(
                    H1("Select a Platform"),
                    P(f"Welcome, {sess.get('email', 'User')}! Choose a platform to view analytics."),
                    cls="platform-header"
                ),
                Div(*platform_boxes, cls="platform-grid"),
                cls="platform-container"
            )
        )

    @rt("/coming-soon")
    def coming_soon(sess: dict = None):
        """Coming soon page for platforms under development"""
        redirect = require_auth(sess)
        if redirect:
            return redirect

        return Titled("KPI - Altsignals | Coming Soon",
            Div(
                Div(
                    H1("🚧"),
                    H1("Coming Soon", style="margin-top: 0;"),
                    P("This platform dashboard is currently under development."),
                    P("Check back soon for updates!", style="margin-bottom: 40px;"),
                    A("← Back to Platforms", href="/platforms", cls="btn-back"),
                    cls="coming-soon-box"
                ),
                cls="coming-soon-container"
            )
        )
