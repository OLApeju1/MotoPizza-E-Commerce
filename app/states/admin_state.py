import reflex as rx
from typing import TypedDict
from app.states.state import State, Product
from app.states.auth_state import AuthState
import asyncio
import time
import logging
import bleach
import os


class AdminState(rx.State):
    product_form: Product = {
        "id": 0,
        "name": "",
        "description": "",
        "price": 0.0,
        "image": "",
        "category": "",
        "full_description": "",
        "ingredients": [],
    }
    new_ingredient: str = ""
    is_saving: bool = False
    is_editing: bool = False
    MAX_FILE_SIZE = 10 * 1024 * 1024
    ALLOWED_MIME_TYPES = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
        "video/mp4",
        "video/quicktime",
        "video/x-msvideo",
    ]

    def _sanitize_input(self, value: str | None) -> str:
        if value is None:
            return ""
        return bleach.clean(value.strip())

    @rx.event
    def set_product_form_field(self, field: str, value):
        self.product_form[field] = self._sanitize_input(value)

    @rx.event
    def set_price(self, price: str):
        try:
            self.product_form["price"] = float(price)
        except ValueError as e:
            self.product_form["price"] = 0.0
            logging.exception(f"Error: {e}")

    @rx.event
    def add_ingredient(self):
        sanitized_ingredient = self._sanitize_input(self.new_ingredient)
        if (
            sanitized_ingredient
            and sanitized_ingredient not in self.product_form["ingredients"]
        ):
            self.product_form["ingredients"].append(sanitized_ingredient)
        self.new_ingredient = ""

    @rx.event
    def remove_ingredient(self, ingredient: str):
        self.product_form["ingredients"] = [
            i for i in self.product_form["ingredients"] if i != ingredient
        ]

    @rx.event
    def clear_form(self):
        self.product_form = {
            "id": 0,
            "name": "",
            "description": "",
            "price": 0.0,
            "image": "",
            "category": "",
            "full_description": "",
            "ingredients": [],
        }
        self.is_editing = False
        return rx.clear_selected_files("product_image_upload")

    @rx.event
    async def set_editing_product(self, product: Product):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return (rx.toast.error("Unauthorized"), rx.redirect("/login"))
        self.product_form = product.copy()
        self.is_editing = True

    @rx.event
    async def handle_product_image_upload(self, files: list[rx.UploadFile]):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            yield (rx.toast.error("Unauthorized"), rx.redirect("/login"))
            return
        if not files:
            return
        file = files[0]
        if file.size > self.MAX_FILE_SIZE:
            yield rx.toast.error("File is too large (max 10MB).")
            return
        if file.content_type not in self.ALLOWED_MIME_TYPES:
            yield rx.toast.error("Invalid file type.")
            return
        sanitized_filename = self._sanitize_input(file.name).replace(" ", "_")
        upload_data = await file.read()
        outfile = rx.get_upload_dir() / sanitized_filename
        try:
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)
            self.product_form["image"] = sanitized_filename
            yield rx.toast.success("Image uploaded successfully!")
        except Exception as e:
            logging.exception(f"File upload failed: {e}")
            yield rx.toast.error("File upload failed.")

    @rx.event
    async def save_product(self, form_data: dict[str, str]):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            yield (rx.toast.error("Unauthorized"), rx.redirect("/login"))
            return
        self.is_saving = True
        yield
        for field in ["name", "description", "category", "full_description"]:
            if field in form_data:
                self.product_form[field] = form_data[field]
        if "price" in form_data and form_data["price"]:
            self.set_price(form_data["price"])
        main_state = await self.get_state(State)
        products = main_state.products
        if (
            not self.product_form["name"]
            or self.product_form["price"] <= 0
            or (not self.product_form["image"])
        ):
            self.is_saving = False
            yield rx.toast.error("Name, price, and image are required.")
            return
        product_to_save = self.product_form.copy()
        if self.is_editing:
            index_to_update = next(
                (i for i, p in enumerate(products) if p["id"] == product_to_save["id"]),
                -1,
            )
            if index_to_update != -1:
                main_state.products[index_to_update] = product_to_save
                yield rx.toast.success("Product updated successfully!")
            else:
                yield rx.toast.error("Product not found for updating.")
        else:
            new_id = max([p["id"] for p in products] or [0]) + 1
            product_to_save["id"] = new_id
            main_state.products.append(product_to_save)
            yield rx.toast.success("Product added successfully!")
        self.is_saving = False
        yield AdminState.clear_form()