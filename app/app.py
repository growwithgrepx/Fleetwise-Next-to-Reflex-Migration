import reflex as rx
from app.states.auth_state import AuthState
from app.pages.login import login_page
from app.pages.drivers import drivers_page
from app.components.sidebar import sidebar

def require_login(page: rx.Component) -> rx.Component:
    """A decorator to require login for a page."""
    # If not authenticated, show the login page component instead of returning an event.
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
                        size="3",
                    ),
                    rx.text(
                        "Select an option from the sidebar to get started.",
                        color="gray.600",
                    ),
                    align="start",
                    spacing="4",
                ),
                padding="6",
            ),
            class_name="min-h-screen bg-gray-50",
        )
    )

# Configure the app
app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="teal",
        has_background=True,
    ),
    style={
        "font-family": "Inter, sans-serif",
    },
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ]
)

# Add pages
app.add_page(index, route="/")
app.add_page(login_page, route="/login")
app.add_page(drivers_page, route="/drivers")