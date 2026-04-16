from abc import ABC, abstractmethod
from typing import Dict, List

"""
Hardware Abstraction Layer for Aura Retail OS.
Handles different dispenser types and modular hardware components (Optional Modules).
"""

class Dispenser(ABC):
    """Abstract base for all product delivery mechanisms."""
    def __init__(self, name: str):
        self.name = name
        self.health_status = "OPERATIONAL"

    @abstractmethod
    def dispense(self, product_id: str) -> bool:
        """Executes the physical product dispensation."""
        pass


class SpiralDispenser(Dispenser):
    """Classic vending machine spiral mechanism."""
    def dispense(self, product_id: str) -> bool:
        print(f"[HARDWARE] SpiralDispenser '{self.name}' rotating to release {product_id}")
        return True


class RoboticArmDispenser(Dispenser):
    """High-precision robotic arm for fragile items (e.g., Pharmacy)."""
    def dispense(self, product_id: str) -> bool:
        print(f"[HARDWARE] RoboticArmDispenser '{self.name}' picking product {product_id}")
        return True


class ConveyorDispenser(Dispenser):
    """Conveyor belt system for large or bulky items."""
    def dispense(self, product_id: str) -> bool:
        print(f"[HARDWARE] ConveyorDispenser '{self.name}' moving product {product_id} to drop zone")
        return True


class OptionalModule(ABC):
    """Base class for modular hardware expansions."""
    def __init__(self, name: str):
        self.name = name
        self.active = False

    @abstractmethod
    def attach(self) -> None:
        """Physical/software attachment of the module."""
        pass

    @abstractmethod
    def detach(self) -> None:
        """Safe detachment of the module."""
        pass

    @abstractmethod
    def status(self) -> str:
        """Returns the current operational status of the module."""
        pass


class RefrigerationModule(OptionalModule):
    """Module for temperature-controlled storage."""
    def attach(self) -> None:
        self.active = True
        print(f"[HARDWARE] RefrigerationModule '{self.name}' cooling system activated.")

    def detach(self) -> None:
        self.active = False
        print(f"[HARDWARE] RefrigerationModule '{self.name}' cooling system deactivated.")

    def status(self) -> str:
        return "COLD-STABLE" if self.active else "AMBIENT"


class SolarMonitorModule(OptionalModule):
    """Energy management module for remote/off-grid deployment."""
    def attach(self) -> None:
        self.active = True
        print(f"[HARDWARE] SolarMonitorModule '{self.name}' tracking battery health and sun exposure.")

    def detach(self) -> None:
        self.active = False
        print(f"[HARDWARE] SolarMonitorModule '{self.name}' monitoring disabled.")

    def status(self) -> str:
        return "CHARGING" if self.active else "UNKNOWN"


class NetworkModule(OptionalModule):
    """Redundant connectivity module (5G/Satellite)."""
    def attach(self) -> None:
        self.active = True
        print(f"[HARDWARE] NetworkModule '{self.name}' link established via 5G.")

    def detach(self) -> None:
        self.active = False
        print(f"[HARDWARE] NetworkModule '{self.name}' link severed.")

    def status(self) -> str:
        return "CONNECTED" if self.active else "DISCONNECTED"


class HardwareManager:
    """Manages the active dispenser and attached optional modules for a kiosk."""
    
    def __init__(self, dispenser: Dispenser):
        self.active_dispenser = dispenser
        self.modules: Dict[str, OptionalModule] = {}

    def replace_dispenser(self, new_dispenser: Dispenser) -> None:
        """Swaps the primary dispenser at runtime."""
        print(f"[HARDWARE] Swapping {type(self.active_dispenser).__name__} with {type(new_dispenser).__name__}")
        self.active_dispenser = new_dispenser

    def add_module(self, module: OptionalModule) -> None:
        """Attaches and activates a new optional hardware module."""
        module.attach()
        self.modules[module.name] = module

    def remove_module(self, name: str) -> None:
        """Safely detaches an existing module."""
        if name in self.modules:
            self.modules[name].detach()
            del self.modules[name]

    def get_health(self) -> Dict[str, str]:
        """Returns a consolidated health report for all active hardware components."""
        report = {
            "DISPENSER": self.active_dispenser.health_status,
            "TYPE": type(self.active_dispenser).__name__
        }
        for name, mod in self.modules.items():
            report[name] = mod.status()
        return report
