import reflex as rx


def md_button(*children, **props) -> rx.Component:
    """A Material Design 3 inspired button."""
    base_props = {
        "bg": "teal.600",
        "color": "white",
        "font_weight": "medium",
        "padding_x": "4",
        "padding_y": "2",
        "border_radius": "full",
        "_hover": {"bg": "teal.700"},
        "_focus": {"ring": 2, "ring_color": "teal.500"},
        "transition": "all",
        "shadow": "sm",
        "_hover_shadow": "md",
    }
    return rx.button(*children, **{**base_props, **props})


def md_input(placeholder: str, type_: str = "text", **props) -> rx.Component:
    """A Material Design 3 inspired input field."""
    base_props = {
        "width": "100%",
        "padding_x": "4",
        "padding_y": "2",
        "border": "1px solid",
        "border_color": "gray.300",
        "border_radius": "lg",
        "_focus": {"ring": 2, "ring_color": "teal.500", "border_color": "transparent"},
        "transition": "shadow",
        "placeholder": placeholder,
        "type": type_,
    }
    return rx.input(**{**base_props, **props})


def md_card(*children, **props) -> rx.Component:
    """A Material Design 3 inspired card."""
    base_props = {
        "bg": "white",
        "border_radius": "xl",
        "shadow": "sm",
        "padding": "6",
        "border": "1px solid",
        "border_color": "gray.100",
    }
    return rx.box(*children, **{**base_props, **props})