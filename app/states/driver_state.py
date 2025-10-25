import reflex as rx
import requests
from typing import Optional
import logging
from .auth_state import AuthState
from .base_state import API_BASE_URL
from pydantic import BaseModel


class Driver(BaseModel):
    id: int | None = None
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    license_number: str = ""
    license_expiry: str = ""
    status: str = "active"


class DriverState(AuthState):
    """State for managing drivers."""

    drivers: list[Driver] = []
    current_driver: Driver = Driver()
    show_modal: bool = False
    is_edit_mode: bool = False
    is_saving: bool = False
    form_errors: list[str] = []
    deleting_driver_id: int = 0

    @rx.event
    async def on_load_fetch_drivers(self):
        """Event handler for page load. Ensures user is authenticated before fetching."""
        if not self.is_authenticated:
            return rx.redirect("/login")
        await self._fetch_drivers()

    async def _fetch_drivers(self):
        """Internal method to fetch all drivers from the API."""
        self.is_loading = True
        self.clear_messages()
        try:
            auth_headers = await self.get_var_value(self.auth_headers)
            resp = requests.get(
                f"{API_BASE_URL}/drivers", headers=auth_headers, timeout=5
            )
            resp.raise_for_status()
            self.drivers = [Driver(**d) for d in resp.json()]
        except requests.exceptions.RequestException as e:
            logging.exception(f"Error: {e}")
            self.show_error(
                f"API Error: Could not fetch drivers. Please ensure the backend is running."
            )
        finally:
            self.is_loading = False

    @rx.event
    def open_add_modal(self):
        """Open the modal to add a new driver."""
        self.clear_messages()
        self.form_errors = []
        self.current_driver = Driver(status="active")
        self.is_edit_mode = False
        self.show_modal = True

    @rx.event
    def open_edit_modal(self, driver_id: int):
        """Open the modal to edit an existing driver."""
        self.clear_messages()
        self.form_errors = []
        driver = next((d for d in self.drivers if d.id == driver_id), None)
        if not driver:
            self.show_error("Driver not found.")
            return
        self.current_driver = driver
        self.is_edit_mode = True
        self.show_modal = True

    def _validate_driver_form(self) -> bool:
        """Validate the driver form data."""
        self.form_errors = []
        if not self.current_driver.first_name.strip():
            self.form_errors.append("First name is required.")
        if not self.current_driver.last_name.strip():
            self.form_errors.append("Last name is required.")
        if not self.current_driver.email.strip():
            self.form_errors.append("Email is required.")
        if not self.current_driver.license_number.strip():
            self.form_errors.append("License number is required.")
        if not self.current_driver.license_expiry:
            self.form_errors.append("License expiry date is required.")
        return len(self.form_errors) == 0

    async def _save_driver(self):
        """Internal method to create or update a driver via API."""
        self.is_saving = True
        self.clear_messages()
        if not self._validate_driver_form():
            self.is_saving = False
            return
        json_data = self.current_driver.model_dump(
            exclude={"id"} if not self.is_edit_mode else None
        )
        try:
            auth_headers = await self.get_var_value(self.auth_headers)
            if self.is_edit_mode and self.current_driver.id:
                url = f"{API_BASE_URL}/drivers/{self.current_driver.id}"
                resp = requests.put(
                    url, json=json_data, headers=auth_headers, timeout=5
                )
            else:
                url = f"{API_BASE_URL}/drivers"
                resp = requests.post(
                    url, json=json_data, headers=auth_headers, timeout=5
                )
            resp.raise_for_status()
            self.show_success("Driver saved successfully!")
            await self._fetch_drivers()
            self.close_modal()
        except requests.exceptions.RequestException as e:
            logging.exception(f"Error: {e}")
            self.show_error(f"API Error: Failed to save driver.")
        finally:
            self.is_saving = False

    @rx.event
    async def save_driver_from_modal(self):
        """Event handler to save the driver from the modal form."""
        await self._save_driver()

    @rx.event
    async def delete_driver(self):
        """Delete a driver after confirmation."""
        if self.deleting_driver_id == 0:
            self.show_error("No driver selected for deletion.")
            return
        self.is_loading = True
        self.clear_messages()
        try:
            auth_headers = await self.get_var_value(self.auth_headers)
            url = f"{API_BASE_URL}/drivers/{self.deleting_driver_id}"
            resp = requests.delete(url, headers=auth_headers, timeout=5)
            resp.raise_for_status()
            self.show_success("Driver deleted successfully.")
            await self._fetch_drivers()
        except requests.exceptions.RequestException as e:
            logging.exception(f"Error: {e}")
            self.show_error(f"API Error: Failed to delete driver.")
        finally:
            self.close_delete_confirm()
            self.is_loading = False

    @rx.event
    def close_modal(self):
        """Close the add/edit modal and reset state."""
        self.show_modal = False
        self.current_driver = Driver()
        self.is_edit_mode = False
        self.is_saving = False
        self.form_errors = []

    @rx.event
    async def handle_driver_submit(self, form_data: dict):
        """Handle form submission from the modal."""
        if not isinstance(form_data, dict):
            self.show_error("Invalid form submission")
            return
        self.current_driver.first_name = str(form_data.get("first_name", ""))
        self.current_driver.last_name = str(form_data.get("last_name", ""))
        self.current_driver.email = str(form_data.get("email", ""))
        self.current_driver.phone = str(form_data.get("phone", ""))
        self.current_driver.license_number = str(form_data.get("license_number", ""))
        self.current_driver.license_expiry = str(form_data.get("license_expiry", ""))
        self.current_driver.status = str(form_data.get("status", "active"))
        await self._save_driver()

    @rx.event
    def open_delete_confirm(self, driver_id: int):
        """Open the delete confirmation dialog."""
        self.clear_messages()
        self.deleting_driver_id = driver_id

    @rx.event
    def close_delete_confirm(self):
        """Close the delete confirmation dialog."""
        self.deleting_driver_id = 0