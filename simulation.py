import os
import json
from src.central_registry import CentralRegistry
from src.kiosk_factory import (
    PharmacyKioskFactory, FoodKioskFactory, 
    EmergencyReliefKioskFactory, ElectronicsKioskFactory
)
from src.kiosk_interface import KioskInterface
from src.i_product import SingleProduct, BundleProduct
from src.hardware import (
    RoboticArmDispenser, SpiralDispenser, RefrigerationModule
)
from src.payment_gateway import PaymentProcessor

"""
Aura Retail OS - Simulation Runner
Demonstrates Path B: Modular Hardware Platform and required design patterns.
"""

# =====================================================================
# SCENARIO 4 - EXTENSIBILITY DEMO (Open/Closed Principle)
# =====================================================================
# We define a brand new payment provider without touching src/ files.

class CryptoAPI:
    """New third-party Crypto payment API."""
    def pay_with_crypto(self, amount: float, wallet_address: str) -> bool:
        print(f"[EXTERNAL-API] Crypto: Processing {amount} BTC from {wallet_address}")
        return True

class CryptoAdapter(PaymentProcessor):
    """Adapter for the new CryptoAPI."""
    def __init__(self):
        self.api = CryptoAPI()

    def process(self, amount: float, user_id: str) -> bool:
        # Map parameters to API expectations
        return self.api.pay_with_crypto(amount, f"0x{user_id.upper()}BEEF")


def run_simulation():
    print("="*60)
    print("       AURA RETAIL OS - SYSTEM SIMULATION (PATH B)       ")
    print("="*60)

    # Scenarios initialization
    registry = CentralRegistry.get_instance()

    # -----------------------------------------------------------------
    print("\n[SYSTEM] Scenario 1: Hardware Replacement at Runtime")
    # -----------------------------------------------------------------
    pharma_kiosk = KioskInterface("PHARMA-SEC-01", PharmacyKioskFactory())
    # Manually downgrade dispenser to show a runtime upgrade later
    pharma_kiosk.hardware.active_dispenser = SpiralDispenser("Legacy-Spiral-Unit")
    
    # Setup inventory
    insulin = SingleProduct("P001", "Insulin", 500.0, 10)
    pharma_kiosk.inventory.add_product(insulin)
    
    print("[HARDWARE] Current dispenser: ", type(pharma_kiosk.hardware.active_dispenser).__name__)
    pharma_kiosk.purchase_item("P001", "USER_A", "credit_card")
    
    # Replace dispenser at runtime
    print("[HARDWARE] Upgrading dispenser to RoboticArm...")
    pharma_kiosk.hardware.replace_dispenser(RoboticArmDispenser("Precision-Arm-X"))
    pharma_kiosk.purchase_item("P001", "USER_A", "credit_card")
    
    # Attach optional module
    print("[HARDWARE] Adding Refrigeration Module...")
    pharma_kiosk.hardware.add_module(RefrigerationModule("ColdVault-3000"))
    pharma_kiosk.run_diagnostics()


    # -----------------------------------------------------------------
    print("\n[SYSTEM] Scenario 2: Multiple Payment Providers")
    # -----------------------------------------------------------------
    food_kiosk = KioskInterface("METRO-FOOD-05", FoodKioskFactory())
    coffee = SingleProduct("F101", "Coffee", 40.0, 50)
    food_kiosk.inventory.add_product(coffee)

    print("[PAYMENT] Processing Credit Card payment...")
    food_kiosk.purchase_item("F101", "Durgesh", "credit_card")
    
    print("[PAYMENT] Processing UPI payment...")
    food_kiosk.purchase_item("F101", "Priyanshu", "upi")
    
    print("[PAYMENT] Processing Wallet payment...")
    food_kiosk.purchase_item("F101", "Jay", "wallet")


    # -----------------------------------------------------------------
    print("\n[SYSTEM] Scenario 3: Nested Bundle Inventory")
    # -----------------------------------------------------------------
    tech_kiosk = KioskInterface("CAMPUS-TECH-01", ElectronicsKioskFactory())
    
    laptop = SingleProduct("E001", "Laptop", 60000.0, 5)
    mouse = SingleProduct("E002", "Mouse", 1500.0, 20)
    bag = SingleProduct("E003", "Laptop Bag", 2000.0, 15)
    
    # Bundle Level 1: Student Kit
    student_kit = BundleProduct("B_STUDENT", "Student Tech Kit")
    student_kit.add_product(laptop)
    student_kit.add_product(mouse)
    
    # Bundle Level 2: Mega Bundle (Nested)
    mega_bundle = BundleProduct("B_MEGA", "Mega Campus Bundle")
    mega_bundle.add_product(student_kit)
    mega_bundle.add_product(bag)
    
    tech_kiosk.inventory.add_product(laptop)
    tech_kiosk.inventory.add_product(mouse)
    tech_kiosk.inventory.add_product(bag)
    tech_kiosk.inventory.add_product(mega_bundle)
    
    print(f"[INVENTORY] Mega Bundle recursive price check: {mega_bundle.get_price()} INR")
    print(f"[PURCHASE] Buying the Mega Bundle...")
    tech_kiosk.purchase_item("B_MEGA", "Moksh", "upi")
    
    print("[INVENTORY] Verifying stocks after bundle purchase...")
    print(f"  Laptop remaining: {laptop.quantity}")
    print(f"  Mouse remaining: {mouse.quantity}")
    print(f"  Mega Bundle available: {mega_bundle.is_available()}")


    # -----------------------------------------------------------------
    print("\n[SYSTEM] Scenario 4: Extensibility (Crypto Payment)")
    # -----------------------------------------------------------------
    relief_kiosk = KioskInterface("DISASTER-RELIEF-01", EmergencyReliefKioskFactory())
    med_kit = SingleProduct("R999", "Emergency Med Kit", 1200.0, 100)
    relief_kiosk.inventory.add_product(med_kit)
    
    # Register the new adapter at runtime
    relief_kiosk.payment_gateway.register_adapter("crypto", CryptoAdapter())
    
    # Use the new payment method
    relief_kiosk.purchase_item("R999", "Kurin", "crypto")


    # -----------------------------------------------------------------
    print("\n[SYSTEM] Final Verification & History")
    # -----------------------------------------------------------------
    print("\n[SYSTEM] Command History (from relief_kiosk):")
    for cmd in relief_kiosk.invoker.get_history():
        print(f"  -> {cmd}")

    print("\n[SYSTEM] Verifying persistence files...")
    files = [
        "data/inventory_PHARMA-SEC-01.json",
        "data/transactions_METRO-FOOD-05.json",
        "data/config.json"
    ]
    for f in files:
        status = "EXISTS" if os.path.exists(f) else "MISSING"
        print(f"  File {f}: {status}")

    print("\n" + "="*60)
    print("               SIMULATION COMPLETE               ")
    print("="*60)

if __name__ == "__main__":
    run_simulation()
