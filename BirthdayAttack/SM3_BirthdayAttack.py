import downloadSM3
import random
import time

start = time.time()
while 1:
    x = str(random.randint(0,2**256))
    y = str(random.randint(0,2**256))
    if eSM3(x)==eSM3(y):
        print(x)
        print(y)
        break
end = time.time()
print("It cost", end-start, "s")
print("===end===")
