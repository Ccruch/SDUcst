import time
from hashlib import sha256
from random import randint as rd
start = time.time()

def sha(s):
    msg = bytes(bytearray(s, encoding = 'utf-8'))
    return sha256(msg).hexdigest()

while 1:
    x = str(rd(0, 2**256))
    y = str(rd(0, 2**256))
    if sha(x) == sha(y):
        print(x)
        print(y)
        break
end = time.time()
print("It cost", end - start, "s")
