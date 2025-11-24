import reflex as rx
from app.states.state import State
from app.components.shared import page_layout


def about_hero() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Our Story: A Passion for Baking",
                class_name="text-4xl font-bold tracking-tight text-gray-900 animate-fade-in-up",
            ),
            rx.el.p(
                "From a small home kitchen to a beloved community bakery, our journey is fueled by love, family, and flour.",
                class_name="mt-2 text-lg text-gray-600 animate-fade-in-up delay-200",
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
                    class_name="max-w-xl animate-slide-in-left",
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
                    class_name="max-w-xl animate-slide-in-right",
                ),
                class_name="grid md:grid-cols-2 gap-12",
            ),
            class_name="container mx-auto p-8 md:p-16",
        ),
    )


def get_carousel_item_class(index: rx.Var[int]) -> rx.Component:
    total = State.carousel_total_images
    current = State.current_image_index
    is_center = index == current
    is_left_1 = index == (current - 1 + total) % total
    is_right_1 = index == (current + 1) % total
    is_left_2 = index == (current - 2 + total) % total
    is_right_2 = index == (current + 2) % total
    return rx.cond(
        is_center,
        "carousel-item-center",
        rx.cond(
            is_left_1,
            "carousel-item-left-1",
            rx.cond(
                is_right_1,
                "carousel-item-right-1",
                rx.cond(
                    is_left_2,
                    "carousel-item-left-2",
                    rx.cond(
                        is_right_2, "carousel-item-right-2", "carousel-item-hidden"
                    ),
                ),
            ),
        ),
    )


def carousel_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    State.uploaded_images,
                    lambda filename, index: rx.el.div(
                        rx.image(
                            src=rx.get_upload_url(filename),
                            alt="Gallery image",
                            class_name="w-full h-full object-cover",
                        ),
                        class_name=rx.Var.create("carousel-item cursor-pointer ")
                        + get_carousel_item_class(index),
                        on_click=lambda: State.set_image_index(index),
                    ),
                ),
                class_name="carousel-container",
            ),
            rx.el.button(
                rx.icon("chevron-left", class_name="w-8 h-8 text-gray-800"),
                on_click=State.prev_image,
                disabled=State.carousel_total_images <= 1,
                class_name="absolute left-0 top-1/2 -translate-y-1/2 z-50 p-2 bg-white/80 rounded-full shadow-lg hover:bg-white hover:scale-110 transition-all disabled:opacity-0 disabled:pointer-events-none",
            ),
            rx.el.button(
                rx.icon("chevron-right", class_name="w-8 h-8 text-gray-800"),
                on_click=State.next_image,
                disabled=State.carousel_total_images <= 1,
                class_name="absolute right-0 top-1/2 -translate-y-1/2 z-50 p-2 bg-white/80 rounded-full shadow-lg hover:bg-white hover:scale-110 transition-all disabled:opacity-0 disabled:pointer-events-none",
            ),
            class_name="relative w-full max-w-5xl mx-auto h-[300px] md:h-[500px]",
        ),
        class_name="carousel-perspective w-full overflow-hidden py-8 animate-fade-in-up",
    )


