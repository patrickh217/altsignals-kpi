"""
Authentication routes
"""
from fasthtml.common import *
from auth import validate_credentials, login_user, logout_user


def setup_auth_routes(rt):
    """Setup authentication routes"""

    @rt("/")
    def get(sess: dict = None, error: str = None):
        """Login page"""
        error_div = Div(P(error), cls="error-message") if error else Div()

        return Titled("KPI - Altsignals | Login",
            Div(
                Div(
                    error_div,
                    H1("🔐 Login"),
                    Form(
                        Div(
                            Label("Email", _for="email"),
                            Input(type="email", name="email", id="email",
                                  placeholder="Enter your email", required=True),
                            cls="form-group"
                        ),
                        Div(
                            Label("Password", _for="password"),
                            Input(type="password", name="password", id="password",
                                  placeholder="Enter your password", required=True),
                            cls="form-group"
                        ),
                        Button("Login", type="submit", cls="btn-login"),
                        action="/login",
                        method="post"
                    ),
                    cls="login-box"
                ),
                cls="login-container"
            )
        )

    @rt("/login")
    def post(email: str, password: str, sess: dict):
        """Login handler"""
        if validate_credentials(email, password):
            login_user(sess, email)
            return RedirectResponse("/platforms", status_code=303)
        else:
            return RedirectResponse("/?error=Invalid credentials", status_code=303)

    @rt("/logout")
    def logout(sess: dict):
        """Logout handler"""
        logout_user(sess)
        return RedirectResponse("/", status_code=303)
