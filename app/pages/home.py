import reflex as rx
from app.states.state import State
from app.components.shared import product_card, page_layout


def home_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.section(
                rx.el.div(
                    rx.el.h1(
                        "Handcrafted Cakes & Pastries,",
                        rx.el.br(),
                        "Made with Love.",
                        class_name="text-4xl md:text-6xl font-extrabold text-gray-900 tracking-tighter animate-fade-in-up",
                    ),
                    rx.el.p(
                        "Discover artisanal baked goods, perfect for any occasion. From celebratory cakes to daily treats, every bite is a delight.",
                        class_name="mt-4 max-w-xl text-lg text-gray-600 animate-fade-in-up delay-200",
                    ),
                    rx.el.div(
                        rx.el.a(
                            "Explore Our Menu",
                            href="/products",
                            class_name="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-lg text-white bg-teal-500 hover:bg-teal-600 transition-colors shadow-md",
                        ),
                        class_name="mt-8 animate-scale-in delay-400",
                    ),
                    class_name="container mx-auto px-4 py-16 md:py-24 text-center",
                ),
                class_name="bg-teal-50/50",
            ),
            rx.el.section(
                rx.el.div(
                    rx.el.h2(
                        "Featured Products",
                        class_name="text-3xl font-bold text-gray-900 tracking-tight animate-fade-in-up",
                    ),
                    rx.el.p(
                        "Our customers' favorites, fresh from the oven.",
                        class_name="mt-2 text-gray-600 animate-fade-in-up delay-200",
                    ),
                    rx.el.div(
                        rx.foreach(
                            State.featured_products,
                            lambda product, index: rx.el.div(
                                product_card(product),
                                class_name="animate-fade-in-up opacity-0",
                                style={
                                    "animation-delay": (index * 200).to_string() + "ms"
                                },
                            ),
                        ),
                        class_name="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-12",
                    ),
                    class_name="container mx-auto px-4 py-16 md:py-24",
                )
            ),
        )
    )