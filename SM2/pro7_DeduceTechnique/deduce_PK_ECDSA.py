from email import message
from pre_SM2 import *
import secrets
from gmssl import func, sm3


def Tonelli_Shanks(n, p):
    """Tonelli Shanks to Quadratic Residue"""
    def Legendre(n, p):
        """judge QR"""
        return pow(n, (p - 1) // 2, p)

    assert Legendre(n, p) == 1
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q = q // 2
        s += 1
    for z in range(2, p):
        if Legendre(z, p) == p - 1:
            c = pow(z, q, p)
            break
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    if t % p == 1:
        return r
    else:
        i = 0
        while t % p != 1:
            temp = pow(t, 2 ** (i + 1), p)
            i += 1
            if temp % p == 1:
                b = pow(c, 2 ** (m - i - 1), p)
                r = r * b % p
                c = b * b % p
                t = t * c % p
                m = i
                i = 0  # i = 0 for every inner loop
        return r


def key_gen():
    sk = int(secrets.token_hex(32), 16)  # private key
    pk = EC_multi(sk, G)  # public key
    return sk, pk

def ECDSA_sign(m, sk):
    """ECDSA signature algorithm
    :param m: message
    :param sk: private key
    :return v: prefix of signature
    :return (r,s): signature
    """
    while 1:
        k = secrets.randbelow(N)  # N is prime, then k <- Zn*
        R = EC_multi(k, G)
        r = R[0] % N  # Rx mod n
        if r != 0: break
    e = sm3.sm3_hash(func.bytes_to_list(bytes(m, encoding='utf-8')))  # e = hash(m)
    e = int(e, 16)
    tmp1 = inv(k, N)
    tmp2 = (e + sk * r) % N
    s = tmp1 * tmp2 % N

    x = r % P
    right = (x ** 3 + A * x + B) % P  # y ^ 2 = x ^ 3 + A * x + B
    y = Tonelli_Shanks(right, P)
    # compute prefix of signature
    if y == R[1]:
        v = 2  # even
    else: v = 1  # odd

    return v, (r, s)


def ECDSA_verify(signature, m, pk):
    """ECDSA algorithm
    :param signature: (r, s)
    :param m: message
    :param pk: public key
    :return:True or False
    """
    r, s = signature
    e = sm3.sm3_hash(func.bytes_to_list(bytes(m, encoding='utf-8')))  # e = hash(m)
    e = int(e, 16)
    w = inv(s, N)
    tmp1 = EC_multi(e * w, G)
    tmp2 = EC_multi(r * w, pk)
    dot = EC_add(tmp1, tmp2)
    x = dot[0]
    return x == r





def deduce_pk(v, m, signature):
    """pk = inv_r * (s * R - e * G)
    :param v: prefix of signature
    :param m: message
    :param signature: (r, s)
    :return: pk
    """
    r, s = signature
    e = int(sm3.sm3_hash(func.bytes_to_list(bytes(m, encoding='utf-8'))), 16)  # e = hash(m)
    x = r % P
    right = x ** 3 + A * x + B  # y ^ 2 = x ^ 3 + A * x + B
    y = Tonelli_Shanks(right, P)
    if v == 2:
        R = (x, y)
    else:
        R = (x, P - y)
    return EC_multi(inv(r, N), EC_sub(EC_multi(s, R), EC_multi(e, G)))

if __name__ == '__main__':
    sk, pk = key_gen()
    print("public key from generation:")
    print(pk)
    message = "deduce pk in EVDSA"
    v, signa = ECDSA_sign(message, sk)
    dpk = deduce_pk(v, message, signa)
    print("\ndeduced pk:")
    print(dpk)
    print("=" * 54, "\n")
    print("Dudece pk in ECDSA is successful!\n" if pk == dpk else "Failed!\n")
