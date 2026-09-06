class TreapMultiSet:
    """
    Randomized ordered multiset.
    Supported operations:
        add(x)
        discard(x)
        remove(x) # raises
        count(x)

        lower_bound(x)
        upper_bound(x)
        bisect_left(x)
        bisect_right(x)
        predecessor(x)
        floor(x)
        kth(k)

        minimum()
        maximum()
        len(t)
        x in t: iteration in sorted order
    """
    _MASK64 = (1 << 64) - 1
    __slots__ = ("root", "_rng_state")

    class _Node:
        __slots__ = ("key", "prio", "cnt", "size", "left", "right")

        def __init__(self, key, prio):
            self.key, self.prio, self.cnt, self.size = key, prio, 1, 1
            self.left = self.right = None

    def __init__(self, iterable=(), *, seed=None):
        if seed is None:
            from time import time_ns
            seed = time_ns() ^ id(self)
        self.root = None
        self._rng_state = seed & self._MASK64
        for x in iterable: self.add(x)

    def _size(self, t): return 0 if t is None else t.size
    def _pull(self, t): t.size = t.cnt + self._size(t.left) + self._size(t.right)

    def _rotate_right(self, y):
        x = y.left
        y.left, x.right = x.right, y
        self._pull(y)
        self._pull(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        x.right, y.left = y.left, x
        self._pull(x)
        self._pull(y)
        return y

    def _insert(self, t, key, prio):
        if t is None:
            return self._Node(key, prio)
        if key == t.key:
            t.cnt += 1
        elif key < t.key:
            t.left = self._insert(t.left, key, prio)
            if t.left.prio > t.prio:
                t = self._rotate_right(t)
        else:
            t.right = self._insert(t.right, key, prio)
            if t.right.prio > t.prio:
                t = self._rotate_left(t)
        self._pull(t)
        return t

    def _merge(self, a, b):
        if a is None or b is None:
            return a or b
        if a.prio > b.prio:
            a.right = self._merge(a.right, b)
            self._pull(a)
            return a
        b.left = self._merge(a, b.left)
        self._pull(b)
        return b

    def _erase(self, t, key):
        if t is None:
            return None, False
        if key < t.key:
            t.left, removed = self._erase(t.left, key)
        elif key > t.key:
            t.right, removed = self._erase(t.right, key)
        else:
            if t.cnt > 1:
                t.cnt -= 1
                self._pull(t)
                return t, True
            return self._merge(t.left, t.right), True
        if removed:
            self._pull(t)
        return t, removed

    def _rand64(self):
        self._rng_state = (self._rng_state + 0x9E3779B97F4A7C15) & self._MASK64
        z = self._rng_state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & self._MASK64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & self._MASK64
        return z ^ (z >> 31)

    def add(self, key): self.root = self._insert(self.root, key, self._rand64())

    def discard(self, key):
        self.root, removed = self._erase(self.root, key)
        return removed

    def remove(self, key):
        if not self.discard(key): raise KeyError(key)

    def count(self, key):
        t = self.root
        while t:
            if key < t.key:
                t = t.left
            elif key > t.key:
                t = t.right
            else:
                return t.cnt
        return 0

    def _bisect(self, key, right):
        ans, t = 0, self.root
        while t:
            if key < t.key or (key == t.key and not right):
                t = t.left
            else:
                ans += self._size(t.left) + t.cnt
                t = t.right
        return ans

    def bisect_left(self, key): return self._bisect(key, False)
    def bisect_right(self, key): return self._bisect(key, True)

    def kth(self, k):
        if k < 0 or k >= len(self):
            raise IndexError("Treap index out of range")
        t = self.root
        while t:
            left = self._size(t.left)
            if k < left:
                t = t.left
            elif k < left + t.cnt:
                return t.key
            else:
                k -= left + t.cnt
                t = t.right
        raise RuntimeError("corrupted Treap")

    def _successor(self, key, strict):
        ans, t = None, self.root
        while t:
            if t.key > key or (t.key == key and not strict):
                ans, t = t.key, t.left
            else:
                t = t.right
        return ans

    def lower_bound(self, key): return self._successor(key, False)
    def upper_bound(self, key): return self._successor(key, True)

    def _previous(self, key, inclusive):
        ans, t = None, self.root
        while t:
            if t.key < key or (t.key == key and inclusive):
                ans, t = t.key, t.right
            else:
                t = t.left
        return ans

    def predecessor(self, key): return self._previous(key, False)
    def floor(self, key): return self._previous(key, True)

    def minimum(self):
        if self.root is None:
            raise IndexError("minimum from empty Treap")
        t = self.root
        while t.left: t = t.left
        return t.key

    def maximum(self):
        if self.root is None:
            raise IndexError("maximum from empty Treap")
        t = self.root
        while t.right: t = t.right
        return t.key

    def __len__(self): return self._size(self.root)
    def __contains__(self, key): return self.count(key) > 0

    def __iter__(self):
        stack, t = [], self.root
        while stack or t:
            while t:
                stack.append(t)
                t = t.left
            t = stack.pop()
            for _ in range(t.cnt): yield t.key
            t = t.right

