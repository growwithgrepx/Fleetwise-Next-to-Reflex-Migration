import reflex as rx
from app.states.auth_state import AuthState
from app.components.ui import md_input, md_button, md_card, heading_1, label_text, alert_error
from app.styles import COLORS, LAYOUT


def login_page() -> rx.Component:
    """Responsive login page."""
    return rx.el.main(
        rx.el.div(
            md_card(
                rx.el.form(
                    rx.el.div(
                        # Header
                        rx.el.div(
                            rx.icon("truck", class_name=f"h-12 w-12 text-{COLORS['secondary_main']}"),
                            rx.el.h1("Sign in to your account", class_name=f"text-2xl font-bold text-{COLORS['text_primary']} mt-4"),
                            class_name="flex flex-col items-center text-center gap-2 mb-8",
                        ),
                        # Email field
                        rx.el.div(
                            label_text("Email"),
                            md_input(
                                placeholder="admin@fleetwise.com",
                                name="email",
                                type="email",
                                default_value="",
                            ),
                            class_name="space-y-2",
                        ),
                        # Password field
                        rx.el.div(
                            label_text("Password"),
                            md_input(
                                placeholder="••••••••",
                                name="password",
                                type="password",
                                default_value="",
                            ),
                            class_name="space-y-2",
                        ),
                        # Forgot password link
                        rx.el.a(
                            "Forgot your password?",
                            href="#",
                            class_name=f"text-{COLORS['secondary_main']} hover:text-{COLORS['secondary_light']} text-sm font-medium transition-colors",
                        ),
                        # Error message
                        rx.cond(
                            AuthState.error,
                            alert_error(AuthState.error),
                        ),
                        # Submit button
                        md_button("Sign In", type="submit", class_name="w-full mt-6"),
                        class_name="flex flex-col gap-4",
                    ),
                    on_submit=AuthState.login,
                ),
                class_name="max-w-md w-full mx-4 md:mx-0",
            ),
            class_name=f"flex items-center justify-center min-h-screen bg-{COLORS['primary_main']} px-4",
        ),
        class_name=f"bg-{COLORS['primary_main']}",
    )