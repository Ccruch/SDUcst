import time
from random import randint as rd
3start = time.time()
while 1:
    x = str(rd(0, 2**256))
    y = str(rd(0, 2**256))
    if sha(x) == sha(y):
        print(x)
        print(y)
        break
end = time.time()
print("It cost", end - start, "s")

        
