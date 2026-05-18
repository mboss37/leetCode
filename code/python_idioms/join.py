# Idiom: ''.join(iterable)
# Use: build a string from a list of strings FAST.
# Why: doing `s += c` in a loop is O(n²) because each += creates a NEW string.
#      ''.join() is O(n) — single allocation.

# === Basic form ===

parts = ["hello", " ", "world"]
print(''.join(parts))            # "hello world"

# The separator between parts:
print(', '.join(["a", "b", "c"]))   # "a, b, c"
print('-'.join(["2026", "05", "15"])) # "2026-05-15"
print(''.join(["a", "b", "c"]))     # "abc"        (no separator)

# === Join works on any iterable of strings ===

# A list comp / generator that yields chars:
chars = ['h', 'e', 'l', 'l', 'o']
print(''.join(chars))            # "hello"

# A filter + map (very common):
text = "Hello, World!"
cleaned = ''.join(c.lower() for c in text if c.isalnum())
print(cleaned)                   # "helloworld"

# === Why NOT use += in a loop ===

# Slow (O(n²)):
result = ""
for c in "hello":
    result += c   # Each += creates a brand new string. n iterations × n bytes.

# Fast (O(n)):
result = ''.join(c for c in "hello")

# For small strings the difference is invisible. For 100K characters: brutal.

# === Gotcha: items must be strings ===

# This crashes — int in the list:
# ''.join([1, 2, 3])   -> TypeError: sequence item 0: expected str instance, int found

# Fix: convert each first.
nums = [1, 2, 3]
print(''.join(str(n) for n in nums))   # "123"

# === Common patterns ===

# Build a string by reversing:
print(''.join(reversed("hello")))      # "olleh"  (same as "hello"[::-1] but more explicit)

# Build a CSV row:
row = ["alice", "30", "designer"]
print(','.join(row))                   # "alice,30,designer"
