# Idiom: zip
# Use: walk two (or more) sequences in lockstep, yielding tuples of corresponding items.
# Canonical form:
#     for a, b in zip(seq_a, seq_b):
#         ...
# Same shape as enumerate — unpack the tuple in the for-loop.

ids = [1, 2, 3]
names = ["alice", "bob", "carol"]

for id_, name in zip(ids, names):
    print(f"{id_} -> {name}")

# Expected output:
# 1 -> alice
# 2 -> bob
# 3 -> carol

# Why id_ with trailing underscore:
# `id` is a Python built-in (returns object identity). To use it as a variable
# name without shadowing the built-in, PEP 8 says append a trailing underscore.
# Same trick: type_, list_, dict_, class_.

# Variation: multiple sequences.
scores = [90, 85, 95]
for id_, name, score in zip(ids, names, scores):
    print(f"{id_} {name}: {score}")

# Expected output:
# 1 alice: 90
# 2 bob: 85
# 3 carol: 95

# Gotcha: zip stops at the SHORTEST sequence. The rest is silently dropped.
short = [1, 2]
long_ = ["a", "b", "c", "d"]
for x, y in zip(short, long_):
    print(x, y)

# Expected output:
# 1 a
# 2 b
# (Items "c" and "d" are dropped — no error.)

# Never name a variable `zip` — it shadows the built-in.
# Bad:  zip = zip(ids, names)   <- now `zip` is no longer a function
# Good: pairs = list(zip(ids, names))   <- if you need to store the result
