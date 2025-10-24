import reflex as rx
import requests
import os
import logging
from typing import Optional
from app.states.base_state import BaseState

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


class AuthState(BaseState):
    """Handles authentication and session management."""

    token: Optional[str] = rx.Cookie("")
    error_message: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        """Checks if the user is authenticated."""
        return self.token is not None and self.token != ""

    @rx.var
    def auth_headers(self) -> dict[str, str]:
        """Returns the authentication headers for API requests."""
        if not self.is_authenticated:
            return {}
        return {"Authorization": f"Bearer {self.token}"}

    @rx.event
    async def login(self, form_data: dict[str, str]):
        """Logs the user in by calling the backend API."""
        self.error_message = ""
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "").strip()
        if not email or not password:
            self.error_message = "Email and password are required."
            return rx.toast("Please fill in all fields", duration=3000)
        try:
            response = requests.post(
                f"{API_URL}/api/auth/login",
                json={"email": email, "password": password},
                timeout=10,
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token", "")
                return rx.redirect("/")
            elif response.status_code == 401:
                self.error_message = "Invalid email or password. Please try again."
                return rx.toast(self.error_message, duration=3000)
            else:
                self.error_message = (
                    f"Login failed. Server error: {response.status_code}"
                )
                return rx.toast(self.error_message, duration=3000)
        except requests.exceptions.ConnectionError:
            logging.exception("Connection error during login")
            self.error_message = "Cannot connect to server. Please ensure the backend is running on port 8000."
            return rx.toast(self.error_message, duration=5000)
        except requests.exceptions.Timeout:
            logging.exception("Timeout during login")
            self.error_message = "Request timed out. Please try again."
            return rx.toast(self.error_message, duration=3000)
        except requests.exceptions.RequestException as e:
            logging.exception(f"Request error during login: {e}")
            self.error_message = "An error occurred during login. Please try again."
            return rx.toast(self.error_message, duration=3000)

    @rx.event
    def logout(self):
        """Logs the user out."""
        self.token = ""
        return rx.redirect("/login")