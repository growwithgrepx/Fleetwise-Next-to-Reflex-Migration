import reflex as rx
import requests
import logging
from typing import TypedDict, Optional
from app.states.auth_state import AuthState, API_URL


class Driver(TypedDict):
    id: int
    name: str
    contact_number: str
    license_number: str
    license_expiry: str
    status: str


class DriverState(AuthState):
    """State for managing drivers via API."""

    drivers: list[Driver] = []
    show_driver_modal: bool = False
    is_editing: bool = False
    editing_driver_id: Optional[int] = None
    driver_form_data: dict[str, str] = {}
    form_errors: dict[str, str] = {}
    show_delete_confirm: bool = False
    deleting_driver_id: Optional[int] = None

    @rx.event
    async def get_all_drivers(self):
        """Fetches all drivers from the backend API."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return
        try:
            response = requests.get(
                f"{API_URL}/api/drivers", headers=auth_state.auth_headers
            )
            response.raise_for_status()
            self.drivers = response.json()
        except requests.exceptions.HTTPError as e:
            logging.exception(f"HTTP Error fetching drivers: {e.response.text}")
            if e.response.status_code == 401:
                yield rx.toast("Session expired. Please log in again.", duration=3000)
                yield AuthState.logout
            else:
                yield rx.toast("Failed to fetch drivers.", duration=3000)
        except requests.exceptions.RequestException as e:
            logging.exception(f"Request Error fetching drivers: {e}")
            yield rx.toast(
                "Failed to fetch drivers. Check server connection.", duration=3000
            )

    @rx.event
    def open_add_modal(self):
        """Opens the modal to add a new driver."""
        self.is_editing = False
        self.editing_driver_id = None
        self.driver_form_data = {"status": "Active"}
        self.form_errors = {}
        self.show_driver_modal = True

    @rx.event
    async def open_edit_modal(self, driver_id: int):
        """Opens the modal to edit an existing driver."""
        auth_state = await self.get_state(AuthState)
        try:
            response = requests.get(
                f"{API_URL}/api/drivers/{driver_id}", headers=auth_state.auth_headers
            )
            response.raise_for_status()
            driver = response.json()
            self.is_editing = True
            self.editing_driver_id = driver_id
            self.driver_form_data = {
                "name": driver["name"],
                "contact_number": driver["contact_number"],
                "license_number": driver["license_number"],
                "license_expiry": driver["license_expiry"],
                "status": driver["status"],
            }
            self.form_errors = {}
            self.show_driver_modal = True
        except requests.exceptions.HTTPError as e:
            logging.exception(f"Error fetching driver details: {e.response.text}")
            yield rx.toast("Failed to load driver details.", duration=3000)

    @rx.event
    def close_driver_modal(self):
        """Closes the driver form modal."""
        self.show_driver_modal = False
        self.is_editing = False
        self.editing_driver_id = None
        self.driver_form_data = {}
        self.form_errors = {}

    def _validate_form(self, form_data: dict[str, str]) -> bool:
        """Validates the driver form data."""
        errors = {}
        if not form_data.get("name"):
            errors["name"] = "Name is required."
        if not form_data.get("contact_number"):
            errors["contact_number"] = "Contact number is required."
        if not form_data.get("license_number"):
            errors["license_number"] = "License number is required."
        if not form_data.get("license_expiry"):
            errors["license_expiry"] = "License expiry is required."
        self.form_errors = errors
        return not errors

    @rx.event
    async def handle_driver_submit(self, form_data: dict[str, str]):
        """Handles the submission of the driver form to the backend."""
        self.driver_form_data = form_data
        if not self._validate_form(form_data):
            return
        auth_state = await self.get_state(AuthState)
        headers = auth_state.auth_headers
        try:
            if self.is_editing and self.editing_driver_id is not None:
                response = requests.put(
                    f"{API_URL}/api/drivers/{self.editing_driver_id}",
                    headers=headers,
                    json=form_data,
                )
                response.raise_for_status()
                yield rx.toast("Driver updated successfully!", duration=3000)
            else:
                response = requests.post(
                    f"{API_URL}/api/drivers", headers=headers, json=form_data
                )
                response.raise_for_status()
                yield rx.toast("Driver added successfully!", duration=3000)
            yield DriverState.close_driver_modal
            yield DriverState.get_all_drivers
        except requests.exceptions.HTTPError as e:
            logging.exception(f"Error submitting driver form: {e.response.text}")
            if e.response.status_code == 401:
                yield rx.toast("Session expired.", duration=3000)
                yield AuthState.logout
            elif e.response.status_code == 422:
                yield rx.toast("Please correct the form errors.", duration=3000)
                self.form_errors = e.response.json().get("errors", {})
            else:
                yield rx.toast("An error occurred. Please try again.", duration=3000)
        except requests.exceptions.RequestException as e:
            logging.exception(f"Request Error: {e}")
            yield rx.toast("Could not connect to server.", duration=3000)

    @rx.event
    def open_delete_confirm(self, driver_id: int):
        """Opens the delete confirmation dialog."""
        self.deleting_driver_id = driver_id
        self.show_delete_confirm = True

    @rx.event
    def close_delete_confirm(self):
        """Closes the delete confirmation dialog."""
        self.deleting_driver_id = None
        self.show_delete_confirm = False

    @rx.event
    async def delete_driver(self):
        """Deletes a driver after confirmation via API."""
        if self.deleting_driver_id is not None:
            auth_state = await self.get_state(AuthState)
            try:
                response = requests.delete(
                    f"{API_URL}/api/drivers/{self.deleting_driver_id}",
                    headers=auth_state.auth_headers,
                )
                response.raise_for_status()
                yield rx.toast("Driver deleted successfully!", duration=3000)
                yield DriverState.get_all_drivers
            except requests.exceptions.HTTPError as e:
                logging.exception(f"Error deleting driver: {e.response.text}")
                if e.response.status_code == 401:
                    yield rx.toast("Session expired.", duration=3000)
                    yield AuthState.logout
                else:
                    yield rx.toast("Failed to delete driver.", duration=3000)
            except requests.exceptions.RequestException as e:
                logging.exception(f"Request Error: {e}")
                yield rx.toast("Could not connect to server.", duration=3000)
        yield DriverState.close_delete_confirm