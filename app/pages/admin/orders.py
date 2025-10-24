import reflex as rx
from app.states.state import State, Order
from app.states.auth_state import AuthState
from app.components.shared import page_layout


def order_row(order: Order) -> rx.Component:
    return rx.el.tr(
        rx.el.td(order["id"].to_string(), class_name="p-4 border-b font-medium"),
        rx.el.td(order["timestamp"], class_name="p-4 border-b"),
        rx.el.td(order["username"], class_name="p-4 border-b"),
        rx.el.td(order["email"], class_name="p-4 border-b"),
        rx.el.td(order["phone"], class_name="p-4 border-b"),
        rx.el.td(
            rx.el.ul(
                rx.foreach(
                    order["cart_items"],
                    lambda item: rx.el.li(
                        f"{item['product']['name']} (x{item['quantity']})"
                    ),
                ),
                class_name="list-disc list-inside text-sm",
            ),
            class_name="p-4 border-b",
        ),
        rx.el.td(
            rx.el.span(
                order["status"].to_string().capitalize(),
                class_name=rx.cond(
                    order["status"] == "pending",
                    "px-2 py-1 text-xs font-semibold text-yellow-800 bg-yellow-100 rounded-full",
                    "px-2 py-1 text-xs font-semibold text-green-800 bg-green-100 rounded-full",
                ),
            ),
            class_name="p-4 border-b text-center",
        ),
        class_name="hover:bg-gray-50 text-sm",
    )


def orders_table() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Customer Orders", class_name="text-2xl font-bold text-gray-900 mb-6"),
        rx.cond(
            State.orders.length() > 0,
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th("Order ID", class_name="px-4 py-2 text-left"),
                            rx.el.th("Timestamp", class_name="px-4 py-2 text-left"),
                            rx.el.th("Username", class_name="px-4 py-2 text-left"),
                            rx.el.th("Email", class_name="px-4 py-2 text-left"),
                            rx.el.th("Phone", class_name="px-4 py-2 text-left"),
                            rx.el.th("Items", class_name="px-4 py-2 text-left"),
                            rx.el.th("Status", class_name="px-4 py-2 text-center"),
                            class_name="border-b bg-gray-50",
                        )
                    ),
                    rx.el.tbody(rx.foreach(State.orders, order_row)),
                    class_name="w-full text-sm",
                ),
                class_name="overflow-x-auto rounded-lg border border-gray-200",
            ),
            rx.el.div(
                rx.el.p("No orders have been placed yet.", class_name="text-gray-500"),
                class_name="text-center py-10 border-2 border-dashed rounded-lg",
            ),
        ),
    )


def admin_orders_page_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Order Management", class_name="text-4xl font-bold"),
            rx.el.p("View and manage customer orders.", class_name="text-gray-600"),
            class_name="mb-8 text-center",
        ),
        rx.el.div(orders_table(), class_name="max-w-7xl mx-auto"),
        class_name="container mx-auto p-8",
    )


def admin_orders_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.cond(
                AuthState.is_authenticated,
                admin_orders_page_content(),
                rx.el.div(
                    rx.el.p("Redirecting to login..."),
                    class_name="min-h-[60vh] flex items-center justify-center",
                ),
            ),
            on_mount=AuthState.check_auth,
        )
    )