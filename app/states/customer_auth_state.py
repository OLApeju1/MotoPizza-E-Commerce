import reflex as rx
from typing import TypedDict
import re
import datetime
from app.states.state import State


class Customer(TypedDict):
    email: str
    name: str
    phone: str
    signup_date: str


class CustomerAuthState(rx.State):
    current_customer: Customer | None = None
    error_message: str = ""

    @rx.var
    def is_customer_authenticated(self) -> bool:
        return self.current_customer is not None

    def _validate_email(self, email: str) -> bool:
        return bool(re.match("[^@]+@[^@]+\\.[^@]+", email))

    @rx.event
    async def signup(self, form_data: dict[str, str]):
        name = form_data.get("name", "").strip()
        email = form_data.get("email", "").strip()
        phone = form_data.get("phone", "").strip()
        if not name or not email or (not phone):
            self.error_message = "All fields are required."
            return
        if not self._validate_email(email):
            self.error_message = "Invalid email format."
            return
        main_state = await self.get_state(State)
        if any((c["email"] == email for c in main_state.customers)):
            self.error_message = "A customer with this email already exists."
            return
        new_customer = Customer(
            name=name,
            email=email,
            phone=phone,
            signup_date=datetime.datetime.utcnow().isoformat(),
        )
        main_state.customers.append(new_customer)
        self.current_customer = new_customer
        self.error_message = ""
        return rx.redirect("/checkout")

    @rx.event
    async def login(self, form_data: dict[str, str]):
        email = form_data.get("email", "").strip()
        if not email:
            self.error_message = "Email is required."
            return
        main_state = await self.get_state(State)
        customer = next((c for c in main_state.customers if c["email"] == email), None)
        if customer:
            self.current_customer = customer
            self.error_message = ""
            return rx.redirect("/checkout")
        else:
            self.error_message = "No account found with this email. Please sign up."

    @rx.event
    def customer_logout(self):
        self.current_customer = None
        return rx.redirect("/")

    @rx.event
    def check_customer_auth(self):
        if not self.is_customer_authenticated:
            return rx.redirect("/checkout/login")