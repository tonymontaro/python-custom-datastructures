# collections
from collections import Counter, defaultdict, deque

str1 = "abcde"
count = Counter(str1)

int_default_dict = defaultdict(int) # default value is 0
int_val_default_dict = defaultdict(lambda : 76) # default value is 76
list_default_dict = defaultdict(list) # default value is []
int_val_default_dict['key'] = 100

dq = deque()
dq.append(1)
dq.append(2)
dq.append(3)
dq.pop()
dq.popleft()


# character to number and vice versa
charNum = ord('a')
char = chr(97)


from functools import cache, lru_cache 

# cache == lru_cache(maxsize=None)

@cache
def fib(n):
    if n < 2:
        return n 
    return fib(n-1) + fib(n-1)


# Priority Queue
from heapq import heappush, heappop

heap = []
heappush(heap, 32)
heappush(heap, 2)
heappush(heap, 8)
heappush(heap, 22)
while heap:
    val = heappop(heap)
    print(val)