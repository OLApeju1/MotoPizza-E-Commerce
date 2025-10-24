import reflex as rx
from app.pages.home import home_page
from app.pages.products import products_page
from app.pages.product_detail import product_detail_page
from app.pages.about import about_page
from app.pages.cart import cart_page
from app.pages.admin.upload import upload_page
from app.pages.admin.products import admin_products_page
from app.pages.login import login_page
from app.pages.checkout_login import checkout_login_page
from app.pages.checkout import checkout_page
from app.pages.admin.customers import admin_customers_page

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(home_page, route="/")
app.add_page(products_page, route="/products")
app.add_page(about_page, route="/about")
app.add_page(cart_page, route="/cart")
app.add_page(upload_page, route="/admin/upload")
app.add_page(admin_products_page, route="/admin/products")
app.add_page(login_page, route="/login")
app.add_page(checkout_login_page, route="/checkout/login")
app.add_page(checkout_page, route="/checkout")
app.add_page(admin_customers_page, route="/admin/customers")
app.add_page(product_detail_page, route="/products/[product_id]")