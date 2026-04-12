# primec-zephyrus — Code Explanation
### Prime Coders | IT620

---

## What is this project?

This is a simulation of a **smart kiosk management system** called *Aura Retail OS*. Think of it like the software that runs self-service vending machines placed around a smart city — one for pharmacy items, one for food, and one for emergency supplies. The project demonstrates how real-world software is structured using **design patterns**.

---

## What are Design Patterns?

Design patterns are **proven, reusable solutions** to common problems in software design. Instead of figuring out a solution from scratch, you use a well-known blueprint. This project uses **five** patterns.

---

## Pattern 1 — Singleton (`central_registry.py`)

### What problem does it solve?
You need **exactly one** central registry for the whole system. If two parts of your code create two separate registries, they'd each have incomplete lists of kiosks — a disaster.

### How it works
The `CentralRegistry` class keeps a private class-level variable `_inst`. The first time `get_instance()` is called, it creates one object and saves it there. Every call after that returns the same saved object — no new one is ever made.

```python
@classmethod
def get_instance(cls):
    if cls._inst is None:
        cls._inst = CentralRegistry()   # created only once
    return cls._inst
```

### Python vs JavaScript
In JS, `CentralRegistry._inst = null` was set outside the class. In Python, `_inst = None` is declared inside the class body — cleaner and more Pythonic.

### Why we used it
There must be only one global registry. Like a country can only have one central government — not two running in parallel.

---

## Pattern 2 — Abstract Factory (`kiosk_factory.py`)

### What problem does it solve?
Each kiosk type (pharmacy, food, emergency) needs a **matching set** of parts: its own dispenser, payment module, and inventory policy. You don't want to accidentally mix a food dispenser with a pharmacy payment system.

### How it works
`KioskFactory` is an abstract base class that declares three methods: `make_dispenser()`, `make_payment()`, `make_inv_policy()`. Each concrete factory (`PharmacyKioskFactory`, `FoodKioskFactory`, `EmergencyKioskFactory`) overrides all three and returns the right combination of objects.

```python
class PharmacyKioskFactory(KioskFactory):
    def make_dispenser(self): return PharmacyDispenser()   # robotic arm
    def make_payment(self):   return PharmacyPayment()     # card only
    def make_inv_policy(self): return PharmacyPolicy()     # needs prescription
```

### Python vs JavaScript
In JS, the "products" (dispenser, payment, policy) were plain objects with functions attached — JavaScript's duck typing made that easy. In Python, we properly defined `Dispenser`, `PaymentModule`, and `InvPolicy` base classes and extended them. This is more structured and gives better IDE support and error checking.

We also used Python's `abc` module (`ABC`, `abstractmethod`) to enforce that subclasses must implement every method — something JS didn't enforce at all.

### Why we used it
You guarantee that all parts of a kiosk are compatible with each other. Adding a new kiosk type (say, `LibraryKioskFactory`) just means writing one new factory class — the rest of the code doesn't change.

---

## Pattern 3 — Adapter (`payment_gateway.py`)

### What problem does it solve?
Imagine you want to support three payment providers — UPI, Card, and Wallet. Each has its own API with completely different method names (`send`, `charge`, `deduct`). Your kiosk code shouldn't have to know or care which one it's talking to.

### How it works
`PaymentGateway` defines the interface your kiosk expects: `do_payment()` and `do_refund()`. Each adapter class wraps one third-party API and **translates** calls:

```
Kiosk calls  →  do_payment(150)
UpiAdapter   →  self.api.send("aura@upi", 150)
CardAdapter  →  self.api.charge("xxxx-1234", 150)
WalletAdapter → self.api.deduct("usr_wallet_01", 150)
```

The kiosk only ever calls `do_payment()` — it never knows which provider ran underneath.

### Python vs JavaScript
Both versions are nearly identical here. In Python we used `ABC` and `@abstractmethod` to make `PaymentGateway` a proper interface — in JS it just threw a plain `Error` if you forgot to implement a method.

