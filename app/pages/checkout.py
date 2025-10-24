import reflex as rx
from app.states.state import State
from app.components.shared import page_layout


def checkout_cart_summary() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Order Summary", class_name="text-xl font-bold mb-4"),
        rx.el.div(
            rx.foreach(
                State.cart,
                lambda item: rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            f"{item['product']['name']} x {item['quantity']}",
                            class_name="font-medium",
                        ),
                        rx.el.p(
                            f"₦{item['product']['price'] * item['quantity']:.2f}",
                            class_name="text-gray-600",
                        ),
                        class_name="flex justify-between items-center",
                    ),
                    class_name="py-2 border-b border-gray-200 text-sm",
                ),
            )
        ),
        rx.el.div(
            rx.el.p("Total", class_name="font-bold text-lg"),
            rx.el.p(
                f"₦{State.cart_total:.2f}", class_name="font-bold text-lg text-teal-600"
            ),
            class_name="flex justify-between items-center mt-4 pt-4 border-t-2 border-gray-300",
        ),
        class_name="w-full lg:w-2/5 p-6 bg-gray-50 rounded-lg shadow-sm border h-fit",
    )


def checkout_form() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Checkout", class_name="text-3xl font-bold mb-2"),
        rx.el.p(
            "Please provide your email to complete the order via WhatsApp.",
            class_name="text-gray-600 mb-6",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Email Address",
                    html_for="email",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    id="email",
                    name="email",
                    type="email",
                    placeholder="you@example.com",
                    class_name="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500",
                    required=True,
                ),
            ),
            rx.el.button(
                "Complete Order on WhatsApp",
                type="submit",
                class_name="mt-6 w-full bg-teal-500 text-white text-center font-bold py-3 rounded-lg hover:bg-teal-600 transition-colors shadow-md",
            ),
            on_submit=State.process_checkout,
            class_name="w-full",
        ),
        class_name="w-full lg:w-3/5 pr-0 lg:pr-12",
    )


def checkout_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.cond(
                State.cart_count > 0,
                rx.el.div(
                    checkout_form(),
                    checkout_cart_summary(),
                    class_name="container mx-auto p-8 flex flex-col-reverse lg:flex-row items-start gap-8",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Your cart is empty.", class_name="text-2xl font-semibold"
                    ),
                    rx.el.p(
                        "You can't checkout without any items.",
                        class_name="text-gray-600 mt-2",
                    ),
                    rx.el.a(
                        "Browse Products",
                        href="/products",
                        class_name="mt-4 inline-block bg-teal-500 text-white font-medium px-6 py-2 rounded-lg hover:bg-teal-600 transition-colors",
                    ),
                    class_name="text-center py-20 border-2 border-dashed rounded-lg container mx-auto my-8",
                ),
            )
        )
    )