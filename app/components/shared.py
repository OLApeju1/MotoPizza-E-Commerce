import reflex as rx
from app.states.state import State, Product
from app.states.auth_state import AuthState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.image(
                        src="/logo_bakery_slice.png",
                        alt="Motobites Logo",
                        class_name="h-8 w-auto",
                    ),
                    rx.el.span("Motobites", class_name="font-bold text-lg"),
                    class_name="flex items-center gap-2",
                ),
                href="/",
            ),
            rx.el.div(
                rx.el.a(
                    "Home",
                    href="/",
                    class_name="px-3 py-2 text-sm font-medium text-gray-600 hover:text-teal-500 transition-colors",
                ),
                rx.el.a(
                    "Products",
                    href="/products",
                    class_name="px-3 py-2 text-sm font-medium text-gray-600 hover:text-teal-500 transition-colors",
                ),
                rx.el.a(
                    "About",
                    href="/about",
                    class_name="px-3 py-2 text-sm font-medium text-gray-600 hover:text-teal-500 transition-colors",
                ),
                class_name="hidden md:flex items-center gap-2",
            ),
            rx.el.div(
                rx.cond(
                    AuthState.is_admin,
                    rx.el.div(
                        rx.el.a(
                            "Uploads",
                            href="/admin/upload",
                            class_name=rx.cond(
                                State.router.page.path == "/admin/upload",
                                "px-3 py-2 text-sm font-bold text-teal-500",
                                "px-3 py-2 text-sm font-medium text-gray-600 hover:text-teal-500 transition-colors",
                            ),
                        ),
                        rx.el.a(
                            "Products",
                            href="/admin/products",
                            class_name=rx.cond(
                                State.router.page.path == "/admin/products",
                                "px-3 py-2 text-sm font-bold text-teal-500",
                                "px-3 py-2 text-sm font-medium text-gray-600 hover:text-teal-500 transition-colors",
                            ),
                        ),
                        rx.el.a(
                            "Customers",
                            href="/admin/customers",
                            class_name=rx.cond(
                                State.router.page.path == "/admin/customers",
                                "px-3 py-2 text-sm font-bold text-teal-500",
                                "px-3 py-2 text-sm font-medium text-gray-600 hover:text-teal-500 transition-colors",
                            ),
                        ),
                        rx.el.a(
                            "Orders",
                            href="/admin/orders",
                            class_name=rx.cond(
                                State.router.page.path == "/admin/orders",
                                "px-3 py-2 text-sm font-bold text-teal-500",
                                "px-3 py-2 text-sm font-medium text-gray-600 hover:text-teal-500 transition-colors",
                            ),
                        ),
                        rx.el.a(
                            "Users",
                            href="/admin/users",
                            class_name=rx.cond(
                                State.router.page.path == "/admin/users",
                                "px-3 py-2 text-sm font-bold text-teal-500",
                                "px-3 py-2 text-sm font-medium text-gray-600 hover:text-teal-500 transition-colors",
                            ),
                        ),
                        class_name="flex items-center gap-2 border-l ml-4 pl-4",
                    ),
                    None,
                ),
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.button(
                        "Logout",
                        on_click=AuthState.logout,
                        class_name="px-3 py-2 text-sm font-medium text-red-600 hover:text-red-800 transition-colors",
                    ),
                    rx.el.a(
                        "Login",
                        href="/login",
                        class_name="px-3 py-2 text-sm font-medium text-gray-600 hover:text-teal-500 transition-colors",
                    ),
                ),
                rx.el.a(
                    rx.icon("shopping-cart", class_name="h-5 w-5"),
                    rx.cond(
                        State.cart_count > 0,
                        rx.el.span(
                            State.cart_count,
                            class_name="absolute -top-2 -right-2 flex items-center justify-center w-5 h-5 text-xs font-bold text-white bg-red-500 rounded-full",
                        ),
                        None,
                    ),
                    href="/cart",
                    class_name="relative px-3 py-2 text-sm font-medium text-gray-600 hover:text-teal-500 transition-colors",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="container mx-auto flex items-center justify-between p-4",
        ),
        class_name="w-full bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-40",
    )


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src="/logo_bakery_slice.png",
                        alt="Motobites Logo",
                        class_name="h-8 w-auto",
                    ),
                    rx.el.span("Motobites", class_name="font-bold text-lg"),
                    class_name="flex items-center gap-2 mb-4",
                ),
                rx.el.p(
                    "Crafting delicious memories, one bite at a time.",
                    class_name="text-gray-600 text-sm max-w-xs",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3("Navigate", class_name="font-semibold text-gray-800 mb-3"),
                    rx.el.a(
                        "Home",
                        href="/",
                        class_name="text-gray-600 hover:text-teal-500 block mb-2 text-sm",
                    ),
                    rx.el.a(
                        "Products",
                        href="/products",
                        class_name="text-gray-600 hover:text-teal-500 block mb-2 text-sm",
                    ),
                    rx.el.a(
                        "About",
                        href="/about",
                        class_name="text-gray-600 hover:text-teal-500 block mb-2 text-sm",
                    ),
                ),
                rx.el.div(
                    rx.el.h3("Contact", class_name="font-semibold text-gray-800 mb-3"),
                    rx.el.p(
                        "123 Bakery Lane, Foodie City",
                        class_name="text-gray-600 text-sm mb-1",
                    ),
                    rx.el.p(
                        "contact@motobites.com", class_name="text-gray-600 text-sm"
                    ),
                ),
                class_name="grid grid-cols-2 gap-8",
            ),
            class_name="container mx-auto grid md:grid-cols-2 gap-8 p-8 md:p-12",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "© 2024 Motobites. All rights reserved.",
                    class_name="text-sm text-gray-500",
                ),
                rx.el.div(
                    rx.icon(
                        "twitter",
                        class_name="h-5 w-5 text-gray-500 hover:text-teal-500 cursor-pointer",
                    ),
                    rx.icon(
                        "instagram",
                        class_name="h-5 w-5 text-gray-500 hover:text-teal-500 cursor-pointer",
                    ),
                    rx.icon(
                        "facebook",
                        class_name="h-5 w-5 text-gray-500 hover:text-teal-500 cursor-pointer",
                    ),
                    class_name="flex items-center gap-4",
                ),
                class_name="container mx-auto flex justify-between items-center p-4",
            ),
            class_name="border-t border-gray-200",
        ),
        class_name="bg-gray-50",
    )


