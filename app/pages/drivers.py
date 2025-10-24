import reflex as rx
from app.states.driver_state import DriverState
from app.components.ui import md_button, md_input, md_card
from app.components.sidebar import sidebar
from app.app import require_login


def _status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Active",
                "bg-green-100 text-green-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full",
            ),
            (
                "Inactive",
                "bg-red-100 text-red-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full",
            ),
            "bg-gray-100 text-gray-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-full",
        ),
    )


def _driver_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                md_card(
                    rx.el.form(
                        rx.radix.primitives.dialog.title(
                            rx.cond(
                                DriverState.is_editing, "Edit Driver", "Add New Driver"
                            ),
                            class_name="text-xl font-bold text-gray-800 mb-4",
                        ),
                        rx.el.div(
                            md_input(
                                placeholder="Full Name",
                                name="name",
                                default_value=DriverState.driver_form_data.get(
                                    "name", ""
                                ),
                                key=f"{DriverState.is_editing}-{DriverState.editing_driver_id}-name",
                            ),
                            rx.cond(
                                DriverState.form_errors.contains("name"),
                                rx.el.p(
                                    DriverState.form_errors["name"],
                                    class_name="text-red-500 text-sm mt-1",
                                ),
                                None,
                            ),
                            md_input(
                                placeholder="Contact Number",
                                name="contact_number",
                                default_value=DriverState.driver_form_data.get(
                                    "contact_number", ""
                                ),
                                key=f"{DriverState.is_editing}-{DriverState.editing_driver_id}-contact",
                            ),
                            rx.cond(
                                DriverState.form_errors.contains("contact_number"),
                                rx.el.p(
                                    DriverState.form_errors["contact_number"],
                                    class_name="text-red-500 text-sm mt-1",
                                ),
                                None,
                            ),
                            md_input(
                                placeholder="License Number",
                                name="license_number",
                                default_value=DriverState.driver_form_data.get(
                                    "license_number", ""
                                ),
                                key=f"{DriverState.is_editing}-{DriverState.editing_driver_id}-license",
                            ),
                            rx.cond(
                                DriverState.form_errors.contains("license_number"),
                                rx.el.p(
                                    DriverState.form_errors["license_number"],
                                    class_name="text-red-500 text-sm mt-1",
                                ),
                                None,
                            ),
                            md_input(
                                placeholder="License Expiry",
                                name="license_expiry",
                                type="date",
                                default_value=DriverState.driver_form_data.get(
                                    "license_expiry", ""
                                ),
                                key=f"{DriverState.is_editing}-{DriverState.editing_driver_id}-expiry",
                            ),
                            rx.cond(
                                DriverState.form_errors.contains("license_expiry"),
                                rx.el.p(
                                    DriverState.form_errors["license_expiry"],
                                    class_name="text-red-500 text-sm mt-1",
                                ),
                                None,
                            ),
                            rx.el.select(
                                rx.el.option("Active", value="Active"),
                                rx.el.option("Inactive", value="Inactive"),
                                name="status",
                                default_value=DriverState.driver_form_data.get(
                                    "status", "Active"
                                ),
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-shadow",
                            ),
                            class_name="flex flex-col gap-4",
                        ),
                        rx.el.div(
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    "Cancel",
                                    type="button",
                                    on_click=DriverState.close_driver_modal,
                                    class_name="bg-gray-200 text-gray-800 font-medium py-2 px-4 rounded-full hover:bg-gray-300 transition-colors",
                                )
                            ),
                            md_button(
                                rx.cond(
                                    DriverState.is_editing, "Save Changes", "Add Driver"
                                ),
                                type="submit",
                            ),
                            class_name="flex justify-end gap-4 mt-6",
                        ),
                        on_submit=DriverState.handle_driver_submit,
                        reset_on_submit=False,
                    )
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 max-w-lg w-full",
            ),
        ),
        open=DriverState.show_driver_modal,
        on_open_change=DriverState.set_show_driver_modal,
    )


def _delete_confirm_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                md_card(
                    rx.radix.primitives.dialog.title(
                        "Confirm Deletion",
                        class_name="text-xl font-bold text-gray-800 mb-2",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Are you sure you want to delete this driver? This action cannot be undone.",
                        class_name="text-gray-600 mb-6",
                    ),
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Cancel",
                                on_click=DriverState.close_delete_confirm,
                                class_name="bg-gray-200 text-gray-800 font-medium py-2 px-4 rounded-full hover:bg-gray-300 transition-colors",
                            )
                        ),
                        rx.el.button(
                            "Delete",
                            on_click=DriverState.delete_driver,
                            class_name="bg-red-600 text-white font-medium py-2 px-4 rounded-full hover:bg-red-700 transition-colors",
                        ),
                        class_name="flex justify-end gap-4",
                    ),
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50",
            ),
        ),
        open=DriverState.show_delete_confirm,
        on_open_change=DriverState.set_show_delete_confirm,
    )


def _drivers_table() -> rx.Component:
    return md_card(
        rx.el.div(
            rx.el.h3("Manage Drivers", class_name="text-2xl font-bold text-gray-800"),
            md_button(
                rx.el.span(
                    rx.icon("plus", class_name="mr-2"),
                    "Add Driver",
                    class_name="flex items-center",
                ),
                on_click=DriverState.open_add_modal,
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Name",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Contact",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "License No.",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "License Expiry",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Status",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Actions",
                            class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        class_name="bg-gray-50",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        DriverState.drivers,
                        lambda driver: rx.el.tr(
                            rx.el.td(
                                driver["name"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
                            ),
                            rx.el.td(
                                driver["contact_number"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                driver["license_number"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                driver["license_expiry"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                _status_badge(driver["status"]),
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.button(
                                        rx.icon("pencil", class_name="h-4 w-4"),
                                        on_click=lambda: DriverState.open_edit_modal(
                                            driver["id"]
                                        ),
                                        class_name="p-2 text-gray-500 hover:text-teal-600 hover:bg-gray-100 rounded-full transition-colors",
                                    ),
                                    rx.el.button(
                                        rx.icon("trash-2", class_name="h-4 w-4"),
                                        on_click=lambda: DriverState.open_delete_confirm(
                                            driver["id"]
                                        ),
                                        class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-gray-100 rounded-full transition-colors",
                                    ),
                                    class_name="flex items-center justify-end gap-2",
                                ),
                                class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
                            ),
                            class_name="border-b border-gray-200",
                        ),
                    ),
                    class_name="bg-white divide-y divide-gray-200",
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="overflow-x-auto border border-gray-200 rounded-lg",
        ),
        _driver_modal(),
        _delete_confirm_dialog(),
    )


def drivers_page() -> rx.Component:
    return require_login(
        rx.el.div(
            sidebar(),
            rx.el.main(
                _drivers_table(),
                class_name="flex-1 p-6",
                on_mount=DriverState.get_all_drivers,
            ),
            class_name="flex min-h-screen font-['Inter'] bg-gray-50",
        )
    )