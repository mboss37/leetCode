# Idiom: bisect
# Use: binary search in a SORTED list. Returns the index where a value should
#      be inserted to keep the list sorted. No need to write the binary search
#      yourself.
# Canonical form:
#     from bisect import bisect_left, bisect_right, insort
#     bisect_left(arr, x)   -> leftmost insertion index
#     bisect_right(arr, x)  -> rightmost insertion index
#     insort(arr, x)        -> insert x in sorted order (mutates arr)

from bisect import bisect_left, bisect_right, insort

nums = [1, 3, 5, 5, 5, 7, 9]
#        0  1  2  3  4  5  6

# bisect_left: leftmost position where target could go.
# If target IS in the list, returns the index of the FIRST occurrence.
print(bisect_left(nums, 5))    # 2  (first 5 is at index 2)
print(bisect_left(nums, 4))    # 2  (4 would go before the 5s)
print(bisect_left(nums, 10))   # 7  (insert at end)
print(bisect_left(nums, 0))    # 0  (insert at start)

# bisect_right: rightmost position where target could go.
# If target IS in the list, returns the index AFTER the last occurrence.
print(bisect_right(nums, 5))   # 5  (after the last 5)
print(bisect_right(nums, 4))   # 2  (same as bisect_left for non-members)

# Useful combo for "find first AND last occurrence":
#     first = bisect_left(nums, target)
#     last  = bisect_right(nums, target) - 1
#     if first <= last and nums[first] == target:  return [first, last]
#     else:                                          return [-1, -1]

# insort: insert in sorted order, mutates the list.
arr = [1, 3, 5, 7]
insort(arr, 4)
print(arr)   # [1, 3, 4, 5, 7]

# Why use bisect? Each call is O(log n). Writing your own binary search
# is fine, but bisect is concise + battle-tested + no off-by-one bugs.
# In an interview: it's totally acceptable to use bisect IF the interviewer
# allows library calls. Some specifically ask you to implement it yourself.
