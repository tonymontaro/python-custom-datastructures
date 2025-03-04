class SegmentTree:
    def __init__(self, left, right, arr):
        self.left = left
        self.right = right
        self.sum = 0

        if left == right:
            self.sum = arr[left]
        else:
            mid = (left + right) // 2
            self.leftChild = SegmentTree(left, mid, arr)
            self.rightChild = SegmentTree(mid + 1, right, arr)
            self.reCalculate()

    def reCalculate(self):
        if self.left != self.right:
            self.sum = self.leftChild.sum + self.rightChild.sum
    
    def rangeSum(self, left, right):
        if left > self.right or right < self.left:
            return 0
        if self.left >= left and self.right <= right:
            return self.sum
        return self.leftChild.rangeSum(left, right) + self.rightChild.rangeSum(left, right)
    
    def update(self, idx, valueToAdd):
        if self.left > idx or self.right < idx:
            return
        if self.left == self.right:
            self.sum += valueToAdd
        else:
            self.leftChild.update(idx, valueToAdd)
            self.rightChild.update(idx, valueToAdd)
            self.reCalculate()
