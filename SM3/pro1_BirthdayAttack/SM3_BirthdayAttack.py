from gmssl import sm3, func
import time
import random

hex_len = 4  # 碰撞比特数//4的结果（转成16进制表示时的位数）
bin_len = hex_len * 4
total = 1000  # 重复次数
num = pow(2, bin_len//2)
counter = 0
start = time.time()
for i in range(total):
    msg = []
    Hash = []
    for i in range(num):
        x = str(random.randint(0, 2**256))
        a = sm3.sm3_hash(func.bytes_to_list(bytes(x, encoding = 'utf-8')))[:hex_len]  # only highest bin_len bit
        if Hash.count(a) == 1:
            counter += 1
            break
        msg.append(x)
        Hash.append(a)

print("=========寻找最高{}-bit的碰撞=========".format(bin_len))
rate = counter / total
print("成功率：  {}".format(rate))

end = time.time()
print("{}次尝试总花费时间：{}s".format(total, end - start))
