from src.central_registry import CentralRegistry
from src.kiosk_factory import PharmacyKioskFactory, FoodKioskFactory, EmergencyKioskFactory
from src.payment_gateway import UpiAdapter, CardAdapter, WalletAdapter
from src.i_product import SingleProduct, ProductBundle
from src.kiosk_interface import KioskInterface

print("aura retail os simulation --->")

# singleton test - both should point to same object
reg1 = CentralRegistry.get_instance()
reg2 = CentralRegistry.get_instance()
print("singleton check (should be true):", reg1 is reg2)

# creating kiosks using abstract factory
print("\ncreating kiosks -->")
pharma = KioskInterface("PHARMA-01", PharmacyKioskFactory())
food   = KioskInterface("FOOD-01",   FoodKioskFactory())
emrg   = KioskInterface("EMRG-01",   EmergencyKioskFactory())

# setting up inventory using composite pattern
print("\n-- loading inventory --")

medicine = SingleProduct("Paracetamol", 25, 10)
band     = SingleProduct("Bandage", 15, 5)
kit      = ProductBundle("First Aid Kit")
kit.add(medicine)
kit.add(band)

pharma.load_item(medicine)
pharma.load_item(kit)
pharma.show_items()

chips = SingleProduct("Chips", 20, 3)
water = SingleProduct("Water Bottle", 15, 0)   # out of stock on purpose
juice = SingleProduct("Juice", 30, 2)
combo = ProductBundle("Snack Combo")
combo.add(chips)
combo.add(juice)

food.load_item(chips)
food.load_item(water)
food.load_item(combo)
food.show_items()

blanket = SingleProduct("Blanket", 0, 20)
torch   = SingleProduct("Flashlight", 0, 15)
ekit    = ProductBundle("Emergency Kit")
ekit.add(blanket)
ekit.add(torch)

emrg.load_item(blanket)
emrg.load_item(ekit)
emrg.show_items()

# buying stuff through the facade
print("\npurchase simulation -->")
pharma.buy("Paracetamol", 25)
food.buy("Chips", 20)
food.buy("Water Bottle", 15)   # should fail
emrg.buy("Blanket", 0)

# adapter pattern - swapping payment providers
print("\npayment adapter test -->")
upi    = UpiAdapter()
card   = CardAdapter()
wallet = WalletAdapter()

# all three use same method names even though internal apis differ
upi.do_payment(150)
card.do_payment(150)
wallet.do_payment(150)

upi.do_refund("TXN101")
card.do_refund("TXN102")

# diagnostics and restock via facade
print("\ndiagnostics -->")
pharma.diagnostics()

print("\n-- restock test --")
food.restock("Water Bottle", 10)
food.buy("Water Bottle", 15)   # should work now

# check registry has all kiosks
print("\nregistry check -->")
all_kiosks = CentralRegistry.get_instance().get_all_kiosks()
print("total kiosks registered:", len(all_kiosks))
for k in all_kiosks:
    print(" ->", k.kiosk_id)

print("\n..simulation done..")