### Why we used it
You can swap payment providers without touching any kiosk code. Want to add PayPal later? Write one new adapter class. Nothing else changes. This is the **Open/Closed Principle** in action.

---

## Pattern 4 — Composite (`i_product.py`)

### What problem does it solve?
Your inventory can have individual products (Paracetamol, Chips) or **bundles** (First Aid Kit = Paracetamol + Bandage). You want to treat both exactly the same way — check if they're in stock, get the price, display them — without caring which type you have.

### How it works
`IProduct` is the abstract base. `SingleProduct` is a **leaf** — one item with a name, price, and quantity. `ProductBundle` is a **composite** — it holds a list of other `IProduct`s (which can themselves be bundles). Both implement the same interface.

```python
kit = ProductBundle("First Aid Kit")
kit.add(SingleProduct("Paracetamol", 25, 10))
kit.add(SingleProduct("Bandage", 15, 5))

kit.get_price()   # returns 40  (25 + 15, calculated recursively)
kit.in_stock()    # True only if ALL items inside are in stock
```

### Python vs JavaScript
In JS, `IProduct` methods just threw errors if not overridden — no true enforcement. In Python, `ABC` + `@abstractmethod` means Python itself will refuse to instantiate a class that hasn't implemented all required methods. This is safer.

### Why we used it
You can build arbitrarily nested product groups (a bundle inside a bundle) and still call `show()`, `get_price()`, `in_stock()` uniformly. The inventory display code loops through items without caring whether each one is a single product or a bundle.

---

## Pattern 5 — Facade (`kiosk_interface.py`)

### What problem does it solve?
The simulation code (`simulation.py`) doesn't need to know about dispensers, payment modules, or inventory policies directly. It just needs to say: "buy this item", "show inventory", "restock". The Facade hides all the complexity.

### How it works
`KioskInterface` is the **single point of contact** for all kiosk operations. Internally it holds references to the dispenser, payment module, and policy — but from outside you never touch those. You just call:

```python
pharma.buy("Paracetamol", 25)
pharma.restock("Bandage", 10)
pharma.diagnostics()
```

The `buy()` method alone coordinates: look up item → check stock → verify policy → process payment → dispense → record transaction. Six steps, one call.

### Python vs JavaScript
The conversion here was almost line-for-line. The only real change was using `is` instead of `===` for identity checks, and `str()` to convert numbers for string concatenation (Python doesn't auto-coerce like JS does).

### Why we used it
Without a facade, `simulation.py` would be cluttered with calls to four or five different subsystems per purchase. With it, the simulation reads cleanly like plain English instructions.

---

## JavaScript → Python: Key Differences

| JavaScript | Python |
|---|---|
| `class X { }` + `require()` | `class X:` + `import` |
| No true abstract classes (just throws Error) | `ABC` + `@abstractmethod` enforces it |
| `===` (strict equality) | `is` for identity, `==` for value |
| `null` | `None` |
| `console.log()` | `print()` |
| `module.exports = { ... }` | No equivalent needed — `import` works on files |
| Auto string+number coercion (`"rs." + 25`) | Must convert: `"rs." + str(25)` |
| Objects as simple bags `{ dtype: "x", give: fn }` | Proper classes with `__init__` and methods |
| `this.x` | `self.x` |

---

## File Map

```
simulation.py          ← runs the whole demo (entry point)
src/
  central_registry.py  ← Singleton pattern
  kiosk_factory.py     ← Abstract Factory pattern
  payment_gateway.py   ← Adapter pattern
  i_product.py         ← Composite pattern
  kiosk_interface.py   ← Facade pattern
diagrams/
  architecture.xml     ← system architecture diagram
  class-diagram.xml    ← UML class diagram
```

---

## How to Run

```bash
python simulation.py
```

No pip installs needed. Standard Python 3.7+ only.

---

*Prime Coders — Durgesh, Priyanshu, Jay, Moksh | IT620*
