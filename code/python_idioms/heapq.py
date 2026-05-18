# Idiom: heapq
# Use: priority queue / min-heap. Get the smallest element in O(log n) per op.
# Canonical form:
#     import heapq
#     heap = []                     -> just a regular list, treated as a heap
#     heapq.heappush(heap, x)       -> push, O(log n)
#     heapq.heappop(heap)           -> pop the SMALLEST, O(log n)
#     heap[0]                       -> peek at smallest WITHOUT removing, O(1)
#     heapq.heapify(my_list)        -> turn an existing list into a heap, O(n)
#
# IMPORTANT: Python's heapq is a MIN-heap. There is NO native max-heap.
#            To simulate a max-heap, negate values before pushing.

import heapq

# === Basic min-heap ===

heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 2)
heapq.heappush(heap, 8)
heapq.heappush(heap, 1)
heapq.heappush(heap, 7)

print(heap)                # [1, 2, 8, 5, 7]
# Note: the list looks "wrong" — that's because the heap is stored in a special
# tree-shaped order, not sorted order. The ROOT (index 0) is always the smallest.
print(heap[0])             # 1  — peek at smallest, O(1)

# Pop the smallest
print(heapq.heappop(heap)) # 1
print(heapq.heappop(heap)) # 2
print(heapq.heappop(heap)) # 5
print(heap)                # [7, 8]

# === Turning a list into a heap in O(n) ===

nums = [5, 2, 8, 1, 7, 3]
heapq.heapify(nums)        # mutates in place
print(nums)                # [1, 2, 3, 5, 7, 8]   — heap order; root = min

# === Max-heap trick: negate values ===

# Suppose you want the LARGEST element each time:
nums = [5, 2, 8, 1, 7]
max_heap = [-n for n in nums]    # negate each
heapq.heapify(max_heap)
print(-heapq.heappop(max_heap))  # 8  — largest (negate back when popping)
print(-heapq.heappop(max_heap))  # 7

# === Top K elements pattern (LC 347 Top K Frequent) ===

# Find the 3 largest in a list:
nums = [4, 1, 7, 3, 8, 2, 9, 5]
k = 3

# Approach: keep a min-heap of size K. If a new value is bigger than the smallest
# in the heap (heap[0]), it deserves to be in the top-K — replace the smallest.

heap = []
for n in nums:
    heapq.heappush(heap, n)
    if len(heap) > k:
        heapq.heappop(heap)     # drop the smallest — heap stays at size K

print(sorted(heap, reverse=True))   # [9, 8, 7]   — the top 3

# This is O(n log k), which beats sorting (O(n log n)) when k is small.

# === heapq.nlargest / nsmallest — built-in shortcuts ===

print(heapq.nlargest(3, [4, 1, 7, 3, 8, 2, 9, 5]))     # [9, 8, 7]
print(heapq.nsmallest(3, [4, 1, 7, 3, 8, 2, 9, 5]))    # [1, 2, 3]

# In an interview: implement the algorithm manually if asked. nlargest is fine
# if not asked, but be ready to explain how it works (heap of size k).

# === Storing tuples (priority + data) ===

# Heaps compare elements LEFT-TO-RIGHT. To prioritize by one field:
tasks = []
heapq.heappush(tasks, (3, "low priority task"))
heapq.heappush(tasks, (1, "URGENT"))
heapq.heappush(tasks, (2, "medium task"))

print(heapq.heappop(tasks))   # (1, 'URGENT')        — smallest priority first
print(heapq.heappop(tasks))   # (2, 'medium task')
print(heapq.heappop(tasks))   # (3, 'low priority task')

# === Gotcha ===
# heappush / heappop work on a LIST. Python doesn't have a real Heap class.
# Always remember to keep the same list reference — don't reassign.
