# support_alerts.py
# Observer Pattern to log hardware events
# Made by Durgesh

import os

class SupportObserver:
    def update_alert(self, message):
        pass

class TechSupportAlert(SupportObserver):
    def __init__(self):
        self.log_file = "data/tech_support_logs.txt"
        
    def update_alert(self, message):
        # act like an alert sending to technician dashboards
        print(f"\n[ALERT NOTIFICATION] --> Sending to Tech Support: {message}")
        
        # log it organically
        if not os.path.exists("data"):
            os.makedirs("data")
            
        with open(self.log_file, "a") as f:
            f.write(message + "\n")
