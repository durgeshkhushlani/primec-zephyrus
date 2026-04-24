from abc import ABC, abstractmethod
from typing import Dict

"""
Payment Gateway Module for Aura Retail OS.
Implements the Adapter pattern to unify disparate third-party payment APIs.
"""

class PaymentProcessor(ABC):
    """The central interface (Target) that the system expects."""
    
    @abstractmethod
    def process(self, amount: float, user_id: str) -> bool:
        """Standard method to process a payment."""
        pass


# --- Adaptees (Simulated Third Party APIs with different signatures) ---

class CreditCardAPI:
    """External API for credit cards."""
    def charge_card(self, user: str, amt: float, provider: str = "VISA") -> bool:
        print(f"[EXTERNAL-API] CreditCard: Charging {amt} to user {user} via {provider}")
        return True


class WalletAPI:
    """External API for digital wallets."""
    def debit_balance(self, wallet_id: str, amount: float) -> bool:
        print(f"[EXTERNAL-API] Wallet: Debiting {amount} from account {wallet_id}")
        return True


class UPIAPI:
    """External API for Unified Payments Interface."""
    def perform_transfer(self, vpa: str, amount_in_inr: float) -> bool:
        print(f"[EXTERNAL-API] UPI: Initiating transfer of {amount_in_inr} to {vpa}")
        return True


# --- Adapters (Concrete implementations of PaymentProcessor) ---

class CreditCardAdapter(PaymentProcessor):
    """Adapts CreditCardAPI to PaymentProcessor interface."""
    def __init__(self):
        self.api = CreditCardAPI()

    def process(self, amount: float, user_id: str) -> bool:
        return self.api.charge_card(user=user_id, amt=amount)


class WalletAdapter(PaymentProcessor):
    """Adapts WalletAPI to PaymentProcessor interface."""
    def __init__(self):
        self.api = WalletAPI()

    def process(self, amount: float, user_id: str) -> bool:
        return self.api.debit_balance(wallet_id=f"W-{user_id}", amount=amount)


class UPIAdapter(PaymentProcessor):
    """Adapts UPIAPI to PaymentProcessor interface."""
    def __init__(self):
        self.api = UPIAPI()

    def process(self, amount: float, user_id: str) -> bool:
        return self.api.perform_transfer(vpa=f"{user_id}@aurapay", amount_in_inr=amount)


class PaymentGateway:
    """The gateway that manages and selects the appropriate adapter."""
    
    def __init__(self):
        self._adapters: Dict[str, PaymentProcessor] = {
            "credit_card": CreditCardAdapter(),
            "wallet": WalletAdapter(),
            "upi": UPIAdapter()
        }

    def register_adapter(self, name: str, adapter: PaymentProcessor) -> None:
        """Allows runtime extension of payment methods (Open/Closed Principle)."""
        self._adapters[name] = adapter
        print(f"[PAYMENT] Registered new payment provider: {name}")

    def get_adapter(self, method: str) -> PaymentProcessor:
        """Retrieves an adapter by method name."""
        if method not in self._adapters:
            raise ValueError(f"Unsupported payment method: {method}")
        return self._adapters[method]
