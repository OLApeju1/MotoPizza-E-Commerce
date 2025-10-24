import reflex as rx
import reflex as rx
from app.states.state import State
from app.states.customer_auth_state import CustomerAuthState
from app.components.shared import page_layout


def cart_item_row(item: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=item["product"]["image"],
                    alt=item["product"]["name"],
                    class_name="w-16 h-16 object-cover rounded-md",
                ),
                rx.el.div(
                    rx.el.p(
                        item["product"]["name"],
                        class_name="font-semibold text-gray-800",
                    ),
                    rx.el.button(
                        "Remove",
                        on_click=lambda: State.remove_from_cart(item["product"]["id"]),
                        class_name="text-red-500 text-sm hover:underline",
                    ),
                    class_name="ml-4",
                ),
                class_name="flex items-center",
            ),
            class_name="py-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("minus", class_name="h-4 w-4"),
                    on_click=lambda: State.decrement_quantity(item["product"]["id"]),
                    class_name="px-2 py-1 border rounded-md hover:bg-gray-100",
                ),
                rx.el.span(item["quantity"], class_name="px-4 font-medium"),
                rx.el.button(
                    rx.icon("plus", class_name="h-4 w-4"),
                    on_click=lambda: State.increment_quantity(item["product"]["id"]),
                    class_name="px-2 py-1 border rounded-md hover:bg-gray-100",
                ),
                class_name="flex items-center",
            ),
            class_name="py-4",
        ),
        rx.el.td(
            f"₦{item['product']['price']:.2f}", class_name="py-4 text-right font-medium"
        ),
        rx.el.td(
            f"₦{item['product']['price'] * item['quantity']:.2f}",
            class_name="py-4 text-right font-bold text-teal-600",
        ),
    )


def cart_summary() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Order Summary", class_name="text-2xl font-bold mb-4"),
        rx.el.div(
            rx.el.p("Subtotal"),
            rx.el.p(f"₦{State.cart_total:.2f}", class_name="font-semibold"),
            class_name="flex justify-between py-2 border-b",
        ),
        rx.el.div(
            rx.el.p("Taxes & Fees"),
            rx.el.p("Calculated at checkout", class_name="text-sm text-gray-500"),
            class_name="flex justify-between py-2 border-b",
        ),
        rx.el.div(
            rx.el.p("Total", class_name="font-bold text-lg"),
            rx.el.p(
                f"₦{State.cart_total:.2f}", class_name="font-bold text-lg text-teal-600"
            ),
            class_name="flex justify-between py-2",
        ),
        rx.el.a(
            "Proceed to Checkout",
            href=rx.cond(
                CustomerAuthState.is_customer_authenticated,
                "/checkout",
                "/checkout/login",
            ),
            class_name="mt-6 w-full bg-teal-500 text-white text-center font-bold py-3 rounded-lg hover:bg-teal-600 transition-colors shadow-md",
        ),
        class_name="w-full lg:w-1/3 p-6 bg-gray-50 rounded-lg shadow-sm border",
    )


def cart_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Your Cart", class_name="text-4xl font-bold"),
            rx.el.p(f"{State.cart_count} items", class_name="text-gray-600"),
            class_name="mb-8",
        ),
        rx.cond(
            State.cart_count > 0,
            rx.el.div(
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Product", class_name="text-left font-semibold pb-4"
                                ),
                                rx.el.th(
                                    "Quantity",
                                    class_name="text-left font-semibold pb-4",
                                ),
                                rx.el.th(
                                    "Price", class_name="text-right font-semibold pb-4"
                                ),
                                rx.el.th(
                                    "Total", class_name="text-right font-semibold pb-4"
                                ),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(State.cart, cart_item_row),
                            class_name="divide-y divide-gray-200",
                        ),
                        class_name="w-full",
                    ),
                    class_name="w-full lg:w-2/3 pr-8",
                ),
                cart_summary(),
                class_name="flex flex-col lg:flex-row items-start",
            ),
            rx.el.div(
                rx.el.h2("Your cart is empty.", class_name="text-2xl font-semibold"),
                rx.el.p(
                    "Looks like you haven't added any items yet.",
                    class_name="text-gray-600 mt-2",
                ),
                rx.el.a(
                    "Browse Products",
                    href="/products",
                    class_name="mt-4 inline-block bg-teal-500 text-white font-medium px-6 py-2 rounded-lg hover:bg-teal-600 transition-colors",
                ),
                class_name="text-center py-20 border-2 border-dashed rounded-lg",
            ),
        ),
        class_name="container mx-auto p-8",
    )


def cart_page() -> rx.Component:
    return page_layout(cart_content())