# kiosk_controller.py
# The main facade pattern to hide the heavy lifting from the user interface
# By: Moksh

from src.sys_config import SysConfig
from src.inventory_mgr import InventoryMgr
from src.hw_components import HwController
from src.pay_methods import PayGateway
from src.transactions import TxnRunner, BuyCmd
from src.support_alerts import TechSupportAlert
from src.pricing_strategies import StudentDiscount, NormalPricing

class KioskController:
    def __init__(self, kiosk_id, factory_obj):
        self.k_id = kiosk_id
        
        config = SysConfig()
        config.register_kiosk(self.k_id, factory_obj.get_kiosk_type())
        
        self.inv = InventoryMgr(self.k_id)
        
        # HW layer
        self.hw = HwController(factory_obj.create_dispenser())
        
        # Pattern: Observer (attaching support log to this kiosk)
        self.hw.add_observer(TechSupportAlert())
        
        self.pay = PayGateway()
        self.runner = TxnRunner(self.k_id)
        
    def buy_item(self, item_code, usr_ref, pay_mode, is_student=False):
        # Check hw health first
        hw_stats = self.hw.check_health()
        for k, v in hw_stats.items():
            if v == "FAILED":
                print(f"!!! Error: Hardware {k} failed. Halting purchase.")
                return False

        # check if item exists
        prod = self.inv.get_prod(item_code)
        if not prod:
            print("Item not found!")
            return False

        # Pattern: Strategy
        pricing = StudentDiscount() if is_student else NormalPricing()
        final_amt = pricing.calc_price(prod.get_total_price())
        
        # Execute via command pattern
        cmd = BuyCmd(self.inv, self.pay, self.hw, item_code, final_amt, usr_ref, pay_mode)
        
        print(f"\n--- Starting Transaction at [{self.k_id}] ---")
        return self.runner.run_cmd(cmd)

    def diag_check(self):
        # random func to trigger health checks
        self.hw.check_health()
