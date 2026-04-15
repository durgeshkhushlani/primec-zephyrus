import os
from typing import Dict, Any
from src.persistence import save_json, load_json

"""
Central Registry Module for Aura Retail OS.
Implements the Singleton pattern to manage global configuration and kiosk registrations.
"""

class CentralRegistry:
    """Singleton registry for the entire retail infrastructure."""
    
    _instance = None
    _CONFIG_PATH = "data/config.json"

    def __new__(cls):
        """Enforces a single instance and initializes registry data."""
        if cls._instance is None:
            cls._instance = super(CentralRegistry, cls).__new__(cls)
            cls._instance.kiosks: Dict[str, Any] = {}
            
            # Load config or use defaults
            loaded_config = load_json(cls._CONFIG_PATH)
            cls._instance.config: Dict[str, Any] = loaded_config if loaded_config else {
                "system_name": "Aura Retail OS",
                "version": "2.0.0-PathB",
                "maintenance_mode": False,
                "default_currency": "INR"
            }
            
            cls._instance.system_status: Dict[str, Any] = {
                "is_active": True,
                "startup_time": "2026-04-14",
                "total_kiosks": 0
            }
            
            # Save initial config if it was empty
            if not loaded_config:
                save_json(cls._CONFIG_PATH, cls._instance.config)
                
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'CentralRegistry':
        """Static access method for the singleton instance."""
        return cls()

    def register_kiosk(self, kiosk_id: str, kiosk_obj: Any) -> None:
        """Adds a kiosk to the central registry."""
        self.kiosks[kiosk_id] = kiosk_obj
        self.system_status["total_kiosks"] = len(self.kiosks)
        print(f"[SYSTEM] Kiosk registered: {kiosk_id}")

    def get_kiosk(self, kiosk_id: str) -> Any:
        """Retrieves a kiosk by its unique identifier."""
        return self.kiosks.get(kiosk_id)

    def update_config(self, key: str, value: Any) -> None:
        """Updates a global configuration setting and persists to disk."""
        self.config[key] = value
        save_json(self._CONFIG_PATH, self.config)
        print(f"[SYSTEM] Config updated - {key}: {value}")

    def get_status(self) -> Dict[str, Any]:
        """Returns the current system status dictionary."""
        return self.system_status
