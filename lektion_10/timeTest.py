import time
import random

l = [random.randint(1, 100000) for i in range(100000000)]

start = time.time()
sort = sorted(l)
print(f"sorted() time: {time.time()-start}")


start = time.time()
l.sort()
print(f"List.sort() time: {time.time()-start}")