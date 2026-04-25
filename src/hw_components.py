# hw_components.py
# Models the physical kiosk parts and manages swapping
# - Durgesh

class BaseHardwareModule:
    def __init__(self, n):
        self.name = n
        self.health_status = "OK"  # could be FAILED if broken
        
    def fail_hardware(self):
        self.health_status = "FAILED"

class SpiralDispenser(BaseHardwareModule):
    def dispense_action(self, item_name):
        print(f"[HW] Turning spiral to drop {item_name}...")

class RoboticArmDispenser(BaseHardwareModule):
    def dispense_action(self, item_name):
        print(f"[HW] Arm safely grabbing and placing {item_name} into tray...")

class HwController:
    def __init__(self, default_disp):
        self.dispenser = default_disp
        self.addons = []
        self._observers = []
        
    # Pattern: Observer (Attach)
    def add_observer(self, obs):
        self._observers.append(obs)
        
    def _notify(self, msg):
        for o in self._observers:
            o.update_alert(msg)
            
    def set_dispenser(self, new_disp):
        self.dispenser = new_disp
        self._notify(f"Main dispenser changed to {new_disp.name}")
        
    def attach_addon(self, addon_obj):
        self.addons.append(addon_obj)
        self._notify(f"Module {addon_obj.name} plugged in")
        
    def check_health(self):
        stats = {self.dispenser.name: self.dispenser.health_status}
        for a in self.addons:
            stats[a.name] = a.health_status
            if a.health_status == "FAILED":
                self._notify(f"CRITICAL FAULT: {a.name} went offline!")
        return stats
        
    def drop_item(self, item_tag):
        # assume logic connects Dispenser to the item id
        self.dispenser.dispense_action(item_tag)
