# Idiom: list comprehension
# Use: filter + transform a sequence in one expression. Produces a new list.
# Canonical form:
#     [expr for x in seq if condition]
# Read it left-to-right backwards: "for each x in seq, if condition holds, include expr."

nums = [1, 2, 3, 4, 5]

# Transform: square every number.
squares = [n * n for n in nums]
print(squares)
# Expected: [1, 4, 9, 16, 25]

# Filter: only the evens.
evens = [n for n in nums if n % 2 == 0]
print(evens)
# Expected: [2, 4]

# Combined: squares of the evens only.
even_squares = [n * n for n in nums if n % 2 == 0]
print(even_squares)
# Expected: [4, 16]

# Conditional expression INSIDE the expr (different from the `if` filter):
# This is "if-else as a value", not "include-or-skip".
labels = ["even" if n % 2 == 0 else "odd" for n in nums]
print(labels)
# Expected: ['odd', 'even', 'odd', 'even', 'odd']

# Two for-clauses (cartesian product):
pairs = [(x, y) for x in [1, 2] for y in ["a", "b"]]
print(pairs)
# Expected: [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

# Set comprehension and dict comprehension exist too:
unique_lengths = {len(w) for w in ["cat", "car", "dog", "bird"]}
print(unique_lengths)
# Expected: {3, 4}

word_lengths = {w: len(w) for w in ["cat", "bird"]}
print(word_lengths)
# Expected: {'cat': 3, 'bird': 4}

# Gotcha: don't nest deeply. If you need >2 for-clauses or complex logic,
# use a regular for-loop. Readability > compactness.
