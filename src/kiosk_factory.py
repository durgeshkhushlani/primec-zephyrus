# abstract factory - each kiosk type gets its own factory

from abc import ABC, abstractmethod


# --- product interfaces (dispenser, payment module, inventory policy) ---

class Dispenser:
    def __init__(self, dtype):
        self.dtype = dtype

    def give(self, item):
        raise NotImplementedError


class PaymentModule:
    def __init__(self, ptype):
        self.ptype = ptype

    def pay(self, amt):
        raise NotImplementedError

    def refund(self, txn_id):
        raise NotImplementedError


class InvPolicy:
    def __init__(self, pol):
        self.pol = pol

    def verify(self, item):
        raise NotImplementedError


# --- abstract factory ---

class KioskFactory(ABC):

    @abstractmethod
    def make_dispenser(self): pass

    @abstractmethod
    def make_payment(self): pass

    @abstractmethod
    def make_inv_policy(self): pass


# --- pharmacy kiosk ---

class PharmacyDispenser(Dispenser):
    def __init__(self):
        super().__init__("robotic_arm")

    def give(self, item):
        print("[pharma dispenser] giving out " + item + " via robotic arm")


class PharmacyPayment(PaymentModule):
    def __init__(self):
        super().__init__("card")

    def pay(self, amt):
        print("[pharma] card swiped for rs." + str(amt))

    def refund(self, txn_id):
        print("[pharma] refund done for txn " + txn_id)


class PharmacyPolicy(InvPolicy):
    def __init__(self):
        super().__init__("prescription_needed")

    def verify(self, item):
        print("[pharma] checking prescription for " + item)
        return True


class PharmacyKioskFactory(KioskFactory):
    def make_dispenser(self): return PharmacyDispenser()
    def make_payment(self):   return PharmacyPayment()
    def make_inv_policy(self): return PharmacyPolicy()


# --- food kiosk ---

class FoodDispenser(Dispenser):
    def __init__(self):
        super().__init__("spiral")

    def give(self, item):
        print("[food dispenser] spiral drop -> " + item)


class FoodPayment(PaymentModule):
    def __init__(self):
        super().__init__("upi")

    def pay(self, amt):
        print("[food] upi payment done rs." + str(amt))

    def refund(self, txn_id):
        print("[food] upi refund for " + txn_id)


class FoodPolicy(InvPolicy):
    def __init__(self):
        super().__init__("normal")

    def verify(self, item):
        print("[food] stock ok for " + item)
        return True


class FoodKioskFactory(KioskFactory):
    def make_dispenser(self): return FoodDispenser()
    def make_payment(self):   return FoodPayment()
    def make_inv_policy(self): return FoodPolicy()


# --- emergency kiosk ---

class EmergencyDispenser(Dispenser):
    def __init__(self):
        super().__init__("conveyor")

    def give(self, item):
        print("[emergency dispenser] conveyor releasing " + item)


class EmergencyPayment(PaymentModule):
    def __init__(self):
        super().__init__("free")

    def pay(self, amt):
        print("[emergency] no payment, item is free")

    def refund(self, txn_id):
        print("[emergency] nothing to refund")


class EmergencyPolicy(InvPolicy):
    def __init__(self):
        super().__init__("emergency_override")

    def verify(self, item):
        print("[emergency] override active, releasing " + item)
        return True


class EmergencyKioskFactory(KioskFactory):
    def make_dispenser(self): return EmergencyDispenser()
    def make_payment(self):   return EmergencyPayment()
    def make_inv_policy(self): return EmergencyPolicy()
