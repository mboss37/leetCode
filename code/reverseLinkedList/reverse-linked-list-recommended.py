# Practice script: docs/exercise_scripts/LC206_ReverseLinkedList_practice.md

from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Three pointers walking the list:
        #   prev: the node we just reversed (initially None — the new tail)
        #   curr: the node we're currently flipping
        #   next_node: saved BEFORE we overwrite curr.next, so we don't lose the rest

        prev = None
        curr = head

        while curr:
            next_node = curr.next   # save the rest of the list
            curr.next = prev        # flip current's arrow backwards
            prev = curr             # prev moves forward
            curr = next_node        # curr moves forward

        # When curr is None, prev is the new head (old tail).
        return prev


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

print(dump(solution.reverseList(build([1, 2, 3, 4, 5]))))   # [5, 4, 3, 2, 1]
print(dump(solution.reverseList(build([1, 2]))))             # [2, 1]
print(dump(solution.reverseList(build([]))))                  # []
print(dump(solution.reverseList(build([42]))))                # [42]
