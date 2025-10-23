import reflex as rx
import hashlib
import time


class AuthState(rx.State):
    username: str = ""
    password: str = ""
    error_message: str = ""
    is_authenticated: bool = False
    def_user: str = "admin"
    def_pass: str = hashlib.sha256("admin".encode()).hexdigest()

    @rx.var
    def token_is_valid(self) -> bool:
        return self.is_authenticated

    @rx.event
    def set_username(self, value: str):
        self.username = value
        self.error_message = ""

    @rx.event
    def set_password(self, value: str):
        self.password = value
        self.error_message = ""

    @rx.event
    def login(self, form_data: dict[str, str]):
        self.username = form_data.get("username", "")
        self.password = form_data.get("password", "")
        if not self.username or not self.password:
            self.error_message = "Username and password are required."
            return
        hashed_password = hashlib.sha256(self.password.encode()).hexdigest()
        if self.username == self.def_user and hashed_password == self.def_pass:
            self.is_authenticated = True
            token = f"fake-token-for-{self.username}-{time.time()}"
            self.password = ""
            return rx.redirect("/")
        else:
            self.error_message = "Invalid username or password."
            self.password = ""

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.username = ""
        self.password = ""
        return rx.redirect("/")

    @rx.event
    def check_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/login")