# FILE: app/states/driver_state.py
import reflex as rx
import requests
from typing import List, Optional
from .auth_state import AuthState, API_BASE_URL
from reflex import Base

class Driver(Base):
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    license_number: str = ""
    license_expiry: str = ""
    status: str = "active"

class DriverState(AuthState):
    """State for managing drivers."""

    drivers: List[Driver] = []
    current_driver: Driver = Driver()
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
                self.drivers = [Driver(**d) for d in resp.json()]
            else:
                self.show_error(f"Failed to fetch drivers: {resp.status_code}")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Error fetching drivers: {e}")

    @rx.event
    def open_add_modal(self):
        self.current_driver = Driver()
        self.is_edit_mode = False
        self.show_modal = True

    @rx.event
    def open_edit_modal(self, driver_id: int):
        driver = next((d for d in self.drivers if d.id == driver_id), None)
        if not driver:
            self.show_error("Driver not found")
            return
        self.current_driver = driver
        self.is_edit_mode = True
        self.show_modal = True

    @rx.event
    def save_driver(self):
        """Create or update a driver via API."""
        if not self.current_driver:
            self.show_error("No driver data to save")
            return
        json_data = self.current_driver.model_dump(exclude=["id"] if notself.is_edit_mode else None)
        try:
            if self.is_edit_mode and self.current_driver.id:
                resp = requests.put(
                    f"{API_BASE_URL}/drivers/{self.current_driver.id}",
                    json=json_data,
                    headers=self.auth_headers,
                    timeout=5,
                )
            else:
                resp = requests.post(
                    f"{API_BASE_URL}/drivers",
                    json=json_data,
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
        self.current_driver = Driver()
        self.is_edit_mode = False

    @rx.event
    def handle_driver_submit(self, form_data: dict[str, str]):
        """Handle form submission coming from the page form (form_data dict)."""
        if not isinstance(form_data, dict):
            self.show_error("Invalid form submission")
            return

        id_value = self.current_driver.id if self.is_edit_mode else None
        self.current_driver = Driver(**form_data, id=id_value)
        return self.save_driver()

    @rx.event
    def open_delete_confirm(self, driver_id: int):
        self.deleting_driver_id = driver_id

    @rx.event
    def close_delete_confirm(self):
        self.deleting_driver_id = None