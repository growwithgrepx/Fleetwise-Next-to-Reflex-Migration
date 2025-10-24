import reflex as rx


def md_button(*children, **props) -> rx.Component:
    """A Material Design 3 inspired button."""
    base_class = "bg-teal-600 text-white font-medium py-2 px-4 rounded-full hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-opacity-50 transition-colors shadow-sm hover:shadow-md"
    props["class_name"] = f"{base_class} {props.get('class_name', '')}"
    return rx.el.button(*children, **props)


def md_input(placeholder: str, name: str, type: str = "text", **props) -> rx.Component:
    """A Material Design 3 inspired input field."""
    return rx.el.input(
        placeholder=placeholder,
        name=name,
        type=type,
        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-shadow",
        **props,
    )


def md_card(*children, **props) -> rx.Component:
    """A Material Design 3 inspired card."""
    return rx.el.div(
        *children,
        class_name="bg-white rounded-xl shadow-sm p-6 border border-gray-100",
        **props,
    )