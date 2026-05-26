# Composition over Inheritance — Computer Build · Practice Script

> **Bonus pillar.** Composition = build a complex object by **containing** other objects ("has-a"), instead of inheriting from them ("is-a"). The famous guideline: *favor composition over inheritance.*

---

## The principle

Inheritance models **"is-a"** (a `Manager` is an `Employee`). Composition models **"has-a"** (a `Computer` has a `CPU`, has `RAM`, has `Storage`). When the relationship is "has-a" or "uses-a," composition is the right tool — and it's usually more flexible than a tall inheritance tree.

Why "favor composition"? Inheritance locks behavior in at class-definition time and couples the child to the parent's internals. Composition lets you **swap parts at runtime**, mix capabilities freely, and avoid the brittle, deep hierarchies that inheritance tends to grow.

The test: say it out loud. "A computer **is a** CPU"? No. "A computer **has a** CPU"? Yes → compose.

---

## The exercise

> Model a `Computer` assembled from parts: a `CPU`, `RAM`, and `Storage`.
> The computer reports its specs and total price by **delegating** to its parts.
> You should be able to swap any part (e.g. upgrade storage) without rewriting the computer.

---

## ❌ NOT RECOMMENDED — inheritance for "has-a"

```python
class CPU:
    def __init__(self, model, price):
        self.model = model
        self.price = price

# A computer is NOT a CPU — but here it pretends to be one.
class Computer(CPU):
    def __init__(self, cpu_model, cpu_price, ram_gb):
        super().__init__(cpu_model, cpu_price)
        self.ram_gb = ram_gb
    # Now want RAM AND Storage as rich objects too?
    # You can't inherit from three things cleanly. The model breaks down.
```

"Computer is-a CPU" is false, so the design fights you the moment you add a second part. You also inherit CPU's whole surface, which a computer shouldn't expose.

---

## ✅ RECOMMENDED — compose from parts

```python
class CPU:
    def __init__(self, model: str, price: float):
        self.model = model
        self.price = price


class RAM:
    def __init__(self, gb: int, price: float):
        self.gb = gb
        self.price = price


class Storage:
    def __init__(self, kind: str, gb: int, price: float):
        self.kind = kind          # "SSD" / "HDD"
        self.gb = gb
        self.price = price


class Computer:
    def __init__(self, cpu: CPU, ram: RAM, storage: Storage):
        self.cpu = cpu            # HAS-A cpu
        self.ram = ram            # HAS-A ram
        self.storage = storage    # HAS-A storage

    def total_price(self) -> float:
        return self.cpu.price + self.ram.price + self.storage.price   # delegate

    def specs(self) -> str:
        return (f"{self.cpu.model} · {self.ram.gb}GB RAM · "
                f"{self.storage.gb}GB {self.storage.kind}")
```

```python
pc = Computer(
    cpu=CPU("Ryzen 7", 320),
    ram=RAM(32, 110),
    storage=Storage("SSD", 1000, 90),
)
print(pc.specs())          # Ryzen 7 · 32GB RAM · 1000GB SSD
print(pc.total_price())    # 520

# Swap a part at runtime — no Computer changes needed:
pc.storage = Storage("SSD", 2000, 150)
print(pc.total_price())    # 580
```

- A `Computer` **has** parts and **delegates** to them (`self.cpu.price`).
- Parts are independent — testable and reusable on their own.
- Swapping a part is a one-line assignment; the hierarchy never has to flex.

---

## "Has-a" vs "is-a" — the decision

| Relationship | Tool | Example |
|---|---|---|
| is-a (specialization) | Inheritance | `Manager` is-a `Employee` |
| has-a (containment) | Composition | `Computer` has-a `CPU` |
| uses-a (collaboration) | Composition | `Checkout` uses-a `PaymentProcessor` |

If you're unsure, default to composition — it's easier to refactor *toward* inheritance later than away from it.

---

## Key points

- **Composition = "has-a"; inheritance = "is-a".** Pick by the real relationship.
- Composition gives **runtime flexibility** — swap collaborators without touching the container.
- It avoids deep, fragile inheritance trees and the tight coupling they create.
- The container **delegates** to its parts rather than inheriting their behavior.

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Inheriting for code reuse alone | "is-a" is false → brittle, leaks parent's API | Compose and delegate |
| Exposing parts' internals everywhere | Container couples callers to part details | Delegate via the container's own methods |
| Rebuilding the container to swap a part | Lost the main benefit of composition | Store parts as attributes you can reassign |
| Forcing one big inheritance tree | Combinatorial explosion of subclasses | Mix capabilities by composing small parts |

---

## Interview out-loud

> "A computer isn't a kind of CPU — it *has* a CPU, RAM, and storage. So I compose: the `Computer` holds those parts as attributes and delegates to them for price and specs. That keeps each part independent and testable, and I can swap or upgrade a part at runtime without changing the `Computer` class. I reach for inheritance only when the relationship is genuinely 'is-a'; for 'has-a' or 'uses-a', composition is more flexible — which is why the guidance is to favor composition over inheritance."

---

**Pillar position:** Composition is the counterweight to inheritance (Pillar 2). Knowing *when not to inherit* is as important as knowing how — together they let you model relationships honestly instead of forcing everything into a class tree.
