from gmssl import sm3, func
from random import randint as ri
import time

b_len = 16
h_len = b_len // 4

def rho_attack():
    x = str(ri(0, pow(2, b_len)))  # randomly generate a number
    msg1 = x  # 0->1->2->3
    a = sm3.sm3_hash(func.bytes_to_list(bytes(msg1, encoding='utf-8')))
    msg2 = a  # 0->2->4
    b = sm3.sm3_hash(func.bytes_to_list(bytes(msg2, encoding='utf-8')))
    while a[:h_len] != b[:h_len]:
        msg1 = a
        msg2 = sm3.sm3_hash(func.bytes_to_list(bytes(b, encoding='utf-8')))
        a = sm3.sm3_hash(func.bytes_to_list(bytes(msg1, encoding='utf-8')))
        b = sm3.sm3_hash(func.bytes_to_list(bytes(msg2, encoding='utf-8')))
    print("Collision of highest", b_len, "-bit:", a[:h_len])
    print("\nmsg1:", msg1)
    print("hash of msg1:", a)
    print("\nmsg2:", msg2)
    print("hash of msg2:", b)

if __name__ == '__main__':
    start = time.time()
    rho_attack()
    end = time.time()
    print("\nIt cost", end - start, "s")
