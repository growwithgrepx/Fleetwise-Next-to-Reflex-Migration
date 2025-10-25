import reflex as rx
from typing import Optional
import logging

API_HOST = "127.0.0.1"
API_PORT = 8000  # Python backend port (not Reflex backend)
API_BASE_URL = f"http://{API_HOST}:{API_PORT}/api"


class BaseState(rx.State):
    """The base state for the app. All other states should inherit from this state."""

    is_loading: bool = False
    error: str = ""
    success: str = ""

    @rx.event
    def show_error(self, message: str, log: bool = True):
        """Set the error message and clear success. Optionally log the error."""
        self.error = message
        self.success = ""
        if log:
            logging.error(message)

    @rx.event
    def show_success(self, message: str):
        """Set the success message and clear error."""
        self.success = message
        self.error = ""

    @rx.event
    def clear_messages(self):
        """Clear all messages."""
        self.error = ""
        self.success = ""