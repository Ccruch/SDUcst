from inspect import formatargspec
import random
import time

#-------以下函数也可用于其它算法中---------
def rotation_left(x, num):
    # 循环左移
    num %= 32
    left = (x << num) % (2 ** 32)
    right = (x >> (32 - num)) % (2 ** 32)
    result = left ^ right
    return result

def Int2Bin(x, k):
    x = str(bin(x)[2:])
    result = "0" * (k - len(x)) + x
    return result

#-------以上函数也可用于其余算法中-----------

class SM3:

    def __init__(self):
        # 常量初始化
        self.IV = [0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600, 0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E]
        self.T = [0x79cc4519, 0x7a879d8a]
        self.maxu32 = 2 ** 32
        self.w1 = [0] * 68
        self.w2 = [0] * 64

    def ff(self, x, y, z, j):
        # 布尔函数FF
        result = 0
        if j < 16:
            result = x ^ y ^ z
        elif j >= 16:
            result = (x & y) | (x & z) | (y & z)
        return result

    def gg(self, x, y, z, j):
        # 布尔函数GG
        result = 0
        if j < 16:
            result = x ^ y ^ z
        elif j >= 16:
            result = (x & y) | (~x & z)
        return result

    def p(self, x, mode):
        result = 0
        # 置换函数P
        # 输入参数X的长度为32bit(=1个字)
        # 输入参数mode共两种取值：0和1
        if mode == 0:
            result = x ^ rotation_left(x, 9) ^ rotation_left(x, 17)
        elif mode == 1:
            result = x ^ rotation_left(x, 15) ^ rotation_left(x, 23)
        return result

    def sm3_fill(self, msg):
        # 填充消息，使其长度为512bit的整数倍
        # 输入参数msg为bytearray类型
        # 中间参数msg_new_bin为二进制string类型
        # 输出参数msg_new_bytes为bytearray类型
        length = len(msg)   # msg的长度（单位：byte）
        l = length * 8      # msg的长度（单位：bit）

        num = length // 64
        remain_byte = length % 64
        msg_remain_bin = ""
        msg_new_bytes = bytearray((num + 1) * 64)  ##填充后的消息长度，单位：byte
                                                   ##全0

        # 将原数据存储至msg_new_bytes中
        for i in range(length):
            msg_new_bytes[i] = msg[i]

        # remain部分以二进制字符串形式存储
        remain_bit = remain_byte * 8     #单位：bit
        for i in range(remain_byte):
            msg_remain_bin += "{:08b}".format(msg[num * 64 + i])

        k = (448 - l - 1) % 512
        while k < 0:
            # k为满足 l + k + 1 = 448 % 512 的最小非负整数
            k += 512

        msg_remain_bin += "1" + "0" * k + Int2Bin(l, 64)

        for i in range(0, 64 - remain_byte):
            str = msg_remain_bin[i * 8 + remain_bit: (i + 1) * 8 + remain_bit]
            temp = length + i
            msg_new_bytes[temp] = int(str, 2) #将2进制字符串按byte为组转换为整数
        return msg_new_bytes

    def sm3_msg_extend(self, msg):
        # 扩展函数: 将512bit的数据msg扩展为132个字（w1共68个字，w2共64个字）
        # 输入参数msg为bytearray类型,长度为512bit=64byte
        for i in range(0, 16):
            self.w1[i] = int.from_bytes(msg[i * 4:(i + 1) * 4], byteorder="big")

        for i in range(16, 68):
            self.w1[i] = self.p(self.w1[i-16] ^ self.w1[i-9] ^ rotation_left(self.w1[i-3], 15), 1) ^ rotation_left(self.w1[i-13], 7) ^ self.w1[i-6]

        for i in range(64):
            self.w2[i] = self.w1[i] ^ self.w1[i+4]

        # 测试扩展数据w1和w2
        # print("w1:")
        # for i in range(0, len(self.w1), 8):
        #     print(hex(self.w1[i]))
        # print("w2:")
        # for i in range(0, len(self.w2), 8):
        #     print(hex(self.w2[i]))

    def sm3_compress(self,iv,msg):
        # 压缩函数
        # 输入参数v为初始化参数，类型为bytes/bytearray，大小为256bit
        # 输入参数msg为512bit的待压缩数据

        self.sm3_msg_extend(msg)
        ss1 = 0

        A = iv[0]
        B = iv[1]
        C = iv[2]
        D = iv[3]
        E = iv[4]
        F = iv[5]
        G = iv[6]
        H = iv[7]

        for j in range(64):
            if j < 16:
                ss1 = rotation_left((rotation_left(A, 12) + E + rotation_left(self.T[0], j)) % self.maxu32, 7)
            elif j >= 16:
                ss1 = rotation_left((rotation_left(A, 12) + E + rotation_left(self.T[1], j)) % self.maxu32, 7)
            ss2 = ss1 ^ rotation_left(A, 12)
            tt1 = (self.ff(A, B, C, j) + D + ss2 + self.w2[j]) % self.maxu32
            tt2 = (self.gg(E, F, G, j) + H + ss1 + self.w1[j]) % self.maxu32
            D = C
            C = rotation_left(B, 9)
            B = A
            A = tt1
            H = G
            G = rotation_left(F, 19)
            F = E
            E = self.p(tt2, 0)

            # 测试IV的压缩中间值
            # print("j= %d：" % j, hex(A)[2:], hex(B)[2:], hex(C)[2:], hex(D)[2:], hex(E)[2:], hex(F)[2:], hex(G)[2:], hex(H)[2:])

        iv[0] ^= A
        iv[1] ^= B
        iv[2] ^= C
        iv[3] ^= D
        iv[4] ^= E
        iv[5] ^= F
        iv[6] ^= G
        iv[7] ^= H

        r = []
        for i in range(8):
            r.append(iv[i])
        return r

    def sm3_update(self, msg):
        # 迭代函数
        # 输入参数msg为bytearray类型
        # msg_new为bytearray类型
        msg_new = self.sm3_fill(msg)   # msg_new经过填充后一定是512的整数倍
        n = len(msg_new) // 64         # n是整数，n>=1

        for i in range(0, n):
            self.sm3_compress(self.IV, msg_new[i * 64:(i + 1) * 64])

    def sm3_final(self):
        digest_str = ""
        for i in range(len(self.IV)):
            digest_str += hex(self.IV[i])[2:].rjust(8, '0')

        return digest_str.upper()

