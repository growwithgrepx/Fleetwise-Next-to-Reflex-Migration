# FILE: app/states/base_state.py
import reflex as rx
from typing import Optional

API_BASE_URL = "http://localhost:8000/api"

class BaseState(rx.State):
    """The base state for the app. All other states should inherit from this state."""
    
    is_loading: bool = False
    error: Optional[str] = None
    success: Optional[str] = None
    
    def show_error(self, message: str):
        """Show an error message."""
        self.error = message
        self.success = None
    
    def show_success(self, message: str):
        """Show a success message."""
        self.success = message
        self.error = None
    
    def clear_messages(self):
        """Clear all messages."""
        self.error = None
        self.success = None