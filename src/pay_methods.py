# pay_methods.py
# Uses Adapter pattern to connect to imaginary APIs
# Jay

class DummyUpiAPI:
    def transfer_upi(self, vpa_id, amt_inr):
        print(f"[UPI API] Checking upi for {vpa_id}... Transferred {amt_inr} Rs.")
        return True

class DummyCardAPI:
    def charge_card(self, cc_num, amount):
        print(f"[Card API] Swiping CC {cc_num}... Approved {amount}.")
        return True

# Our main interface that system uses
class PayAdapter:
    def execute_payment(self, amount, user_tag) -> bool:
        pass

class UpiAdapter(PayAdapter):
    def __init__(self):
        self.api = DummyUpiAPI()
    def execute_payment(self, amount, user_tag):
        # convert our standard call to what upi api wants
        return self.api.transfer_upi(f"{user_tag}@okbank", amount)

class CardAdapter(PayAdapter):
    def __init__(self):
        self.api = DummyCardAPI()
    def execute_payment(self, amount, user_tag):
        # convert our standard call to cc api
        return self.api.charge_card(f"4111-XXXX-XXXX-{user_tag}", amount)

class PayGateway:
    def __init__(self):
        self.methods = {
            "upi": UpiAdapter(),
            "credit_card": CardAdapter()
        }
        
    def add_custom_method(self, name, adapter_obj):
        # good for extensibility later
        self.methods[name] = adapter_obj
        
    def do_transaction(self, mode, amt, usr):
        provider = self.methods.get(mode)
        if not provider:
            print("Payment mode not supported.")
            return False
            
        return provider.execute_payment(amt, usr)
