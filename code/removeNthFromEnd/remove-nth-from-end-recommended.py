# Practice script: docs/exercise_scripts/LC19_RemoveNthFromEnd_practice.md

from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # Two-pointer trick: keep a gap of n between fast and slow.
        # When fast walks off the end, slow is positioned RIGHT BEFORE the
        # node we want to remove.
        #
        # A dummy node before head handles the edge case where we remove
        # the actual head — no special-casing needed.

        dummy = ListNode(0, head)
        slow = fast = dummy

        # Move fast n+1 steps ahead so the gap between slow and fast is n+1.
        # That way when fast.next is None, slow is at the node BEFORE the target.
        for _ in range(n):
            fast = fast.next

        # Walk both pointers together until fast hits the last node.
        while fast.next:
            slow = slow.next
            fast = fast.next

        # slow.next is the node to remove. Skip over it.
        slow.next = slow.next.next

        return dummy.next


# ============= TEST HELPERS =============
def build(values):
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def dump(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


# ============= TEST CASES =============
solution = Solution()

print(dump(solution.removeNthFromEnd(build([1, 2, 3, 4, 5]), 2)))   # [1, 2, 3, 5]
print(dump(solution.removeNthFromEnd(build([1]), 1)))                # []
print(dump(solution.removeNthFromEnd(build([1, 2]), 1)))             # [1]
print(dump(solution.removeNthFromEnd(build([1, 2]), 2)))             # [2]
print(dump(solution.removeNthFromEnd(build([1, 2, 3]), 3)))          # [2, 3]
