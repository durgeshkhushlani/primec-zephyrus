# primec-zephyrus


Kiosk management system for a smart city setup. Built as part of a group assignment. Uses design patterns like singleton, abstract factory, adapter, composite and facade.

## how to run

On your machine Python 3.7+ is installed. No external dependencies needed.

```
python simulation.py
```

## What's implemented

| Pattern | File |
|---|---|
| Singleton | src/central_registry.py |
| Abstract Factory | src/kiosk_factory.py |
| Adapter | src/payment_gateway.py |

Composite and Facade are partially scaffolded in i_product.py and kiosk_interface.py — will be completed in final submission.

## folder structure

```
src/
  central_registry.py
  kiosk_factory.py
  payment_gateway.py
  i_product.py
  kiosk_interface.py
  __init__.py
diagrams/
  architecture.xml
  class-diagram.xml
simulation.py
README.md
```

## group

Prime Coders — Durgesh, Priyanshu, Jay, Moksh
