import reflex as rx
from app.states.state import State
from app.states.customer_auth_state import CustomerAuthState
from app.components.shared import page_layout


def checkout_page() -> rx.Component:
    return page_layout(checkout_content())


def checkout_content() -> rx.Component:
    return rx.el.div(
        rx.cond(
            CustomerAuthState.is_customer_authenticated,
            rx.el.div(
                rx.el.a(
                    rx.icon("arrow-left", class_name="mr-2 h-4 w-4"),
                    "Back to Cart",
                    href="/cart",
                    class_name="inline-flex items-center text-sm text-gray-600 hover:text-teal-600 mb-8",
                ),
                rx.el.h1(
                    "Checkout Summary",
                    class_name="text-4xl font-bold text-gray-900 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        order_details_card(),
                        customer_details_card(),
                        class_name="flex-1 space-y-8",
                    ),
                    order_summary_card(),
                    class_name="grid lg:grid-cols-3 gap-8 items-start",
                ),
                class_name="container mx-auto p-8",
            ),
            rx.el.div(
                rx.el.p("Redirecting to login..."),
                class_name="min-h-[60vh] flex items-center justify-center",
            ),
        ),
        on_mount=CustomerAuthState.check_customer_auth,
    )


def order_details_card() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Order Items",
            class_name="text-2xl font-bold text-gray-800 mb-4 border-b pb-3",
        ),
        rx.el.div(
            rx.foreach(State.cart, cart_item_checkout_row), class_name="space-y-4"
        ),
        class_name="lg:col-span-2 bg-white p-6 rounded-lg border border-gray-200 shadow-sm",
    )


def cart_item_checkout_row(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=item["product"]["image"],
                alt=item["product"]["name"],
                class_name="w-16 h-16 object-cover rounded-md",
            ),
            rx.el.div(
                rx.el.p(item["product"]["name"], class_name="font-semibold"),
                rx.el.p(f"Qty: {item['quantity']}", class_name="text-sm text-gray-600"),
                class_name="ml-4",
            ),
        ),
        rx.el.div(
            rx.el.p(
                f"…{item['product']['price'] * item['quantity']:.2f}",
                class_name="font-semibold",
            ),
            class_name="text-right",
        ),
        class_name="flex justify-between items-center",
    )


def customer_details_card() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Your Information",
            class_name="text-2xl font-bold text-gray-800 mb-4 border-b pb-3",
        ),
        rx.cond(
            CustomerAuthState.current_customer,
            rx.el.div(
                rx.el.div(
                    rx.el.p("Name", class_name="font-medium text-gray-500"),
                    rx.el.p(
                        CustomerAuthState.current_customer["name"],
                        class_name="font-semibold text-gray-800",
                    ),
                ),
                rx.el.div(
                    rx.el.p("Email", class_name="font-medium text-gray-500"),
                    rx.el.p(
                        CustomerAuthState.current_customer["email"],
                        class_name="font-semibold text-gray-800",
                    ),
                ),
                rx.el.div(
                    rx.el.p("Phone", class_name="font-medium text-gray-500"),
                    rx.el.p(
                        CustomerAuthState.current_customer["phone"],
                        class_name="font-semibold text-gray-800",
                    ),
                ),
                class_name="space-y-3",
            ),
        ),
        class_name="lg:col-span-2 bg-white p-6 rounded-lg border border-gray-200 shadow-sm",
    )


def order_summary_card() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Order Summary", class_name="text-2xl font-bold mb-4"),
        rx.el.div(
            rx.el.p("Subtotal"),
            rx.el.p(f"…{State.cart_total:.2f}", class_name="font-semibold"),
            class_name="flex justify-between py-2 border-b",
        ),
        rx.el.div(
            rx.el.p("Total", class_name="font-bold text-lg"),
            rx.el.p(
                f"…{State.cart_total:.2f}", class_name="font-bold text-lg text-teal-600"
            ),
            class_name="flex justify-between pt-2",
        ),
        rx.el.a(
            rx.icon("message-circle", class_name="mr-2"),
            "Send Order via WhatsApp",
            href=State.whatsapp_url,
            target="_blank",
            class_name="mt-6 w-full bg-green-500 text-white flex items-center justify-center font-bold py-3 rounded-lg hover:bg-green-600 transition-colors shadow-md",
        ),
        rx.el.p(
            "You will be redirected to WhatsApp to confirm your order.",
            class_name="text-xs text-gray-500 mt-2 text-center",
        ),
        class_name="w-full p-6 bg-gray-50 rounded-lg shadow-sm border sticky top-28",
    )