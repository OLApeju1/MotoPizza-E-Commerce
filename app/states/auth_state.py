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


class Admin(TypedDict):
    username: str
    password_hash: str
    created_at: str


class AuthState(rx.State):
    error_message: str = ""
    is_authenticated: bool = False
    authenticated_user: User | None = None
    users: list[User] = []
    admins: list[Admin] = []
    admin_to_delete: str = ""
    show_delete_dialog: bool = False

    @rx.var
    def is_main_admin(self) -> bool:
        admin_user = os.getenv("ADMIN_USERNAME", "admin")
        return (
            self.is_authenticated
            and self.authenticated_user is not None
            and (self.authenticated_user["email"] == admin_user)
        )

    @rx.var
    def token_is_valid(self) -> bool:
        return self.is_authenticated

    @rx.event
    def clear_error_message(self):
        self.error_message = ""

    @rx.event
    def set_admin_to_delete(self, username: str):
        self.admin_to_delete = username
        self.show_delete_dialog = True

    @rx.event
    def cancel_delete(self):
        self.admin_to_delete = ""
        self.show_delete_dialog = False

    @rx.event
    def confirm_delete_admin(self):
        self.show_delete_dialog = False
        admin_user = os.getenv("ADMIN_USERNAME", "admin")
        if self.admin_to_delete == admin_user:
            self.admin_to_delete = ""
            return rx.toast.error("Main admin cannot be deleted.")
        initial_admin_count = len(self.admins)
        self.admins = [a for a in self.admins if a["username"] != self.admin_to_delete]
        if len(self.admins) < initial_admin_count:
            yield rx.toast.success(f"Admin '{self.admin_to_delete}' has been removed.")
        else:
            yield rx.toast.error(f"Failed to remove admin '{self.admin_to_delete}'.")
        self.admin_to_delete = ""

    @rx.event
    async def login(self, form_data: dict[str, str]):
        from app.states.state import State

        username = form_data.get("username", "")
        password = form_data.get("password", "")
        if not username or not password:
            self.error_message = "Username and password are required."
            return
        self._ensure_main_admin()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        for admin in self.admins:
            if (
                admin["username"] == username
                and admin["password_hash"] == hashed_password
            ):
                self.is_authenticated = True
                self.authenticated_user = {
                    "name": "Admin User",
                    "email": admin["username"],
                    "phone": "N/A",
                    "password_hash": admin["password_hash"],
                }
                self.error_message = ""
                return rx.redirect("/admin/products")
        return_url = self.router.page.params.get("return_url", "/")
        for user in self.users:
            if user["email"] == username and user["password_hash"] == hashed_password:
                self.is_authenticated = True
                self.authenticated_user = user
                self.error_message = ""
                return rx.redirect(return_url)
        self.error_message = "Invalid credentials."

    def _ensure_main_admin(self):
        admin_user = os.getenv("ADMIN_USERNAME", "admin")
        if not any((a["username"] == admin_user for a in self.admins)):
            import datetime

            admin_pass_hash = os.getenv(
                "ADMIN_PASSWORD_HASH", hashlib.sha256("admin".encode()).hexdigest()
            )
            self.admins.append(
                {
                    "username": admin_user,
                    "password_hash": admin_pass_hash,
                    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
            )

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
    async def add_admin(self, form_data: dict[str, str]):
        self.error_message = ""
        username = form_data.get("username", "")
        password = form_data.get("password", "")
        confirm_password = form_data.get("confirm_password", "")
        if not self.is_main_admin:
            self.error_message = "Only the main admin can add other admins."
            yield rx.toast.error(self.error_message)
            return
        if not all([username, password, confirm_password]):
            self.error_message = "All fields are required."
            return
        if password != confirm_password:
            self.error_message = "Passwords do not match."
            return
        if any((admin["username"] == username for admin in self.admins)):
            self.error_message = f"Admin username '{username}' already exists."
            return
        import datetime

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        new_admin: Admin = {
            "username": username,
            "password_hash": hashed_password,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.admins.append(new_admin)
        yield rx.toast.success(f"Admin '{username}' added successfully!")
        self.error_message = ""

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.authenticated_user = None
        return rx.redirect("/")

    @rx.event
    def check_auth(self):
        self._ensure_main_admin()
        if not self.is_authenticated:
            return rx.redirect("/login")