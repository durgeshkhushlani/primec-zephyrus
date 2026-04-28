# main_runner.py
# The main simulation that ties everything together.
# Put together by Durgesh

from src.setup_factory import PharmaFactory, ElectronicsFactory
from src.kiosk_controller import KioskController
from src.catalog_models import SingleItem, ComboOffer
from src.hw_components import BaseHardwareModule
from src.pay_methods import PayAdapter

import time

# Let's add a custom crypto adapter here to show extensibility like before
class CryptoCoinAPI:
    def pay_wallet(self, addr, val):
        print(f"[Crypto API] Sent {val} INR equiv to {addr} from blockchain wallet.")
        return True

class CryptoAdapter(PayAdapter):
    def __init__(self):
        self.coin_api = CryptoCoinAPI()
    def execute_payment(self, amount, user_tag):
        return self.coin_api.pay_wallet(f"0x{user_tag}", amount)

def start_sim():
    print("\n" + "="*50)
    print(" AURA RETAIL OS - FULL SYSTEM BOOTUP ")
    print("="*50)
    time.sleep(0.5)
    
    # 1. Start a pharmacy kiosk
    kiosk_1 = KioskController("MED-STATION-1", PharmaFactory())
    
    # populate items
    med = SingleItem("M1", "Paracetamol", 50.0, 100)
    kiosk_1.inv.add_prod(med)
    
    # normal buy
    kiosk_1.buy_item("M1", "User_Alpha", "credit_card")
    
    # 2. Hardware swap naturally triggering Observer pattern
    print("\n[Sim] Tech arrives and updates the HW Dispenser...")
    from src.hw_components import RoboticArmDispenser
    kiosk_1.hw.set_dispenser(RoboticArmDispenser("Pharma-Arm-V2_FAST"))
    kiosk_1.buy_item("M1", "User_Beta", "upi")
    
    # 3. Add a refrigeration module, let it fail, and see observer log it
    print("\n[Sim] Plugging in Fridge Module...")
    refrigerator = BaseHardwareModule("Cold-Storage-5L")
    kiosk_1.hw.attach_addon(refrigerator)
    
    print("\n[Sim] Power outage strikes!")
    refrigerator.fail_hardware()
    # next buy will trigger health check and fail
    kiosk_1.buy_item("M1", "User_Charlie", "upi")
    
    # 4. Strategy Pattern (Student Discount) & Composite (Combos)
    kiosk_2 = KioskController("TECH-LAB-X", ElectronicsFactory())
    
    laptop = SingleItem("L1", "Gaming Laptop", 80000.0, 5)
    mouse = SingleItem("L2", "Wireless Mouse", 1500.0, 10)
    
    # create combo
    back_to_school = ComboOffer("CB_1", "Back to School Kit")
    back_to_school.add_to_combo(laptop)
    back_to_school.add_to_combo(mouse)
    
    kiosk_2.inv.add_prod(laptop)
    kiosk_2.inv.add_prod(mouse)
    kiosk_2.inv.add_prod(back_to_school)
    
    print(f"\n[Sim] Durgesh buying combo with Student Strategy Pattern...")
    kiosk_2.buy_item("CB_1", "Durgesh", "upi", is_student=True)
    
    # 5. Crypto Adapter
    print(f"\n[Sim] Upgrading tech kiosk with custom Crypto processor...")
    kiosk_2.pay.add_custom_method("crypto", CryptoAdapter())
    kiosk_2.buy_item("L2", "Miner_Bob", "crypto")

    print("\n" + "="*50)
    print(" SYSTEM SIMULATION COMPLETED ")
    print("="*50)

if __name__ == "__main__":
    start_sim()
