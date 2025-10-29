import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.image(
                            src="/triangle_geometric_motobites.png",
                            alt="Motobites Logo",
                            class_name="h-10 w-auto",
                        ),
                        rx.el.span("Motobites", class_name="font-bold text-xl"),
                        class_name="flex items-center gap-2",
                    ),
                    href="/",
                ),
                rx.el.h2(
                    "Login to Your Account",
                    class_name="mt-6 text-2xl font-bold text-gray-900",
                ),
                rx.el.p(
                    "Enter your details to access your account or the admin dashboard.",
                    class_name="text-sm text-gray-600 mt-2",
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
                        rx.el.div(
                            rx.el.input(
                                id="password",
                                name="password",
                                type=rx.cond(
                                    AuthState.show_password, "text", "password"
                                ),
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500",
                            ),
                            rx.el.button(
                                rx.icon(
                                    rx.cond(AuthState.show_password, "eye-off", "eye"),
                                    class_name="h-5 w-5",
                                ),
                                on_click=AuthState.toggle_password_visibility,
                                type="button",
                                class_name="absolute inset-y-0 right-0 flex items-center px-3 text-gray-500 hover:text-teal-600",
                            ),
                            class_name="relative mt-1",
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
            rx.el.p(
                "Don't have an account? ",
                rx.el.a(
                    "Sign up",
                    href="/signup",
                    class_name="font-medium text-teal-600 hover:text-teal-500",
                ),
                class_name="mt-4 text-center text-sm text-gray-600",
            ),
            class_name="w-full max-w-md p-8 space-y-8 bg-white rounded-xl shadow-lg border border-gray-200",
        ),
        class_name="min-h-screen flex items-center justify-center bg-gray-50 font-['Lato']",
    )