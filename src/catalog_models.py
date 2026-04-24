# catalog_models.py
# Composite pattern to handle single items and bundles/combos
# Done by: Priyanshu

from abc import ABC, abstractmethod

class BaseItem(ABC):
    @abstractmethod
    def get_total_price(self):
        pass
        
    @abstractmethod
    def has_stock(self):
        pass

class SingleItem(BaseItem):
    def __init__(self, c_code, c_name, c_price, c_qty):
        self.code = c_code
        self.name = c_name
        self.price = c_price
        self.stock = c_qty

    def get_total_price(self):
        return self.price
        
    def has_stock(self):
        return self.stock > 0

class ComboOffer(BaseItem):
    # This acts as the composite wrapper
    def __init__(self, combo_code, combo_name):
        self.code = combo_code
        self.name = combo_name
        self.items_inside = []
        
    def add_to_combo(self, item_obj):
        # print("added item to combo:", item_obj.name)
        self.items_inside.append(item_obj)

    def get_total_price(self):
        # recursively find total price
        total_amt = 0.0
        for i in self.items_inside:
            total_amt += i.get_total_price()
        return total_amt

    def has_stock(self):
        # combo is available only if every single piece inside has stock
        for i in self.items_inside:
            if not i.has_stock():
                return False
        return True
