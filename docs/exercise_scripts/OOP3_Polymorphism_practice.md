# Polymorphism — Shapes & Areas · Practice Script

> **Pillar 3 of 4.** Polymorphism = "many forms." Call the **same method** on different objects and each does the *right thing for its type* — without the caller knowing which type it has.

---

## The principle

Code against an **interface**, not a concrete type. If every shape has an `area()` method, you can total a mixed list of shapes with one loop — no `if isinstance(...)` ladder. New shape types plug in without touching that loop.

This is the payoff of inheritance: a `Circle`, `Rectangle`, and `Triangle` are all `Shape`s, so anywhere that expects a `Shape` accepts any of them and calls `area()` polymorphically.

Two flavors in Python:
- **Override-based** (subclasses override a base method)
- **Duck typing** (any object with an `area()` works — "if it quacks like a duck…"), no shared base required.

---

## The exercise

> Build shapes — `Circle`, `Rectangle`, `Triangle` — each with an `area()`.
> Then write **one** function that sums the area of any list of shapes, and **one** that returns the largest — neither knowing the concrete types.

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Should a negative radius or width raise an error?"** — Yes — validate in each `__init__` and raise `ValueError`, so a shape can't exist in a bad state.
- **"Must shapes share a base class, or is duck typing enough?"** — Both work in Python; the ABC documents the contract and catches missing `area()` at construction.
- **"What should `largest` do on an empty list — raise or return None?"** — Agree up front; bare `max()` raises `ValueError`.
- **"If two shapes tie for largest, which one wins?"** — `max` returns the first; confirm that's acceptable.

---

## ❌ NOT RECOMMENDED — type-checking ladder

```python
def total_area(shapes):
    total = 0
    for s in shapes:
        if s["kind"] == "circle":
            total += 3.14159 * s["r"] ** 2
        elif s["kind"] == "rectangle":
            total += s["w"] * s["h"]
        elif s["kind"] == "triangle":
            total += 0.5 * s["base"] * s["height"]
        # add a new shape? edit this function. and every other one like it.
    return total
```

Every new shape forces edits to every function that walks shapes. The behavior is scattered outside the things it describes.

---

## ✅ RECOMMENDED — one interface, many forms

```python
import math
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        ...


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    def area(self) -> float:
        return math.pi * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    def area(self) -> float:
        return self.width * self.height


class Triangle(Shape):
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height
    def area(self) -> float:
        return 0.5 * self.base * self.height
```

Now the callers don't care what's in the list:

```python
def total_area(shapes: list[Shape]) -> float:
    return sum(s.area() for s in shapes)        # polymorphic call

def largest(shapes: list[Shape]) -> Shape:
    return max(shapes, key=lambda s: s.area())  # polymorphic call


shapes = [Circle(2), Rectangle(3, 4), Triangle(6, 8)]
print(round(total_area(shapes), 2))   # 50.57
print(largest(shapes))                # the Rectangle
```

Add a `Pentagon(Shape)` with its own `area()` — `total_area` and `largest` keep working, **untouched**. That's the win.

---

## Duck typing — polymorphism without a base class

Python doesn't *require* the shared base. Any object with `area()` works:

```python
class Blob:                 # not a Shape subclass at all
    def area(self): return 42

total_area([Circle(1), Blob()])   # works — both have .area()
```

The base class (`Shape`) is still worth it: it documents the contract and lets `@abstractmethod` reject incomplete shapes early.

---

## Key points

- **Same call, type-specific behavior.** `s.area()` dispatches to the right method automatically.
- Polymorphism is what kills the `if/elif` type ladder.
- **Open/Closed in action:** open to new shapes (add a subclass), closed to modifying existing callers.
- Duck typing = polymorphism by capability, not by inheritance.

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| `isinstance` ladder in the caller | New type → edit every caller | Put behavior in the type, call it polymorphically |
| Subclass forgets to implement the method | `AttributeError` at call time | Use an ABC + `@abstractmethod` to fail at construction |
| Inconsistent signatures across subclasses | Caller can't treat them uniformly | Keep the overridden method's signature identical |
| Returning different types from the same method | Caller can't rely on the result | Keep return types consistent across subclasses |

---

## Interview out-loud

> "I'll give every shape a common `area()` method via a `Shape` base class. Then `total_area` and `largest` just call `area()` on each element — they don't branch on the concrete type. Adding a new shape means adding one subclass with its own `area()`; the existing loops never change. That's polymorphism: one interface, many implementations, and it's what lets the code stay open to extension but closed to modification."

---

## Likely Follow-ups

The interview is one question that grows in parts — expect new shapes and new operations.

- **"Add a Pentagon without touching `total_area`."** → One new subclass with its own `area()`. The existing functions never change — say that out loud, it's the whole point.
- **"Now every shape needs a `perimeter()` too."** → Add a second `@abstractmethod` to `Shape`; Python refuses to construct any subclass that skips it.
- **"Sort the shapes by area."** → `sorted(shapes, key=lambda s: s.area())` — the same polymorphic call, no type checks.
- **"What if someone passes an object without `area()`?"** → With the ABC it can't be constructed as a Shape; with pure duck typing it fails at call time — that trade-off is the Abstraction exercise (OOP4).

---

**Pillar position:** Polymorphism rides on inheritance (Pillar 2) and is enforced by abstraction (Pillar 4) — the abstract base class defines the interface that all the forms must honor.
