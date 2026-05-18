# Practice script: docs/exercise_scripts/LC155_MinStack_practice.md

class MinStack:
    """
    Stack supporting O(1) push, pop, top, AND getMin.

    Key idea — auxiliary "min stack" running in parallel with the main stack.
    At every level i, minStack[i] = min of stack[0..i]. Pop both together,
    push both together — they stay synchronized.
    """

    def __init__(self):
        # Two stacks, both start empty. Each instance has its own.
        self.stack = []      # main values
        self.minStack = []   # running minimum at each level

    def push(self, val: int) -> None:
        self.stack.append(val)
        # Compute the new minimum for this level.
        # If minStack has items, new_min = min(val, current_min).
        # If minStack is empty (first push), new_min = val.
        if self.minStack:
            val = min(val, self.minStack[-1])
        self.minStack.append(val)

    def pop(self) -> None:
        # Always pop BOTH stacks together — they're synchronized.
        self.stack.pop()
        self.minStack.pop()

    def top(self) -> int:
        # Peek main stack's top.
        return self.stack[-1]

    def getMin(self) -> int:
        # Peek minStack's top — this is the running min for the current state.
        return self.minStack[-1]


# ============= TEST CASES =============

ms = MinStack()
ms.push(-2)
ms.push(0)
ms.push(-3)
print(ms.getMin())   # -3
ms.pop()
print(ms.top())      # 0
print(ms.getMin())   # -2

# Edge: single element
ms2 = MinStack()
ms2.push(5)
print(ms2.top())     # 5
print(ms2.getMin())  # 5
ms2.pop()
# main stack and minStack are now both empty

# Edge: pushing increasing then popping all
ms3 = MinStack()
ms3.push(1)
ms3.push(2)
ms3.push(3)
print(ms3.getMin())  # 1
ms3.pop()
print(ms3.getMin())  # 1 (still — 1 was the floor)
ms3.pop()
print(ms3.getMin())  # 1
