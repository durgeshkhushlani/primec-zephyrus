# primec-zephyrus


Kiosk management system for a smart city setup. Built as part of a group assignment. Uses design patterns like singleton, abstract factory, adapter, composite and facade.

## how to run

On your machine Python 3.7+ is installed. No external dependencies needed.

```
python simulation.py
```

## patterns implemented

- Singleton — CentralRegistry
- Abstract Factory — KioskFactory
- Adapter — PaymentGateway
- Composite — IProduct / SingleProduct / ProductBundle
- Facade — KioskInterface

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
