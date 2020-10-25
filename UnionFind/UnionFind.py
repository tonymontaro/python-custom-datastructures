class UnionFind:
    """
    UnionFind or DisjoinSet data-structure with Path compression. Zero indexed.

    Initialize:
        UnionFind(n)
    Methods:
        unify(p, q)        # unify p and q
        connected(p, q)    # is p connected to q (return bool)
        find(p)            # find the parent of q
        getSize(p)         # return the group size of p
    """
    def __init__(self, n):
        self.size = n
        self.groups = n
        self.sizes = [0] * n
        self.parents = [0] * n
        
        for i in range(n):
            self.parents[i] = i
            self.sizes[i] = 1
    def find(self, p):
        root = p
        while (root != self.parents[root]):
            root = self.parents[root]
        # path compression
        while (p != root):
            p, self.parents[p] = self.parents[p], root
        return root
    def getSize(self, p):
        return self.sizes[self.find(p)]
    def connected(self, p, q):
        return self.find(p) == self.find(q)
    def unify(self, p, q):
        root1 = self.find(p)
        root2 = self.find(q)
        if root1 == root2:
            return
        if self.sizes[root1] < self.sizes[root2]:
            self.parents[root1] = root2
            self.sizes[root2] += self.sizes[root1]
        else:
            self.parents[root2] = root1
            self.sizes[root1] += self.sizes[root2]
        self.groups -= 1
