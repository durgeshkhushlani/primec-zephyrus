# adapter pattern - different payment apis wrapped into one common interface

from abc import ABC, abstractmethod


class PaymentGateway(ABC):

    @abstractmethod
    def do_payment(self, amt): pass

    @abstractmethod
    def do_refund(self, txn_id): pass


# pretend third party apis below

class upi_api:
    def send(self, upi_id, rupees):
        return "upi sent rs." + str(rupees) + " to " + upi_id

    def reverse(self, ref_no):
        return "upi reversed ref:" + ref_no


class card_api:
    def charge(self, card_no, amt):
        return "card " + card_no + " charged rs." + str(amt)

    def give_refund(self, receipt):
        return "card refund for receipt " + receipt


class wallet_api:
    def deduct(self, w_id, amt):
        return "wallet " + w_id + " debited rs." + str(amt)

    def add_back(self, w_id, amt):
        return "wallet " + w_id + " credited rs." + str(amt)


# actual adapters

class UpiAdapter(PaymentGateway):
    def __init__(self):
        self.api = upi_api()

    def do_payment(self, amt):
        res = self.api.send("aura@upi", amt)
        print(res)

    def do_refund(self, txn_id):
        res = self.api.reverse(txn_id)
        print(res)


class CardAdapter(PaymentGateway):
    def __init__(self):
        self.api = card_api()

    def do_payment(self, amt):
        res = self.api.charge("xxxx-1234", amt)
        print(res)

    def do_refund(self, txn_id):
        res = self.api.give_refund(txn_id)
        print(res)


class WalletAdapter(PaymentGateway):
    def __init__(self):
        self.api = wallet_api()

    def do_payment(self, amt):
        res = self.api.deduct("usr_wallet_01", amt)
        print(res)

    def do_refund(self, txn_id):
        res = self.api.add_back("usr_wallet_01", 0)
        print(res)
