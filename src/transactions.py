# transactions.py
# Command pattern to make sure purchases don't fail halfway out of nowhere
# by Jay

import json
import os
import datetime

class BuyCmd:
    def __init__(self, inv_ref, pay_ref, hw_ref, p_code, amt, usr, mode):
        self.inv = inv_ref
        self.pay = pay_ref
        self.hw = hw_ref
        self.code = p_code
        self.amt = amt
        self.usr = usr
        self.mode = mode
        
    def run(self):
        # Step 1: hold the item
        if not self.inv.reserve_item(self.code):
            print("Failed: Out of stock.")
            return False
            
        # Step 2: process money
        if not self.pay.do_transaction(self.mode, self.amt, self.usr):
            print("Payment failed! Rolling back.")
            self.inv.undo_reserve(self.code)
            return False
            
        # Step 3: physically dispense & confirm
        self.hw.drop_item(self.code)
        self.inv.confirm_sale(self.code)
        
        print(">> Transaction Success! <<")
        return True

class TxnRunner:
    def __init__(self, k_id):
        self.history = []
        self.tag = k_id
        
    def run_cmd(self, cmd_obj):
        res = cmd_obj.run()
        if res:
            # log to history only on success
            self.history.append({
                "time": str(datetime.datetime.now()),
                "item": cmd_obj.code,
                "paid": cmd_obj.amt
            })
            self._save_log()
        return res
        
    def _save_log(self):
        f_name = f"data/txns_{self.tag}.json"
        
        if not os.path.exists("data"):
            os.makedirs("data")
            
        with open(f_name, "w") as f:
            json.dump(self.history, f, indent=4)
