from typing import List

from django.conf import settings
from django.db import transaction

from server.models import Product


class Cart:

    def __init__(self, session):
        self.session = session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.actual_prices = {}

    def save(self, product: Product):
        """
        Сначало обновляем корзину - проверяем наличие товара в БД и
        комфликт между его кол-вом и кол-вом товара в корзине;

        Затем сохраняем в сессиях товар;

        Потом сохраняем обновленную информацию о продукте в БД;
        """
        self.update_cart()
        self.session.save()
        product.save()

    def add(self, product_id: int, amount: int = 1) -> None:
        product_info = self.cart.get(str(product_id), False)
        product: Product = Product.objects.filter(id=product_id).first()
        if product:
            amount = amount if product.quantity-amount >= 0 else product.quantity
            with transaction.atomic():
                if isinstance(product_info, dict):
                    product_info["amount"] += amount
                else:
                    self.cart[str(product_id)] = {"amount": amount}
                product.quantity -= amount
            self.save(product)

    def remove(self, product_id: int, amount: int = 1) -> None:
        product_info = self.cart.get(product_id, False)
        if isinstance(product_info, dict):
            product = Product.objects.filter(id=product_id).first()
            if product:
                with transaction.atomic():
                    product.quantity += amount
                    product_info["amount"] -= amount
                self.save(product)
        else:
            raise Exception("Can't remove product, which haven't been added to a cart!")

    def update_cart(self):
        old_cart = self.cart.copy()
        for product_id, product_info in old_cart.items():
            product = Product.objects.filter(id=product_id).first()
            if not product:
                self.cart.pop(product_id)
            if product_info["amount"] < 0:
                with transaction.atomic():
                    extra_amount = abs(product_info["amount"])
                    product_info["amount"] = 0
                    product.quantity += extra_amount
            self.session.save()

    def serialize_data(self) -> List:
        data = []
        for product in Product.objects.filter(id__in=[_id for _id in self.cart]):
            updated_info = self.cart[str(product.id)].copy()
            updated_info["id"] = product.id
            updated_info["image"] = product.image
            updated_info["price"] = product.price
            updated_info["title"] = product.title
            updated_info["description"] = product.description
            data.append(updated_info)
        return data

    def get_total_sum(self) -> int:
        return sum([self.cart[str(product.id)]["amount"] * product.price
                    for product in Product.objects.filter(id__in=[_id for _id in self.cart])])

    def __delitem__(self, product_id: int) -> None:
        product_info = self.cart.get(str(product_id), False)
        if product_info is not False:
            product = Product.objects.filter(id=product_id).first()
            if product:
                with transaction.atomic():
                    product.quantity += product_info["amount"]
                    self.cart.pop(str(product_id))
            self.save(product)

    def __delete__(self):
        self.session.pop(settings.CART_SESSION_ID)
        self.session.save()
