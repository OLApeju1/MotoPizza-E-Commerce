import reflex as rx
from app.states.state import State
from app.components.shared import page_layout


def product_detail_content() -> rx.Component:
    return rx.el.div(
        rx.cond(
            State.current_product,
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src=State.current_product["image"],
                        alt=State.current_product["name"],
                        class_name="w-full h-auto object-cover rounded-xl shadow-lg border border-gray-200",
                    ),
                    class_name="w-full lg:w-1/2",
                ),
                rx.el.div(
                    rx.el.h1(
                        State.current_product["name"],
                        class_name="text-4xl font-extrabold text-gray-900 tracking-tight",
                    ),
                    rx.el.span(
                        State.current_product["category"],
                        class_name="inline-block bg-teal-100 text-teal-800 text-xs font-medium mt-2 px-2.5 py-0.5 rounded-full",
                    ),
                    rx.el.p(
                        State.current_product["full_description"],
                        class_name="mt-4 text-gray-600 text-base leading-relaxed",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Ingredients",
                            class_name="font-semibold text-gray-800 mt-6 mb-2",
                        ),
                        rx.el.div(
                            rx.foreach(
                                State.current_product["ingredients"],
                                lambda ingredient: rx.el.span(
                                    ingredient,
                                    class_name="bg-gray-100 text-gray-700 text-sm font-medium px-3 py-1 rounded-md",
                                ),
                            ),
                            class_name="flex flex-wrap gap-2",
                        ),
                    ),
                    rx.el.div(
                        rx.el.span(
                            f"₦{State.current_product['price']:.2f}",
                            class_name="text-4xl font-bold text-teal-600",
                        ),
                        rx.el.button(
                            rx.icon("shopping-cart", class_name="mr-2 h-5 w-5"),
                            "Add to Cart",
                            on_click=lambda: State.add_to_cart(State.current_product),
                            class_name="flex items-center justify-center w-full md:w-auto px-8 py-4 bg-teal-500 text-white font-bold rounded-lg hover:bg-teal-600 transition-transform hover:scale-105 shadow-md",
                        ),
                        class_name="flex flex-col md:flex-row items-start md:items-center justify-between mt-8 gap-4",
                    ),
                    class_name="w-full lg:w-1/2 p-0 lg:pl-12 mt-8 lg:mt-0",
                ),
                class_name="container mx-auto flex flex-col lg:flex-row items-start p-8",
            ),
            rx.el.div(
                rx.el.h2("Product not found", class_name="text-2xl font-bold"),
                rx.el.a(
                    "Back to products", href="/products", class_name="text-teal-500"
                ),
                class_name="text-center py-20",
            ),
        ),
        class_name="min-h-[60vh] flex items-center justify-center",
    )


def product_detail_page() -> rx.Component:
    return page_layout(product_detail_content())