def gallery_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "A Glimpse Into Our World",
                class_name="text-3xl font-bold text-center text-gray-900 animate-fade-in-up",
            ),
            rx.el.p(
                "The art, the process, and the delicious results. Uploaded from our admin panel.",
                class_name="mt-2 text-center text-gray-600 animate-fade-in-up delay-200",
            ),
            rx.cond(
                (State.uploaded_images.length() == 0)
                & (State.uploaded_videos.length() == 0),
                rx.el.div(
                    rx.el.p(
                        "No images or videos uploaded yet. Visit the admin upload page to add some!",
                        class_name="text-center text-gray-500",
                    ),
                    class_name="mt-12 text-center py-10 border-2 border-dashed rounded-lg animate-fade-in",
                ),
            ),
            rx.cond(
                State.uploaded_images.length() > 0,
                rx.el.div(
                    rx.el.h3(
                        "Image Gallery",
                        class_name="text-2xl font-bold text-gray-800 mb-6 border-b pb-2",
                    ),
                    carousel_view(),
                    class_name="mt-12",
                ),
            ),
            rx.cond(
                State.uploaded_videos.length() > 0,
                rx.el.div(
                    rx.el.h3(
                        "Video Gallery",
                        class_name="text-2xl font-bold text-gray-800 mb-6 border-b pb-2",
                    ),
                    rx.el.div(
                        rx.foreach(
                            State.uploaded_videos,
                            lambda filename, index: rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "video", class_name="h-12 w-12 text-gray-500"
                                    ),
                                    class_name="w-full h-48 flex items-center justify-center bg-gray-100",
                                ),
                                class_name="w-full overflow-hidden rounded-lg shadow-md border border-gray-200 group bg-white animate-scale-in opacity-0",
                                style={
                                    "animation-delay": (index * 100).to_string() + "ms"
                                },
                            ),
                        ),
                        class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6 items-start",
                    ),
                    class_name="mt-16",
                ),
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
                class_name="text-3xl font-bold text-center text-gray-900 animate-fade-in-up",
            ),
            rx.el.p(
                "Don't just take our word for it. Here's what people are saying.",
                class_name="mt-2 text-center text-gray-600 animate-fade-in-up delay-200",
            ),
            rx.el.div(
                rx.foreach(
                    State.testimonials,
                    lambda testimonial, index: rx.el.div(
                        testimonial_card(testimonial),
                        class_name="animate-fade-in-up opacity-0",
                        style={"animation-delay": (index * 200).to_string() + "ms"},
                    ),
                ),
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
                class_name="text-3xl font-bold text-center text-gray-900 animate-fade-in-up",
            ),
            rx.el.p(
                "Everything you need to know before placing an order.",
                class_name="mt-2 text-center text-gray-600 animate-fade-in-up delay-200",
            ),
            rx.el.div(
                rx.foreach(
                    State.faqs,
                    lambda faq, index: rx.el.div(
                        faq_item(faq),
                        class_name="animate-fade-in opacity-0",
                        style={"animation-delay": (index * 150).to_string() + "ms"},
                    ),
                ),
                class_name="mt-8 max-w-3xl mx-auto divide-y divide-gray-200",
            ),
            class_name="container mx-auto px-4 py-16",
        ),
        class_name="bg-gray-50",
    )


def social_media_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Follow Our Journey",
                class_name="text-3xl font-bold text-center text-gray-900 animate-fade-in-up",
            ),
            rx.el.p(
                "Stay connected with us on social media for the latest updates, behind-the-scenes content, and delicious inspiration.",
                class_name="mt-2 text-center text-gray-600 max-w-2xl mx-auto animate-fade-in-up delay-200",
            ),
            rx.el.div(
                rx.el.a(
                    rx.icon("instagram", class_name="h-8 w-8"),
                    rx.el.span("@motobites", class_name="font-semibold text-lg"),
                    href="#",
                    class_name="flex flex-col items-center gap-2 p-6 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-lg hover:border-teal-300 transition-all animate-scale-in delay-100",
                ),
                rx.el.a(
                    rx.icon("facebook", class_name="h-8 w-8"),
                    rx.el.span("Motobites", class_name="font-semibold text-lg"),
                    href="#",
                    class_name="flex flex-col items-center gap-2 p-6 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-lg hover:border-teal-300 transition-all animate-scale-in delay-200",
                ),
                rx.el.a(
                    rx.icon("twitch", class_name="h-8 w-8"),
                    rx.el.span("@motobites", class_name="font-semibold text-lg"),
                    href="#",
                    class_name="flex flex-col items-center gap-2 p-6 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-lg hover:border-teal-300 transition-all animate-scale-in delay-300",
                ),
                class_name="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto",
            ),
            class_name="container mx-auto px-4 py-16",
        )
    )


def about_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            about_hero(),
            gallery_section(),
            testimonials_section(),
            social_media_section(),
            faq_section(),
        )
    )