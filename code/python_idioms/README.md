# Python Idioms Drill

> Quick reference + drill files for interview-day Python fluency.
> Goal: every idiom on this list is muscle memory by Jun 3. You can type any of them in under 30 seconds without thinking.

## How to drill (5 min per idiom)

1. Pick an idiom from the table below.
2. Open its `.py` file. Read the canonical example. Note the gotchas.
3. Close the file.
4. Open a blank scratch buffer (or just a new untitled tab).
5. Type the idiom from memory.
6. Run it. Compare output to the expected.
7. If wrong: log it as a weak spot. Retype tomorrow.

Drill 4–5 idioms per session as warm-up. Rotate so every idiom gets touched at least once per week.

## Idiom index

| Idiom | File | Use |
|---|---|---|
| `enumerate` | [enumerate.py](enumerate.py) | Index + value in one loop |
| `zip` | [zip.py](zip.py) | Walk two sequences together |
| List comprehension | [list_comp.py](list_comp.py) | Filter + transform in one expression |
| `defaultdict` | [defaultdict.py](defaultdict.py) | Auto-default values for missing keys |
| `Counter` | [counter.py](counter.py) | Frequency map of any sequence |
| `dict.get(k, default)` | [dict_get.py](dict_get.py) | Lookup with fallback, no exception |
| `sorted(key=...)` | [sorted_key.py](sorted_key.py) | Custom-key sort, `reverse=True` for descending |
| `bisect` | [bisect.py](bisect.py) | Binary search inside a sorted list — `bisect_left`, `bisect_right`, `insort` |
| `heapq` | [heapq.py](heapq.py) | Min-heap. No native max-heap — negate values |
| `deque` | [deque.py](deque.py) | O(1) appends and pops from both ends — BFS, sliding window |
| Slicing + reverse | [slicing.py](slicing.py) | `s[::-1]`, `s[i:j]`, `s[::2]` |
| String predicates | [str_predicates.py](str_predicates.py) | `.isalnum()`, `.isalpha()`, `.isdigit()`, `.lower()`, `.upper()` |
| `''.join(parts)` | [join.py](join.py) | Build strings fast — `+=` in a loop is O(n²) |
| Set ops | [set_ops.py](set_ops.py) | `union (|)`, `intersection (&)`, `difference (-)`, `^` |
| Tuple unpacking | [tuple_unpacking.py](tuple_unpacking.py) | `a, b = b, a` for swap, `*rest` for capture |

All Phase A idioms covered. Add new files only when a new problem introduces a new idiom (recursion patterns, `bit manipulation`, etc.).

## When you forget an idiom mid-problem

Don't panic. Open the README, scan the table, jump to the file. If you can't recall after a 30-second peek, note it as a weak spot and re-drill tomorrow morning. The point isn't to never forget — it's to notice when you forget and re-burn the path.
