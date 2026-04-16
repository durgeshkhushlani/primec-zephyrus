import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.persistence import save_json

"""
Command Pattern Implementation for Aura Retail OS.
Handles transactional operations with undo support and persistence.
"""

class Command(ABC):
    """Abstract base class for all kiosk commands."""
    
    @abstractmethod
    def execute(self) -> bool:
        """Executes the command logic."""
        pass

    @abstractmethod
    def undo(self) -> bool:
        """Reverses the command effects."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Returns a serializable representation of the command."""
        pass


class PurchaseItemCommand(Command):
    """Encapsulates a product purchase transaction."""
    
    def __init__(self, kiosk, product_id: str, user_id: str, payment_method: str):
        self.kiosk = kiosk
        self.product_id = product_id
        self.user_id = user_id
        self.payment_method = payment_method
        self.timestamp = None
        self.price_paid = 0.0
        self.result = "PENDING"

    def execute(self) -> bool:
        self.timestamp = datetime.datetime.now().isoformat()
        
        # a) Reserve inventory
        if not self.kiosk.inventory.reserve(self.product_id):
            self.result = "FAILED: OUT_OF_STOCK"
            return False

        product = self.kiosk.inventory.get_product(self.product_id)
        self.price_paid = product.get_price()

        # b) Process payment
        try:
            adapter = self.kiosk.payment_gateway.get_adapter(self.payment_method)
            if not adapter.process(self.price_paid, self.user_id):
                raise RuntimeError("Payment provider declined transaction")

            # Check hardware health before final deduction
            health = self.kiosk.hardware.get_health()
            if any(status == "FAILED" for status in health.values()):
                raise RuntimeError("Hardware failure detected during procurement")

            # d) Deduct inventory and log success
            if not self.kiosk.inventory.deduct(self.product_id, hardware_ready=True):
                raise RuntimeError("Final inventory deduction failed")

            self.result = "SUCCESS"
            print(f"[PURCHASE] Successfully processed {self.product_id} for {self.user_id}")
            return True

        except Exception as e:
            # c) If payment/hardware fails -> release reservation, raise/log error
            print(f"[PURCHASE] Atomic Failure: {e}")
            self.kiosk.inventory.release(self.product_id)
            self.result = f"FAILED: {str(e)}"
            return False

    def undo(self) -> bool:
        """Refunds payment and restores inventory."""
        if self.result == "SUCCESS":
            print(f"[UNDO] Reversing purchase of {self.product_id}")
            # a) Refund payment
            adapter = self.kiosk.payment_gateway.get_adapter(self.payment_method)
            # Simulating refund by processing negative or just logging
            print(f"[PAYMENT] Refunded {self.price_paid} to {self.user_id} via {self.payment_method}")
            
            # b) Restore inventory
            self.kiosk.inventory.restock(self.product_id, 1)
            self.result = "UNDONE"
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "type": "PURCHASE",
            "kiosk_id": self.kiosk.kiosk_id,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "amount": self.price_paid,
            "status": self.result
        }


class RefundCommand(Command):
    """Encapsulates a manual refund operaton."""
    def __init__(self, kiosk, transaction_id: str):
        self.kiosk = kiosk
        self.transaction_id = transaction_id
        self.timestamp = datetime.datetime.now().isoformat()

    def execute(self) -> bool:
        print(f"[REFUND] Processing manual refund for Transaction ID: {self.transaction_id}")
        return True

    def undo(self) -> bool:
        print("[REFUND] Refund cannot be undone.")
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "type": "REFUND",
            "txn_id": self.transaction_id
        }


class RestockCommand(Command):
    """Encapsulates an inventory replenishment operation."""
    def __init__(self, kiosk, product_id: str, quantity: int):
        self.kiosk = kiosk
        self.product_id = product_id
        self.quantity = quantity
        self.timestamp = datetime.datetime.now().isoformat()

    def execute(self) -> bool:
        self.kiosk.inventory.restock(self.product_id, self.quantity)
        return True

    def undo(self) -> bool:
        # Reverse restock by deducting
        self.kiosk.inventory.deduct(self.product_id, self.quantity)
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "type": "RESTOCK",
            "product_id": self.product_id,
            "qty": self.quantity
        }


class CommandInvoker:
    """The invoker that manages history and triggers persistence after every call."""
    
    def __init__(self, history_file: str = "data/transactions.json"):
        self.history_file = history_file
        self.history: List[Command] = []

    def execute_command(self, command: Command) -> bool:
        """Executes a command, adds to history if successful, and persists."""
        result = command.execute()
        self.history.append(command)
        self._persist()
        return result

    def undo_last(self) -> bool:
        """Reverses the last successful command in history."""
        if not self.history:
            print("[SYSTEM] No commands to undo.")
            return False
        
        command = self.history.pop()
        success = command.undo()
        self._persist()
        return success

    def _persist(self) -> None:
        """Saves entire history to transactions.json."""
        data = [cmd.to_dict() for cmd in self.history]
        save_json(self.history_file, data)

    def get_history(self) -> List[Dict[str, Any]]:
        """Returns the list of processed commands."""
        return [cmd.to_dict() for cmd in self.history]
