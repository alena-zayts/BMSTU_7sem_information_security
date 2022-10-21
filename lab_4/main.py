from math import sqrt
from random import choices, choice, seed
import numpy as np
from math import ceil, log2
from base64 import *


class RSA:
    def generateKeys(self, primesLimit):
        primes = self.generatePrimes(primesLimit)
        P, Q = choice(primes[:len(primes) // 2]), choice(primes[len(primes) // 2:])
        if P == Q:
            raise ValueError("P=Q")
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
        #return self.powByMod(M, E, N)

    def cipherMessageNumsArray(self, M, Key, N):
        return [self.cipherNum(num, Key, N) for num in M]
    #
    # def decipherMessageNumsArray(self, M, D, N):
    #     return [self.decipherNum(num, D, N) for num in M]

    # решето Эратосфена
    @staticmethod
    def generatePrimes(primesLimit):
        isPrime = [False, False] + [True for _ in range(primesLimit - 1)]

        for num in range(2, int(sqrt(primesLimit + 1)) + 1):
            if isPrime[num]:
                for i in range(num * 2, primesLimit + 1, num):
                    isPrime[i] = False

        primes = [i for i in range(primesLimit + 1) if isPrime[i]]

        return primes

    def coSimple(self, x):
        simples = []
        for i in range(2, x):
            if self.gcd(i, x) == 1:
                simples.append(i)
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


seed(0)
PRIMES_LIMIT = 100


f = "test_text.rar"
f_enciphered = "test_enciphered.rar"
f_deciphered = "test_deciphered.rar"


cryptographer = RSA()
e, d, n = cryptographer.generateKeys(PRIMES_LIMIT)
# получаем число в кольце вычетов по n, поэтому каждое число надо кодировать как минимум ceil(log2(n)) битами
oneSymbolBit = ceil(log2(n))
# используем кодировку по 8 бит, поэтому число должно также делиться на 8
#oneSymbolBit += (8 - oneSymbolBit % 8)



def fromFile(filename):
    with open(filename, 'rb') as f_in:
        messageBytes = f_in.read()

    print(f'bytes from file: {messageBytes}')

    messageBinary = ''
    for b in messageBytes:
        messageBinary += format(b, '08b')

    messageNums = []
    for i in range(len(messageBinary) // oneSymbolBit):
        messageNums.append(int(messageBinary[i * oneSymbolBit: (i + 1) * oneSymbolBit], 2))

    # if len(messageBinary) % oneSymbolBit:
    #     messageNums.append(int(messageBinary[-(len(messageBinary) % oneSymbolBit):], 2))

    return messageNums


def toFile(messageNums, filename):
    messageBinary = ""
    for num in messageNums:
        messageBinary += format(num, f'0{oneSymbolBit}b')
    # у последнего числа первые нули убрать

    messageBytes = []
    for i in range(len(messageBinary) // 8):
        messageBytes.append((int(messageBinary[i * 8: (i + 1) * 8], 2)).to_bytes(1, byteorder='big'))

    with open(filename, 'wb') as f_out:
        for b in messageBytes:
            f_out.write(b)

    # if len(messageBinary) % oneSymbolBit:
    #     messageNums.append(int(messageBinary[-(len(messageBinary) % oneSymbolBit):], 2))


def cipherFile(filename_in, filename_out, Key, N):
    messageNums = fromFile(filename_in)
    print(messageNums)
    encipheredNums = cryptographer.cipherMessageNumsArray(messageNums, Key, N)
    print(encipheredNums)
    toFile(encipheredNums, filename_out)


print(f'n: {n}, oneSymbolBit: {oneSymbolBit}, e: {e}, d: {d}')
cipherFile(f, f_enciphered, e, n)
cipherFile(f_enciphered, f_deciphered, d, n)

#
#
# #
# #
# # def binaryToFile(messageBinary, filename):
# #     messageOrd = []
# #     for i in range(len(messageBinary) // 8):
# #         messageOrd.append(int(messageBinary[i * 8: (i+1) * 8], 2))
# #     if len(messageBinary) % 8:
# #         messageOrd.append(int(messageBinary[-(len(messageBinary) % 8):], 2))
# #
# #     messageBytes = [(x).to_bytes(1, byteorder='big') for x in messageOrd]
# #
# #     with open(filename, 'wb') as f_out:
# #         for x in messageBytes:
# #             f_out.write(x)
# #     print(f'bytes to file:   {messageBytes}')
# #
# #
# # def messageBinaryToNumArray(messageBinary, oneSymbSize):
# #     result = []
# #     for i in range(len(messageBinary) // oneSymbSize):
# #         result.append(int(messageBinary[i * oneSymbSize: (i + 1) * oneSymbSize], 2))
# #
# #     if len(messageBinary) % oneSymbSize:
# #         result.append(int(messageBinary[-(len(messageBinary) % oneSymbSize):], 2))
# #
# #     return result
# #
# #
# # def numArrayToMessageBinary(numsArray, oneSymbSize):
# #     messageBinary = ""
# #     for num in numsArray:
# #         messageBinary += format(num, f'0{oneSymbSize}b')
# #     return messageBinary
# #
# #
# # def encipherFile(filename_in, filename_out, E, N, oneSymbSize):
# #     # байты -(*8б)> бинарный -(:oneSymbSize)> цифры
# #     messageBinary = binaryFromFile(filename_in)
# #     messageNums = messageBinaryToNumArray(messageBinary, oneSymbSize)
# #     print(messageNums)
# #     encipheredNums = cryptographer.encipherMessageNumsArray(messageNums, E, N)
# #     print(encipheredNums)
# #     encipheredBinary = numArrayToMessageBinary(encipheredNums, oneSymbSize)
# #     binaryToFile(encipheredBinary, filename_out)
# #
# #
# # def decipherFile(filename_in, filename_out, D, N, oneSymbSize):
# #     messageBinary = binaryFromFile(filename_in)
# #     messageNums = messageBinaryToNumArray(messageBinary, oneSymbSize)
# #     print(messageNums)
# #     decipheredNums = cryptographer.decipherMessageNumsArray(messageNums, D, N)
# #     print(decipheredNums)
# #     decipheredBinary = numArrayToMessageBinary(decipheredNums, oneSymbSize)
# #     binaryToFile(decipheredBinary, filename_out)
#
#
#
#
#
# #
# # encipherFile(f, f_enciphered, e, n, oneSymbolBit)
# # decipherFile(f_enciphered, f_deciphered, d, n, oneSymbolBit)
#
#
# mes = 24930
# enc = cryptographer.cipherNum(mes, e, n)
# dec = cryptographer.cipherNum(enc, d, n)
# print(mes, enc, dec)
#
#
# def encipherFile2(filename_in, filename_out):
#     with open(filename_in, 'rb') as input_file:
#         data = input_file.read()
#
#     data = b32encode(data)
#     data = data.decode("ascii")
#
#     encryptedData = ""
#     for char in data:
#         current_char = cryptographer.cipherNum(ord(char), e, n)
#         encryptedData += chr(current_char)
#         print(current_char)
#     print(encryptedData)
#
#     # encryptedData = b32encode(encryptedData)
#     #encryptedData = encryptedData.encode("ascii")
#     with open(filename_out, 'w') as out_file:
#         out_file.write(encryptedData)
#
#
# def decipherFile2(filename_in, filename_out):
#     with open(filename_in, 'rb') as input_file:
#         data = input_file.read()
#
#     data = b32encode(data)
#     data = data.decode("ascii")
#
#     encryptedData = ""
#     for char in data:
#         current_char = cryptographer.cipherNum(ord(char), e, n)
#         encryptedData += chr(current_char)
#         print(current_char)
#     print(encryptedData)
#
#     # encryptedData = b32encode(encryptedData)
#     #encryptedData = encryptedData.encode("ascii")
#     with open(filename_out, 'w') as out_file:
#         out_file.write(encryptedData)
#
#
#
# encipherFile2(f, f_enciphered)
# decipherFile2(f_enciphered, f_deciphered)
# def main():
#     # if len(sys.argv) < 2:
#     #     print("Usage: python3", sys.argv[0], "<filename>")
#     #     return -1
#
#     filename = "test_text.txt"
#     with open(filename, 'rb') as input_file:
#         data = input_file.read()
#         #rsa = RSA()
#         # print("RSA parametrs\np:", rsa.p, "\nq:", rsa.q, "\ne:", rsa.e, "\nN:", rsa.n, "\nd:", rsa.d)
#
#         source_str = b32encode(data)
#         decoded_str = source_str.decode("ascii")
#         # print("Encrypting...")
#
#         encrypted = ""
#         for char in decoded_str:
#             current_char = cryptographer.cipherNum(ord(char), e, n)
#             encrypted += chr(current_char)
#
#         print(encrypted)
#         # with open("enc_" + filename, "w") as encrypted_file:
#         #     encrypted_file.write(encrypted)
#         #     encrypted_file.close()
#         # print("Decrypting...")
#
#         decrypted = ""
#         for char in encrypted:
#             current_char = cryptographer.decipherNum(ord(char), d, n)
#             decrypted += chr(current_char)
#
#         #decrypted = rsa.decrypt_string(encrypted)
#         decrypted = b32decode(decrypted)
#         print(decrypted)
#         # with open("dec_" + filename, "wb") as decrypted_file:
#         #     decrypted_file.write(decrypted)
#         #     decrypted_file.close()
#     return 0
#
# main()