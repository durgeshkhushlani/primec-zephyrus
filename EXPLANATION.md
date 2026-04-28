# Aura Retail OS - Project Deep Dive 

This document explains our code and who built what for the **Aura Retail OS** final submission.

## 1. Simple Overview
We built software for autonomous vending kiosks. It handles stock, takes payments, and manages hardware (like robotic arms or spirals). The system is robust—if power fails during a payment, the stock is rolled back (Atomicity).

---

## 2. Team Member Contributions

### 🏗️ Core System & Configuration (By: Moksh)
Moksh laid down the foundation to ensure everything starts correctly.
- **Singleton (`sys_config.py`)**: The `SysConfig` ensures only one instance is active.
- **Abstract Factory (`setup_factory.py`)**: Built the `BaseKioskFactory` so a Pharmacy gives you a robotic arm and a Snack kiosk gives you a spiral naturally.
- **Facade (`kiosk_controller.py`)**: Wrote the `KioskController` class. A single `buy_item()` call coordinates hardware, money, and inventory so the runner script doesn't get complicated.

### 📦 Inventory System & Product Models (By: Priyanshu)
Priyanshu handled product data and persistence.
- **Composite Pattern (`catalog_models.py`)**: Created `SingleItem` and `ComboOffer`. Calling `.get_total_price()` on a combo automatically loops through all sub-items to fetch their cost.
- **Inventory Management (`inventory_mgr.py`)**: Handles the "hold/reserve" logic before a payment finishes, and writes everything to JSONs.

### 💳 Payment System & Transactions (By: Jay)
Jay handled the money logic and safety.
- **Adapter Pattern (`pay_methods.py`)**: Used adapters so `UpiAdapter` and `CardAdapter` look identical to the system but talk to different fake APIs underneath.
- **Command Pattern (`transactions.py`)**: The `BuyCmd` isolates the purchase logic. It reserves, attempts pay, and if anything drops, it safely rolls back stock so nothing is lost.

### 🦾 Hardware & Integration (By: Durgesh / Kurin)
Durgesh handled the physical layer and the "cool" extra features.
- **Hardware Abstraction (`hw_components.py`)**: Base classes ensuring hot-swapping dispensers doesn't break the codebase.
- **Observer Pattern (`support_alerts.py`)**: Hooked into the hardware so a `TechSupportAlert` fires mechanically whenever part status goes to FAILED.
- **Strategy Pattern (`pricing_strategies.py`)**: Plug-in logic for normal shoppers vs students (so taxes/discounts apply recursively).
- **Simulation (`main_runner.py`)**: Tied everyone's classes together in a terminal test run.

---

## 3. Preparation for Teacher Q&A

### Q1: Why use an Abstract Factory here? 
**Answer:** It completely stops devs from putting a basic snack spiral into a pharmacy kiosk. It forces the system to boot up with a compatible "family" of parts automatically.

### Q2: What is Atomicity and how did you do it? 
**Answer:** Atomicity means "all or nothing". In `transactions.py` (Command), we do a 3-step check. Reserve -> Pay -> Dispense. If Pay drops, we rollback the reserve. This prevents "ghost items".

### Q3: Why add the Strategy Pattern?
**Answer:** We wanted pricing logic decoupled from items. A Student Discount vs Standard Tax changes dynamically, it shouldn't be hardcoded into the items themselves.

### Q4: How the Adapter pattern solves "Interface Mismatch"? 
**Answer:** External APIs like Crypto or UPI use totally different parameter orders. Our internal system just calls `execute_payment(amt, usr)`. The Adapter translates this inside to fit the clunky external API.
