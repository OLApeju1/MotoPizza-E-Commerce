import reflex as rx
from app.states.admin_state import AdminState
from app.states.auth_state import AuthState
from app.states.customer_auth_state import Customer
from app.components.shared import page_layout


def admin_customers_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.cond(
                AuthState.is_authenticated,
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Customer Management", class_name="text-4xl font-bold"
                        ),
                        rx.el.p(
                            "View and manage your registered customers.",
                            class_name="text-gray-600",
                        ),
                        class_name="mb-8 text-center",
                    ),
                    rx.el.div(
                        customer_dashboard(),
                        customers_table(),
                        class_name="max-w-5xl mx-auto",
                    ),
                    class_name="container mx-auto p-8",
                ),
                rx.el.div(
                    rx.el.p("Redirecting to login..."),
                    class_name="min-h-[60vh] flex items-center justify-center",
                ),
            ),
            on_mount=[AdminState.check_auth, AdminState.load_customers],
        )
    )


def customer_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Total Customers", class_name="text-sm font-medium text-gray-500"),
            rx.el.p(
                AdminState.total_customers,
                class_name="text-2xl font-bold text-gray-900",
            ),
            class_name="p-4 bg-white border rounded-lg shadow-sm",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Search by name or email...",
                on_change=AdminState.set_customer_search_query,
                class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500",
            ),
            rx.el.button(
                rx.icon("download", class_name="h-4 w-4 mr-2"),
                "Export CSV",
                on_click=AdminState.export_customers_csv,
                class_name="flex items-center px-4 py-2 bg-teal-500 text-white font-semibold rounded-lg hover:bg-teal-600 shadow-md",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="mb-6 flex justify-between items-center",
    )


def customers_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Name", class_name="px-4 py-3 text-left font-semibold"
                        ),
                        rx.el.th(
                            "Email", class_name="px-4 py-3 text-left font-semibold"
                        ),
                        rx.el.th(
                            "Phone", class_name="px-4 py-3 text-left font-semibold"
                        ),
                        rx.el.th(
                            "Signup Date",
                            class_name="px-4 py-3 text-left font-semibold",
                        ),
                        class_name="border-b bg-gray-50",
                    )
                ),
                rx.el.tbody(
                    rx.cond(
                        AdminState.filtered_customers.length() > 0,
                        rx.foreach(AdminState.filtered_customers, customer_table_row),
                        rx.el.tr(
                            rx.el.td(
                                "No customers found.",
                                col_span=4,
                                class_name="text-center p-8 text-gray-500",
                            )
                        ),
                    )
                ),
                class_name="w-full text-sm",
            ),
            class_name="overflow-x-auto rounded-lg border border-gray-200",
        )
    )


def customer_table_row(customer: Customer) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={customer['name']}",
                    class_name="h-8 w-8 rounded-full mr-3",
                ),
                rx.el.p(customer["name"], class_name="font-medium"),
                class_name="flex items-center",
            ),
            class_name="p-4 border-b",
        ),
        rx.el.td(customer["email"], class_name="p-4 border-b text-gray-600"),
        rx.el.td(customer["phone"], class_name="p-4 border-b text-gray-600"),
        rx.el.td(customer["signup_date"], class_name="p-4 border-b text-gray-600"),
        class_name="hover:bg-gray-50",
    )