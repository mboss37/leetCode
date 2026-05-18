# Idiom: string predicates (.isalnum, .isalpha, .isdigit, .lower, .upper)
# Use: classify or normalize characters during string scanning.
# Common in: Valid Palindrome, problems that "ignore spaces/punctuation."

# === Classification predicates (return bool) ===

# .isalnum() — alphanumeric (letters OR digits)
print("a".isalnum())     # True
print("3".isalnum())     # True
print(" ".isalnum())     # False
print("!".isalnum())     # False
print("a3".isalnum())    # True   (works on whole strings too — all chars must qualify)

# .isalpha() — letters only (no digits)
print("a".isalpha())     # True
print("3".isalpha())     # False
print("hello".isalpha()) # True
print("hello3".isalpha())# False  (the '3' disqualifies the whole string)

# .isdigit() — digits only (0-9)
print("3".isdigit())     # True
print("a".isdigit())     # False
print("123".isdigit())   # True
print("1.5".isdigit())   # False  ('.' disqualifies)

# .isspace() — whitespace (space, tab, newline, etc.)
print(" ".isspace())     # True
print("\t".isspace())    # True
print("a".isspace())     # False

# === Case conversion (return new string) ===

# .lower() — to lowercase
print("Hello".lower())   # "hello"

# .upper() — to uppercase
print("Hello".upper())   # "HELLO"

# These return NEW strings. Original is unchanged.
s = "Hello"
s.lower()
print(s)                 # "Hello" — still original; .lower() return was discarded

# To save: assign the result
s_lower = s.lower()
print(s_lower)           # "hello"

# === Common idiom: filter + normalize a string ===

# Build a cleaned version: keep only alphanumerics, lowercase them
text = "Was it a car or a cat I saw?"
cleaned = ''.join(c.lower() for c in text if c.isalnum())
print(cleaned)           # "wasitacaroracatisaw"

# That single list-comprehension line covers: filter (isalnum) + map (.lower)
# + join (''.join). Very common in palindrome / anagram / string-parsing problems.

# === Gotcha ===

# Empty strings: .isalnum() and friends return False for "" — they require AT LEAST ONE char.
print("".isalnum())      # False
