# Practice script: docs/exercise_scripts/LC359_LoggerRateLimit_practice.md


class Logger:
    """Print a message only if it hasn't been printed in the last 10 seconds.

    Cheapest approach: remember the LAST time each message was printed.
    No queues, no heaps. Just a dict.

    Trade-off: dict grows forever (one entry per unique message).
    Fine for the LeetCode constraints; in production you'd evict old entries.
    """

    def __init__(self):
        self.last_seen: dict[str, int] = {}

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        prev = self.last_seen.get(message)
        if prev is not None and timestamp - prev < 10:
            return False
        self.last_seen[message] = timestamp
        return True


# ============= TEST CASES =============
logger = Logger()
print(logger.shouldPrintMessage(1, "foo"))    # True
print(logger.shouldPrintMessage(2, "bar"))    # True
print(logger.shouldPrintMessage(3, "foo"))    # False  (3 - 1 = 2 < 10)
print(logger.shouldPrintMessage(8, "bar"))    # False  (8 - 2 = 6 < 10)
print(logger.shouldPrintMessage(10, "foo"))   # False  (10 - 1 = 9 < 10)
print(logger.shouldPrintMessage(11, "foo"))   # True   (11 - 1 = 10, NOT < 10)
