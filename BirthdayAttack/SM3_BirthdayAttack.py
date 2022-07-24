from gmssl import sm3, func
import time
import random

hex_len = 4
bin_len = hex_len * 4
num = pow(2, bin_len // 2)
print(num)
start = time.time()
for i in range(num):
    x = str(random.randint(0,2**256))
    y = str(random.randint(0,2**256))
    a = sm3.sm3_hash(func.bytes_to_list(bytes(x, encoding = 'utf-8')))
    b = sm3.sm3_hash(func.bytes_to_list(bytes(y, encoding = 'utf-8')))
    if a[:hex_len] == b[:hex_len]:
        print("success")
        print(x)
        print(a)
        print(y)
        print(b)
        break
end = time.time()
print("It cost", end-start, "s")
print("===end===")
