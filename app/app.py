import reflex as rx
from app.states.auth_state import AuthState
from app.states.driver_state import DriverState
from app.pages.login import login_page
from app.pages.drivers import drivers_page
from app.components.sidebar import sidebar

def require_login(page: rx.Component) -> rx.Component:
    """A decorator to require login for a page."""
    return rx.cond(
        AuthState.is_authenticated,
        page,
        login_page(),
    )

def index() -> rx.Component:
    """The main dashboard page."""
    return require_login(
        rx.box(
            sidebar(),
            rx.box(
                rx.vstack(
                    rx.heading(
                        "Welcome to Fleetwise",
                        size="6",
                    ),
                    rx.text(
                        "Select an option from the sidebar to get started.",
                        color="gray",
                        size="3",
                    ),
                    align="start",
                    spacing="4",
                ),
                padding="6",
                flex="1",
            ),
            class_name="flex min-h-screen bg-gray-50",
        )
    )

def protected_drivers_page() -> rx.Component:
    """Protected drivers page that requires authentication."""
    return require_login(drivers_page())

# Configure the app
app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="teal",
        has_background=True,
    ),
    style={
        "font_family": "Inter, sans-serif",
    },
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ]
)

# Add pages
app.add_page(index, route="/", title="Dashboard - Fleetwise")
app.add_page(login_page, route="/login", title="Login - Fleetwise")
app.add_page(protected_drivers_page, route="/drivers", title="Drivers - Fleetwise", on_load=DriverState.fetch_drivers)