from math import sqrt
from random import choices, choice, seed
import numpy as np
from math import ceil, log2, floor
from base64 import *


class RSA:
    def generateKeys(self, primesLimit):
        primes = self.generatePrimes(primesLimit)
        P = choice(primes)
        primes.remove(P)
        Q = choice(primes)
        if P == Q:
            raise ValueError("P=Q")
        print(f'P: {P}, Q: {Q}')
        N = P * Q
        Fi = (P - 1) * (Q - 1)
        E = self.coSimple(Fi)
        # ED mod Fi = 1 => ED + Fik = 1 (ax + by = 1)
        gcd, x, y = self.xgcd(E, Fi)
        D = int(x if x > 0 else x + Fi)
        if (E * D) % Fi != 1:
            raise ValueError("Incorrect keys")
        return E, D, N

    def cipherNum(self, M, Key, N):
        return pow(M, Key, N)

    def cipherMessageNumsArray(self, M, Key, N):
        return [self.cipherNum(num, Key, N) for num in M]

    # решето Эратосфена
    @staticmethod
    def generatePrimes(primesLimit):
        isPrime = [False, False] + [True for _ in range(primesLimit - 1)]

        for num in range(2, int(sqrt(primesLimit + 1)) + 1):
            if isPrime[num]:
                for i in range(num * 2, primesLimit + 1, num):
                    isPrime[i] = False

        primes = [i for i in range(primesLimit + 1) if isPrime[i]]

        return primes[-LEAVE_LAST:]

    def coSimple(self, x):
        simples = []
        for i in range(x, 2, -1):
            if self.gcd(i, x) == 1:
                simples.append(i)
            if len(simples) >= CO_SIMPLES_TO_GENERATE:
                break
        return choice(simples)

    # НОД по алгоритму Евклида
    # Пусть a = bq + r, тогда НОД (a, b) = НОД (b, r).
    # НОД(r, 0) = r
    @staticmethod
    def gcd(a, b):
        a, b = max(a, b), min(a, b)
        while b != 0:
            a, b = b, a % b
        return a

    # расширенный алгоритм Eвклида
    # НОД и целые x и y, такие что
    # ax+by=НОД(a,b)
    @staticmethod
    def xgcd(a, b):
        x, old_x = 0, 1
        y, old_y = 1, 0

        while (b != 0):
            quotient = a // b
            a, b = b, a - quotient * b
            old_x, x = x, old_x - quotient * x
            old_y, y = y, old_y - quotient * y

        return a, old_x, old_y

        # a, b = max(a, b), min(a, b)
        # m = np.eye(2, 2)
        #
        # while b != 0:
        #     quotient = a // b
        #     m = np.matmul(m, np.matrix([[-quotient, 1], [1, 0]]))
        #     a, b = b, a % b
        #
        # return a, m[0, 1], m[1, 1]

    # (a^k) mod n
    # http://poivs.tsput.ru/Downloads/Article/2150/Алгоритмы%20быстрого%20возведения%20в%20степень%20по%20модулю.pdf
    @staticmethod
    def powByMod(a, k, n):
        r = 1
        while k > 0:
            if k % 2:
                r = (r * a) % n
            k //= 2
            a = (a * a) % n

        return r



