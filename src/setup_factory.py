# setup_factory.py
# Factory pattern to build the correct parts for different kiosk types
# Author: Moksh

from abc import ABC, abstractmethod
from src.hw_components import SpiralDispenser, RoboticArmDispenser

class BaseKioskFactory(ABC):
    @abstractmethod
    def create_dispenser(self):
        pass
        
    @abstractmethod
    def get_kiosk_type(self):
        pass

class PharmaFactory(BaseKioskFactory):
    def create_dispenser(self):
        return RoboticArmDispenser("Pharma-Arm-V1")
        
    def get_kiosk_type(self):
        return "PHARMACY"

class SnackFactory(BaseKioskFactory):
    def create_dispenser(self):
        # basic spiral for food
        return SpiralDispenser("Snack-Spiral-Unit")
        
    def get_kiosk_type(self):
        return "FOOD"

class ElectronicsFactory(BaseKioskFactory):
    def create_dispenser(self):
        return RoboticArmDispenser("Tech-Arm-Heavy")
        
    def get_kiosk_type(self):
        return "ELECTRONICS"

class EmergencyFactory(BaseKioskFactory):
    def create_dispenser(self):
        return SpiralDispenser("Relief-Disp-Fast")
        
    def get_kiosk_type(self):
        return "EMERGENCY_RELIEF"
