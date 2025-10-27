import reflex as rx
import hashlib
import os
from typing import TypedDict
import re
import bcrypt
import bleach
import time
import datetime


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
    SESSION_TIMEOUT: int = 1800
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION: int = 900
    error_message: str = ""
    is_authenticated: bool = False
    authenticated_user: User | None = None
    users: list[User] = []
    admins: list[Admin] = []
    admin_to_delete: str = ""
    show_delete_dialog: bool = False
    login_timestamp: float = 0.0
    failed_login_attempts: dict[str, int] = {}
    account_lockout_until: dict[str, float] = {}

    @rx.var
    def is_main_admin(self) -> bool:
        admin_user = os.getenv("ADMIN_USERNAME", "admin")
        return (
            self.is_authenticated
            and self.authenticated_user is not None
            and (self.authenticated_user["email"] == admin_user)
        )

    @rx.var
    def is_admin(self) -> bool:
        return (
            self.is_authenticated
            and self.authenticated_user is not None
            and any(
                (a["username"] == self.authenticated_user["email"] for a in self.admins)
            )
        )

    @rx.var
    def token_is_valid(self) -> bool:
        return self.is_authenticated

    def _sanitize_input(self, value: str) -> str:
        return bleach.clean(value.strip())

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
        admin_user = os.getenv("ADMIN_USERNAME")
        if not admin_user:
            return rx.toast.error("Admin user not configured.")
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

        username = self._sanitize_input(form_data.get("username", ""))
        password = form_data.get("password", "")
        if self.account_lockout_until.get(username, 0) > time.time():
            self.error_message = "Account locked. Please try again later."
            return
        if not username or not password:
            self.error_message = "Username and password are required."
            return
        self._ensure_main_admin()
        for admin in self.admins:
            if admin["username"] == username and bcrypt.checkpw(
                password.encode(), admin["password_hash"].encode()
            ):
                self.is_authenticated = True
                self.authenticated_user = {
                    "name": "Admin User",
                    "email": admin["username"],
                    "phone": "N/A",
                    "password_hash": admin["password_hash"],
                }
                self.error_message = ""
                self.failed_login_attempts.pop(username, None)
                self.account_lockout_until.pop(username, None)
                self.login_timestamp = time.time()
                return rx.redirect("/admin/products")
        return_url = self.router.page.params.get("return_url", "/")
        for user in self.users:
            if user["email"] == username and bcrypt.checkpw(
                password.encode(), user["password_hash"].encode()
            ):
                self.is_authenticated = True
                self.authenticated_user = user
                self.error_message = ""
                self.failed_login_attempts.pop(username, None)
                self.account_lockout_until.pop(username, None)
                self.login_timestamp = time.time()
                return rx.redirect(return_url)
        self.failed_login_attempts[username] = (
            self.failed_login_attempts.get(username, 0) + 1
        )
        if self.failed_login_attempts.get(username, 0) >= self.MAX_LOGIN_ATTEMPTS:
            self.account_lockout_until[username] = time.time() + self.LOCKOUT_DURATION
            self.error_message = (
                "Account locked for 15 minutes due to too many failed login attempts."
            )
        else:
            self.error_message = "Invalid credentials."

    def _ensure_main_admin(self):
        admin_user = os.getenv("ADMIN_USERNAME")
        admin_pass = os.getenv("ADMIN_PASSWORD")
        if not admin_user or not admin_pass:
            print("CRITICAL: ADMIN_USERNAME and ADMIN_PASSWORD must be set in .env")
            return
        if not any((a["username"] == admin_user for a in self.admins)):
            hashed_password = bcrypt.hashpw(
                admin_pass.encode(), bcrypt.gensalt()
            ).decode("utf-8")
            self.admins.append(
                {
                    "username": admin_user,
                    "password_hash": hashed_password,
                    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
            )

    @rx.event
    async def signup(self, form_data: dict[str, str]):
        self.error_message = ""
        name = self._sanitize_input(form_data.get("name", ""))
        email = self._sanitize_input(form_data.get("email", "").lower())
        phone = self._sanitize_input(form_data.get("phone", ""))
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
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(
            "utf-8"
        )
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
        username = self._sanitize_input(form_data.get("username", ""))
        password = form_data.get("password", "")
        confirm_password = form_data.get("confirm_password", "")
        if not self.is_main_admin:
            self.error_message = "Authorization error."
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
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(
            "utf-8"
        )
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
        self.login_timestamp = 0.0
        return rx.redirect("/")

    @rx.event
    def check_auth(self):
        self._ensure_main_admin()
        if not self.is_authenticated:
            return rx.redirect("/login")
        if time.time() - self.login_timestamp > self.SESSION_TIMEOUT:
            self.is_authenticated = False
            self.authenticated_user = None
            self.login_timestamp = 0.0
            return (
                rx.toast.info("Session expired. Please log in again."),
                rx.redirect("/login"),
            )
        self.login_timestamp = time.time()