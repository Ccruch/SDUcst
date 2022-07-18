import time
from hashlib import sha256
from random import randint as rd
start = time.time()

def sha(s):
    msg = bytes(bytearray(s, encoding = 'utf-8'))
    return sha256(msg).hexdigest()


x = '26546752986922089874801109887172314271845319137021902205497137397151572602836'
print(sha(x))
#sha(x) == 'bfd5202ce321a191047df931748bfadd8ab9ab01d698503b4eaff0f79d6cba8d'

y = '50996638151691999201732257994496132372435011205364243468022568721871895544628'
print(sha(y))
#sha(y) == 'bfd5202c62fe1d346d87e5f5530a81184c8fe370c50f06578721e6ff69d0468a'

while 1:
    x = str(rd(0, 2**256))
    y = str(rd(0, 2**256))
    if sha(x)[:8] == sha(y)[:8]:
        print(x)
        print(y)
        break
end = time.time()
print("It cost", end - start, "s")
