import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.image(
                            src="/logo_bakery_slice.png",
                            alt="MotoPizza Logo",
                            class_name="h-12 w-auto",
                        ),
                        class_name="flex items-center justify-center gap-2",
                    ),
                    href="/",
                ),
                rx.el.h2(
                    "Admin Login", class_name="mt-6 text-2xl font-bold text-gray-900"
                ),
                class_name="text-center",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Username",
                            html_for="username",
                            class_name="block text-sm font-medium text-gray-700",
                        ),
                        rx.el.input(
                            id="username",
                            name="username",
                            type="text",
                            class_name="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Password",
                            html_for="password",
                            class_name="block text-sm font-medium text-gray-700",
                        ),
                        rx.el.input(
                            id="password",
                            name="password",
                            type="password",
                            class_name="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500",
                        ),
                    ),
                    rx.cond(
                        AuthState.error_message != "",
                        rx.el.p(
                            AuthState.error_message,
                            class_name="text-sm text-red-600 font-medium",
                        ),
                        None,
                    ),
                    class_name="space-y-4",
                ),
                rx.el.button(
                    "Sign in",
                    type="submit",
                    class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 mt-6",
                ),
                on_submit=AuthState.login,
                reset_on_submit=True,
                class_name="mt-8",
            ),
            class_name="w-full max-w-md p-8 space-y-8 bg-white rounded-xl shadow-lg border border-gray-200",
        ),
        class_name="min-h-screen flex items-center justify-center bg-gray-50 font-['Lato']",
    )