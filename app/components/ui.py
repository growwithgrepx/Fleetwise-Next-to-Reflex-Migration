import reflex as rx


def md_button(*children, **props) -> rx.Component:
    """A Material Design 3 inspired button."""
    class_name = " ".join(
        [
            "bg-teal-600 text-white font-medium px-4 py-2 rounded-full",
            "hover:bg-teal-700 focus:ring-2 focus:ring-teal-500",
            "transition-all shadow-sm hover:shadow-md",
            props.pop("class_name", ""),
        ]
    )
    return rx.el.button(*children, class_name=class_name, **props)


def md_input(**props) -> rx.Component:
    """A Material Design 3 inspired input field."""
    class_name = " ".join(
        [
            "w-full px-4 py-2 border border-gray-300 rounded-lg",
            "focus:ring-2 focus:ring-teal-500 focus:border-transparent",
            "transition-shadow",
            props.pop("class_name", ""),
        ]
    )
    return rx.el.input(class_name=class_name, **props)


def md_card(*children, **props) -> rx.Component:
    """A Material Design 3 inspired card."""
    class_name = " ".join(
        [
            "bg-white rounded-xl shadow-sm p-6 border border-gray-100",
            props.pop("class_name", ""),
        ]
    )
    return rx.el.div(*children, class_name=class_name, **props)