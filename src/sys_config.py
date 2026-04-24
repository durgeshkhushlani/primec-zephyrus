# sys_config.py
# Using the singleton pattern here so we don't have multiple configs floating around.
# Built by Moksh

class SysConfig:
    _instance = None

    def __new__(cls):
        # standard singleton pattern implementation
        if cls._instance is None:
            cls._instance = super(SysConfig, cls).__new__(cls)
            cls._instance._init_config()
        return cls._instance

    def _init_config(self):
        # some dummy configs for the kiosks
        self.kiosk_list = {}
        self.global_status = "ONLINE"
        # print("debug: sys config initialized.")
        
    def register_kiosk(self, kiosk_id, kiosk_type):
        self.kiosk_list[kiosk_id] = kiosk_type
        print(f"[SysLog] Registered Kiosk {kiosk_id} of type {kiosk_type}")
