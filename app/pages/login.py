import reflex as rx
from app.states.auth_state import AuthState
from app.components.ui import md_input, md_button, md_card


def login_page() -> rx.Component:
    """The login page for the Fleetwise app."""
    return rx.el.main(
        rx.el.div(
            md_card(
                rx.el.form(
                    rx.el.div(
                        rx.el.div(
                            rx.icon("truck", class_name="h-10 w-10 text-teal-600"),
                            rx.el.h1(
                                "Fleetwise Login",
                                class_name="text-2xl font-bold text-gray-800",
                            ),
                            class_name="flex flex-col items-center text-center gap-2 mb-6",
                        ),
                        md_input(placeholder="Email", name="email", type="email"),
                        md_input(
                            placeholder="Password", name="password", type="password"
                        ),
                        rx.cond(
                            AuthState.error_message != "",
                            rx.el.p(
                                AuthState.error_message,
                                class_name="text-red-500 text-sm mt-2 text-center",
                            ),
                            None,
                        ),
                        md_button(
                            "Login", type="submit", width="100%", class_name="mt-4"
                        ),
                        class_name="flex flex-col gap-4",
                    ),
                    on_submit=AuthState.login,
                ),
                max_width="400px",
            ),
            class_name="flex items-center justify-center min-h-screen bg-gray-50",
        ),
        class_name="font-['Inter'] bg-white",
    )