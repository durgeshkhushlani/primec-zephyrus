# Aura Retail OS

**Autonomous Modular Smart-City Retail Infrastructure**  
Build as part of the IT620 Object-Oriented Programming Course.

## Project Details
- **Group Name**: Prime Coders (Group 21)
- **Members**: Kurin, Durgesh, Priyanshu, Jay, Moksh
- **Project Path**: Path B (Modular Hardware Platform)

## Overview
Aura Retail OS is a robust kiosk management system designed for diverse urban environments, including hospitals, metro stations, university campuses, and disaster zones. It features a highly modular hardware abstraction layer and an atomic transaction system built on modern design patterns.

## Design Patterns

| Pattern | File | Purpose |
| :--- | :--- | :--- |
| **Singleton** | `central_registry.py` | Manages global config, system status, and kiosk registration. |
| **Abstract Factory** | `kiosk_factory.py` | Creates families of compatible components (Dispensers, Verifiers, etc.). |
| **Adapter** | `payment_gateway.py` | Unifies disparate third-party payment APIs under a common interface. |
| **Command** | `commands.py` | Encapsulates transactions as objects with undo support and persistence. |
| **Facade** | `kiosk_interface.py` | Simplifies complex subsystem interactions for high-level operations. |
| **Composite** | `i_product.py` | Models complex product bundles containing single items or other bundles. |

## Folder Structure
```text
primec-zephyrus/
├── src/
│   ├── central_registry.py   # Singleton Pattern
│   ├── i_product.py          # Composite Pattern & Product Models
│   ├── kiosk_factory.py      # Abstract Factory Pattern
│   ├── kiosk_interface.py    # Facade Pattern
│   ├── payment_gateway.py    # Adapter Pattern
│   ├── hardware.py           # Hardware Abstraction Layer
│   ├── inventory.py          # Inventory System with Persistence
│   ├── commands.py           # Command Pattern & Invoker
│   └── persistence.py        # File I/O (JSON/CSV)
├── data/                     # Auto-generated Persistence Store
│   ├── inventory_*.json
│   ├── transactions_*.json
│   └── config.json
├── diagrams/
│   ├── architecture.xml      # System Architecture
│   └── class-diagram.xml     # UML Class Diagram
├── simulation.py             # Main Simulation Runner (4 Scenarios)
└── README.md                 # Project Documentation
```

## How to Run
Ensure you have Python 3.7+ installed. Run the simulation using:
```bash
python simulation.py
```

## System Constraints Enforced
1. **Atomic Transactions**: Purchase involves inventory reservation, payment processing, and final deduction with rollback on failure.
2. **Hardware Health**: Operations are blocked if critical hardware components status is "FAILED".
3. **Recursive Bundles**: Bundle pricing and stock calculations traverse nested children automatically.
4. **Data Persistence**: All system states (inventory, transactions, config) are persisted to JSON after every state-changing operation.
