import reflex as rx
from app.states.customer_auth_state import CustomerAuthState
from app.components.shared import page_layout


def form_field(
    label: str, name: str, placeholder: str, type: str = "text"
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label, htmlFor=name, class_name="block text-sm font-medium text-gray-700"
        ),
        rx.el.input(
            id=name,
            name=name,
            type=type,
            placeholder=placeholder,
            class_name="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500",
        ),
    )


def signup_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            form_field("Full Name", "name", "John Doe"),
            form_field("Email Address", "email", "you@example.com", "email"),
            form_field("Phone Number", "phone", "+1234567890", "tel"),
            class_name="space-y-4",
        ),
        rx.el.button(
            "Sign Up & Continue",
            type="submit",
            class_name="w-full mt-6 py-2 px-4 bg-teal-600 text-white font-semibold rounded-lg hover:bg-teal-700",
        ),
        on_submit=CustomerAuthState.signup,
    )


def login_form() -> rx.Component:
    return rx.el.form(
        form_field("Email Address", "email", "you@example.com", "email"),
        rx.el.button(
            "Login & Continue",
            type="submit",
            class_name="w-full mt-6 py-2 px-4 bg-teal-600 text-white font-semibold rounded-lg hover:bg-teal-700",
        ),
        on_submit=CustomerAuthState.login,
    )


def checkout_login_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("arrow-left", class_name="mr-2 h-4 w-4"),
                    "Back to Cart",
                    href="/cart",
                    class_name="inline-flex items-center text-sm text-gray-600 hover:text-teal-600 mb-8",
                ),
                rx.el.h1(
                    "Checkout", class_name="text-3xl font-bold text-gray-900 mb-2"
                ),
                rx.el.p(
                    "Please login or sign up to continue.",
                    class_name="text-gray-600 mb-8",
                ),
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("Login", value="login"),
                        rx.tabs.trigger("Sign Up", value="signup"),
                    ),
                    rx.el.div(
                        rx.tabs.content(login_form(), value="login"),
                        rx.tabs.content(signup_form(), value="signup"),
                        class_name="mt-6",
                    ),
                    default_value="login",
                    class_name="w-full",
                ),
                rx.cond(
                    CustomerAuthState.error_message != "",
                    rx.el.div(
                        CustomerAuthState.error_message,
                        class_name="mt-4 p-3 bg-red-100 text-red-700 border border-red-200 rounded-md text-sm",
                    ),
                    None,
                ),
                class_name="max-w-md w-full mx-auto",
            ),
            class_name="container mx-auto p-8 flex justify-center",
        )
    )