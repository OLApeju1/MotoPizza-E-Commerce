import reflex as rx
import hashlib
import os


class AuthState(rx.State):
    error_message: str = ""
    is_authenticated: bool = False

    @rx.var
    def token_is_valid(self) -> bool:
        return self.is_authenticated

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
            self.error_message = ""
            main_state = await self.get_state(State)
            if return_url == "/checkout":
                return rx.redirect("/admin/products")
            return rx.redirect("/admin/products")
        else:
            self.error_message = "Invalid credentials."

    @rx.event
    def logout(self):
        self.is_authenticated = False
        return rx.redirect("/")

    @rx.event
    def check_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/login")