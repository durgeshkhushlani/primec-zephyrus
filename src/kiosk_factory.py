from abc import ABC, abstractmethod
from src.hardware import (
    Dispenser, SpiralDispenser, RoboticArmDispenser, ConveyorDispenser
)

"""
Abstract Factory Module for Aura Retail OS.
Ensures that compatible hardware and software components are created for each kiosk type.
"""

# --- Component Interfaces ---

class Verifier(ABC):
    """Interface for user or age verification."""
    @abstractmethod
    def verify(self, user_id: str) -> bool: pass

class PricingModule(ABC):
    """Interface for dynamic or static pricing strategies."""
    @abstractmethod
    def calculate(self, base_price: float) -> float: pass

class InventoryPolicy(ABC):
    """Interface for stock management rules (e.g., prescription checks)."""
    @abstractmethod
    def check_eligibility(self, product_id: str) -> bool: pass


# --- Concrete Components ---

class IDVerifier(Verifier):
    def verify(self, user_id: str) -> bool:
        print(f"[VERIFIER] Checking ID for user {user_id}...")
        return True

class BiometricVerifier(Verifier):
    def verify(self, user_id: str) -> bool:
        print(f"[VERIFIER] Scanning biometrics for {user_id}...")
        return True

class NoVerifier(Verifier):
    def verify(self, user_id: str) -> bool:
        return True

class StandardPricing(PricingModule):
    def calculate(self, base_price: float) -> float:
        return base_price

class DiscountPricing(PricingModule):
    def calculate(self, base_price: float) -> float:
        return base_price * 0.9  # 10% off

class PremiumPricing(PricingModule):
    def calculate(self, base_price: float) -> float:
        return base_price * 1.2  # 20% surcharge

class StrictPolicy(InventoryPolicy):
    def check_eligibility(self, product_id: str) -> bool:
        print(f"[POLICY] Strict check enabled for {product_id}")
        return True

class OpenPolicy(InventoryPolicy):
    def check_eligibility(self, product_id: str) -> bool:
        return True


# --- Abstract Factory ---

class KioskFactory(ABC):
    """Abstract Factory for creating family of compatible components."""
    
    @abstractmethod
    def create_dispenser(self) -> Dispenser: pass

    @abstractmethod
    def create_verifier(self) -> Verifier: pass

    @abstractmethod
    def create_pricing_module(self) -> PricingModule: pass

    @abstractmethod
    def create_inventory_policy(self) -> InventoryPolicy: pass


# --- Concrete Factories ---

class PharmacyKioskFactory(KioskFactory):
    def create_dispenser(self): return RoboticArmDispenser("RX-Arm-01")
    def create_verifier(self): return IDVerifier()
    def create_pricing_module(self): return StandardPricing()
    def create_inventory_policy(self): return StrictPolicy()

class FoodKioskFactory(KioskFactory):
    def create_dispenser(self): return SpiralDispenser("SnackSpiral-V2")
    def create_verifier(self): return NoVerifier()
    def create_pricing_module(self): return DiscountPricing()
    def create_inventory_policy(self): return OpenPolicy()

class EmergencyReliefKioskFactory(KioskFactory):
    def create_dispenser(self): return ConveyorDispenser("BulkConveyor-01")
    def create_verifier(self): return BiometricVerifier()
    def create_pricing_module(self): return DiscountPricing() # Emergency discount
    def create_inventory_policy(self): return OpenPolicy()

class ElectronicsKioskFactory(KioskFactory):
    def create_dispenser(self): return RoboticArmDispenser("GripArm-Tech")
    def create_verifier(self): return IDVerifier()
    def create_pricing_module(self): return PremiumPricing()
    def create_inventory_policy(self): return StrictPolicy()
