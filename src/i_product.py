# composite pattern for inventory
# single item and bundle both behave same from outside

from abc import ABC, abstractmethod


class IProduct(ABC):

    @abstractmethod
    def get_price(self): pass

    @abstractmethod
    def in_stock(self): pass

    @abstractmethod
    def get_qty(self): pass

    @abstractmethod
    def show(self, pad=""): pass


# leaf node
class SingleProduct(IProduct):

    def __init__(self, name, price, qty):
        self.name = name
        self.price = price
        self.qty = qty

    def get_price(self):
        return self.price

    def in_stock(self):
        return self.qty > 0

    def get_qty(self):
        return self.qty

    def take_one(self):
        if self.qty > 0:
            self.qty -= 1

    def show(self, pad=""):
        print(pad + "- " + self.name + " | rs." + str(self.price) + " | qty: " + str(self.qty))


# composite node - can hold single items or other bundles
class ProductBundle(IProduct):

    def __init__(self, name):
        self.name = name
        self.stuff = []   # children

    def add(self, p):
        self.stuff.append(p)

    def get_price(self):
        total = 0
        for p in self.stuff:
            total += p.get_price()
        return total

    def in_stock(self):
        for p in self.stuff:
            if not p.in_stock():
                return False
        return True

    def get_qty(self):
        min_qty = 9999
        for p in self.stuff:
            if p.get_qty() < min_qty:
                min_qty = p.get_qty()
        return min_qty

    def show(self, pad=""):
        print(pad + "[bundle] " + self.name + " | total: rs." + str(self.get_price()))
        for p in self.stuff:
            p.show(pad + "   ")
