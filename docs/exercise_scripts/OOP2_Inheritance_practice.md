# Inheritance — Employee Hierarchy · Practice Script

> **Pillar 2 of 4.** Inheritance = a subclass **is-a** kind of its parent, reusing the parent's code and extending or specializing it.

---

## The principle

When several classes share behavior, lift the common part into a **base class** and let the specific classes inherit it. The subclass gets everything for free and only writes what's *different*.

The relationship test is **"is-a"**: a `Manager` **is an** `Employee`. If you can't say "is-a" with a straight face (a `Car` is **not** an `Engine`), you want composition instead — see Pillar 5.

`super().__init__(...)` calls the parent's constructor so the base does its own setup; the subclass adds to it rather than copy-pasting it.

---

## The exercise

> Model employees:
> - every `Employee` has a name and a base salary, and can report `annual_pay()`
> - a `Manager` is an Employee who also gets a yearly bonus
> - a `Salesperson` is an Employee whose pay includes commission on sales
> - no duplicated name/salary logic

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Should a plain `Employee` be constructible, or only Manager/Salesperson?"** — Decides plain base class vs an ABC that can't be instantiated.
- **"Can salary, bonus, or commission be negative?"** — If not, validate once in the base `__init__` and raise `ValueError`.
- **"Is commission a flat amount or a rate times sales?"** — A rate means `Salesperson` needs a `sales` field too — different constructor.
- **"Is `annual_pay` gross yearly pay, before tax?"** — Pin down what the number means before three classes compute it.

---

## ❌ NOT RECOMMENDED — copy-paste, no shared base

```python
class Manager:
    def __init__(self, name, salary, bonus):
        self.name = name
        self.salary = salary
        self.bonus = bonus
    def annual_pay(self):
        return self.salary + self.bonus

class Salesperson:
    def __init__(self, name, salary, commission):
        self.name = name          # duplicated
        self.salary = salary      # duplicated
        self.commission = commission
    def annual_pay(self):
        return self.salary + self.commission
```

`name`/`salary` setup is duplicated. Add a field to "every employee" and you edit every class and hope you didn't miss one.

---

## ✅ RECOMMENDED — shared base, subclasses extend it

```python
class Employee:
    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary

    def annual_pay(self) -> float:
        return self.salary

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name}, pays {self.annual_pay()})"


class Manager(Employee):
    def __init__(self, name: str, salary: float, bonus: float):
        super().__init__(name, salary)   # base does name/salary
        self.bonus = bonus

    def annual_pay(self) -> float:
        return super().annual_pay() + self.bonus   # extend, don't replace


class Salesperson(Employee):
    def __init__(self, name: str, salary: float, commission: float):
        super().__init__(name, salary)
        self.commission = commission

    def annual_pay(self) -> float:
        return super().annual_pay() + self.commission
```

```python
team = [
    Employee("Ada", 90_000),
    Manager("Grace", 120_000, 30_000),
    Salesperson("Lin", 70_000, 25_000),
]
for member in team:
    print(member)            # __repr__ + annual_pay both inherited/overridden
```

- `name`/`salary` live in **one** place.
- Subclasses call `super().__init__` to reuse base setup, then add their own fields.
- `super().annual_pay()` reuses the base calculation and **extends** it — no copy-paste of `self.salary`.
- `__repr__` is written once and works for every subclass (`type(self).__name__` reports the real class).

---

## Key points

- **Inheritance is for "is-a".** Reach for it when subclasses genuinely *are* specialized versions of the base.
- `super()` reuses parent behavior — both in `__init__` and in overridden methods.
- Override to **specialize**; call `super().method()` when you want to *add to* the base rather than *replace* it.
- Favor shallow hierarchies. Deep chains (A→B→C→D) get brittle fast — that's the cue to consider composition.

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Forgetting `super().__init__()` | Base fields (name, salary) never set → `AttributeError` | Always call it first in the subclass `__init__` |
| Using inheritance for "has-a" | `Car(Engine)` makes no sense; fragile design | Use composition (Pillar 5) |
| Overriding by copy-pasting base logic | Base change doesn't propagate | Call `super().method()` and add to it |
| Deep inheritance chains | Hard to trace where behavior comes from | Keep it shallow; prefer composition |

---

## Interview out-loud

> "Name and salary are common to every employee, so they go in a base `Employee` class with a default `annual_pay`. `Manager` and `Salesperson` inherit that and override `annual_pay`, but they call `super().annual_pay()` so they extend the base calculation instead of duplicating it. The relationship is genuinely 'is-a' — a manager is an employee — which is exactly when inheritance is the right tool."

---

## Likely Follow-ups

The interview is one question that grows in parts — expect the hierarchy to gain members.

- **"Add a Contractor paid by the hour."** → One new subclass with `hours` and `rate`, overriding `annual_pay`. Nothing existing changes — that's the point.
- **"Compute total payroll for a mixed list."** → One loop calling `member.annual_pay()` — no type checks. That's the Polymorphism exercise (OOP3).
- **"A Manager who ALSO earns commission?"** → Don't deepen the tree. Compose: give employees a list of pay components and sum them — the Composition exercise (OOP5).
- **"Force every subclass to define `annual_pay`."** → Make `Employee` an ABC with `@abstractmethod` — the Abstraction exercise (OOP4).

---

**Pillar position:** Inheritance sets up the class hierarchy. Polymorphism (Pillar 3) is what makes that hierarchy *useful* — treating every subclass through the same interface.
