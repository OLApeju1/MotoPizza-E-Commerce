import reflex as rx
from typing import TypedDict
from app.states.state import State, Product
from app.states.auth_state import AuthState
import asyncio
import time
import logging


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

    @rx.event
    def set_product_form_field(self, field: str, value):
        self.product_form[field] = value

    @rx.event
    def set_price(self, price: str):
        try:
            self.product_form["price"] = float(price)
        except ValueError as e:
            self.product_form["price"] = 0.0
            logging.exception(f"Error: {e}")

    @rx.event
    def add_ingredient(self):
        if (
            self.new_ingredient
            and self.new_ingredient not in self.product_form["ingredients"]
        ):
            self.product_form["ingredients"].append(self.new_ingredient.strip())
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
    def set_editing_product(self, product: Product):
        self.product_form = product.copy()
        self.is_editing = True

    @rx.event
    async def handle_product_image_upload(self, files: list[rx.UploadFile]):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            yield rx.toast.error("You must be logged in to upload images.")
            return
        if not files:
            return
        upload_data = await files[0].read()
        outfile = rx.get_upload_dir() / files[0].name
        with outfile.open("wb") as file_object:
            file_object.write(upload_data)
        self.product_form["image"] = files[0].name
        yield rx.toast.success("Image uploaded successfully!")

    @rx.event
    async def save_product(self, form_data: dict[str, str]):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            yield rx.toast.error("You must be logged in to save products.")
            return
        self.is_saving = True
        yield
        if form_data.get("new_ingredient"):
            self.set_new_ingredient(form_data["new_ingredient"])
        for field in ["name", "description", "category", "full_description"]:
            if field in form_data:
                self.product_form[field] = form_data[field]
        if "price" in form_data:
            self.set_price(form_data["price"])
        main_state = await self.get_state(State)
        products = main_state.products
        if (
            not self.product_form["name"]
            or self.product_form["price"] <= 0
            or (not self.product_form["image"])
        ):
            yield rx.toast.error("Name, price, and image are required.")
            self.is_saving = False
            return
        product_to_save = self.product_form.copy()
        if self.is_editing:
            index_to_update = -1
            for i, p in enumerate(products):
                if p["id"] == product_to_save["id"]:
                    index_to_update = i
                    break
            if index_to_update != -1:
                main_state.products[index_to_update] = product_to_save
                yield rx.toast.success("Product updated successfully!")
            else:
                yield rx.toast.error("Product not found for updating.")
        else:
            new_id = max([p["id"] for p in products], default=0) + 1
            product_to_save["id"] = new_id
            main_state.products.append(product_to_save)
            yield rx.toast.success("Product added successfully!")
        self.is_saving = False
        yield AdminState.clear_form()