# Idiom: collections.deque
# Use: a double-ended queue. O(1) append AND pop from BOTH ends.
# Why use it: a regular list is O(n) for pop(0) and insert(0, x) — slow at the front.
#             deque is O(1) at both ends, perfect for BFS and sliding window.
# Canonical form:
#     from collections import deque
#     dq = deque()
#     dq.append(x)         -> add to right end (same as list.append)
#     dq.appendleft(x)     -> add to LEFT end
#     dq.pop()             -> remove from right end
#     dq.popleft()         -> remove from LEFT end (this is the killer feature)

from collections import deque

# === Basic operations ===

dq = deque()
dq.append(1)        # [1]
dq.append(2)        # [1, 2]
dq.append(3)        # [1, 2, 3]
dq.appendleft(0)    # [0, 1, 2, 3]
print(dq)           # deque([0, 1, 2, 3])

print(dq.pop())     # 3   — from right
print(dq.popleft()) # 0   — from left
print(dq)           # deque([1, 2])

# === Initialize from an iterable ===

dq = deque([1, 2, 3, 4])
print(dq)           # deque([1, 2, 3, 4])

# === Why not just use a list? ===

# list.pop(0) is O(n) — it has to shift all the remaining elements left.
# deque.popleft() is O(1) — internal doubly-linked structure.

# For BFS (LC 102 Level Order Traversal, etc.) and any "process a queue" pattern,
# always use deque.

# === BFS template using deque ===

# graph = {0: [1, 2], 1: [3], 2: [3], 3: []}
graph = {0: [1, 2], 1: [3], 2: [3], 3: []}

def bfs(start):
    visited = set([start])
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()      # O(1) — the whole reason we use deque
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

print(bfs(0))   # [0, 1, 2, 3]

# === Bounded deque (fixed size) ===

# A deque with maxlen drops elements from the OPPOSITE end when full.
# Great for rolling windows.
dq = deque(maxlen=3)
for n in [1, 2, 3, 4, 5]:
    dq.append(n)
    print(dq)
# After each append:
# deque([1], maxlen=3)
# deque([1, 2], maxlen=3)
# deque([1, 2, 3], maxlen=3)
# deque([2, 3, 4], maxlen=3)        — 1 dropped from left
# deque([3, 4, 5], maxlen=3)        — 2 dropped from left

# === Sliding window with deque (advanced) ===

# Maximum in each window of size k (LC 239):
# Keep a deque of INDICES, monotonically decreasing values.
# Used for O(n) sliding window max — faster than a heap (O(n log k)).
# This is a Phase B problem; pattern reference here.

# === Gotcha ===

# deque doesn't support random indexing efficiently.
# dq[5] works but is O(n) — internal walk.
# If you need indexing, use a regular list.
