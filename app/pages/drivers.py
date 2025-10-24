import reflex as rx
from app.states.driver_state import DriverState
from app.components.ui import md_button, md_input, md_card
from app.components.sidebar import sidebar

def status_badge(status: str) -> rx.Component:
    """Render a status badge with appropriate color."""
    return rx.badge(
        status.capitalize(),
        color_scheme="green" if status == "active" else "red",
        variant="subtle",
        border_radius="full"
    )

def driver_form() -> rx.Component:
    """Render the driver form for adding/editing."""
    return rx.form(
        rx.vstack(
            rx.hstack(
                rx.input(
                    placeholder="First Name",
                    name="first_name",
                    default_value=DriverState.current_driver.get("first_name", ""),
                ),
                rx.input(
                    placeholder="Last Name",
                    name="last_name",
                    default_value=DriverState.current_driver.get("last_name", ""),
                ),
            ),
            rx.input(
                placeholder="Email",
                type_="email",
                name="email",
                default_value=DriverState.current_driver.get("email", ""),
            ),
            rx.input(
                placeholder="Phone",
                name="phone",
                default_value=DriverState.current_driver.get("phone", ""),
            ),
            rx.input(
                placeholder="License Number",
                name="license_number",
                default_value=DriverState.current_driver.get("license_number", ""),
            ),
            rx.input(
                type_="date",
                name="license_expiry",
                default_value=DriverState.current_driver.get("license_expiry", ""),
            ),
            rx.select(
                ["active", "inactive"],
                placeholder="Status",
                name="status",
                default_value=DriverState.current_driver.get("status", "active"),
            ),
            rx.button(
                "Save",
                type_="submit",
                width="100%",
            ),
            spacing="4",
        ),
        on_submit=DriverState.handle_driver_submit,
    )

def driver_modal() -> rx.Component:
    """Modal for adding/editing drivers."""
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header(
                    rx.heading(
                        "Edit Driver" if DriverState.is_edit_mode else "Add Driver"
                    )
                ),
                rx.modal_body(driver_form()),
                rx.modal_footer(
                    rx.button(
                        "Close",
                        on_click=DriverState.close_modal,
                    )
                ),
            )
        ),
        is_open=DriverState.show_modal,
    )

def drivers_table() -> rx.Component:
    """Render the drivers table."""
    # Simple stacked list since Reflex doesn't provide table primitives
    header = rx.hstack(
        rx.text("Name", class_name="font-semibold w-1/4"),
        rx.text("Email", class_name="font-semibold w-1/4"),
        rx.text("Phone", class_name="font-semibold w-1/6"),
        rx.text("License", class_name="font-semibold w-1/6"),
        rx.text("Status", class_name="font-semibold w-1/12"),
        rx.text("Actions", class_name="font-semibold w-1/12 text-right"),
        class_name="px-4 py-2 border-b",
    )

    # Use rx.foreach to iterate over the Var list `DriverState.drivers`.
    # Each `d` here is a Var representing the driver dict; access fields via .get or indexing.
    rows = rx.vstack(
        rx.foreach(
            DriverState.drivers,
            lambda d: rx.hstack(
                rx.text(f"{d.get('first_name','')} {d.get('last_name','')}", class_name="w-1/4"),
                rx.text(d.get('email',''), class_name="w-1/4"),
                rx.text(d.get('phone',''), class_name="w-1/6"),
                rx.vstack(
                    rx.text(d.get('license_number','')),
                    rx.text(f"Expires: {d.get('license_expiry','')}", class_name="text-sm text-gray-600"),
                    class_name="w-1/6",
                ),
                rx.text(d.get('status',''), class_name="w-1/12"),
                rx.hstack(
                    rx.button("Edit", size="sm", on_click=lambda _=None, _id=d.get('id'): DriverState.open_edit_modal(_id)),
                    rx.button("Delete", size="sm", on_click=lambda _=None, _id=d.get('id'): DriverState.open_delete_confirm(_id), class_name="ml-2 bg-red-600 text-white"),
                    class_name="w-1/12 justify-end",
                ),
                class_name="px-4 py-3 border-b items-center",
            ),
        ),
        spacing="0",
    )

    return rx.vstack(header, rows, class_name="w-full bg-white rounded shadow-sm")

def drivers_page() -> rx.Component:
    """The main drivers management page."""
    return rx.box(
        sidebar(),
        rx.box(
            rx.hstack(
                rx.heading("Drivers", size="3"),
                rx.spacer(),
                rx.button(
                    "Add Driver",
                    on_click=DriverState.open_add_modal,
                ),
                width="100%",
                padding="4",
            ),
            rx.cond(
                DriverState.error,
                rx.box(
                    DriverState.error,
                    class_name="text-red-600 bg-red-50 border border-red-100 p-3 rounded mb-4",
                ),
            ),
            rx.cond(
                DriverState.success,
                rx.box(
                    DriverState.success,
                    class_name="text-green-700 bg-green-50 border border-green-100 p-3 rounded mb-4",
                ),
            ),
            drivers_table(),
            driver_modal(),
            padding="4",
        ),
        class_name="min-h-screen bg-gray-50",
    )
