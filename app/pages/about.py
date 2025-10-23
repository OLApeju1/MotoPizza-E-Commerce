import reflex as rx
from app.states.state import State
from app.components.shared import page_layout


def about_hero() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Our Story: A Passion for Baking",
                class_name="text-4xl font-bold tracking-tight text-gray-900",
            ),
            rx.el.p(
                "From a small home kitchen to a beloved community bakery, our journey is fueled by love, family, and flour.",
                class_name="mt-2 text-lg text-gray-600",
            ),
            class_name="text-center py-12 bg-teal-50/50 border-b border-gray-200",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Our Mission", class_name="text-2xl font-bold text-gray-900"
                    ),
                    rx.el.p(
                        "To craft the most delicious and memorable baked goods that bring joy to our community, using only the finest ingredients and a touch of artisanal magic.",
                        class_name="mt-2 text-gray-600 leading-relaxed",
                    ),
                    class_name="max-w-xl",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Our Values", class_name="text-2xl font-bold text-gray-900"
                    ),
                    rx.el.ul(
                        rx.el.li(
                            "Quality: We never compromise on the quality of our ingredients."
                        ),
                        rx.el.li(
                            "Community: We are proud to be a part of and serve our local community."
                        ),
                        rx.el.li(
                            "Passion: Every cake and pastry is made with love and dedication."
                        ),
                        class_name="mt-2 text-gray-600 list-disc list-inside space-y-1",
                    ),
                    class_name="max-w-xl",
                ),
                class_name="grid md:grid-cols-2 gap-12",
            ),
            class_name="container mx-auto p-8 md:p-16",
        ),
    )


def gallery_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "A Glimpse Into Our World",
                class_name="text-3xl font-bold text-center text-gray-900",
            ),
            rx.el.p(
                "The art, the process, and the delicious results.",
                class_name="mt-2 text-center text-gray-600",
            ),
            rx.el.div(
                rx.foreach(
                    State.gallery_images,
                    lambda img: rx.el.div(
                        rx.image(
                            src=img,
                            alt="Gallery image",
                            class_name="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300",
                        ),
                        class_name="aspect-video w-full overflow-hidden rounded-lg shadow-md border border-gray-200 group",
                    ),
                ),
                class_name="mt-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            class_name="container mx-auto px-4 py-16",
        ),
        class_name="bg-gray-50",
    )


def testimonial_card(testimonial: dict[str, str]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={testimonial['avatar']}",
                    class_name="size-12 rounded-full",
                ),
                rx.el.p(testimonial["name"], class_name="font-semibold text-gray-800"),
                class_name="flex items-center gap-4",
            ),
            rx.el.p(
                f'''"{testimonial["review"]}"''', class_name="mt-4 text-gray-600 italic"
            ),
            class_name="p-6 border border-gray-200 rounded-lg bg-white",
        )
    )


def testimonials_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "From Our Customers",
                class_name="text-3xl font-bold text-center text-gray-900",
            ),
            rx.el.p(
                "Don't just take our word for it. Here's what people are saying.",
                class_name="mt-2 text-center text-gray-600",
            ),
            rx.el.div(
                rx.foreach(State.testimonials, testimonial_card),
                class_name="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8",
            ),
            class_name="container mx-auto px-4 py-16",
        )
    )


def faq_item(faq: dict[str, str]) -> rx.Component:
    return rx.el.div(
        rx.el.details(
            rx.el.summary(
                faq["question"],
                class_name="font-semibold text-lg cursor-pointer text-gray-800 hover:text-teal-600",
            ),
            rx.el.p(faq["answer"], class_name="mt-2 text-gray-600 leading-relaxed"),
            class_name="py-4",
        )
    )


def faq_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Frequently Asked Questions",
                class_name="text-3xl font-bold text-center text-gray-900",
            ),
            rx.el.p(
                "Everything you need to know before placing an order.",
                class_name="mt-2 text-center text-gray-600",
            ),
            rx.el.div(
                rx.foreach(State.faqs, faq_item),
                class_name="mt-8 max-w-3xl mx-auto divide-y divide-gray-200",
            ),
            class_name="container mx-auto px-4 py-16",
        ),
        class_name="bg-gray-50",
    )


def about_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            about_hero(), gallery_section(), testimonials_section(), faq_section()
        )
    )