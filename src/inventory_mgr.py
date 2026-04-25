# inventory_mgr.py
# Inventory logic, reserving items and parsing JSON
# Priyanshu

import json
import os

class InventoryMgr:
    def __init__(self, kiosk_tag):
        self.tag = kiosk_tag
        self.stock_list = {}
        self.reserved = []     # holds temporarily reserved items during txn
        
        # we will save state here
        self.file_path = f"data/inv_{self.tag}.json"
        
    def add_prod(self, p_obj):
        self.stock_list[p_obj.code] = p_obj
        
    def get_prod(self, p_code):
        return self.stock_list.get(p_code)
        
    def reserve_item(self, p_code):
        # mark item as in progress
        p = self.get_prod(p_code)
        if p and p.has_stock():
            self.reserved.append(p_code)
            
            # just reduce locally if single item for now
            if hasattr(p, 'stock'):
                p.stock -= 1
            return True
        return False
        
    def undo_reserve(self, p_code):
        # rollback if txn failed!
        if p_code in self.reserved:
            self.reserved.remove(p_code)
            p = self.get_prod(p_code)
            if hasattr(p, 'stock'):
                p.stock += 1
                
    def confirm_sale(self, p_code):
        # fully finalize because payment succeeded
        if p_code in self.reserved:
            self.reserved.remove(p_code)
            self._save_to_json()
            return True
        return False
        
    def _save_to_json(self):
        dict_data = {}
        for k, v in self.stock_list.items():
            if hasattr(v, 'stock'):
                dict_data[k] = {"name": v.name, "left": v.stock}
            else:
                dict_data[k] = {"name": v.name, "type": "combo_pack"}
                
        # ensure dir created
        if not os.path.exists("data"):
            os.makedirs("data")
            
        with open(self.file_path, "w") as f:
            json.dump(dict_data, f, indent=4)
