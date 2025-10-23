import reflex as rx
from app.states.state import State, Product
from app.states.admin_state import AdminState
from app.states.auth_state import AuthState
from app.components.shared import page_layout


def product_form_field(
    label: str, placeholder: str, value: rx.Var, on_change, type: str = "text"
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            placeholder=placeholder,
            on_change=on_change,
            type=type,
            class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500",
            default_value=value,
        ),
        class_name="w-full",
    )


def product_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.h2(
                rx.cond(AdminState.is_editing, "Edit Product", "Add New Product"),
                class_name="text-2xl font-bold text-gray-900 mb-6",
            ),
            rx.el.div(
                product_form_field(
                    "Name",
                    "e.g. Classic Chocolate Fudge",
                    AdminState.product_form["name"],
                    lambda v: AdminState.set_product_form_field("name", v),
                ),
                product_form_field(
                    "Price",
                    "e.g. 21000.0",
                    AdminState.product_form["price"].to_string(),
                    AdminState.set_price,
                    type="number",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Category",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.input(
                    placeholder="e.g. Cakes",
                    name="category",
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500",
                    default_value=AdminState.product_form["category"],
                    key=f"category-{AdminState.is_editing}",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Short Description",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.textarea(
                    placeholder="Short description for product card...",
                    name="description",
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500 h-24",
                    default_value=AdminState.product_form["description"],
                    key=f"description-{AdminState.is_editing}",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Full Description",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.textarea(
                    placeholder="Full description for product detail page...",
                    name="full_description",
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500 h-32",
                    default_value=AdminState.product_form["full_description"],
                    key=f"full_description-{AdminState.is_editing}",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Ingredients",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="Add an ingredient",
                        name="new_ingredient",
                        class_name="flex-grow px-3 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-teal-500 focus:border-teal-500",
                        default_value=AdminState.new_ingredient,
                        key=f"new_ingredient-{AdminState.is_editing}",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="h-5 w-5"),
                        on_click=AdminState.add_ingredient,
                        type="button",
                        class_name="px-4 py-2 bg-gray-200 text-gray-700 rounded-r-md hover:bg-gray-300",
                    ),
                    class_name="flex mb-2",
                ),
                rx.el.div(
                    rx.foreach(
                        AdminState.product_form["ingredients"],
                        lambda ing: rx.el.div(
                            ing,
                            rx.el.button(
                                rx.icon("x", class_name="h-3 w-3"),
                                on_click=lambda: AdminState.remove_ingredient(ing),
                                type="button",
                                class_name="ml-2 text-red-500 hover:text-red-700",
                            ),
                            class_name="flex items-center bg-gray-100 text-gray-800 text-sm font-medium px-3 py-1 rounded-full",
                        ),
                    ),
                    class_name="flex flex-wrap gap-2",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Product Image",
                    class_name="block text-sm font-medium text-gray-700 mb-2",
                ),
                rx.upload.root(
                    rx.el.div(
                        rx.icon("image-up", class_name="h-8 w-8 text-gray-400"),
                        rx.el.p(
                            "Drag & drop or click to upload",
                            class_name="text-sm text-gray-500",
                        ),
                        class_name="flex flex-col items-center justify-center p-6 border-2 border-dashed border-gray-300 rounded-lg text-center cursor-pointer hover:bg-gray-50",
                    ),
                    id="product_image_upload",
                    multiple=False,
                    accept={
                        "image/png": [".png"],
                        "image/jpeg": [".jpg", ".jpeg"],
                        "image/webp": [".webp"],
                    },
                    on_drop=AdminState.handle_product_image_upload,
                    class_name="mb-2",
                ),
                rx.cond(
                    rx.selected_files("product_image_upload").length() > 0,
                    rx.el.p(
                        rx.selected_files("product_image_upload")[0],
                        class_name="text-sm text-green-600",
                    ),
                    None,
                ),
                rx.cond(
                    AdminState.product_form["image"] != "",
                    rx.image(
                        src=rx.get_upload_url(AdminState.product_form["image"]),
                        class_name="h-24 w-auto rounded-md mt-2 border",
                    ),
                    None,
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(AdminState.is_editing, "Update Product", "Add Product"),
                    type="submit",
                    is_loading=AdminState.is_saving,
                    class_name="px-6 py-2 bg-teal-500 text-white font-semibold rounded-lg hover:bg-teal-600 shadow-md disabled:opacity-50",
                ),
                rx.el.button(
                    "Cancel",
                    on_click=AdminState.clear_form,
                    type="button",
                    class_name="px-6 py-2 bg-gray-500 text-white font-semibold rounded-lg hover:bg-gray-600",
                ),
                class_name="flex items-center gap-4",
            ),
        ),
        on_submit=AdminState.save_product,
        class_name="p-8 bg-white border border-gray-200 rounded-xl shadow-sm",
    )


def products_table() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Existing Products", class_name="text-2xl font-bold text-gray-900 mb-6"
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Image", class_name="px-4 py-2 text-left"),
                        rx.el.th("Name", class_name="px-4 py-2 text-left"),
                        rx.el.th("Price", class_name="px-4 py-2 text-left"),
                        rx.el.th("Actions", class_name="px-4 py-2 text-right"),
                        class_name="border-b bg-gray-50",
                    )
                ),
                rx.el.tbody(rx.foreach(State.products, product_table_row)),
                class_name="w-full text-sm",
            ),
            class_name="overflow-x-auto rounded-lg border border-gray-200",
        ),
        class_name="mt-12",
    )


def product_table_row(product: Product) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.image(
                src=product["image"], class_name="h-12 w-12 object-cover rounded-md"
            ),
            class_name="p-4 border-b",
        ),
        rx.el.td(product["name"], class_name="p-4 border-b font-medium"),
        rx.el.td(f"₦{product['price']:.2f}", class_name="p-4 border-b"),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("copy", class_name="h-4 w-4"),
                    on_click=lambda: AdminState.set_editing_product(product),
                    class_name="p-2 text-blue-600 hover:bg-blue-50 rounded-md",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: State.delete_product(product["id"]),
                    class_name="p-2 text-red-600 hover:bg-red-50 rounded-md",
                ),
                class_name="flex justify-end gap-2",
            ),
            class_name="p-4 border-b",
        ),
        class_name="hover:bg-gray-50",
    )


def admin_products_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.cond(
                AuthState.is_authenticated,
                rx.el.div(
                    rx.el.div(
                        rx.el.h1("Product Management", class_name="text-4xl font-bold"),
                        rx.el.p(
                            "Add, edit, and remove products from your store.",
                            class_name="text-gray-600",
                        ),
                        class_name="mb-8 text-center",
                    ),
                    rx.el.div(
                        product_form(), products_table(), class_name="max-w-5xl mx-auto"
                    ),
                    class_name="container mx-auto p-8",
                ),
                rx.el.div(
                    rx.el.p("Redirecting to login..."),
                    class_name="min-h-[60vh] flex items-center justify-center",
                ),
            ),
            on_mount=AuthState.check_auth,
        )
    )