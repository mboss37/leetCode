# Practice script: docs/exercise_scripts/LC424_LongestRepeatingCharReplacement_practice.md

from collections import defaultdict


class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        # Sliding window with max-count tracker.
        # Window is VALID iff (window_size - max_count) <= k.
        # That's the number of "non-majority" chars we'd need to replace.

        counts = defaultdict(int)
        left = 0
        best = 0
        max_count = 0  # count of the most frequent char in the current window

        for right in range(len(s)):
            counts[s[right]] += 1
            max_count = max(max_count, counts[s[right]])

            # Window invariant violated → shrink from the left.
            while (right - left + 1) - max_count > k:
                counts[s[left]] -= 1
                left += 1
                # Note: max_count isn't decremented on shrink. Stale max only
                # affects best monotonically — best only grows, so no impact.

            best = max(best, right - left + 1)

        return best


# ============= TEST CASES =============
solution = Solution()

print(solution.characterReplacement("ABAB", 2))         # 4  (replace both A's with B, or both B's with A)
print(solution.characterReplacement("AABABBA", 1))      # 4  ("AABA" or "ABBB")
print(solution.characterReplacement("ABCDE", 1))        # 2
print(solution.characterReplacement("AAAA", 2))         # 4
print(solution.characterReplacement("ABAA", 0))         # 2  (no replacements allowed, "AA")
