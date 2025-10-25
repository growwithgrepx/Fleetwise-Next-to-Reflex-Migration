import reflex as rx
from app.states.driver_state import DriverState
from app.components.ui import md_button, md_input, md_card, badge_success, badge_error, alert_error, alert_success, heading_2, label_text
from app.components.sidebar import sidebar
from app.styles import COMPONENTS, COLORS, LAYOUT


def status_badge(status: str) -> rx.Component:
    """Status badge component."""
    return rx.cond(
        status == "active",
        badge_success(status.capitalize()),
        badge_error(status.capitalize()),
    )


def driver_form() -> rx.Component:
    """Driver form component."""
    return rx.el.form(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    label_text("First Name"),
                    md_input(
                        placeholder="First Name",
                        name="first_name",
                        default_value=DriverState.current_driver.first_name,
                        key=f"fn-{DriverState.current_driver.id}",
                    ),
                    class_name="space-y-2",
                ),
                rx.el.div(
                    label_text("Last Name"),
                    md_input(
                        placeholder="Last Name",
                        name="last_name",
                        default_value=DriverState.current_driver.last_name,
                        key=f"ln-{DriverState.current_driver.id}",
                    ),
                    class_name="space-y-2",
                ),
                class_name="flex flex-col md:flex-row gap-4",
            ),
            rx.el.div(
                label_text("Email"),
                md_input(
                    placeholder="Email",
                    type="email",
                    name="email",
                    default_value=DriverState.current_driver.email,
                    key=f"email-{DriverState.current_driver.id}",
                ),
                class_name="space-y-2",
            ),
            rx.el.div(
                label_text("Phone"),
                md_input(
                    placeholder="Phone",
                    name="phone",
                    default_value=DriverState.current_driver.phone,
                    key=f"phone-{DriverState.current_driver.id}",
                ),
                class_name="space-y-2",
            ),
            rx.el.div(
                label_text("License Number"),
                md_input(
                    placeholder="License Number",
                    name="license_number",
                    default_value=DriverState.current_driver.license_number,
                    key=f"lic_num-{DriverState.current_driver.id}",
                ),
                class_name="space-y-2",
            ),
            rx.el.div(
                label_text("License Expiry"),
                md_input(
                    type="date",
                    name="license_expiry",
                    default_value=DriverState.current_driver.license_expiry,
                    key=f"lic_exp-{DriverState.current_driver.id}",
                ),
                class_name="space-y-2",
            ),
            rx.el.div(
                label_text("Status"),
                rx.el.select(
                    rx.el.option("active", value="active"),
                    rx.el.option("inactive", value="inactive"),
                    name="status",
                    default_value=DriverState.current_driver.status,
                    key=f"status-{DriverState.current_driver.id}",
                    class_name=COMPONENTS["input"],
                ),
                class_name="space-y-2",
            ),
            rx.el.div(
                rx.foreach(
                    DriverState.form_errors,
                    lambda error: rx.el.div(error, class_name=f"text-{COLORS['error']} text-sm font-medium"),
                ),
                class_name="mt-2 space-y-1",
            ),
            class_name="flex flex-col gap-4",
        ),
        on_submit=DriverState.handle_driver_submit,
        reset_on_submit=True,
        id="driver-form",
    )


def driver_modal() -> rx.Component:
    """Modal for adding/editing drivers."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name=f"fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    rx.cond(DriverState.is_edit_mode, "Edit Driver", "Add Driver"),
                    class_name=f"text-2xl font-bold text-{COLORS['text_primary']}",
                ),
                rx.radix.primitives.dialog.description(driver_form()),
                rx.el.div(
                    md_button(
                        "Cancel",
                        on_click=DriverState.close_modal,
                        variant="secondary",
                    ),
                    md_button(
                        rx.cond(
                            DriverState.is_edit_mode, "Save Changes", "Create Driver"
                        ),
                        type="submit",
                        form="driver-form",
                        is_loading=DriverState.is_saving,
                    ),
                    class_name="flex justify-end gap-3 pt-4",
                ),
                class_name=COMPONENTS["modal"],
            ),
        ),
        open=DriverState.show_modal,
        on_open_change=DriverState.close_modal,
    )


def delete_confirmation_dialog() -> rx.Component:
    """Delete confirmation dialog."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Confirm Deletion", class_name=f"text-2xl font-bold text-{COLORS['text_primary']}"
                ),
                rx.radix.primitives.dialog.description(
                    "Are you sure you want to delete this driver? This action cannot be undone.",
                    class_name=f"text-{COLORS['text_secondary']}",
                ),
                rx.el.div(
                    md_button(
                        "Cancel",
                        on_click=DriverState.close_delete_confirm,
                        variant="secondary",
                    ),
                    md_button(
                        "Delete",
                        on_click=DriverState.confirm_delete,
                        variant="danger",
                    ),
                    class_name="flex justify-end gap-3 mt-4",
                ),
                class_name=COMPONENTS["modal"],
            ),
        ),
        open=DriverState.deleting_driver_id != 0,
        on_open_change=DriverState.close_delete_confirm,
    )


