# LC 739 — Daily Temperatures · Practice Script

---

## Problem

> Given an array `temperatures` representing daily temperatures, return an array `answer` such that `answer[i]` is the number of days you'd have to wait after the `i`-th day to get a warmer temperature. If there's no future day with a warmer temperature, put `0` instead.

**Constraints:**
- `1 <= temperatures.length <= 10⁵`
- `30 <= temperatures[i] <= 100`

---

## Clarifying Questions (ask 2-3 before you code)

The interviewer scores you on capturing requirements before typing. Pick the ones that genuinely change your approach:

- **"Does 'warmer' mean strictly warmer, or does an equal temperature count?"** — Strictly warmer. This decides `<` vs `<=` in the stack comparison.
- **"Should I return the number of days to wait, or the index of the warmer day?"** — Days (`j - i`). That's why the stack must hold indices, not values.
- **"What do I return when no warmer day ever comes?"** — 0. So I pre-fill the result with zeros and only overwrite on a pop.
- **"How large can the input get?"** — Up to 10⁵ days, so the O(n²) scan is too slow and I need roughly linear.

---

## NOT RECOMMENDED — Brute Force (O(n²))

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        result = [0] * n
        for i in range(n):
            for j in range(i + 1, n):
                if temperatures[j] > temperatures[i]:
                    result[i] = j - i
                    break
        return result
```

- **Time:** O(n²)
- For n = 10⁵: 10¹⁰ ops → TLE.

State verbally:
> *"Brute force is for each day, scan forward until I find a warmer one — O(n²). I'll use a monotonic stack for O(n)."*

---

## RECOMMENDED — Monotonic Stack (O(n))

```python
from typing import List

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        result = [0] * n
        stack = []   # indices, kept in decreasing-temperature order

        for i, t in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < t:
                prev_idx = stack.pop()
                result[prev_idx] = i - prev_idx
            stack.append(i)

        return result
```

### The pattern — Monotonic Stack

The stack stores **indices whose answers we haven't found yet**. It stays in **decreasing temperature order** from bottom to top (each item below has a higher-or-equal temperature than the items above).

When a new day arrives with a warmer temperature than the top:
- Pop the top → its "warmer day" is the current day.
- Record `result[popped_idx] = current_idx - popped_idx`.
- Keep popping while the new day is still warmer than the (new) top.
- Then push the current index.

When the loop ends, anything left on the stack has no warmer future day → answer stays 0 (default).

### Why O(n)

Each index is **pushed once and popped at most once**. Total push+pop operations = 2n. The outer for loop is n. Total work: O(n).

It LOOKS like nested loops (for + while), but the while only runs when it does work that's "charged" to a unique index. Amortized linear.

### Trace on `[73, 74, 75, 71, 69, 72, 76, 73]`

Indices: `0  1  2  3  4  5  6  7`

| i | t | stack before | action | result |
|---|---|---|---|---|
| 0 | 73 | [] | push 0 → [0] | [0,0,0,0,0,0,0,0] |
| 1 | 74 | [0] | 74>73 → pop 0, result[0]=1; push 1 → [1] | [1,0,0,0,0,0,0,0] |
| 2 | 75 | [1] | 75>74 → pop 1, result[1]=1; push 2 → [2] | [1,1,0,0,0,0,0,0] |
| 3 | 71 | [2] | 71<75 → push 3 → [2,3] | (same) |
| 4 | 69 | [2,3] | 69<71 → push 4 → [2,3,4] | (same) |
| 5 | 72 | [2,3,4] | 72>69 → pop 4, result[4]=1. 72>71 → pop 3, result[3]=2. 72<75 → push 5 → [2,5] | [1,1,0,2,1,0,0,0] |
| 6 | 76 | [2,5] | 76>72 → pop 5, result[5]=1. 76>75 → pop 2, result[2]=4. push 6 → [6] | [1,1,4,2,1,1,0,0] |
| 7 | 73 | [6] | 73<76 → push 7 → [6,7] | (same) |

Final: `[1, 1, 4, 2, 1, 1, 0, 0]` ✓ (Indices 6 and 7 remain on the stack — never found a warmer day.)

### Complexity

- **Time:** O(n) — amortized; each index pushed and popped once
- **Space:** O(n) — stack worst case

---

## Pitfalls

| Trap | What goes wrong | Fix |
|---|---|---|
| Storing VALUES on the stack instead of indices | Can't compute the distance (number of days) | Store indices |
| Comparison direction: `> temperature[stack[-1]]` | Need STRICTLY warmer → use `<` from stack's POV: `temperatures[stack[-1]] < t` | Strict |
| Using `<=` instead of `<` | Equal temperatures shouldn't count as warmer | Strict `<` |
| Forgetting to push the current index after popping | Some indices never get on the stack | Push after the while |
| Computing distance as `popped_idx - current_idx` | Sign flipped | `current_idx - popped_idx` |

---

## Interview Out-Loud

> "Brute force is O(n²) — for each day scan forward. I'll use a monotonic stack for O(n).
>
> Stack stores indices of days waiting for an answer, kept in decreasing temperature order. Walk the array. When the current day is warmer than the day at the top of the stack, pop it and record the distance — that's the popped day's answer. Keep popping while applicable. Then push the current index.
>
> Indices left on the stack at the end have no warmer future day — their answer stays at the default 0.
>
> O(n) time — each index pushed and popped at most once. O(n) space."

---

## Likely Follow-ups

The interview is one question that grows in parts — expect a twist after the base solution works.

- **"Now find the next COLDER day instead."** → Flip the comparison: pop while the stack top is warmer than the current day. The stack order flips too; nothing else changes.
- **"Return the warmer temperature itself, not the wait."** → Same stack of indices; on pop, write `temperatures[i]` instead of `i - prev_idx`. This is Next Greater Element.
- **"Temperatures arrive one at a time as a stream — can you still do it?"** → Yes. The stack approach is already online: each new day pops and answers the waiting days as it arrives.
- **"Can you exploit the value range 30-100?"** → Scan right-to-left, keep the nearest index for each of the ~70 temperatures, and check the warmer values for each day. Constant work per day.

---

**Chain position:** Monotonic stack. Same pattern in: Next Greater Element, Largest Rectangle in Histogram, Trapping Rain Water (variant).
