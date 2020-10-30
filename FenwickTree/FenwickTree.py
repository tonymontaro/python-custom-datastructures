class FenwickTree:
    """One indexed FenwickTree (Binary Indexed Tree)"""
    def __init__(self, n, arr=[]):
        self.tree = [0] * (n + 1)
        self.n = n
        if arr:
            for i in range(1, n + 1):
                self.tree[i] += arr[i - 1]
                parent = i + (i & -i)
                if (parent <= n):
                    self.tree[parent] += self.tree[i]
    
    def getSum(self, idx):
        total = 0
        while idx > 0:
            total += self.tree[idx]
            idx = idx - (idx & -idx)
        return total
    
    def rangeSum(self, a, b):
        # a - b inclusive: b > a 
        return self.getSum(b) - self.getSum(a - 1)
    
    def update(self, idx, valueToAdd):
        while idx <= self.n:
            self.tree[idx] += valueToAdd
            idx = idx + (idx & -idx)