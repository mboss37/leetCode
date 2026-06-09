# Encapsulation — Bank Account · Practice Script

> **Pillar 1 of 4.** Encapsulation = bundle data + the methods that operate on it into one unit, and **control access** to the data so it can never enter an invalid state.

---

## The principle

A class should **hide its internal state** and expose a small, safe surface. Callers go through methods (or properties), never reach in and mutate raw fields. The class is the only thing that can change its own data — so it can enforce its own rules.

The signal: *"this value should never be negative / should only change in specific ways."* That rule belongs **inside** the class, not scattered across every caller.

In Python there is no `private` keyword. The convention is a leading underscore (`_balance`), and a double underscore (`__balance`) triggers name-mangling for stronger "don't touch this" intent.

---

## The exercise

> Build a `BankAccount` where:
> - balance can never go negative
> - you can't deposit or withdraw a non-positive amount
> - callers can **read** the balance but never assign it directly
> - every withdrawal that would overdraw is rejected

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Should invalid operations raise an exception or return False?"** — I'd raise `ValueError` so failures are loud; returning False makes them easy to ignore.
- **"Float or Decimal for money?"** — Floats have rounding errors; real money code uses `Decimal` or integer cents. Float is fine for the exercise if we agree.
- **"Is any overdraft allowed, even a small limit?"** — No: balance ≥ 0 is the invariant. A limit would just change one check in `withdraw`.
- **"Should callers be able to read the balance at all?"** — Yes, read it but never assign it — that's the read-only property with no setter.

---

## ❌ NOT RECOMMENDED — no encapsulation

```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance   # public, anyone can write it

acct = BankAccount(100)
acct.balance -= 500       # now -400. Nothing stopped it.
acct.balance = "oops"     # now a string. Class is corrupt.
```

The invariant "balance ≥ 0" lives nowhere. Every caller is trusted to do the right thing — and one of them won't.

---

## ✅ RECOMMENDED — controlled access with validation

```python
class BankAccount:
    def __init__(self, opening_balance: float = 0):
        if opening_balance < 0:
            raise ValueError("Opening balance cannot be negative")
        self._balance = opening_balance     # leading _ = "internal"

    @property
    def balance(self) -> float:
        """Read-only view of the balance."""
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
```

```python
acct = BankAccount(100)
acct.deposit(50)          # 150
acct.withdraw(200)        # ValueError: Insufficient funds
print(acct.balance)       # 150  (read OK)
acct.balance = 999        # AttributeError: can't set attribute
```

- The invariant lives in **one place** — the methods.
- `@property` exposes a **read-only** `balance`. No setter → assignment fails loudly.
- The object can never be observed in an invalid state.

---

## Why `@property` instead of `get_balance()`?

Both work. `@property` lets callers write `acct.balance` (clean, attribute-like) while you keep the freedom to compute or guard it. Adding a setter is opt-in:

```python
@balance.setter
def balance(self, value):
    raise AttributeError("Use deposit() / withdraw()")
```

---

## Key points

- **Encapsulation is about invariants, not secrecy.** The point isn't hiding for its own sake — it's that the class guarantees its own rules.
- Leading `_name` = "internal, don't rely on this." Double `__name` = name-mangled, stronger intent.
- Expose **behavior** (`deposit`, `withdraw`), not raw **state**.
- A getter with no setter = read-only field.

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Public mutable field | Any caller can break the invariant | Make it `_field`, expose via method/property |
| Validating in the caller | Rule duplicated everywhere, drifts out of sync | Validate **inside** the class |
| `@property` getter + careless setter | Setter re-opens the hole you closed | Omit the setter, or validate in it too |
| Returning a mutable internal (e.g. a list) | Caller mutates your internals through the reference | Return a copy: `return list(self._items)` |

---

## Interview out-loud

> "I'll make balance internal — `_balance` — so the only ways to change it are `deposit` and `withdraw`, and both validate their input. I expose a read-only `balance` property so callers can see it but not assign it. That way the class enforces its own invariant — balance is always ≥ 0 and always a number — instead of trusting every caller to behave."

---

## Likely Follow-ups

The interview is one question that grows in parts — expect the account to gain features.

- **"Add a transaction history."** → Keep an internal list of `(kind, amount)` tuples, append inside `deposit`/`withdraw`, and expose it as a copy so callers can't edit it.
- **"Add a SavingsAccount that earns interest."** → Subclass `BankAccount`, add `apply_interest()`, reuse the validated `deposit`. That's the Inheritance exercise (OOP2).
- **"Two threads deposit at once — what breaks?"** → `_balance += amount` isn't atomic; wrap deposit/withdraw bodies in a `threading.Lock`.
- **"Add a daily withdrawal limit."** → Track the amount withdrawn today inside the class; the new rule lives next to the old ones, in one place.

---

**Pillar position:** Encapsulation is the foundation — it's what makes the other three pillars safe. Inheritance, polymorphism, and abstraction all assume each class guards its own state.
