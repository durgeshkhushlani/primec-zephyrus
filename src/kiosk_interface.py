# facade - hides all subsystems, only this class is used from outside

from src.central_registry import CentralRegistry


class KioskInterface:

    def __init__(self, kiosk_id, factory):
        self.kiosk_id = kiosk_id
        self.disp = factory.make_dispenser()
        self.pay_mod = factory.make_payment()
        self.pol = factory.make_inv_policy()
        self.items = []
        self.txns = []

        reg = CentralRegistry.get_instance()
        reg.add_kiosk(self)

    def load_item(self, product):
        self.items.append(product)

    def buy(self, item_name, amt):
        print("\n[" + self.kiosk_id + "] buying: " + item_name)

        found = None
        for i in self.items:
            if i.name == item_name:
                found = i
                break

        if not found:
            print("item not found")
            return False

        if not found.in_stock():
            print(item_name + " is out of stock")
            return False

        self.pol.verify(item_name)
        self.pay_mod.pay(amt)
        self.disp.give(item_name)
        found.take_one()

        self.txns.append({"name": item_name, "amt": amt})
        print("done.")
        return True

    def refund(self, txn_id):
        print("\n[" + self.kiosk_id + "] refund for txn: " + txn_id)
        self.pay_mod.refund(txn_id)

    def diagnostics(self):
        print("\n[" + self.kiosk_id + "] diagnostics ---")
        print("  dispenser : " + self.disp.dtype)
        print("  payment   : " + self.pay_mod.ptype)
        print("  policy    : " + self.pol.pol)
        print("  items loaded : " + str(len(self.items)))
        print("  txns done    : " + str(len(self.txns)))

    def restock(self, item_name, add_qty):
        print("\n[" + self.kiosk_id + "] restocking " + item_name + " +" + str(add_qty))
        found = None
        for i in self.items:
            if i.name == item_name:
                found = i
                break
        if found:
            found.qty += add_qty
            print("new qty: " + str(found.qty))
        else:
            print("item not in inventory")

    def show_items(self):
        print("\n[" + self.kiosk_id + "] inventory:")
        for i in self.items:
            i.show("  ")
