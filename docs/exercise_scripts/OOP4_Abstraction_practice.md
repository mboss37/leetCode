# Abstraction — Payment Processor · Practice Script

> **Pillar 4 of 4.** Abstraction = expose **what** a thing does, hide **how** it does it. Callers depend on a contract (an interface), never on the messy internals.

---

## The principle

An abstraction defines a **contract**: "anything that is a `PaymentProcessor` can `pay(amount)`." The caller programs against that contract and stays blissfully ignorant of API keys, HTTP calls, retry logic — all the *how*.

In Python you express the contract with an **Abstract Base Class** (`ABC`) and `@abstractmethod`. An abstract method has no real body; it's a promise that every concrete subclass **must** implement. You can't instantiate a class that leaves any abstract method unimplemented — the mistake is caught at construction, not deep in production.

**Abstraction vs. encapsulation:** encapsulation hides *data* (Pillar 1); abstraction hides *implementation behind an interface*. Related, not the same.

---

## The exercise

> Define a `PaymentProcessor` contract with `pay(amount)`.
> Provide `CreditCardProcessor` and `PayPalProcessor` implementations.
> A checkout function should accept **any** processor and call `pay()` — with zero knowledge of how each one actually moves money.

---

## ❌ NOT RECOMMENDED — no contract, leaked internals

```python
class Checkout:
    def __init__(self, method):
        self.method = method

    def run(self, amount):
        if self.method == "card":
            print("connecting to card gateway...")   # how leaks into the caller
            print(f"charging card ${amount}")
        elif self.method == "paypal":
            print("redirecting to paypal oauth...")
            print(f"charging paypal ${amount}")
        # new payment method? crack open Checkout again.
```

`Checkout` knows the *how* of every payment method. It's coupled to all of them and must change whenever any of them changes.

---

## ✅ RECOMMENDED — abstract contract, hidden implementations

```python
from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Contract: anything that processes a payment honors pay()."""

    @abstractmethod
    def pay(self, amount: float) -> bool:
        """Charge `amount`. Return True on success. HOW is the subclass's secret."""
        ...


class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card_number: str):
        self._card = card_number          # hidden detail

    def pay(self, amount: float) -> bool:
        self._authorize()                 # private how
        print(f"Charged ${amount} to card ending {self._card[-4:]}")
        return True

    def _authorize(self) -> None:
        ...                               # gateway handshake, hidden


class PayPalProcessor(PaymentProcessor):
    def __init__(self, email: str):
        self._email = email

    def pay(self, amount: float) -> bool:
        print(f"Charged ${amount} via PayPal account {self._email}")
        return True
```

The caller depends only on the **contract**:

```python
def checkout(processor: PaymentProcessor, amount: float) -> None:
    if processor.pay(amount):
        print("Order confirmed.")
    else:
        print("Payment failed.")


checkout(CreditCardProcessor("4111111111111111"), 49.99)
checkout(PayPalProcessor("ada@example.com"), 49.99)
```

`checkout` works with any current or future processor. Add `ApplePayProcessor(PaymentProcessor)` and `checkout` doesn't change a line.

```python
PaymentProcessor()        # TypeError: Can't instantiate abstract class
                          # — the contract is enforced
```

---

## Why an ABC and not "just a base class"?

A plain base class with a `pay` that does nothing would let a broken subclass (one that forgot `pay`) slip through and fail at runtime. `@abstractmethod` makes Python **refuse to construct** an incomplete implementation — the error arrives early and points at the real cause.

---

## Key points

- **Abstraction = depend on the interface, not the implementation.** Callers know *what*, never *how*.
- `ABC` + `@abstractmethod` define and **enforce** the contract at construction time.
- It enables loose coupling: high-level code (`checkout`) doesn't drag in low-level details (gateways, OAuth).
- This is the **D** in SOLID — *Dependency Inversion*: depend on abstractions, not concretions.

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Plain base class instead of ABC | Incomplete subclass instantiates, fails later | Use `ABC` + `@abstractmethod` |
| Leaking implementation in the interface | Callers couple to the *how* | Keep abstract methods about *what*, hide *how* in `_private` methods |
| Over-abstracting (one impl, ten layers) | Indirection with no payoff | Abstract when you have ≥2 implementations or a real seam |
| Abstract method with a real body people rely on | Subclasses skip overriding it | Keep it `...`/`raise NotImplementedError` or document it's optional |

---

## Interview out-loud

> "I'll define a `PaymentProcessor` abstract base class with one abstract method, `pay`. Each concrete processor — credit card, PayPal — implements `pay` and keeps its gateway details private. The checkout function takes a `PaymentProcessor` and just calls `pay`; it has no idea how the money actually moves. That's abstraction: the caller depends on the contract, not the implementation, so I can add new payment methods without touching checkout. It's also dependency inversion — high-level code depends on the abstraction, not the concrete classes."

---

**Pillar position:** Abstraction defines the contracts; polymorphism (Pillar 3) is many classes honoring one contract; encapsulation (Pillar 1) hides the data behind it; inheritance (Pillar 2) is one way to share the contract. The four pillars work as a set.
