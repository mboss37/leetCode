# Coding Interview Prep — Visual Learning Hub

Practice scripts, pattern walkthroughs, and interactive visualizations for FDE / SWE coding interview prep. 39 LeetCode problems organized by phase (foundations → depth → mock-mode), every problem with a recommended solution, line-by-line reasoning, complexity analysis, a hand-trace, and an interview out-loud script.

**Live site:** https://mboss37.github.io/leetCode/

---

## What's inside

- **39 practice scripts** in [`docs/exercise_scripts/`](docs/exercise_scripts/) — one per problem. Each one: problem statement, recommended solution with annotations, hand-trace table, complexity, pitfalls, "interview out-loud" script.
- **Pattern cheatsheet** ([`patterns_cheatsheet.html`](docs/patterns_cheatsheet.html)) — single-page printable A4 reference. *When you see X, reach for Y.*
- **Flashcards** ([`pattern_flashcards.html`](docs/pattern_flashcards.html)) — signal-to-pattern cards. Click to flip, mark as known, filter by category.
- **Step-through visualizations** — animated walkthroughs of the patterns that are hardest to internalize:
  - [`3sum_skip_visual.html`](docs/3sum_skip_visual.html) — the dedup invariant in 3Sum
  - [`sliding_window_visual.html`](docs/sliding_window_visual.html) — why both pointers move forward
  - [`stack_visual.html`](docs/stack_visual.html) — Valid Parentheses + Min Stack side by side
  - [`binary_search_visual.html`](docs/binary_search_visual.html) — Binary Search + Insert Position + First/Last Position variants
- **Python idioms** ([`python_idioms.md`](docs/python_idioms.md)) — quick reference for the standard-library moves that come up most.

---

## Structure

```
docs/
├── index.html                  # Hub — start here
├── patterns_cheatsheet.html    # Printable pattern reference
├── pattern_flashcards.html     # Signal → pattern drills
├── python_idioms.md            # Python stdlib reference
├── 3sum_skip_visual.html       # 3Sum dedup walkthrough
├── sliding_window_visual.html  # Sliding window animation
├── stack_visual.html           # Stack patterns
├── binary_search_visual.html   # Binary search variants
└── exercise_scripts/           # 39 practice scripts (LC1 ... LC1768)
```

---

## How to use

**Online:** open the live site, click any problem in the phase lists, the script loads in an inline modal.

**Locally:** clone, open `docs/index.html` in any modern browser. No build step, no dependencies — vanilla HTML / CSS / JS, with marked.js via CDN for in-page markdown rendering.

```
git clone https://github.com/mboss37/leetCode.git
open leetCode/docs/index.html
```

---

## Coverage

| Phase | Theme | Problems |
|---|---|---|
| **A — Foundations** | Hash maps, two pointers, sliding window, binary search, stacks, design intros | 17 |
| **B — Depth + Extensions** | Variant chains, monotonic stack, rotated arrays, linked lists, trees, more design | 15 |
| **C — Mock mode** | Mixed-pattern problems for timed solo mocks | 7 |

Pattern families covered: hash map, set existence, two-pointer (converging + sliding window), binary search variants, stack (LIFO + monotonic + min-stack), heap / bucket sort, BFS, DFS, backtracking, DP (bottom-up + memoized), greedy on intervals, design (LRU, randomized set, hash map, rate limit), linked-list pointer juggling, tree traversal, palindrome center-expansion, prefix/suffix products.

---

## Stack

Vanilla HTML / CSS / JavaScript. No bundler, no framework. The hub uses [marked.js](https://marked.js.org/) via CDN to render practice scripts as in-page modals. Designed to read cleanly both as raw markdown on GitHub and as a rendered site via GitHub Pages.
