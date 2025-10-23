import reflex as rx
from app.states.state import State
from app.components.shared import product_card, page_layout


def products_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Our Menu",
                    class_name="text-4xl font-bold tracking-tight text-gray-900",
                ),
                rx.el.p(
                    "Browse our collection of handcrafted cakes and pastries.",
                    class_name="mt-2 text-lg text-gray-600",
                ),
                class_name="text-center py-12 bg-gray-50 border-b border-gray-200",
            ),
            rx.el.div(
                rx.foreach(State.products, product_card),
                class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 p-8",
            ),
            class_name="container mx-auto",
        )
    )