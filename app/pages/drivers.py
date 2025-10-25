import reflex as rx
from app.states.driver_state import DriverState
from app.components.ui import md_button, md_input, md_card
from app.components.sidebar import sidebar


def status_badge(status: str) -> rx.Component:
    """Render a status badge with appropriate color."""
    return rx.badge(
        status.capitalize(),
        color_scheme=rx.cond(status == "active", "green", "red"),
        variant="soft",
        radius="full",
    )


def driver_form() -> rx.Component:
    """Render the driver form for adding/editing."""
    return rx.el.div(
        rx.el.form(
            rx.el.div(
                rx.el.div(
                    md_input(
                        placeholder="First Name",
                        name="first_name",
                        default_value=DriverState.current_driver.first_name,
                        key=f"fn-{DriverState.show_modal}",
                    ),
                    md_input(
                        placeholder="Last Name",
                        name="last_name",
                        default_value=DriverState.current_driver.last_name,
                        key=f"ln-{DriverState.show_modal}",
                    ),
                    class_name="flex gap-4",
                ),
                md_input(
                    placeholder="Email",
                    type_="email",
                    name="email",
                    default_value=DriverState.current_driver.email,
                    key=f"email-{DriverState.show_modal}",
                ),
                md_input(
                    placeholder="Phone",
                    name="phone",
                    default_value=DriverState.current_driver.phone,
                    key=f"phone-{DriverState.show_modal}",
                ),
                md_input(
                    placeholder="License Number",
                    name="license_number",
                    default_value=DriverState.current_driver.license_number,
                    key=f"lic_num-{DriverState.show_modal}",
                ),
                rx.el.input(
                    type_="date",
                    name="license_expiry",
                    default_value=DriverState.current_driver.license_expiry,
                    key=f"lic_exp-{DriverState.show_modal}",
                    class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-shadow",
                ),
                rx.el.select(
                    rx.el.option("active", value="active"),
                    rx.el.option("inactive", value="inactive"),
                    placeholder="Status",
                    name="status",
                    default_value=DriverState.current_driver.status,
                    key=f"status-{DriverState.show_modal}",
                    class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-shadow",
                ),
                class_name="flex flex-col gap-4",
            ),
            on_submit=DriverState.handle_driver_submit,
            reset_on_submit=True,
            id="driver-form",
        ),
        rx.el.div(
            rx.foreach(
                DriverState.form_errors,
                lambda error: rx.el.p(error, class_name="text-red-500 text-sm"),
            ),
            class_name="mt-2",
        ),
    )


def driver_modal() -> rx.Component:
    """Modal for adding/editing drivers."""
    return rx.dialog.root(
        rx.dialog.trigger(rx.fragment()),
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(DriverState.is_edit_mode, "Edit Driver", "Add Driver")
            ),
            rx.dialog.description(driver_form()),
            rx.el.div(
                rx.dialog.close(
                    md_button(
                        "Cancel",
                        on_click=DriverState.close_modal,
                        bg="gray.200",
                        color="gray.800",
                        _hover={"bg": "gray.300"},
                    )
                ),
                md_button(
                    rx.cond(DriverState.is_edit_mode, "Save Changes", "Create Driver"),
                    type="submit",
                    form="driver-form",
                    is_loading=DriverState.is_saving,
                ),
                class_name="flex justify-end gap-3 pt-4",
            ),
            class_name="space-y-4",
        ),
        open=DriverState.show_modal,
    )


def delete_confirmation_dialog() -> rx.Component:
    """Modal to confirm driver deletion."""
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(rx.fragment()),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Confirm Deletion"),
            rx.alert_dialog.description(
                "Are you sure you want to delete this driver? This action cannot be undone."
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    md_button(
                        "Cancel",
                        on_click=DriverState.close_delete_confirm,
                        bg="gray.200",
                        color="gray.800",
                        _hover={"bg": "gray.300"},
                    )
                ),
                rx.alert_dialog.action(
                    md_button(
                        "Delete",
                        on_click=DriverState.delete_driver,
                        bg="red.500",
                        _hover={"bg": "red.600"},
                    )
                ),
                spacing="3",
                margin_top="4",
                justify="end",
            ),
        ),
        open=DriverState.deleting_driver_id != 0,
    )


def drivers_table() -> rx.Component:
    """Render the drivers table."""
    header = rx.el.div(
        rx.el.p("Name", class_name="font-semibold w-1/4"),
        rx.el.p("Email", class_name="font-semibold w-1/4"),
        rx.el.p("Phone", class_name="font-semibold w-1/6"),
        rx.el.p("License", class_name="font-semibold w-1/6"),
        rx.el.p("Status", class_name="font-semibold w-1/12"),
        rx.el.p("Actions", class_name="font-semibold w-1/12 text-right"),
        class_name="flex px-4 py-2 border-b",
    )
    rows = rx.el.div(
        rx.foreach(
            DriverState.drivers,
            lambda d: rx.el.div(
                rx.el.p(f"{d.first_name} {d.last_name}", class_name="w-1/4 truncate"),
                rx.el.p(d.email, class_name="w-1/4 truncate"),
                rx.el.p(d.phone, class_name="w-1/6 truncate"),
                rx.el.div(
                    rx.el.p(d.license_number, class_name="truncate"),
                    rx.el.p(
                        f"Expires: {d.license_expiry}",
                        class_name="text-sm text-gray-600",
                    ),
                    class_name="w-1/6 flex flex-col items-start",
                ),
                status_badge(d.status),
                rx.el.div(
                    md_button(
                        "Edit",
                        on_click=lambda: DriverState.open_edit_modal(d.id),
                        size="1",
                        bg="gray.200",
                        color="gray.800",
                        _hover={"bg": "gray.300"},
                    ),
                    md_button(
                        "Delete",
                        on_click=lambda: DriverState.open_delete_confirm(d.id),
                        size="1",
                        bg="red.100",
                        color="red.700",
                        _hover={"bg": "red.200"},
                    ),
                    class_name="w-1/12 flex justify-end gap-2",
                ),
                class_name="flex px-4 py-3 border-b items-center text-sm w-full",
            ),
        ),
        class_name="flex flex-col",
    )
    return rx.el.div(
        header,
        rx.cond(
            DriverState.is_loading,
            rx.el.div(
                rx.spinner(size="3"), class_name="p-10 w-full flex justify-center"
            ),
            rows,
        ),
        class_name="w-full bg-white rounded-lg shadow-sm border border-gray-100",
    )


def drivers_page() -> rx.Component:
    """The main drivers management page."""
    return rx.el.div(
        sidebar(),
        rx.el.div(
            rx.el.div(
                rx.el.h1("Drivers", class_name="text-2xl font-bold"),
                rx.el.div(),
                md_button("Add Driver", on_click=DriverState.open_add_modal),
                class_name="flex justify-between items-center w-full p-4",
            ),
            rx.cond(
                DriverState.error != "",
                rx.el.div(
                    DriverState.error,
                    class_name="text-red-600 bg-red-50 border border-red-100 p-3 rounded mb-4",
                ),
            ),
            rx.cond(
                DriverState.success != "",
                rx.el.div(
                    DriverState.success,
                    class_name="text-green-700 bg-green-50 border border-green-100 p-3 rounded mb-4",
                ),
            ),
            drivers_table(),
            driver_modal(),
            delete_confirmation_dialog(),
            class_name="p-4 flex-1 space-y-4",
        ),
        class_name="flex min-h-screen bg-gray-50",
    )