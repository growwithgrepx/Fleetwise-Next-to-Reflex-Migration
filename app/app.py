import reflex as rx
from app.states.auth_state import AuthState
from app.pages.login import login_page
from app.components.sidebar import sidebar


def require_login(page: rx.Component) -> rx.Component:
    """A decorator to require login for a page."""
    return rx.cond(AuthState.is_authenticated, page, login_page())


def index() -> rx.Component:
    """The main dashboard page."""
    return require_login(
        rx.el.div(
            sidebar(),
            rx.el.main(
                rx.el.div(
                    rx.el.h1(
                        "Welcome to Fleetwise",
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "Select an option from the sidebar to get started.",
                        class_name="text-gray-600",
                    ),
                    class_name="p-6",
                ),
                class_name="flex-1",
            ),
            class_name="flex min-h-screen font-['Inter'] bg-gray-50",
        )
    )


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="teal"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
from app.pages.drivers import drivers_page

app.add_page(index, route="/")
app.add_page(login_page, route="/login")
app.add_page(drivers_page, route="/drivers")