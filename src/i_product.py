from abc import ABC, abstractmethod
from typing import List

"""
Product Interface and Hierarchy for Aura Retail OS.
Implements the Composite design pattern for single products and bundles.
"""

class IProduct(ABC):
    """Abstract base class for all products."""
    
    def __init__(self, product_id: str, name: str, price: float, quantity: int):
        self.product_id = product_id
        self.name = name
        self._price = price
        self._quantity = quantity
        self.reserved_quantity = 0

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        self._price = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        self._quantity = value

    @abstractmethod
    def get_price(self) -> float:
        """Returns the total price of the product (recursive for bundles)."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Checks if product is available (quantity - reserved > 0)."""
        pass

    @abstractmethod
    def get_details(self) -> str:
        """Returns descriptive details of the product."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Serializes product to a dictionary for persistence."""
        pass


class SingleProduct(IProduct):
    """A standalone retail item."""
    
    def get_price(self) -> float:
        """Returns the base price."""
        return self.price

    def is_available(self) -> bool:
        """Checks stock against reservations."""
        return (self.quantity - self.reserved_quantity) > 0

    def get_details(self) -> str:
        """Returns product ID, name, price, and stock info."""
        return f"ID: {self.product_id} | {self.name} | Price: {self.price} | Stock: {self.quantity} (Res: {self.reserved_quantity})"

    def to_dict(self) -> dict:
        return {
            "type": "single",
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "reserved": self.reserved_quantity
        }


class BundleProduct(IProduct):
    """A collection of products, potentially including other bundles."""
    
    def __init__(self, product_id: str, name: str):
        super().__init__(product_id, name, 0, 0)
        self.children: List[IProduct] = []

    def add_product(self, product: IProduct):
        """Adds a child product to the bundle."""
        self.children.append(product)

    def get_price(self) -> float:
        """Returns the recursive sum of all child prices."""
        return sum(child.get_price() for child in self.children)

    def is_available(self) -> bool:
        """A bundle is available only if all its components are available."""
        if not self.children:
            return False
        return all(child.is_available() for child in self.children)

    def get_details(self) -> str:
        """Returns bundle info and nested children details."""
        details = f"[BUNDLE] ID: {self.product_id} | {self.name} | Total Price: {self.get_price()}\n"
        for child in self.children:
            item_details = child.get_details().replace("\n", "\n  ")
            details += f"  - {item_details}\n"
        return details.strip()

    def to_dict(self) -> dict:
        return {
            "type": "bundle",
            "product_id": self.product_id,
            "name": self.name,
            "children": [child.to_dict() for child in self.children]
        }

    @property
    def quantity(self) -> int:
        """A bundle's quantity is the minimum quantity of its components."""
        if not self.children:
            return 0
        return min(child.quantity for child in self.children)

    @quantity.setter
    def quantity(self, value: int):
        """Setting bundle quantity is not directly supported; set children instead."""
        pass

    @property
    def reserved_quantity(self) -> int:
        """A bundle's reserved quantity is the max reserved of its components (relative to bundle unit)."""
        if not self.children:
            return 0
        return max(child.reserved_quantity for child in self.children)

    @reserved_quantity.setter
    def reserved_quantity(self, value: int):
        """Manually setting reservation on bundle is handled by children."""
        pass
