# LC 155 — Min Stack · Practice Script

**Chain:** Valid Parentheses → **Min Stack** → Daily Temperatures (monotonic stack)

---

## Problem

> Design a stack supporting `push`, `pop`, `top`, and `getMin` — **all in O(1) time**.
>
> - `MinStack()` — initializes the stack.
> - `push(val)` — pushes val on top.
> - `pop()` — removes the top element.
> - `top()` → int — returns the top element.
> - `getMin()` → int — returns the minimum element currently in the stack.

**Constraints:**
- `-2³¹ <= val <= 2³¹ - 1`
- `pop`, `top`, `getMin` are only called on non-empty stacks.
- At most 3 × 10⁴ method calls total.

**Key requirement:** **O(1) time for ALL four operations.**

---

## 1. Naive (verbal baseline only — DON'T WRITE)

Single stack. `getMin()` scans all elements to find the minimum.
- **Time:** O(1) push/pop/top, but **O(n) getMin** — violates the spec.
- **Rejected:** the problem explicitly requires O(1) on ALL operations.

State it verbally:
> *"Naive is a single stack with O(n) getMin. Spec requires O(1) for all ops, so I'll use a two-stack approach."*

---

## 2. Two Stacks — RECOMMENDED (O(1) all ops)

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.minStack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if self.minStack:
            val = min(val, self.minStack[-1])
        self.minStack.append(val)

    def pop(self) -> None:
        self.stack.pop()
        self.minStack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.minStack[-1]
```

### How it works (the invariant)

> **At every level `i`, `minStack[i]` holds the minimum of `stack[0..i]`.**

Push and pop always touch BOTH stacks together → they stay synchronized in length and state. So `minStack[-1]` is always the current running minimum.

### Trace `push(-2), push(0), push(-3), getMin, pop, top, getMin`

| op | stack | minStack | returns |
|---|---|---|---|
| push(-2) | `[-2]` | `[-2]` | — |
| push(0) | `[-2, 0]` | `[-2, -2]` (min(0,-2)=-2) | — |
| push(-3) | `[-2, 0, -3]` | `[-2, -2, -3]` (min(-3,-2)=-3) | — |
| getMin | (same) | (same) | **-3** ✓ |
| pop | `[-2, 0]` | `[-2, -2]` | — |
| top | (same) | (same) | **0** ✓ |
| getMin | (same) | (same) | **-2** ✓ |

### Complexity

- **Time:** O(1) per operation (each is a list append, pop, or index).
- **Space:** O(n) — two stacks, each up to n items.

---

## 3. How to Practice

### Step 1: Read out loud

> "I need O(1) for all four operations, so a single stack with O(n) getMin won't fly. I use two stacks: the main stack for values, and an auxiliary 'min stack' that holds the running minimum at each level.
>
> On push: append val to the main stack; for the min stack, append min(val, current_min) if min stack has items, otherwise just val.
> On pop: pop both stacks together — they're synchronized.
> top() and getMin() are just `[-1]` on the respective stacks.
>
> All O(1)."

### Step 2: Key Points

- **Two stacks, always synchronized in length** — push both, pop both.
- **`minStack[i]` = min of stack[0..i]** — the invariant.
- **First push: minStack is empty, so just append val** (no min needed).
- **`if self.minStack:`** = "if non-empty" — Python's truthiness rule.

### Step 3: Test Cases

| Sequence | Expected |
|---|---|
| push(-2), push(0), push(-3), getMin() | -3 |
| ... then pop(), top() | 0 |
| ... then getMin() | -2 |
| push(5) on empty, top() | 5 |
| push(5), getMin() | 5 |
| push(1), push(2), push(3), getMin() | 1 |
| ... pop, getMin() | 1 (still — 1 was the floor) |

---

## 4. Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Only pushing to main stack on push | minStack stays empty; getMin breaks | Always push to BOTH |
| Only popping main stack on pop | minStack out of sync | Always pop BOTH |
| `min(val, self.minStack[-1])` on empty minStack | `IndexError` on first push | Guard with `if self.minStack:` first |
| Reset state inside methods | Loses persistence between calls | State lives in `__init__`, NOT in method scope |
| Forgetting `self.` prefix | Creates a local variable instead of touching instance state | Always `self.stack`, never bare `stack` |

---

## 5. Interview Out-Loud Explanation

> "I need O(1) for all operations including getMin, so a single stack with linear-scan getMin won't pass.
>
> I use two stacks running in parallel. The main stack holds the values. The auxiliary min stack holds the running minimum at each level — `minStack[i]` is always the min of the main stack's first i+1 elements.
>
> On push, I append to the main stack and then push min(val, current_min) to the min stack. On pop, I pop both. top() and getMin() just peek the respective tops.
>
> All four operations are O(1). Space is O(n) for the two stacks."

---

## 6. OOP notes

This is a **real OOP problem**, unlike the algorithm problems wrapped in `class Solution:`. Key things:

- **State lives on the instance** (`self.stack`, `self.minStack`) — persists across method calls.
- **`__init__`** runs once when you create the instance with `MinStack()`. Sets up the empty stacks.
- **`self`** = "this instance." Methods read and write via `self.xxx` to share state.

If you create two instances, they have **separate state** — `ms1.push(5)` doesn't affect `ms2`.

---

**Chain position:** Min Stack is the "auxiliary stack" idea — stack alongside stack. Generalizes to **Daily Temperatures** (monotonic stack, where the second stack is implicit) and **Largest Rectangle in Histogram**.
