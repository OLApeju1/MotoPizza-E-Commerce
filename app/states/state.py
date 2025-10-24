import reflex as rx
from typing import TypedDict
import asyncio
from app.states.auth_state import AuthState


class Product(TypedDict):
    id: int
    name: str
    description: str
    price: float
    image: str
    category: str
    full_description: str
    ingredients: list[str]


class CartItem(TypedDict):
    product: Product
    quantity: int


class CustomerEmail(TypedDict):
    email: str
    timestamp: str
    cart_items: list[CartItem]


class State(rx.State):
    """The main state for the MotoPizza app."""

    uploaded_files: list[str] = []
    is_uploading: bool = False
    upload_progress: int = 0
    cart: list[CartItem] = []
    customer_emails: list[CustomerEmail] = []
    products: list[Product] = [
        {
            "id": 1,
            "name": "Classic Chocolate Fudge",
            "description": "Rich, dark chocolate cake with a creamy fudge frosting.",
            "price": 21000.0,
            "image": "https://placehold.co/600x600/5D4037/FFFFFF/png?text=Chocolate+Fudge",
            "category": "Cakes",
            "full_description": "A timeless classic, our Chocolate Fudge cake features multiple layers of moist dark chocolate sponge, filled and frosted with a rich, decadent fudge icing. Perfect for birthdays, celebrations, or any day that needs a touch of sweetness.",
            "ingredients": [
                "Flour",
                "Sugar",
                "Cocoa Powder",
                "Eggs",
                "Milk",
                "Butter",
                "Dark Chocolate",
            ],
        },
        {
            "id": 2,
            "name": "Red Velvet Dream",
            "description": "Velvety red sponge with a smooth cream cheese frosting.",
            "price": 22500.0,
            "image": "https://placehold.co/600x600/A62C2A/FFFFFF/png?text=Red+Velvet",
            "category": "Cakes",
            "full_description": "Experience pure bliss with our Red Velvet Dream cake. Its striking red color and subtle hint of cocoa are perfectly complemented by a luscious, tangy cream cheese frosting. It's a sophisticated choice for any occasion.",
            "ingredients": [
                "Flour",
                "Sugar",
                "Buttermilk",
                "Eggs",
                "Cream Cheese",
                "Vanilla Extract",
            ],
        },
        {
            "id": 3,
            "name": "Lemon Zest Delight",
            "description": "A light and airy lemon sponge with a tangy citrus glaze.",
            "price": 19500.0,
            "image": "https://placehold.co/600x600/FBC02D/333333/png?text=Lemon+Zest",
            "category": "Cakes",
            "full_description": "Brighten your day with our Lemon Zest Delight. This cake is made with freshly squeezed lemon juice and zest for a vibrant, natural flavor. It's light, refreshing, and topped with a sweet and tangy lemon glaze.",
            "ingredients": [
                "Flour",
                "Sugar",
                "Eggs",
                "Lemon Juice",
                "Lemon Zest",
                "Butter",
            ],
        },
        {
            "id": 4,
            "name": "Almond Croissant",
            "description": "Buttery, flaky croissant filled with sweet almond paste.",
            "price": 2500.0,
            "image": "https://placehold.co/600x600/D2B48C/FFFFFF/png?text=Almond+Croissant",
            "category": "Pastries",
            "full_description": "Our Almond Croissant is a true masterpiece. A perfectly baked, buttery croissant is filled with a generous amount of rich almond frangipane and topped with toasted almond slices and a dusting of powdered sugar.",
            "ingredients": ["Flour", "Butter", "Almonds", "Sugar", "Eggs"],
        },
        {
            "id": 5,
            "name": "Strawberry Cheesecake",
            "description": "Creamy cheesecake with a graham cracker crust and fresh strawberries.",
            "price": 25000.0,
            "image": "https://placehold.co/600x600/E91E63/FFFFFF/png?text=Strawberry+Cheesecake",
            "category": "Cakes",
            "full_description": "Indulge in our classic New York-style cheesecake. It features a rich and creamy filling on a crisp graham cracker crust, topped with a fresh strawberry compote. It's the ultimate dessert for cheesecake lovers.",
            "ingredients": [
                "Cream Cheese",
                "Graham Crackers",
                "Sugar",
                "Eggs",
                "Fresh Strawberries",
            ],
        },
        {
            "id": 6,
            "name": "Cinnamon Roll",
            "description": "Soft, fluffy roll with a sweet cinnamon swirl and cream cheese icing.",
            "price": 2200.0,
            "image": "https://placehold.co/600x600/8D6E63/FFFFFF/png?text=Cinnamon+Roll",
            "category": "Pastries",
            "full_description": "Warm, gooey, and comforting. Our Cinnamon Rolls are made from a soft, enriched dough, swirled with a generous amount of cinnamon-sugar filling, and lavishly topped with a tangy cream cheese icing. Best served warm!",
            "ingredients": ["Flour", "Cinnamon", "Sugar", "Butter", "Cream Cheese"],
        },
    ]

    @rx.var
    def featured_products(self) -> list[Product]:
        """Returns the first 3 products as featured."""
        return self.products[:3]

    @rx.var
    def get_product_id(self) -> str:
        """Get the product ID from the router."""
        return self.router.page.params.get("product_id", "1")

    @rx.var
    def current_product(self) -> Product | None:
        """Returns the product that matches the current product ID."""
        return next(
            (p for p in self.products if str(p["id"]) == self.get_product_id), None
        )

    @rx.var
    def whatsapp_message(self) -> str:
        """Generates the WhatsApp message for the current product."""
        if self.current_product:
            product_name = self.current_product["name"]
            return f"Hello MotoPizza! I'm interested in booking the {product_name}. Can we discuss the details?"
        return "Hello MotoPizza! I'm interested in one of your products."

    @rx.var
    def whatsapp_url(self) -> str:
        """Generates the full WhatsApp URL."""
        phone_number = "1234567890"
        return f"https://wa.me/{phone_number}?text={self.whatsapp_message.replace(' ', '%20')}"

    @rx.var
    def cart_count(self) -> int:
        return sum((item["quantity"] for item in self.cart))

    @rx.var
    def cart_total(self) -> float:
        return sum((item["product"]["price"] * item["quantity"] for item in self.cart))

    @rx.var
    def whatsapp_checkout_url(self) -> str:
        """Generates the WhatsApp URL for checking out the current cart."""
        if not self.cart:
            return ""
        message_lines = [
            "Hello MotoPizza! I'd like to place an order for the following items:",
            "",
        ]
        for item in self.cart:
            product_name = item["product"]["name"]
            quantity = item["quantity"]
            price = item["product"]["price"]
            line_total = price * quantity
            message_lines.append(f"- {product_name} (x{quantity}) - ₦{line_total:.2f}")
        message_lines.append("")
        message_lines.append(f"Total: ₦{self.cart_total:.2f}")
        message_lines.append("")
        message_lines.append("Please let me know the next steps. Thank you!")
        message = """
""".join(message_lines)
        phone_number = "1234567890"
        import urllib.parse

        encoded_message = urllib.parse.quote(message)
        return f"https://wa.me/{phone_number}?text={encoded_message}"

    @rx.event
    def add_to_cart(self, product: Product):
        for item in self.cart:
            if item["product"]["id"] == product["id"]:
                item["quantity"] += 1
                return
        self.cart.append({"product": product, "quantity": 1})

    @rx.event
    def remove_from_cart(self, product_id: int):
        self.cart = [item for item in self.cart if item["product"]["id"] != product_id]

    @rx.event
    def increment_quantity(self, product_id: int):
        for item in self.cart:
            if item["product"]["id"] == product_id:
                item["quantity"] += 1
                return

    @rx.event
    def decrement_quantity(self, product_id: int):
        for item in self.cart:
            if item["product"]["id"] == product_id:
                if item["quantity"] > 1:
                    item["quantity"] -= 1
                else:
                    self.cart = [
                        i for i in self.cart if i["product"]["id"] != product_id
                    ]
                return

    @rx.event
    def process_checkout(self, form_data: dict[str, str]):
        import datetime

        email = form_data.get("email")
        if not email:
            return rx.toast.error("Email is required to proceed.")
        customer_info = {
            "email": email,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cart_items": self.cart,
        }
        self.customer_emails.append(customer_info)
        self.cart = []
        return rx.redirect(self.whatsapp_checkout_url, is_external=True)

    @rx.event
    async def delete_product(self, product_id: int):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            yield (rx.toast.error("Unauthorized"), rx.redirect("/login"))
            return
        self.products = [p for p in self.products if p["id"] != product_id]
        self.cart = [c for c in self.cart if c["product"]["id"] != product_id]
        yield rx.toast.info(f"Product with ID {product_id} has been deleted.")

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of files."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            yield (rx.toast.error("Unauthorized"), rx.redirect("/login"))
            return
        if not files:
            yield rx.toast.error("No files selected for upload.")
            return
        self.is_uploading = True
        self.upload_progress = 0
        yield
        for i, file in enumerate(files):
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.name
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)
            self.uploaded_files.append(file.name)
            self.upload_progress = int((i + 1) / len(files) * 100)
            yield
        self.is_uploading = False
        yield rx.toast.success(f"Successfully uploaded {len(files)} files!")
        return

    @rx.event
    async def clear_uploads(self):
        """Clear all uploaded files."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return (rx.toast.error("Unauthorized"), rx.redirect("/login"))
        self.uploaded_files.clear()

    @rx.event
    async def delete_uploaded_file(self, filename: str):
        """Delete a specific uploaded file."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return (rx.toast.error("Unauthorized"), rx.redirect("/login"))
        self.uploaded_files = [f for f in self.uploaded_files if f != filename]

    gallery_images: list[str] = [
        "https://placehold.co/600x400/A62C2A/FFFFFF/png?text=Red+Velvet+Slice",
        "https://placehold.co/600x400/5D4037/FFFFFF/png?text=Chocolate+Cake",
        "https://placehold.co/600x400/FBC02D/333333/png?text=Lemon+Tart",
        "https://placehold.co/600x400/D2B48C/FFFFFF/png?text=Bakery+Interior",
        "https://placehold.co/600x400/E91E63/FFFFFF/png?text=Cheesecake+View",
        "https://placehold.co/600x400/8D6E63/FFFFFF/png?text=Fresh+Pastries",
    ]
    testimonials: list[dict[str, str]] = [
        {
            "name": "Jessica P.",
            "review": "The Classic Chocolate Fudge cake was the star of our party! Incredibly moist and rich. MotoPizza is my new go-to for all celebrations.",
            "avatar": "JP",
        },
        {
            "name": "Alex D.",
            "review": "I ordered the Red Velvet for my anniversary, and my partner was blown away. The cream cheese frosting is to die for. 10/10!",
            "avatar": "AD",
        },
        {
            "name": "Samantha G.",
            "review": "Their pastries are a weekend essential. The almond croissant is flaky, buttery perfection. It's like a little trip to Paris.",
            "avatar": "SG",
        },
    ]
    faqs: list[dict[str, str]] = [
        {
            "question": "Do you offer custom cake designs?",
            "answer": "Yes! We love bringing your vision to life. Contact us via WhatsApp to discuss your custom cake design, and we'll work with you to create something special for your occasion.",
        },
        {
            "question": "How far in advance should I place my order?",
            "answer": "For standard cakes and pastries, 48 hours notice is appreciated. For custom or large orders, we recommend contacting us at least one week in advance to ensure availability.",
        },
        {
            "question": "Do you offer delivery services?",
            "answer": "Currently, we offer local delivery within a 5-mile radius. Please contact us to confirm if your location is within our delivery zone and to get a quote for the delivery fee.",
        },
        {
            "question": "What are your business hours?",
            "answer": "We are open from Tuesday to Sunday, 9:00 AM to 6:00 PM. We are closed on Mondays. You can find us at 123 Bakery Lane, Foodie City.",
        },
    ]