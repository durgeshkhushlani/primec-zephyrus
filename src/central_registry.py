# singleton - only one registry for whole system

class CentralRegistry:

    _inst = None

    def __init__(self):
        self.kiosk_list = []
        self.conf = {
            "max_buy_limit": 5,
            "mode": "NORMAL"
        }

    @classmethod
    def get_instance(cls):
        if cls._inst is None:
            cls._inst = CentralRegistry()
        return cls._inst

    def add_kiosk(self, k):
        self.kiosk_list.append(k)
        print("registered kiosk -> " + k.kiosk_id)

    def get_conf(self, key):
        return self.conf.get(key)

    def set_conf(self, key, val):
        self.conf[key] = val
        print("config changed: " + key + " = " + str(val))

    def get_all_kiosks(self):
        return self.kiosk_list
