import reflex as rx
from app.states.auth_state import AuthState
from app.components.ui import md_button


def sidebar() -> rx.Component:
    """The sidebar component for navigation."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("truck", class_name="h-8 w-8 text-teal-600"),
                rx.el.h2("Fleetwise", class_name="text-2xl font-bold text-gray-800"),
                class_name="flex items-center gap-3 p-4 border-b",
            ),
            rx.el.nav(
                rx.el.a(
                    rx.icon("layout-dashboard", class_name="h-5 w-5"),
                    "Dashboard",
                    href="/",
                    class_name="flex items-center gap-3 px-4 py-2 text-gray-700 font-medium rounded-lg hover:bg-gray-100 transition-colors",
                ),
                rx.el.a(
                    rx.icon("users", class_name="h-5 w-5"),
                    "Drivers",
                    href="/drivers",
                    class_name="flex items-center gap-3 px-4 py-2 text-gray-700 font-medium rounded-lg hover:bg-gray-100 transition-colors",
                ),
                class_name="flex-1 p-4",
            ),
            rx.el.div(
                md_button("Logout", on_click=AuthState.logout, width="100%"),
                class_name="p-4 border-t",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="w-64 h-screen bg-white border-r shrink-0",
    )