def product_card(product: Product) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=rx.cond(
                        product["image"].contains("https://"),
                        product["image"],
                        rx.get_upload_url(product["image"]),
                    ),
                    alt=product["name"],
                    class_name="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300",
                ),
                class_name="aspect-square w-full overflow-hidden rounded-lg",
            ),
            rx.el.div(
                rx.el.h3(
                    product["name"],
                    class_name="font-semibold text-lg text-gray-800 mt-3",
                ),
                rx.el.p(
                    product["description"], class_name="text-sm text-gray-600 mt-1 h-10"
                ),
                rx.el.div(
                    rx.el.span(
                        f"₦{product['price']:.2f}",
                        class_name="text-lg font-bold text-teal-600",
                    ),
                    rx.el.div(
                        "View",
                        rx.icon("arrow-right", class_name="ml-1 h-4 w-4"),
                        class_name="flex items-center text-sm font-medium text-teal-500 group-hover:text-teal-600",
                    ),
                    class_name="flex items-center justify-between mt-4",
                ),
                class_name="p-1",
            ),
            class_name="group",
        ),
        href="/products/" + product["id"].to_string(),
    )


def page_layout(content: rx.Component) -> rx.Component:
    return rx.el.main(
        header(), content, footer(), class_name="font-['Lato'] bg-white text-gray-800"
    )