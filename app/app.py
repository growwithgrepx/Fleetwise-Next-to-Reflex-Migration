import reflex as rx
from app.states.auth_state import AuthState
from app.states.driver_state import DriverState
from app.pages.login import login_page
from app.pages.drivers import drivers_page
from app.components.sidebar import sidebar
from app.components.ui import heading_1, body_text
from app.styles import LAYOUT, COLORS


def require_login(page: rx.Component) -> rx.Component:
    """Require login for a page."""
    return rx.cond(AuthState.is_authenticated, page, login_page())


def index() -> rx.Component:
    """Responsive dashboard page."""
    return require_login(
        rx.el.div(
            sidebar(),
            rx.el.div(
                rx.el.div(
                    rx.el.h1("Welcome to Fleetwise", class_name=f"text-4xl font-bold text-{COLORS['text_primary']} mb-4"),
                    rx.el.p("Select an option from the sidebar to get started.", class_name=f"text-lg text-{COLORS['text_secondary']}"),
                ),
                class_name=f"flex-1 p-8 bg-{COLORS['primary_main']}",
                style={"minHeight": "100vh"},
            ),
            class_name=f"flex min-h-screen bg-{COLORS['primary_main']}",
        )
    )


def protected_drivers_page() -> rx.Component:
    """Protected drivers page that requires authentication."""
    return require_login(drivers_page())


app = rx.App(
    theme=rx.theme(appearance="dark", accent_color="blue", has_background=False),
    style={
        "font_family": "Inter, sans-serif",
        "background_color": COLORS["primary_main"],
    },
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
    ],
)
app.add_page(index, route="/", title="Dashboard - Fleetwise")
app.add_page(login_page, route="/login", title="Login - Fleetwise")
app.add_page(
    protected_drivers_page,
    route="/drivers",
    title="Drivers - Fleetwise",
    on_load=DriverState.on_load_fetch_drivers,
)