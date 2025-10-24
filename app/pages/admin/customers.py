import reflex as rx
from app.states.state import State, CustomerEmail
from app.states.auth_state import AuthState
from app.components.shared import page_layout


def customer_email_row(email: CustomerEmail) -> rx.Component:
    return rx.el.tr(
        rx.el.td(email["email"], class_name="p-4 border-b font-medium"),
        rx.el.td(email["timestamp"], class_name="p-4 border-b"),
        rx.el.td(
            rx.el.ul(
                rx.foreach(
                    email["cart_items"],
                    lambda item: rx.el.li(
                        f"{item['product']['name']} (x{item['quantity']})"
                    ),
                ),
                class_name="list-disc list-inside text-sm",
            ),
            class_name="p-4 border-b",
        ),
        class_name="hover:bg-gray-50",
    )


def customers_table() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Customer Emails", class_name="text-2xl font-bold text-gray-900 mb-6"),
        rx.cond(
            State.customer_emails.length() > 0,
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th("Email", class_name="px-4 py-2 text-left"),
                            rx.el.th("Timestamp", class_name="px-4 py-2 text-left"),
                            rx.el.th("Cart Items", class_name="px-4 py-2 text-left"),
                            class_name="border-b bg-gray-50",
                        )
                    ),
                    rx.el.tbody(rx.foreach(State.customer_emails, customer_email_row)),
                    class_name="w-full text-sm",
                ),
                class_name="overflow-x-auto rounded-lg border border-gray-200",
            ),
            rx.el.div(
                rx.el.p(
                    "No customer emails have been collected yet.",
                    class_name="text-gray-500",
                ),
                class_name="text-center py-10 border-2 border-dashed rounded-lg",
            ),
        ),
    )


def admin_customers_page_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Customer Relationship Management", class_name="text-4xl font-bold"
            ),
            rx.el.p(
                "View emails collected from customers during checkout.",
                class_name="text-gray-600",
            ),
            class_name="mb-8 text-center",
        ),
        rx.el.div(customers_table(), class_name="max-w-5xl mx-auto"),
        class_name="container mx-auto p-8",
    )


def admin_customers_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.cond(
                AuthState.is_authenticated,
                admin_customers_page_content(),
                rx.el.div(
                    rx.el.p("Redirecting to login..."),
                    class_name="min-h-[60vh] flex items-center justify-center",
                ),
            ),
            on_mount=AuthState.check_auth,
        )
    )