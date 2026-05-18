# Practice script: docs/exercise_scripts/LC1768_MergeStringsAlternately_practice.md


class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        # Two pointers walking both strings together. Take one from each per
        # round. When one runs out, append the tail of the other.
        #
        # Python slicing makes the tail-append trivial: word[i:] is empty
        # when i is past the end, so we can unconditionally append both tails.

        out = []
        i, j = 0, 0

        while i < len(word1) and j < len(word2):
            out.append(word1[i])
            out.append(word2[j])
            i += 1
            j += 1

        out.append(word1[i:])   # safe: empty if i == len(word1)
        out.append(word2[j:])

        return "".join(out)


# ============= TEST CASES =============
solution = Solution()

print(solution.mergeAlternately("abc", "pqr"))     # "apbqcr"
print(solution.mergeAlternately("ab", "pqrs"))     # "apbqrs"
print(solution.mergeAlternately("abcd", "pq"))     # "apbqcd"
print(solution.mergeAlternately("", "xyz"))         # "xyz"
print(solution.mergeAlternately("xyz", ""))         # "xyz"
print(solution.mergeAlternately("a", "b"))          # "ab"
