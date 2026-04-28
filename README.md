# Group 21: Aura Retail OS

**Autonomous Modular Smart-City Retail Infrastructure**  
Build as part of the IT620 Object-Oriented Programming Course.

## Project Details
- **Group Name**: Prime Coders (Group 21)
- **Members**: Durgesh (Kurin), Priyanshu, Jay, Moksh
- **Project Path**: Path B (Modular Hardware Platform)

## What is this?
Aura Retail OS is our custom kiosk management software for smart cities. It handles inventory drops, multiple payment API methods, and hardware hot-swapping for things like Pharmacy Kiosks, Campus Snack dispensers, and more. 

We made sure it handles edge cases like hardware failing mid-purchase (using atomic transactions) so users don't lose money.

## 8 Design Patterns Implemented

1. **Singleton** (`sys_config.py`): We only want one master configuration loaded in memory.
2. **Abstract Factory** (`setup_factory.py`): Gives you the correct set of parts depending on if you're building a Food Kiosk vs Pharmacy.
3. **Adapter** (`pay_methods.py`): Masks different payment gateways (UPI, CC, Crypto) behind one uniform wrapper.
4. **Command** (`transactions.py`): Encapsulates every buy action as an object so it can be rolled back if something crashes.
5. **Facade** (`kiosk_controller.py`): Hides all the messy stuff. Just call `buy_item()` and it coordinates the HW, payment, and stock.
6. **Composite** (`catalog_models.py`): Handles complex bundles (like a Student Kit) vs single items gracefully.
7. **Observer** (`support_alerts.py`): Instantly updates a simulated Tech Support log if any physical hardware drops offline.
8. **Strategy** (`pricing_strategies.py`): Adjusts checkout pricing dynamically (like taking off taxes for students).

## Code Structure

```text
primec-zephyrus/
├── src/
│   ├── sys_config.py          # Singleton Pattern
│   ├── catalog_models.py      # Composite Pattern
│   ├── setup_factory.py       # Abstract Factory Pattern
│   ├── kiosk_controller.py    # Facade Pattern
│   ├── pay_methods.py         # Adapter Pattern
│   ├── hw_components.py       # Hardware base components
│   ├── inventory_mgr.py       # Stock state and JSON persistence
│   ├── transactions.py        # Command Pattern
│   ├── support_alerts.py      # Observer Pattern
│   └── pricing_strategies.py  # Strategy Pattern
├── data/                      # Auto-saving JSON storage goes here
├── diagrams/                  # UML (Already Submitted)
├── main_runner.py             # The main script to demo the scenarios
└── README.md                  # This file!
```

## How to test it
Just run the main python file from your terminal:
```bash
python main_runner.py
```
*(Make sure you execute it from the root folder so the `data/` directory builds properly).*