def driver_row(driver: rx.Var) -> rx.Component:
    """Single driver row component."""
    return rx.el.div(
        rx.el.div(
            rx.el.input(
                type="checkbox",
                class_name=f"w-4 h-4 rounded border-{COLORS['border_main']} bg-{COLORS['surface_dark']} text-{COLORS['secondary_main']}",
            ),
            class_name="w-12 flex items-center justify-center",
        ),
        rx.el.p(
            f"{driver.first_name} {driver.last_name}",
            class_name=f"w-1/4 truncate text-{COLORS['text_primary']} font-medium",
        ),
        rx.el.p(
            driver.phone,
            class_name=f"w-1/5 truncate text-{COLORS['text_secondary']} hidden md:block",
        ),
        rx.el.p(
            driver.license_number,
            class_name=f"w-1/3 truncate text-{COLORS['text_secondary']} hidden lg:block",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("pencil", size=18),
                on_click=DriverState.open_edit_modal(driver.id),
                class_name=f"p-2 rounded-lg hover:bg-{COLORS['surface_light']} text-{COLORS['secondary_main']} transition-colors",
            ),
            rx.el.button(
                rx.icon("trash-2", size=18),
                on_click=DriverState.open_delete_confirm(driver.id),
                class_name=f"p-2 rounded-lg hover:bg-{COLORS['error']}/10 text-{COLORS['error']} transition-colors",
            ),
            class_name="w-32 flex items-center justify-end gap-1",
        ),
        class_name=f"flex items-center px-6 py-4 border-b border-{COLORS['border_main']} hover:bg-{COLORS['surface_light']} transition-colors",
    )


def drivers_table() -> rx.Component:
    """Responsive drivers table matching target design."""
    header = rx.el.div(
        rx.el.div(class_name="w-12"),
        rx.el.p("Name", class_name=f"font-semibold w-1/4 text-{COLORS['text_secondary']}"),
        rx.el.p("Mobile", class_name=f"font-semibold w-1/5 text-{COLORS['text_secondary']} hidden md:block"),
        rx.el.p("Vehicle", class_name=f"font-semibold w-1/3 text-{COLORS['text_secondary']} hidden lg:block"),
        rx.el.p("Actions", class_name=f"font-semibold w-32 text-right text-{COLORS['text_secondary']}"),
        class_name=f"flex items-center px-6 py-4 border-b border-{COLORS['border_main']} bg-{COLORS['surface_dark']}",
    )
    
    rows = rx.el.div(
        rx.foreach(DriverState.drivers, driver_row),
        class_name="flex flex-col",
    )
    
    return rx.el.div(
        header,
        rx.cond(
            DriverState.is_loading,
            rx.el.div(
                rx.spinner(size="3", class_name=f"text-{COLORS['secondary_main']}"),
                class_name="p-10 w-full flex justify-center",
            ),
            rows,
        ),
        class_name=f"w-full bg-{COLORS['surface_main']} rounded-xl border border-{COLORS['border_main']} overflow-hidden",
    )


def drivers_page() -> rx.Component:
    """Responsive drivers management page."""
    return rx.el.div(
        sidebar(),
        rx.el.div(
            rx.el.div(
                rx.el.h1("Drivers", class_name=f"text-3xl font-bold text-{COLORS['text_primary']}"),
                md_button(
                    rx.icon("plus", size=20, class_name="mr-2"),
                    "Add Driver",
                    on_click=DriverState.open_add_modal,
                    class_name="flex items-center",
                ),
                class_name=f"flex flex-col md:flex-row justify-between items-start md:items-center gap-4 w-full p-8 bg-{COLORS['primary_main']}",
            ),
            rx.cond(
                DriverState.error != "",
                alert_error(DriverState.error, class_name="mx-8 mt-6"),
            ),
            rx.cond(
                DriverState.success != "",
                alert_success(DriverState.success, class_name="mx-8 mt-6"),
            ),
            rx.el.div(
                drivers_table(),
                class_name="p-8",
            ),
            driver_modal(),
            delete_confirmation_dialog(),
            class_name=f"flex-1 flex flex-col bg-{COLORS['primary_main']} overflow-auto w-full",
        ),
        class_name=f"flex min-h-screen bg-{COLORS['primary_main']}",
    )