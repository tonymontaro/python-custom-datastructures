from FenwickTree import FenwickTree

lines = """5 5
1 2 3 4 5
1 0 5
1 2 4
0 3 10
1 0 5
1 0 3"""
lines = lines.split("\n")

n, q = [int(i) for i in lines[0].split()]
arr = [int(i) for i in lines[1].split()]
fenwick = FenwickTree(len(arr), arr)

for i in range(2, q + 2):
    typ, p, q = [int(j) for j in lines[i].split()]
    if typ == 0:
        fenwick.update(p + 1, q)
    else:
        print(fenwick.rangeSum(p + 1, q))