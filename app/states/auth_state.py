import reflex as rx
import requests
from typing import Optional
import logging
from .base_state import BaseState, API_BASE_URL


class AuthState(BaseState):
    """Handles authentication and session management."""

    token: str = rx.Cookie("")
    email: str = ""
    password: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        return bool(self.token)

    @rx.var
    def auth_headers(self) -> dict:
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}

    @rx.event
    def login(self, form_data: dict | None = None):
        """Handle login form submission. Accepts optional form_data from a page form."""
        if form_data:
            email = form_data.get("email", "").strip()
            password = form_data.get("password", "").strip()
        else:
            email = (self.email or "").strip()
            password = (self.password or "").strip()
        if not email or not password:
            self.show_error("Email and password are required")
            return
        try:
            response = requests.post(
                f"{API_BASE_URL}/auth/login",
                json={"email": email, "password": password},
                timeout=5,
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token")
                self.password = ""
                self.email = email
                self.show_success("Login successful!")
                return rx.redirect("/drivers")
            elif response.status_code == 401:
                self.show_error("Invalid credentials")
            else:
                self.show_error(f"Login failed. Server error: {response.status_code}")
        except requests.exceptions.ConnectionError as e:
            logging.exception(f"Error: {e}")
            self.show_error(
                "Cannot connect to server. Please ensure the backend is running on port 8000."
            )
        except requests.exceptions.Timeout as e:
            logging.exception(f"Error: {e}")
            self.show_error("Request timed out. Please try again.")
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.show_error(f"Login failed: {str(e)}")

    @rx.event
    def logout(self):
        """Handle logout."""
        self.token = ""
        self.email = ""
        self.password = ""
        return rx.redirect("/login")