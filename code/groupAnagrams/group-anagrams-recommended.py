# Practice script: docs/exercise_scripts/LC49_GroupAnagrams_practice.md

from collections import defaultdict
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # The "anagrams share a canonical key" pattern.
        # Anagrams produce the same sorted string → group them under that key.
        # defaultdict(list) auto-creates the bucket on first sight.

        groups = defaultdict(list)

        for s in strs:
            # Sort the characters to get a canonical anagram key.
            # ''.join(sorted(s)) converts the sorted list of chars back to a string.
            key = ''.join(sorted(s))
            groups[key].append(s)

        # Return the values (the actual groups). Order doesn't matter per spec.
        return list(groups.values())


# ===== Alternative: count-tuple key (asymptotically faster) =====
#
# Skips the sort by using a 26-element count array as the key.
# Time: O(n · k) — strictly better than O(n · k log k) above.
# Use this if interviewer asks "can you make it faster?"
# Tied to lowercase a-z; sort version is more general.
#
# class Solution:
#     def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
#         groups = defaultdict(list)
#         for s in strs:
#             counts = [0] * 26
#             for c in s:
#                 counts[ord(c) - ord('a')] += 1
#             groups[tuple(counts)].append(s)
#         return list(groups.values())


# ============= TEST CASES =============
solution = Solution()

print(solution.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# Expected (any order): [["eat","tea","ate"], ["tan","nat"], ["bat"]]

print(solution.groupAnagrams([""]))
# Expected: [[""]]

print(solution.groupAnagrams(["a"]))
# Expected: [["a"]]

print(solution.groupAnagrams(["act", "pots", "tops", "cat", "stop", "hat"]))
# Expected (any order): [["act","cat"], ["pots","tops","stop"], ["hat"]]

print(solution.groupAnagrams(["abc", "bca", "cab", "xyz", "zyx", "yxz", "no"]))
# Expected (any order): [["abc","bca","cab"], ["xyz","zyx","yxz"], ["no"]]
