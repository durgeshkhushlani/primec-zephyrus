from src.kiosk_factory import KioskFactory
from src.inventory import Inventory
from src.hardware import HardwareManager
from src.payment_gateway import PaymentGateway
from src.commands import CommandInvoker, PurchaseItemCommand, RefundCommand, RestockCommand
from src.central_registry import CentralRegistry

"""
Facade Module for Aura Retail OS.
Wraps all complex subsystems into a clean, simple interface for the kiosk operations.
"""

class KioskInterface:
    """The central access point for interacting with a kiosk's hardware, inventory, and payments."""
    
    def __init__(self, kiosk_id: str, factory: KioskFactory):
        self.kiosk_id = kiosk_id
        
        # Initialize subsystems using the factory and configuration
        self.inventory = Inventory(f"data/inventory_{kiosk_id}.json")
        self.hardware = HardwareManager(factory.create_dispenser())
        self.payment_gateway = PaymentGateway()
        self.invoker = CommandInvoker(f"data/transactions_{kiosk_id}.json")
        
        # Internal components created by the factory
        self.verifier = factory.create_verifier()
        self.pricing_module = factory.create_pricing_module()
        self.inventory_policy = factory.create_inventory_policy()

        # Register self with the Singleton Central Registry
        CentralRegistry.get_instance().register_kiosk(kiosk_id, self)

    def purchase_item(self, product_id: str, user_id: str, payment_method: str) -> bool:
        """Orchestrates a purchase using the Command pattern."""
        print(f"\n[SYSTEM] Kiosk {self.kiosk_id} initiating purchase for {product_id}...")
        
        # 1. Hardware health check (Constraint: Block if any component FAILED)
        health = self.hardware.get_health()
        if any(status == "FAILED" for status in health.values()):
            print("[SYSTEM] Transaction BLOCKED: Hardware failure detected.")
            return False

        # 2. External verifications
        if not self.verifier.verify(user_id):
            print("[SYSTEM] Transaction BLOCKED: User verification failed.")
            return False

        if not self.inventory_policy.check_eligibility(product_id):
            print("[SYSTEM] Transaction BLOCKED: Item eligibility check failed.")
            return False

        # 3. Create and execute purchase command
        purchase_cmd = PurchaseItemCommand(self, product_id, user_id, payment_method)
        return self.invoker.execute_command(purchase_cmd)

    def refund_transaction(self, transaction_id: str) -> bool:
        """Triggers a refund for a specific transaction."""
        refund_cmd = RefundCommand(self, transaction_id)
        return self.invoker.execute_command(refund_cmd)

    def run_diagnostics(self) -> None:
        """Prints a comprehensive health and status report for the kiosk."""
        print(f"\n================ DIAGNOSTICS: {self.kiosk_id} ================")
        health = self.hardware.get_health()
        print("[HARDWARE STATUS]")
        for component, status in health.items():
            print(f"  - {component}: {status}")
        
        print("\n[INVENTORY STATUS]")
        products = self.inventory.list_products()
        for p in products:
            print(f"  - {p.get_details()}")

        print("\n[TRANSACTION HISTORY]")
        history = self.invoker.get_history()
        for entry in history[-5:]: # Show last 5
            print(f"  - {entry['timestamp']} | {entry['type']} | {entry.get('status', 'OK')}")
        print("==========================================================")

    def restock_inventory(self, product_id: str, quantity: int) -> bool:
        """Replenishes stock for a product."""
        restock_cmd = RestockCommand(self, product_id, quantity)
        return self.invoker.execute_command(restock_cmd)
