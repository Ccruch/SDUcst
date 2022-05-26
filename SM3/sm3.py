def fill(s):
    '''消息填充'''
    # transfer to bin
    s_bin=''
    for each in s:
        ascii_each = ord(each)
        s_bin = s_bin + '0' + bin(ascii_each)[2:]
    # add 1
    length = len(s_bin)
    s_bin += '1'
    # add 0
    while len(s_bin) % 512 != 448:
        s_bin += '0'
    length_bin = bin(length)[2:]

    while len(length_bin) < 64:
        length_bin = '0' + length_bin
    s_bin = s_bin + length_bin
    return s_bin

def iteration(m, w):
    '''消息迭代'''
    IV = {}
    IV[0] = '7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
    length = len(m)
    n = length//512
    b = {}
    for i in range(n):
        b[i] = m[512 * i:512 * (i + 1)]
        w = expand(b[i])
        IV[i + 1] = compress(w, IV[i])
    return IV[n]

def mod32(a, b):
    ''' 先+ 再mod'''
    c = a + b
    d = c % (2 ** 32)
    ans = str(d)
    return ans

def shiftL(s, num):
    '''循环左移num位'''
    text = str(s)
    return (text[num:] + text[:num])

def XOR(s, t):
    '''0 1 字符串异或'''
    if len(s) != len(t):
        print('len(s)!=len(t)')
        return False
    n = len(s)
    ans = []
    for i in range(n):
        ans.append(str(int(s[i])^int(t[i])))
    A = ''.join(ans)
    return A

def XOR3(a, b, c):
    ''' 三个异或'''
    return XOR(XOR(a, b), c)

def OR(s, t):
    ''' 字符串或运算'''
    ans = ''
    if len(s) != len(t):
        print('len(s)!=len(t)')
        return False
    for i in range(len(s)):
        if(s[i] == '1') | (t[i] == '1'):
            ans += '1'
        else:
            ans += '0'
    return ans

def OR3(a, b, c):
    '''三个或'''
    return OR(OR(a, b), c)

def AND(a, b):
    '''字符串与'''
    ans = ''
    if len(a) != len(b):
        print('len(a)!=len(b)')
        return False
    for i in range(len(a)):
        if (a[i] == '1') & (b[i] == '1'):
            ans += '1'
        else:
            ans += '0'
    return ans


def AND3(a, b, c):
    return AND(AND(a, b), c)


def NOT(a):
    '''字符串非'''
    ans = ''
    for ch in a:
        if ch == '1':
            ans += '0'
        else:
            ans += '1'
    return ans

def substitute(x, mode):
    '''置换函数'''
    if mode == 0:
        ans = XOR3(x, shiftL(x, 9), shiftL(x, 17))
    else:
        ans = XOR3(x, shiftL(x, 15), shiftL(x, 23))
    return ans

def z_h(text):
    ''' 进制转换'''
    text = str(text)
    while len(text) < 32:
        text = '0' + text
    text_16=''
    for i in range(8):
        tmp = hex(int(text[4 * i:4 * (i + 1)], base = 2))[2:]
        text_16 += tmp
    return text_16

def b_h(text):
    text = str(text)
    while len(text) < 32:
        text = '0' + text
    text_16 = ''
    for i in range(len(text) // 4):
        tmp = hex(int(text[4 * i:4 * (i + 1)], base = 2))[2:]
        text_16 += tmp
    return text_16

def h_b(text):
    text_2 = ''
    text = str(text)
    for each in text:
        tmp = bin(int(each, base=16))[2:]
        for i in range(4):
            if len(tmp) % 4 != 0:
                tmp = '0' + tmp
        text_2 = text_2 + tmp
    while len(text_2) < 32:
        text_2 = '0' + text_2
    return text_2


def o_b(text):
    text_10 = ''
    text = str(text)
    tmp = bin(int(text, base=10))[2:]
    text_10 = text_10 + tmp
    while len(text_10) < 32:
        text_10 = '0' + text_10
    return text_10


def o_h(text):
    text_10 = ''
    text = str(text)
    tmp = hex(int(text, base=10))[2:]
    text_10 = text_10 + tmp
    while len(text_10) < 8:
        text_10 = '0' + text_10
    return text_10

def expand(b):
    '''消息拓展'''
    w = {}
    for i in range(16):
        w[i] = b[i * 32:(i + 1) * 32]
    for j in range(16, 68):
        tmp = XOR3(w[j - 16], w[j - 9], shiftL(w[j - 3], 15))
        tmp = substitute(tmp, 1)
        w[j] = XOR3(tmp, shiftL(w[j - 13], 7), w[j - 6])
    for j in range(64):
        w[j + 68] = XOR(w[j], w[j + 4])
    for i in w:
        w[i] = z_h(w[i])
    return w

def FF(x, y, z, j):
    '''布尔函数'''
    if ((j >= 0) & (j <= 15)):
        ans = XOR3(x, y, z)
    else:
        ans = OR3(AND(x, y), AND(x, z), AND(y, z))
    return ans


def GG(x, y, z, j):
    '''布尔函数'''
    if ((j >= 0) & (j <= 15)):
        ans = XOR3(x, y, z)
    else:
        ans = OR(AND(x, y), AND(NOT(x), z))
    return ans

def compress(w, IV):
    '''消息压缩'''
    A = IV[0:8]
    B = IV[8:16]
    C = IV[16:24]
    D = IV[24:32]
    E = IV[32:40]
    F = IV[40:48]
    G = IV[48:56]
    H = IV[56:64]

    SS1 = ''
    SS2 = ''
    TT1 = ''
    TT2 = ''

    for j in range(64):
        if int(j) <= 15:
            T = '79cc4519'
        else:
            T = '7a879d8a'

        tmp = int(shiftL(h_b(A), 12), 2) + int(h_b(E), 2) + int(shiftL(h_b(T), j % 32), 2)
        tmp = mod32(tmp, 0)
        SS1 = shiftL(o_b(tmp), 7)
        SS2 = XOR(SS1, shiftL(h_b(A), 12))

        tmp = int(FF(h_b(A), h_b(B), h_b(C), j), 2) + int(h_b(D), 2) + int(SS2, 2) + int(h_b(w[j + 68]), 2)
        tmp = mod32(tmp, 0)
        TT1 = int(tmp, 10)

        tmp = int(GG(h_b(E), h_b(F), h_b(G), j), 2) + int(h_b(H), 2) + int(SS1, 2) + int(h_b(w[j]), 2)
        tmp = mod32(tmp, 0)
        TT2 = int(tmp, 10)

        D = C
        C = z_h(shiftL(h_b(B), 9))
        B = A
        A = o_h(TT1)
        H = G
        G = z_h(shiftL(h_b(F), 19))
        F = E
        E = z_h(substitute(o_b(TT2), 0))

    r = A + B + C + D + E + F + G + H
    r = h_b(r)
    v = h_b(IV)
    return b_h(XOR(r, v))


if __name__ == "__main__":
    msg = '520'  # 尝试加密
    m = fill(msg)
    w = expand(m)
    c = iteration(m, w)
    print(c)#e0f4551e142f91faeb503a83a4749d6cc44e55ae4635a14e577261bf0d6d3321

