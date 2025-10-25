import reflex as rx
from app.styles import COMPONENTS, TEXT


def md_button(*children, **props) -> rx.Component:
    """Primary button with theme."""
    variant = props.pop("variant", "primary")
    is_loading = props.pop("is_loading", False)
    style_map = {
        "primary": COMPONENTS["button_primary"],
        "secondary": COMPONENTS["button_secondary"],
        "danger": COMPONENTS["button_danger"],
    }
    class_name = " ".join([style_map.get(variant, COMPONENTS["button_primary"]), props.pop("class_name", "")])
    
    # Handle loading state - check if it's a Reflex Var or regular bool
    if is_loading is not False:
        # If is_loading is provided (either Var or True), show loading state
        return rx.cond(
            is_loading,
            rx.el.button(
                rx.spinner(size="1", class_name="mr-2"),
                *children,
                class_name=class_name,
                disabled=True,
                **props
            ),
            rx.el.button(*children, class_name=class_name, **props)
        )
    return rx.el.button(*children, class_name=class_name, **props)


def md_input(**props) -> rx.Component:
    """Input field with theme."""
    class_name = " ".join([COMPONENTS["input"], props.pop("class_name", "")])
    return rx.el.input(class_name=class_name, **props)


def md_card(*children, **props) -> rx.Component:
    """Card component with theme."""
    class_name = " ".join([COMPONENTS["card"], props.pop("class_name", "")])
    return rx.el.div(*children, class_name=class_name, **props)


def heading_1(*children, **props) -> rx.Component:
    """Large heading."""
    class_name = " ".join([TEXT["heading_1"], props.pop("class_name", "")])
    return rx.el.h1(*children, class_name=class_name, **props)


def heading_2(*children, **props) -> rx.Component:
    """Medium heading."""
    class_name = " ".join([TEXT["heading_2"], props.pop("class_name", "")])
    return rx.el.h2(*children, class_name=class_name, **props)


def heading_3(*children, **props) -> rx.Component:
    """Small heading."""
    class_name = " ".join([TEXT["heading_3"], props.pop("class_name", "")])
    return rx.el.h3(*children, class_name=class_name, **props)


def body_text(*children, **props) -> rx.Component:
    """Body text."""
    class_name = " ".join([TEXT["body"], props.pop("class_name", "")])
    return rx.el.p(*children, class_name=class_name, **props)


def label_text(*children, **props) -> rx.Component:
    """Label text."""
    class_name = " ".join([TEXT["label"], props.pop("class_name", "")])
    return rx.el.label(*children, class_name=class_name, **props)


def badge_success(*children, **props) -> rx.Component:
    """Success badge."""
    class_name = " ".join([COMPONENTS["badge_success"], props.pop("class_name", "")])
    return rx.el.span(*children, class_name=class_name, **props)


def badge_error(*children, **props) -> rx.Component:
    """Error badge."""
    class_name = " ".join([COMPONENTS["badge_error"], props.pop("class_name", "")])
    return rx.el.span(*children, class_name=class_name, **props)


def alert_error(*children, **props) -> rx.Component:
    """Error alert."""
    class_name = " ".join([COMPONENTS["alert_error"], props.pop("class_name", "")])
    return rx.el.div(*children, class_name=class_name, **props)


def alert_success(*children, **props) -> rx.Component:
    """Success alert."""
    class_name = " ".join([COMPONENTS["alert_success"], props.pop("class_name", "")])
    return rx.el.div(*children, class_name=class_name, **props)