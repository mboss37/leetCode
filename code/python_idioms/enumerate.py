# Idiom: enumerate
# Use: get index + value in one loop pass.
# Canonical form:
#     for i, v in enumerate(seq):
#         ...
# Convention: name the value after the singular of seq.
#     for i, num in enumerate(nums)       (not "for i, v in enumerate(nums)")
#     for i, name in enumerate(names)
#     for i, char in enumerate(s)

nums = [2, 7, 11, 15]

for i, num in enumerate(nums):
    print(f"Box {i} contains {num}")

# Expected output:
# Box 0 contains 2
# Box 1 contains 7
# Box 2 contains 11
# Box 3 contains 15

# Variation: start counting from 1 instead of 0.
# Useful when output is for humans.

for i, num in enumerate(nums, start=1):
    print(f"Position {i}: {num}")

# Expected output:
# Position 1: 2
# Position 2: 7
# Position 3: 11
# Position 4: 15
