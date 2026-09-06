from .TreapMultiSet import TreapMultiSet

# question: https://leetcode.com/problems/range-module

class RangeModule:
    def __init__(self):
        self.treap = TreapMultiSet()  # (end, start)

    def addRange(self, left: int, right: int) -> None:
        lower = self.treap.lower_bound((left, -1))
        if lower and lower[1] <= right:
            left = min(left, lower[1])
            right = max(right, lower[0])
            self.treap.discard(lower)
            self.addRange(left, right)
            return
        self.treap.add((right, left))

    def queryRange(self, left: int, right: int) -> bool:
        lower = self.treap.lower_bound((left, -1))
        return bool(lower and (left >= lower[1]) and (right <= lower[0]))

    def removeRange(self, left: int, right: int) -> None:
        lower = self.treap.lower_bound((left, left))
        if (not lower) or lower[1] >= right:
            return
        self.treap.discard(lower)
        if right < lower[0]:
            self.treap.add((lower[0], right))
        if lower[1] < left:
            self.treap.add((left, lower[1]))
        self.removeRange(left, right)
