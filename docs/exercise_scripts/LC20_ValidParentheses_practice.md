# LC 20 — Valid Parentheses · Practice Script

**Code:** [code/validParentheses/](../../code/validParentheses/)

---

## Problem

> Given a string `s` containing just the characters `'(', ')', '{', '}', '['` and `']'`, determine if the input string is **valid**.
>
> Valid means:
> 1. Open brackets are closed by the same type of brackets.
> 2. Open brackets are closed in the correct order.
> 3. Every closing bracket has a corresponding open bracket of the same type.

**Constraints:**
- `1 <= s.length <= 10⁴`
- `s` contains only `'()[]{}'`

**Return:** boolean.

---

## 1. Brute Force — Repeated Pair Removal (O(n²))

```python
class Solution:
    def isValid(self, s: str) -> bool:
        while '()' in s or '[]' in s or '{}' in s:
            s = s.replace('()', '').replace('[]', '').replace('{}', '')
        return s == ''
```

- **Time:** O(n²) — outer loop up to n/2 × O(n) per `replace()`.
- **Space:** O(n) — each `replace()` builds a new string.
- **Why it works:** repeatedly peel off any complete pair. Valid input reduces to empty; invalid input has unpeelable leftovers.
- **Why it's rejected:** at n=10⁴, ~50M ops — ~5000× slower than the stack version. Doesn't show the LIFO insight.
- **State out loud only:** "Brute force is repeated pair removal, O(n²). I'll use a stack for O(n)."

---

## 2. Stack — RECOMMENDED (O(n))

```python
class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {")": "(", "]": "[", "}": "{"}    # closer → expected opener
        stack = []

        for c in s:
            if c in pairs:
                # c is a closer. Stack must have a matching opener on top.
                if not stack or stack.pop() != pairs[c]:
                    return False
            else:
                # c is an opener. Push.
                stack.append(c)

        return not stack   # valid iff all openers got matched
```

### Why this works

> Brackets nest **LIFO** — the most recently opened bracket is the one that must close next. That's literally what a stack provides.

- **Push** each opener.
- On a **closer**: the stack's top must be the matching opener. If not (or stack empty) → invalid.
- After the loop: if the stack still has openers → unmatched → invalid.

### Complexity

- **Time:** O(n) — single pass.
- **Space:** O(n) — worst case (all openers, e.g. `"((((("`) the stack holds them all.

---

## 3. Comparison

| Aspect              | Brute (O(n²))          | Stack (O(n))             | Winner |
|---------------------|-------------------------|---------------------------|--------|
| Time                | O(n²)                   | **O(n)**                  | Stack  |
| Space               | O(n)                    | O(n)                      | Tie    |
| Reveals the insight | No — pair-stripping     | **Yes — LIFO nesting**    | Stack  |
| Ops at n = 10⁴      | ~50M                    | **~10K**                  | Stack  |
| Interview-accepted  | No                      | **Yes**                   | Stack  |

---

## 4. How to Practice

### Step 1: Read out loud

> "Brackets nest last-in-first-out — the most recently opened bracket is what must close next. That's exactly what a stack provides.
>
> Walk the string. On an opener, push to the stack. On a closer, check: is the stack empty (no opener to match)? Or is the top of the stack the wrong opener type? Either case → invalid.
>
> After the loop: if the stack still has openers, they went unmatched → invalid. Otherwise valid.
>
> O(n) time, O(n) space."

### Step 2: Key Points

- **Dict maps closer → opener** for O(1) match lookup.
- **`if not stack or stack.pop() != pairs[c]`** — the two failure cases in one expression. Empty stack short-circuits before `.pop()` is called.
- **Return `not stack` at the end** — empty stack means all openers got matched.

### Step 3: Test Cases

| s              | Expected | Notes                         |
|----------------|----------|-------------------------------|
| `"()"`         | True     | Basic match                   |
| `"()[]{}"`     | True     | Sequential pairs              |
| `"(]"`         | False    | Wrong type                    |
| `"([)]"`       | False    | Cross-nested (NOT valid)      |
| `"{[]}"`       | True     | Properly nested               |
| `""`           | True     | Empty is vacuously valid      |
| `"("`          | False    | Unmatched opener              |
| `")"`          | False    | Closer with no opener         |
| `"()[]{})"`    | False    | Extra closer at end           |
| `"((((("`      | False    | All openers, no closers       |

---

## 5. Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| `pairs` dict inverted (opener→closer) but indexed by closer | `KeyError` on first closer | Either flip dict to closer→opener, OR flip the comparison |
| `False` without `return` | Naked `False` is silently discarded; function continues | `return False` |
| Forgetting `not stack` check before `.pop()` | Calling `.pop()` on empty list raises `IndexError` | Use `not stack or ...` — short-circuits when empty |
| Returning `True` at the end unconditionally | Misses the "unmatched openers" case | `return not stack` |
| Two-pointer reflex | Two-pointer fails on `"()[]"` (sequential, not nested) | Use stack — not two-pointer |

---

## 6. Interview Out-Loud Explanation

> "Brackets nest last-in-first-out, so I'll use a stack. Walk the string. On an opener, push it. On a closer, check the top of the stack — if it's the matching opener, pop and continue. If the stack is empty or the top is wrong, return False immediately.
>
> After the loop, the stack must be empty — anything left means an opener never got matched.
>
> O(n) time, O(n) space."

---

**Chain position:** Valid Parentheses is the stack intro. The pattern extends to:
- **Min Stack** — stack + auxiliary min stack for O(1) `getMin()`.
- **Daily Temperatures** — monotonic stack.
- **Largest Rectangle in Histogram** — monotonic stack.

Master the LIFO mental model here — every other stack problem reuses it.
