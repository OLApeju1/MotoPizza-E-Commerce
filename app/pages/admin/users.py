import reflex as rx
from app.states.state import State
from app.states.auth_state import AuthState, Admin
from app.components.shared import page_layout
import os


def add_admin_form() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Add New Admin", class_name="text-2xl font-bold text-gray-900 mb-6"),
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
                rx.el.div(
                    rx.el.label(
                        "Confirm Password",
                        html_for="confirm_password",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        id="confirm_password",
                        name="confirm_password",
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
                "Add Admin",
                type="submit",
                class_name="mt-6 w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500",
            ),
            on_submit=AuthState.add_admin,
            reset_on_submit=True,
            class_name="mt-8",
        ),
        class_name="p-8 bg-white border border-gray-200 rounded-xl shadow-sm",
    )


def admin_table_row(admin: Admin) -> rx.Component:
    return rx.el.tr(
        rx.el.td(admin["username"], class_name="p-4 border-b font-medium"),
        rx.el.td(admin["created_at"], class_name="p-4 border-b"),
        rx.el.td(
            rx.el.div(
                rx.cond(
                    admin["username"] == os.getenv("ADMIN_USERNAME", "admin"),
                    rx.el.span("Cannot Delete", class_name="text-sm text-gray-500"),
                    rx.el.button(
                        rx.icon("trash-2", class_name="h-4 w-4"),
                        on_click=lambda: AuthState.set_admin_to_delete(
                            admin["username"]
                        ),
                        class_name="p-2 text-red-600 hover:bg-red-50 rounded-md",
                    ),
                ),
                class_name="flex justify-end",
            ),
            class_name="p-4 border-b",
        ),
        class_name="hover:bg-gray-50 text-sm",
    )


def admins_table() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Existing Admins", class_name="text-2xl font-bold text-gray-900 mb-6"),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Username", class_name="px-4 py-2 text-left"),
                        rx.el.th("Created At", class_name="px-4 py-2 text-left"),
                        rx.el.th("Actions", class_name="px-4 py-2 text-right"),
                        class_name="border-b bg-gray-50",
                    )
                ),
                rx.el.tbody(rx.foreach(AuthState.admins, admin_table_row)),
                class_name="w-full text-sm",
            ),
            class_name="overflow-x-auto rounded-lg border border-gray-200",
        ),
        class_name="mt-12",
    )


def delete_confirmation_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Confirm Deletion", class_name="text-lg font-semibold text-gray-900"
                ),
                rx.radix.primitives.dialog.description(
                    f"Are you sure you want to delete the admin '{AuthState.admin_to_delete}'? This action cannot be undone.",
                    class_name="text-sm text-gray-600 mt-2",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=AuthState.cancel_delete,
                        class_name="px-4 py-2 bg-gray-200 text-gray-800 font-semibold rounded-lg hover:bg-gray-300",
                    ),
                    rx.el.button(
                        "Delete",
                        on_click=AuthState.confirm_delete_admin,
                        class_name="px-4 py-2 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700",
                    ),
                    class_name="flex justify-end gap-4 mt-6",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-2xl p-6 w-full max-w-md z-50",
            ),
        ),
        open=AuthState.show_delete_dialog,
    )


def admin_users_page_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Admin Management", class_name="text-4xl font-bold"),
            rx.el.p(
                "Add or remove administrator accounts.", class_name="text-gray-600"
            ),
            class_name="mb-8 text-center",
        ),
        rx.el.div(
            rx.cond(
                AuthState.is_main_admin,
                add_admin_form(),
                rx.el.div(
                    rx.el.p(
                        "Only the main admin can manage users.",
                        class_name="text-center text-gray-600",
                    ),
                    class_name="p-8 bg-white border border-gray-200 rounded-xl shadow-sm",
                ),
            ),
            admins_table(),
            delete_confirmation_dialog(),
            class_name="max-w-4xl mx-auto",
        ),
        class_name="container mx-auto p-8",
    )


def admin_users_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.cond(
                AuthState.is_authenticated,
                admin_users_page_content(),
                rx.el.div(
                    rx.el.p("Redirecting to login..."),
                    class_name="min-h-[60vh] flex items-center justify-center",
                ),
            ),
            on_mount=AuthState.check_auth,
        )
    )