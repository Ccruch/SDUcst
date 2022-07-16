from hashlib import sha256
import imp
from random import randint
from math import sqrt

A = 0
B = 7
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337


def SHA256(s):
    """string -> hexdigest"""
    msg = bytes(bytearray(s, encoding='utf-8'))
    return sha256(msg).hexdigest()


def inv(a, n):
    '''求逆'''
    def ext_gcd(a, b, arr):
        '''扩欧'''
        if b == 0:
            arr[0] = 1
            arr[1] = 0
            return a
        g = ext_gcd(b, a%b, arr)
        t = arr[0]
        arr[0] = arr[1]
        arr[1] = t-int(a/b)*arr[1]
        return g
    arr = [0,1,]
    gcd = ext_gcd(a, n, arr)
    if gcd == 1:
        return (arr[0]%n+n)%n
    else:
        return -1

def EC_add(p, q):
    """椭圆曲线加法"""
    # 0 means inf
    if p == 0 and q == 0: return 0  # 0 + 0 = 0
    elif p == 0: return q  # 0 + q = q
    elif q == 0: return p  # p + 0 = p
    else:
        if p[0] == q[0]:  
            if (p[1] + q[1]) % P == 0: return 0  # mutually inverse
            elif p[1] == q[1]: return EC_double(p)
        elif p[0] > q[0]:  # swap if px > qx
            tmp = p
            p = q
            q = tmp
        r = []
        slope = (q[1] - p[1]) * inv(q[0] - p[0], P) % P  # 斜率
        r.append((slope ** 2 - p[0] - q[0]) % P)
        r.append((slope * (p[0] - r[0])- p[1]) % P)
        return (r[0], r[1])

def EC_inv(p):
    """椭圆曲线逆元"""
    r = [p[0]]
    r.append(P - p[1])
    return r

def EC_sub(p, q):
    """椭圆曲线减法：p - q"""
    q_inv = EC_inv(q)
    return EC_add(p, q_inv)


def EC_double(p):
    """椭圆曲线双倍点运算"""
    r = []
    slope = (3 * p[0] ** 2 + A) * inv(2 * p[1], P) % P
    r.append((slope ** 2 - 2 * p[0]) % P)
    r.append((slope * (p[0] - r[0]) - p[1]) % P)
    return (r[0], r[1])


def msg_to_dot(msg):
    def Legendre(y,p): 
        return pow(y,(p - 1) // 2,p)
    def msg_to_x(m):
        """消息转换成横坐标"""
        mdigest = SHA256(m)
        while 1:  # cycle until x belong to QR
            x = int(mdigest, 16)
            if Legendre(x, P):
                break
            mdigest = SHA256(mdigest)
        return x
    def get_y(x):  # Cipolla's algorithm : y^2 = x^3 + 7 mod P
        """y ** 2 = x ** 3 + 7
        已知横坐标，计算纵坐标"""
        right = (x ** 3 + 7) % P
        while 1:
            a = randint(0, P)
            if Legendre(a, P) == -1:
                break
        base = int(a + sqrt(a ** 2 - right))
        expo = (P + 1) // 2
        y = pow(base, expo, P)
        return y
    x = msg_to_x(msg)
    y = get_y(x)
    return (x, y)


# MultiSet Hash -> EC combine/add/remove
def ADD(ecmh, msg):
    dot = msg_to_dot(msg)
    tmp = EC_add(ecmh, dot)
    return tmp

def single(msg):
    return ADD(0, msg)

def remove(ecmh, msg):
    dot = msg_to_dot(msg)
    tmp = EC_sub(ecmh, dot)
    return tmp

def combine(msg_set):
    ans = single(msg_set[0])
    num = len(msg_set) - 1
    for i in range(num):
        ans = ADD(ans, msg_set[i+1])
    return ans


m1 = "i"
m2 = "love"
m3 = "you"
m11 = [m1, m1]
m12 = [m1, m2]
m13 = [m1, m3]
m21 = [m2, m1]
m123 = [m1, m2, m3]
m132 = [m1, m3, m2]
m231 = [m2, m3, m1]
m321 = [m3, m2, m1]


print('========= duplicate elements=========')
print('hash for m1:\n', single(m1))
print('hash for m1_and_m1:\n', combine(m11))

print('\n========= add =========')
print('hash for m1:\n', single(m1))
print('hash for m2:\n', single(m2))
print('hash for m1_and_m2:\n', combine(m12))
print('h1 add h2:\n',ADD(single(m1), m2))

print('\n========= remove =========')
print('hash for m1_and_m2_and_m3:\n', combine(m123))
print('hash for m1_and_m2:\n', combine(m12))
print('h123 sub h3:\n',remove(combine(m123), m3))

print('\n========= order does not matter =========')
print('hash for m2_and_m3_and_m1:\n', combine(m231))
print('hash for m3_and_m2_and_m1:\n', combine(m321))






