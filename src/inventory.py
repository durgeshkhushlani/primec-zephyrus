from typing import Dict, List, Optional
from src.i_product import IProduct, SingleProduct, BundleProduct
from src.persistence import save_json, load_json

"""
Inventory Management System for Aura Retail OS.
Handles product storage, stock reservations, and persistence.
"""

class Inventory:
    """Manages the lifecycle and state of products in a kiosk."""
    
    def __init__(self, filepath: str = "data/inventory.json"):
        self.filepath = filepath
        self.products: Dict[str, IProduct] = {}
        self.load()

    def add_product(self, product: IProduct) -> None:
        """Adds a product to the inventory and persists changes."""
        self.products[product.product_id] = product
        self.save()

    def remove_product(self, product_id: str) -> None:
        """Removes a product from the inventory."""
        if product_id in self.products:
            del self.products[product_id]
            self.save()

    def get_product(self, product_id: str) -> Optional[IProduct]:
        """Retrieves a product by ID."""
        return self.products.get(product_id)

    def list_products(self) -> List[IProduct]:
        """Returns a list of all products in inventory."""
        return list(self.products.values())

    def reserve(self, product_id: str, qty: int = 1) -> bool:
        """Reserves stock for a pending transaction."""
        product = self.get_product(product_id)
        if product and product.is_available():
            self._recursive_reserve(product, qty)
            self.save()
            print(f"[INVENTORY] Reserved {qty} unit(s) of {product_id}")
            return True
        print(f"[INVENTORY] Reservation failed for {product_id} (Insufficent stock)")
        return False

    def _recursive_reserve(self, product: IProduct, qty: int) -> None:
        if isinstance(product, BundleProduct):
            for child in product.children:
                self._recursive_reserve(child, qty)
        else:
            product.reserved_quantity += qty

    def release(self, product_id: str, qty: int = 1) -> None:
        """Releases reserved stock back to available pool."""
        product = self.get_product(product_id)
        if product:
            self._recursive_release(product, qty)
            self.save()
            print(f"[INVENTORY] Released {qty} unit(s) of {product_id}")

    def _recursive_release(self, product: IProduct, qty: int) -> None:
        if isinstance(product, BundleProduct):
            for child in product.children:
                self._recursive_release(child, qty)
        else:
            product.reserved_quantity = max(0, product.reserved_quantity - qty)

    def restock(self, product_id: str, qty: int) -> None:
        """Adds stock to a product."""
        product = self.get_product(product_id)
        if product:
            self._recursive_restock(product, qty)
            self.save()
            print(f"[INVENTORY] Restocked {qty} unit(s) of {product_id}")

    def _recursive_restock(self, product: IProduct, qty: int) -> None:
        if isinstance(product, BundleProduct):
            for child in product.children:
                self._recursive_restock(child, qty)
        else:
            product.quantity += qty

    def deduct(self, product_id: str, qty: int = 1, hardware_ready: bool = True) -> bool:
        """Permanently removes items from inventory after successful purchase."""
        if not hardware_ready:
            print("[INVENTORY] Deduction blocked: Hardware not ready.")
            return False
            
        product = self.get_product(product_id)
        if not product:
            return False
            
        # Check if we have enough reserved or available
        # Implementation assumes deduction follows reservation
        self._recursive_deduct(product, qty)
        self.save()
        print(f"[INVENTORY] Deducted {qty} unit(s) of {product_id}")
        return True

    def _recursive_deduct(self, product: IProduct, qty: int) -> None:
        if isinstance(product, BundleProduct):
            for child in product.children:
                self._recursive_deduct(child, qty)
        else:
            product.quantity = max(0, product.quantity - qty)
            product.reserved_quantity = max(0, product.reserved_quantity - qty)

    def save(self) -> None:
        """Persists current state to JSON."""
        data = {pid: p.to_dict() for pid, p in self.products.items()}
        save_json(self.filepath, data)

    def load(self) -> None:
        """Loads inventory state from JSON."""
        data = load_json(self.filepath)
        if not data:
            return
            
        for pid, pdata in data.items():
            self.products[pid] = self._from_dict(pdata)

    def _from_dict(self, data: dict) -> IProduct:
        """Factory method to reconstruct products from serialized data."""
        if data["type"] == "single":
            p = SingleProduct(data["product_id"], data["name"], data["price"], data["quantity"])
            p.reserved_quantity = data.get("reserved", 0)
            return p
        elif data["type"] == "bundle":
            b = BundleProduct(data["product_id"], data["name"])
            for cdata in data["children"]:
                b.add_product(self._from_dict(cdata))
            return b
        raise ValueError("Unknown product type in JSON")
