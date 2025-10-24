import reflex as rx
import hashlib
import os
from typing import TypedDict
import re


class User(TypedDict):
    name: str
    email: str
    phone: str
    password_hash: str


class AuthState(rx.State):
    error_message: str = ""
    is_authenticated: bool = False
    authenticated_user: User | None = None
    users: list[User] = []

    @rx.var
    def token_is_valid(self) -> bool:
        return self.is_authenticated

    @rx.event
    def clear_error_message(self):
        self.error_message = ""

    @rx.event
    async def login(self, form_data: dict[str, str]):
        from app.states.state import State

        username = form_data.get("username", "")
        password = form_data.get("password", "")
        if not username or not password:
            self.error_message = "Username and password are required."
            return
        admin_user = os.getenv("ADMIN_USERNAME", "admin")
        admin_pass_hash = os.getenv(
            "ADMIN_PASSWORD_HASH", hashlib.sha256("admin".encode()).hexdigest()
        )
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return_url = self.router.page.params.get("return_url", "/")
        if username == admin_user and hashed_password == admin_pass_hash:
            self.is_authenticated = True
            self.authenticated_user = {
                "name": "Admin User",
                "email": admin_user,
                "phone": "N/A",
                "password_hash": admin_pass_hash,
            }
            self.error_message = ""
            main_state = await self.get_state(State)
            if return_url and return_url != "/":
                return rx.redirect(return_url)
            return rx.redirect("/admin/products")
        for user in self.users:
            if user["email"] == username and user["password_hash"] == hashed_password:
                self.is_authenticated = True
                self.authenticated_user = user
                self.error_message = ""
                return rx.redirect(return_url)
        self.error_message = "Invalid credentials."

    @rx.event
    async def signup(self, form_data: dict[str, str]):
        self.error_message = ""
        name = form_data.get("name", "")
        email = form_data.get("email", "").lower()
        phone = form_data.get("phone", "")
        password = form_data.get("password", "")
        confirm_password = form_data.get("confirm_password", "")
        if not all([name, email, phone, password, confirm_password]):
            self.error_message = "All fields are required."
            return
        if password != confirm_password:
            self.error_message = "Passwords do not match."
            return
        if not re.match("[^@]+@[^@]+\\.[^@]+", email):
            self.error_message = "Invalid email address."
            return
        if any((user["email"] == email for user in self.users)):
            self.error_message = "Email already in use."
            return
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        new_user: User = {
            "name": name,
            "email": email,
            "phone": phone,
            "password_hash": hashed_password,
        }
        self.users.append(new_user)
        yield rx.toast.success("Signup successful! Please log in.")
        yield rx.redirect("/login")

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.authenticated_user = None
        return rx.redirect("/")

    @rx.event
    def check_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/login")