def eSM3(s):
    """SM3
    :param: s is string
    :return: 256-bit hex string
    """
    test = SM3()
    msg = bytearray(s,encoding = 'utf-8')
    msg = bytes(msg)
    test.sm3_update(msg)
    return test.sm3_final()

def fill(s):
    """fill
    :param s: (string)
    :return: (bytearray)
    """
    test = SM3()
    s = bytes(bytearray(s, encoding='utf-8'))
    return test.sm3_fill(s)

def forged_SM3(origin_msg, append_msg):
    """forge hash of SM3"""
    def forged_fill(origin_len, msg):
        """forged filling
        :param origin_len: length of origin massage
        :param msg: append_msg
        :return: 
        """
        msg = bytes(bytearray(msg, encoding='utf-8'))
        length = len(msg)   # msg的长度（单位：byte）
        origin_padding_len = ((origin_len // 64) + 1) * 64
        l = (length + origin_padding_len) * 8      # msg的长度（单位：bit）

        num = length // 64
        remain_byte = length % 64
        msg_remain_bin = ""
        msg_new_bytes = bytearray((num + 1) * 64)  ##填充后的消息长度，单位：byte
                                                   ##全0

        # 将原数据存储至msg_new_bytes中
        for i in range(length):
            msg_new_bytes[i] = msg[i]

        # remain部分以二进制字符串形式存储
        remain_bit = remain_byte * 8     #单位：bit
        for i in range(remain_byte):
            msg_remain_bin += "{:08b}".format(msg[num * 64 + i])

        k = (448 - l - 1) % 512
        while k < 0:
            # k为满足 l + k + 1 = 448 % 512 的最小非负整数
            k += 512

        msg_remain_bin += "1" + "0" * k + Int2Bin(l, 64)

        for i in range(0, 64 - remain_byte):
            str = msg_remain_bin[i * 8 + remain_bit: (i + 1) * 8 + remain_bit]
            temp = length + i
            msg_new_bytes[temp] = int(str, 2) #将2进制字符串按byte为组转换为整数
        return msg_new_bytes
    
    origin_hash = eSM3(origin_msg)
    test = SM3()
    origin_len = len(origin_msg)
    tmp = forged_fill(origin_len, append_msg)  # 512-bit == 64bytes
    oh = []
    for i in range(8):
        oh.append(int(origin_hash[8 * i:8 * (i + 1)], 16))
    v = 0
    for i in range(0, len(tmp) // 64):
        if i == 0:
            v = test.sm3_compress(oh, tmp[:64])
        else:
            v = test.sm3_compress(v, tmp[64 * i:64 * (i + 1)])
    r = []
    for i in range(8):
        r.append(hex(v[i])[2:].rjust(8, '0'))
    return (''.join(r)).upper()
     


def forge_msg(origin_msg, append_msg):
    return fill(origin_msg) + bytes(bytearray(append_msg, encoding='utf-8'))

def f_sm3(forged_msg):
    test = SM3()
    test.sm3_update(forged_msg)
    return test.sm3_final()
    

if __name__ == "__main__":
    a = "dBHJKDVFCH55555555555555555555222222222222222222200000000000000000000"
    b = "45ewfq6453478541523786563453756123514356468544564548967468758crtfghcxghmbv jnc vhjg"
    print("origin massage:", bytes(bytearray(a, encoding='utf-8')))
    print("appand massage:", bytes(bytearray(b, encoding='utf-8')))

    re = forged_SM3(a, b)
    print("forged hash:    ", re)

    forged_msg = forge_msg(a, b)
    print("forged massage: ", forged_msg)

    length_attack = f_sm3(forged_msg)
    if(length_attack == re):print("successful attack? Ture")
    else:print("Successful attack? False")