def fromFile(filename):
    with open(filename, 'rb') as f_in:
        messageBytes = f_in.read()

    print(f'bytes from file: {messageBytes}')

    messageBinary = ''
    for b in messageBytes:
        messageBinary += format(b, '08b')

    if len(messageBinary) % oneSymbolBit:
        added = oneSymbolBit - (len(messageBinary) % oneSymbolBit)
        messageBinary += '0'*added
    else:
        added = 0

    messageNums = []
    for i in range(len(messageBinary) // oneSymbolBit):
        messageNums.append(int(messageBinary[i * oneSymbolBit: (i + 1) * oneSymbolBit], 2))
    if len(messageBinary) % oneSymbolBit:
        messageNums.append(int(messageBinary[-(len(messageBinary) % oneSymbolBit):], 2))

    return messageNums, added


def toFile(messageNums, filename, nulls_to_delete_from_bin=0):
    messageBinary = ""
    for num in messageNums:
        messageBinary += format(num, f'0{oneSymbolBit}b')
    if nulls_to_delete_from_bin:
        messageBinary = messageBinary[:-nulls_to_delete_from_bin]
    # у последнего числа первые нули убрать
    # messageBinary = ""
    # for num in messageNums[:-1]:
    #     messageBinary += format(num, f'0{oneSymbolBit}b')
    # messageBinary += format(messageNums[-1], 'b')

    messageBytes = b''
    for i in range(len(messageBinary) // 8):
        messageBytes += ((int(messageBinary[i * 8: (i + 1) * 8], 2)).to_bytes(1, byteorder='big'))
    # if len(messageBinary) % 8:
    #     messageBytes += ((int(messageBinary[-(len(messageBinary) % 8):], 2)).to_bytes(1, byteorder='big'))

    with open(filename, 'wb') as f_out:
        f_out.write(messageBytes)

    print('bytes to file:', messageBytes)

    # if len(messageBinary) % oneSymbolBit:
    #     messageNums.append(int(messageBinary[-(len(messageBinary) % oneSymbolBit):], 2))


def encipherFile(filename_in, filename_out):
    global overflows, nulls_added_to_bin
    overflows = []

    messageNums, nulls_added_to_bin = fromFile(filename_in)
    encipheredNums = cryptographer.cipherMessageNumsArray(messageNums, e, n)
    toFile(encipheredNums, filename_out)

    print(messageNums)
    print(encipheredNums)

    for num in messageNums:
        if num > n:
            overflows.append(True)
        else:
            overflows.append(False)
    return messageNums


def decipherFile(filename_in, filename_out):
    global overflows, nulls_added_to_bin

    messageNums, _ = fromFile(filename_in)
    encipheredNums = cryptographer.cipherMessageNumsArray(messageNums, d, n)

    for i in range(len(encipheredNums)):
        if encipheredNums[i] > n and not overflows[i]:
            encipheredNums[i] -= n
        elif encipheredNums[i] < n and overflows[i]:
            encipheredNums[i] += n

    toFile(encipheredNums, filename_out, nulls_to_delete_from_bin=nulls_added_to_bin)
    print(messageNums)
    print(encipheredNums)
    return messageNums




seed(0)
PRIMES_LIMIT = int(1e6)
LEAVE_LAST = 100
CO_SIMPLES_TO_GENERATE = 100


# f = "img.jpeg"
# f_enciphered = "img_enciphered.jpeg"
# f_deciphered = "img_deciphered.jpeg"

# f = "img2.jpg"
# f_enciphered = "img2_enciphered.jpg"
# f_deciphered = "img2_deciphered.jpg"

# f = "img3.png"
# f_enciphered = "img3_enciphered.png"
# f_deciphered = "img3_deciphered.png"

f = "text.txt"
f_enciphered = "text_enciphered.txt"
f_deciphered = "text_deciphered.txt"

cryptographer = RSA()
e, d, n = cryptographer.generateKeys(PRIMES_LIMIT)
# получаем число в кольце вычетов по n, поэтому каждое число надо кодировать как минимум ceil(log2(n)) битами
oneSymbolBit = ceil(log2(n))
# используем кодировку по 8 бит, поэтому число должно также делиться на 8
#oneSymbolBit += (8 - oneSymbolBit % 8)

overflows = []
nulls_added_to_bin = 0
print(f'n: {n}, oneSymbolBit: {oneSymbolBit}, e: {e}, d: {d}')
print(f'len of keys in bit: len(e)={len(format(e, "b"))}, len(d)={len(format(d, "b"))}')
encipherFile(f, f_enciphered)
decipherFile(f_enciphered, f_deciphered)
