from UnionFind import UnionFind

lines = """4 7
1 0 1
0 0 1
0 2 3
1 0 1
1 1 2
0 0 2
1 1 3"""
lines = lines.split("\n")
n, q = [int(i) for i in lines[0].split()]
n, q
disjoint = UnionFind(n)
for i in range(1, q + 1):
    typ, p, q = [int(j) for j in lines[i].split()]
    if typ == 0:
        disjoint.unify(p, q)
    else:
        print(1 if disjoint.connected(p, q) else 0)