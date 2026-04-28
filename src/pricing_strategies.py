# pricing_strategies.py
# Strategy pattern to dynamically adjust prices (e.g. for students vs generic tax)
# Coded by Durgesh

class BasePricing:
    def calc_price(self, base_price: float) -> float:
        return base_price

class NormalPricing(BasePricing):
    def calc_price(self, base_price):
        # standard 5% tax or something similar
        tax = base_price * 0.05
        return base_price + tax

class StudentDiscount(BasePricing):
    def calc_price(self, base_price):
        # students get a 10% flat discount!
        discount = base_price * 0.10
        return base_price - discount
