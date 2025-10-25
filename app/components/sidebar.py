import reflex as rx
from app.states.auth_state import AuthState
from app.components.ui import md_button
from app.styles import SIDEBAR, COLORS


def sidebar() -> rx.Component:
    """Responsive sidebar component matching target design."""
    return rx.el.aside(
        rx.el.div(
            # Header
            rx.el.div(
                rx.icon("truck", class_name=f"h-6 w-6 text-{COLORS['text_primary']}"),
                rx.el.h2("Fleetwise", class_name=f"text-xl font-bold text-{COLORS['text_primary']}"),
                class_name=f"flex items-center gap-3 p-6 border-b border-{COLORS['border_main']}",
            ),
            # Navigation
            rx.el.nav(
                rx.el.a(
                    rx.icon("layout-dashboard", class_name=f"h-5 w-5"),
                    "Dashboard",
                    href="/",
                    class_name=f"flex items-center gap-3 px-6 py-3 text-{COLORS['text_secondary']} hover:bg-{COLORS['surface_light']} hover:text-{COLORS['text_primary']} transition-colors",
                ),
                rx.el.a(
                    rx.icon("users", class_name=f"h-5 w-5"),
                    "Drivers",
                    href="/drivers",
                    class_name=f"flex items-center gap-3 px-6 py-3 text-{COLORS['text_secondary']} hover:bg-{COLORS['surface_light']} hover:text-{COLORS['text_primary']} transition-colors",
                ),
                class_name="flex-1 py-4",
            ),
            # Footer
            rx.el.div(
                md_button(
                    "Logout",
                    on_click=AuthState.logout,
                    variant="secondary",
                    class_name="w-full",
                ),
                class_name=f"p-6 border-t border-{COLORS['border_main']}",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name=f"w-64 h-screen bg-{COLORS['primary_dark']} border-r border-{COLORS['border_main']} flex flex-col shrink-0",
    )