import json
from typing import List
from products import Product, get_product
from cart import dao


class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> 'Cart':
        # Explicit parsing for contents for better handling
        parsed_contents = [get_product(item_id) for item_id in json.loads(data['contents'])]
        return Cart(data['id'], data['username'], parsed_contents, data['cost'])


def get_cart(username: str) -> List[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    # Parse all cart items and convert them to Product objects
    items = []
    for cart_detail in cart_details:
        contents = json.loads(cart_detail['contents'])  # Safely parse JSON instead of using eval
        for item_id in contents:
            product = get_product(item_id)
            if product:
                items.append(product)
    return items


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)
