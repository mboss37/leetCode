# LC 20 — Valid Parentheses · Practice Script

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

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Is the string only bracket characters, or can other text appear between them?"** — Only brackets here. With mixed text you'd skip non-bracket characters — one extra branch.
- **"Is the empty string valid?"** — Yes, vacuously. Constraints say length ≥ 1, but the code handles it for free.
- **"Exactly these three pair types — no angle brackets or quotes?"** — Just `()[]{}` here. More types only means a bigger dict.
- **"Do you want just true/false, or the position of the first error?"** — Boolean only. Reporting a position means pushing indices, not characters.

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
            if c in "([{":
                # c is an opener. Push.
                stack.append(c)
            elif c in ")]}":
                # c is a closer. Stack must have a matching opener on top.
                if not stack or stack.pop() != pairs[c]:
                    return False
            # any other character is ignored — robust to mixed text

        return not stack   # valid iff all openers got matched
```

### Why this works

> Brackets nest **LIFO** — the most recently opened bracket is the one that must close next. That's literally what a stack provides.

- **Push** each opener.
- On a **closer**: the stack's top must be the matching opener. If not (or stack empty) → invalid.
- Any **other** character falls through both branches and is ignored.
- After the loop: if the stack still has openers → unmatched → invalid.

### Why enumerate openers *and* closers explicitly

The tighter `if c in pairs: ... else: stack.append(c)` form treats "anything that isn't a closer" as an opener. Under this problem's `()[]{}`-only constraint that's fine — but the moment the input contains other text (a real follow-up, see below), that `else` pushes stray letters as phantom openers and `"(a)"` wrongly fails. Enumerating both bracket sets and ignoring everything else handles mixed text for free, at the cost of one extra membership check per character.

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
> Walk the string. On an opener, push to the stack. On a closer, check: is the stack empty (no opener to match)? Or is the top of the stack the wrong opener type? Either case → invalid. Any non-bracket character I just skip.
>
> After the loop: if the stack still has openers, they went unmatched → invalid. Otherwise valid.
>
> O(n) time, O(n) space."

### Step 2: Key Points

- **Dict maps closer → opener** for O(1) match lookup.
- **Branch on openers and closers explicitly** (`c in "([{"` / `c in ")]}"`) so any non-bracket character is ignored — robust to mixed text.
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
| `else: stack.append(c)` (push anything not a closer) | Assumes bracket-only input; stray text gets pushed as phantom openers, so `"(a)"` fails | Enumerate openers explicitly (`c in "([{"`) and ignore the rest |
| `pairs` dict inverted (opener→closer) but indexed by closer | `KeyError` on first closer | Either flip dict to closer→opener, OR flip the comparison |
| `False` without `return` | Naked `False` is silently discarded; function continues | `return False` |
| Forgetting `not stack` check before `.pop()` | Calling `.pop()` on empty list raises `IndexError` | Use `not stack or ...` — short-circuits when empty |
| Returning `True` at the end unconditionally | Misses the "unmatched openers" case | `return not stack` |
| Two-pointer reflex | Two-pointer fails on `"()[]"` (sequential, not nested) | Use stack — not two-pointer |

---

## 6. Interview Out-Loud Explanation

> "Brackets nest last-in-first-out, so I'll use a stack. Walk the string. On an opener, push it. On a closer, check the top of the stack — if it's the matching opener, pop and continue. If the stack is empty or the top is wrong, return False immediately. I enumerate openers and closers explicitly, so any other character is just ignored — that keeps it robust if the input ever contains non-bracket text.
>
> After the loop, the stack must be empty — anything left means an opener never got matched.
>
> O(n) time, O(n) space."

---

## Likely Follow-ups

The interview is one question that grows in parts — once the stack version works, expect one of these.

- **"Now the input is real text with brackets mixed in."** → The recommended code already handles it: openers and closers are enumerated explicitly, so every other character falls through and is ignored. No change needed.
- **"Only `'('` and `')'` — can you do it without a stack?"** → Yes, a single counter: +1 on open, -1 on close, fail if it ever goes negative, valid if it ends at 0.
- **"How many characters would you remove to make it valid?"** → Count closers that find no opener plus openers left on the stack at the end.
- **"Design your own stack class with an extra O(1) min operation."** → That is Min Stack (LC 155), the next script in this chain.

---

**Chain position:** Valid Parentheses is the stack intro. The pattern extends to:
- **Min Stack** — stack + auxiliary min stack for O(1) `getMin()`.
- **Daily Temperatures** — monotonic stack.
- **Largest Rectangle in Histogram** — monotonic stack.

Master the LIFO mental model here — every other stack problem reuses it.
