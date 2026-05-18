# Idiom: slicing
# Use: get a contiguous chunk of a string or list. Or reverse with [::-1].
# Canonical forms:
#     s[start:stop]        -> chars from `start` up to but NOT including `stop`
#     s[start:]            -> from `start` to the end
#     s[:stop]             -> from the beginning up to (not including) `stop`
#     s[::-1]              -> the whole thing, reversed
#     s[start:stop:step]   -> every `step`-th character
#     s[::2]               -> every other character

s = "hello world"

# Basic slice — get substring
print(s[0:5])      # "hello"        — indices 0,1,2,3,4 (5 NOT included)
print(s[6:11])     # "world"
print(s[6:])       # "world"        — from 6 to end (omit stop)
print(s[:5])       # "hello"        — from start to 5 (omit start)
print(s[:])        # "hello world"  — full copy

# Reverse with [::-1]
print(s[::-1])     # "dlrow olleh"

# Step (skip)
print(s[::2])      # "hlowrd"       — every other char
print(s[::3])      # "hlwl"

# Negative indices count from the end
print(s[-5:])      # "world"        — last 5 chars
print(s[:-6])      # "hello"        — everything except the last 6
print(s[-1])       # "d"            — last char (this is indexing, not slicing)

# Same syntax works on lists
nums = [1, 2, 3, 4, 5]
print(nums[1:4])   # [2, 3, 4]
print(nums[::-1])  # [5, 4, 3, 2, 1]

# Important: slicing CREATES A NEW object. Original is unchanged.
# This is different from `.reverse()` which mutates in place.
original = [1, 2, 3]
reversed_copy = original[::-1]
print(original)        # [1, 2, 3]   — unchanged
print(reversed_copy)   # [3, 2, 1]

# Gotcha: out-of-range slices DON'T throw — they silently clamp.
print(s[100:200])  # ""         — empty string, no error
print(nums[10:])   # []         — empty list, no error
# But indexing out of range DOES throw: nums[10]  -> IndexError

# Quick palindrome check using slicing:
def is_palindrome(s):
    return s == s[::-1]

print(is_palindrome("racecar"))   # True
print(is_palindrome("hello"))     # False
