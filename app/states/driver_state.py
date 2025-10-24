import reflex as rx
import requests
from typing import List, Dict, Optional
from .auth_state import AuthState, API_BASE_URL


class DriverState(AuthState):
    """State for managing drivers using simple dicts for serializability."""

    drivers: List[Dict] = []
    current_driver: Dict = {}
    show_modal: bool = False
    is_edit_mode: bool = False
    deleting_driver_id: Optional[int] = None

    @rx.event
    def fetch_drivers(self):
        """Fetch all drivers from the API."""
        if not self.is_authenticated:
            return
        try:
            resp = requests.get(f"{API_BASE_URL}/drivers", headers=self.auth_headers, timeout=5)
            if resp.status_code == 200:
                self.drivers = resp.json()
            else:
                self.show_error(f"Failed to fetch drivers: {resp.status_code}")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Error fetching drivers: {e}")

    @rx.event
    def open_add_modal(self):
        self.current_driver = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "phone": "",
            "license_number": "",
            "license_expiry": "",
            "status": "active",
        }
        self.is_edit_mode = False
        self.show_modal = True

    @rx.event
    def open_edit_modal(self, driver_id: int):
        driver = next((d for d in self.drivers if d.get("id") == driver_id), None)
        if not driver:
            self.show_error("Driver not found")
            return
        self.current_driver = dict(driver)
        self.is_edit_mode = True
        self.show_modal = True

    @rx.event
    def save_driver(self):
        """Create or update a driver via API."""
        if not self.current_driver:
            self.show_error("No driver data to save")
            return
        try:
            if self.is_edit_mode and self.current_driver.get("id"):
                resp = requests.put(
                    f"{API_BASE_URL}/drivers/{self.current_driver['id']}",
                    json=self.current_driver,
                    headers=self.auth_headers,
                    timeout=5,
                )
            else:
                resp = requests.post(
                    f"{API_BASE_URL}/drivers",
                    json=self.current_driver,
                    headers=self.auth_headers,
                    timeout=5,
                )

            if resp.status_code in (200, 201):
                self.show_success("Driver saved")
                self.fetch_drivers()
                self.close_modal()
            else:
                self.show_error(f"Failed to save driver: {resp.status_code}")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Error saving driver: {e}")

    @rx.event
    def confirm_delete(self, driver_id: int):
        self.deleting_driver_id = driver_id
        # show confirm handled in component state

    @rx.event
    def delete_driver(self):
        if not self.deleting_driver_id:
            self.show_error("No driver selected to delete")
            return
        try:
            resp = requests.delete(
                f"{API_BASE_URL}/drivers/{self.deleting_driver_id}",
                headers=self.auth_headers,
                timeout=5,
            )
            if resp.status_code == 200:
                self.show_success("Driver deleted")
                self.fetch_drivers()
            else:
                self.show_error(f"Failed to delete driver: {resp.status_code}")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Error deleting driver: {e}")
        finally:
            self.deleting_driver_id = None

    @rx.event
    def close_modal(self):
        self.show_modal = False
        self.current_driver = {}
        self.is_edit_mode = False

    @rx.event
    def handle_driver_submit(self, form_data: Dict[str, str]):
        """Handle form submission coming from the page form (form_data dict)."""
        # Merge form data into current_driver (without changing id)
        if not isinstance(form_data, dict):
            self.show_error("Invalid form submission")
            return

        # If editing, keep the id from current_driver
        if self.is_edit_mode and self.current_driver.get("id"):
            form_payload = dict(form_data)
            form_payload["id"] = self.current_driver.get("id")
        else:
            form_payload = dict(form_data)

        try:
            if self.is_edit_mode and form_payload.get("id"):
                resp = requests.put(
                    f"{API_BASE_URL}/drivers/{form_payload['id']}",
                    json=form_payload,
                    headers=self.auth_headers,
                    timeout=5,
                )
            else:
                resp = requests.post(
                    f"{API_BASE_URL}/drivers",
                    json=form_payload,
                    headers=self.auth_headers,
                    timeout=5,
                )

            if resp.status_code in (200, 201):
                self.show_success("Driver saved")
                self.fetch_drivers()
                self.close_modal()
            else:
                self.show_error(f"Failed to save driver: {resp.status_code}")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Error submitting form: {e}")

    @rx.event
    def open_delete_confirm(self, driver_id: int):
        self.deleting_driver_id = driver_id

    @rx.event
    def close_delete_confirm(self):
        self.deleting_driver_id = None

    @rx.event
    def delete_driver(self):
        if not self.deleting_driver_id:
            self.show_error("No driver selected to delete")
            return
        try:
            resp = requests.delete(
                f"{API_BASE_URL}/drivers/{self.deleting_driver_id}",
                headers=self.auth_headers,
                timeout=5,
            )
            if resp.status_code == 200:
                self.show_success("Driver deleted")
                self.fetch_drivers()
            else:
                self.show_error(f"Failed to delete driver: {resp.status_code}")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Error deleting driver: {e}")
        finally:
            self.deleting_driver_id = None