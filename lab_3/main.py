from copy import deepcopy
from random import choices, seed

ENCIPHER = 1
DECIPHER = -1

# def applyPermutationToMessage(perm, mes):
#     res = []
#     for i in range(len(perm)):
#         res.append(mes[perm[i] - 1])

def xorForTwoList(a1, a2):
    return [a ^ b for (a, b) in zip(a1, a2)]

class RoundKeysGenerator:
    permutationC0 = [
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36
    ]

    permutationD0 = [
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4,
    ]

    shiftsS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    compressivePermutationCP = [
        14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32,
    ]

    def applyInitialPermutationB(self, initial_key):  # 64 -> 2*28
        C0 = [initial_key[i - 1] for i in self.permutationC0]
        D0 = [initial_key[i - 1] for i in self.permutationD0]
        return C0, D0

    def applyCompressivePermutationCP(self, round_key):  # 56 -> 48
        return [round_key[i - 1] for i in self.compressivePermutationCP]

    def generate(self, initial_key):  # 64 -> 16 * 48
        round_keys = []  # 16 * 48

        C_array = []  # 17 * 28
        D_array = []  # 17 * 28

        C0, D0 = self.applyInitialPermutationB(initial_key)
        C_array.append(C0)
        D_array.append(D0)

        for i in range(16):
            # Ccur = C_array[-1][-self.shiftsS[i]:] + C_array[-1][:-self.shiftsS[i]]  # 28
            # Dcur = D_array[-1][-self.shiftsS[i]:] + D_array[-1][:-self.shiftsS[i]]  # 28

            Ccur = C_array[-1][self.shiftsS[i]:] + C_array[-1][:self.shiftsS[i]]  # 28
            Dcur = D_array[-1][self.shiftsS[i]:] + D_array[-1][:self.shiftsS[i]]  # 28

            C_array.append(Ccur)
            D_array.append(Dcur)

            currentKey = Ccur + Dcur  # 56
            curKeyCompressed = self.applyCompressivePermutationCP(currentKey)  # 48
            round_keys.append(curKeyCompressed)

        return round_keys





class FeistelCipher:
    expandingPermutationE = [
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1,
    ]

    SBlocks = [  # 8 * 16 * 4
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]

        ],
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
        ],
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
        ],
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ]
    ]

    finishingPermutationP = [
        16, 7, 20, 21,
        29, 12, 28, 17,
        1, 15, 23, 26,
        5, 18, 31, 10,
        2, 8, 24, 14,
        32, 27, 3, 9,
        19, 13, 30, 6,
        22, 11, 4, 25,
    ]

    def applyExpandingPermutationE(self, message):  # 32->48
        return [message[i - 1] for i in self.expandingPermutationE]

    def dec115ToBinary(self, elem):
        res = [0, 0, 0, 0]
        for i in range(3, -1, -1):
            res[i] = elem // (2 ** i)
            elem -= res[i] * (2 ** i)
        #res.reverse()
        return res

    def decimalArrayToBinary(self, arr):
        res = []
        for elem in arr:
            res.extend(self.dec115ToBinary(elem))
        return res

    def applyFinishingPermutationP(self, message):  # 32->32
        return [message[i - 1] for i in self.finishingPermutationP]

    def apply(self, key, message):  # key: 48, message: 32
        expandedMessage = self.applyExpandingPermutationE(message)  # 48
        Z = xorForTwoList(expandedMessage, key)

        changes = []  # 8 чисел [1, 15], каждое по 4 бита
        for i in range(8):
            curBlock = i * 6
            x = (  # 1 и 6 бит
                    2 * Z[curBlock + 0] +
                    1 * Z[curBlock + 5]
            )
            y = (  # 2, 3, 4, 5 биты
                    8 * Z[curBlock + 1] +
                    4 * Z[curBlock + 2] +
                    2 * Z[curBlock + 3] +
                    1 * Z[curBlock + 4]
            )

            changes.append(self.SBlocks[i][x][y])

        changedMessage = self.decimalArrayToBinary(changes)  # 32
        permutatedMessage = self.applyFinishingPermutationP(changedMessage)  # 32

        return permutatedMessage


class Cryptographer:
    initialPermutationIP = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,

    ]
    finalPermutationIP = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25,
    ]

    def applyInitialPermutationIP(self, message):  # 64 -> 64
        return [message[i - 1] for i in self.initialPermutationIP]

    def applyFinalPermutationIP(self, message):  # 64 -> 64
        return [message[i - 1] for i in self.finalPermutationIP]

    def encipher(self, keys, message, direction):  # keys: 16*48, message: 64
        permutatedMessage = self.applyInitialPermutationIP(message)  # 64
        L, R = permutatedMessage[:32], permutatedMessage[32:]

        if direction == ENCIPHER:
            for i in range(16):
                right_copy = deepcopy(R)
                R = xorForTwoList(L, FeistelCipher().apply(keys[i], R))
                L = right_copy
        else:
            for i in range(15, -1, -1):
                left_copy = deepcopy(L)
                L = xorForTwoList(R, FeistelCipher().apply(keys[i], L))
                R = left_copy

        joinedMessage = L + R
        permutatedJoinedMessage = self.applyFinalPermutationIP(joinedMessage)  # 64

        return permutatedJoinedMessage


def encipherFile(filename_in, filename_out, direction):
    cryptographer = Cryptographer()
    with open(filename_in, 'rb') as f_in:
        with open(filename_out, 'wb') as f_out:
            block = f_in.read(64)
            block_enciphered = cryptographer.encipher(keys, block, direction)
            f_out.write(block_enciphered)


seed(0)
key = choices([0, 1], k=64)
keys = RoundKeysGenerator().generate(key)


f = "test.txt"
f_enciphered = "test_enciphered.rar"
f_deciphered = "test_deciphered.rar"



encipherFile(f, f_enciphered, ENCIPHER)
encipherFile(f_enciphered, f_deciphered, DECIPHER)


# message = [0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, ]
# encipheredMessage = Cryptographer().encipher(keys, message, direction=ENCIPHER)
# decipheredMessage = Cryptographer().encipher(keys, encipheredMessage, direction=DECIPHER)
#
# print(message)
# print(encipheredMessage)
# print(decipheredMessage)






# seed(0)
# key = choices([0, 1], k=64)
# keys = RoundKeysGenerator().generate(key)
# message = [0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, ]
# encipheredMessage = Cryptographer().encipher(keys, message, direction=ENCIPHER)
# decipheredMessage = Cryptographer().encipher(keys, encipheredMessage, direction=DECIPHER)
# print(key)
# print(keys)
# print('  ', message)
# print(encipheredMessage)
# print('  ', decipheredMessage)
#
# print('{', end=' ')
# for x in key:
#     if x:
#         print('true, ', end='')
#     else:
#         print('false, ', end = '')
# print('};', end=' ')
