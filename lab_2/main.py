from random import shuffle, seed
import copy
import os

seed(0)
SYMBOLS_COUNT = 256
SYMBOLS = [chr(i) for i in range(SYMBOLS_COUNT)]


class Rotor:
    def __init__(self):
        self.__countShift = 0
        self.__values = SYMBOLS.copy()
        shuffle(self.__values)

    def __str__(self):
        s = ''
        for i in range(SYMBOLS_COUNT):
            s += f'{self.__values[i]}'
        return s

    def getValue(self, index: int) -> chr:
        return self.__values[index]

    def getIndex(self, value: chr) -> int:
        return self.__values.index(value)

    def shift(self) -> None:
        symb = self.__values.pop(0)
        self.__values.append(symb)
        self.__countShift += 1
        if self.__countShift == SYMBOLS_COUNT:
            self.__countShift = 0

    @property
    def fullTurnover(self) -> bool:
        return self.__countShift == 0


class Reflector:
    def __init__(self):
        self.__values = SYMBOLS.copy()
        shuffle(self.__values)

    def __str__(self):
        s = ''
        for i in range(SYMBOLS_COUNT // 2):
            s += f'({self.__values[i * 2]},{self.__values[i * 2 + 1]})'
        return s

    def getReflectedValue(self, value: chr) -> chr:
        index = self.__values.index(value)
        reflection_index = index + 1 if index % 2 == 0 else index - 1
        return self.__values[reflection_index]


class Enigma:
    def __init__(self, rotorsAmount=3, with_print=False):
        self.__rotorsAmount = rotorsAmount
        self.__rotors = [Rotor() for _ in range(self.__rotorsAmount)]

        self.__reflector = Reflector()
        if with_print:
            print(str(self))

    def __str__(self):
        s = ''
        for i in range(self.__rotorsAmount):
            s += f'Rotor{i}: ' + str(self.__rotors[i])
        s += '\nReflector: ' + str(self.__reflector)
        return s

    def __encipherSymbolOdd(self, symbol: chr) -> chr:
        cur = ord(symbol)
        for i in range(self.__rotorsAmount):
            if i % 2 == 0:
                cur = self.__rotors[i].getValue(cur)
            else:
                cur = self.__rotors[i].getIndex(cur)

        cur = self.__reflector.getReflectedValue(cur)

        for i in range(self.__rotorsAmount - 1, -1, -1):
            if i % 2 == 0:
                cur = self.__rotors[i].getIndex(cur)
            else:
                cur = self.__rotors[i].getValue(cur)

        cur = SYMBOLS[cur]

        return cur

    def __encipherSymbolEven(self, symbol: chr) -> chr:
        cur = symbol
        for i in range(self.__rotorsAmount):
            if i % 2:
                cur = self.__rotors[i].getValue(cur)
            else:
                cur = self.__rotors[i].getIndex(cur)

        cur = self.__reflector.getReflectedValue(cur)

        for i in range(self.__rotorsAmount - 1, -1, -1):
            if i % 2:
                cur = self.__rotors[i].getIndex(cur)
            else:
                cur = self.__rotors[i].getValue(cur)

        return cur

    def __encipherSymbol(self, symbol: chr) -> chr:
        if self.__rotorsAmount % 2:
            return self.__encipherSymbolOdd(symbol)
        else:
            return self.__encipherSymbolEven(symbol)

    # def __encipherSymbol(self, symbol: chr) -> chr:
    #     i0 = ord(symbol)
    #
    #     v1 = self.__rotor1.getValue(i0)
    #
    #     i2 = self.__rotor2.getIndex(v1)
    #
    #     v3 = self.__rotor3.getValue(i2)
    #
    #     v4 = self.__reflector.getReflectedValue(v3)
    #
    #     i5 = self.__rotor3.getIndex(v4)
    #
    #     v6 = self.__rotor2.getValue(i5)
    #
    #     i7 = self.__rotor1.getIndex(v6)
    #
    #     v8 = SYMBOLS_FOR_ENIGMA[i7]
    #
    #     return v8

    def encipherText(self, text: str) -> str:
        encipheredText = ''

        for symbol in text:
            encipheredSymbol = self.__encipherSymbol(symbol)
            encipheredText += encipheredSymbol

            for i in range(self.__rotorsAmount):
                self.__rotors[i].shift()
                if not self.__rotors[i].fullTurnover:
                    break

        return encipheredText

    def encipherFile(self, inputFileName: str, outputFileName: str) -> None:
        with open(inputFileName, 'rb') as f:
            textByte = f.read()

        textSymbols = ""
        for byte in textByte:
            textSymbols += chr(byte)

        print(f"Text to encipher:\n'''\n{textSymbols}\n'''")
        textSymbolsEnciphered = self.encipherText(textSymbols)
        print(f"Enciphered text:\n'''\n{textSymbolsEnciphered}\n'''")

        textBytesEnciphered = b""
        for symbolEnciphered in textSymbolsEnciphered:
            textBytesEnciphered += bytes([ord(symbolEnciphered)])

        with open(outputFileName, 'wb') as f:
            f.write(textBytesEnciphered)


enigma = Enigma(rotorsAmount=4)
enigmaCopy = copy.deepcopy(enigma)

fileName = 'text2.rar'
encipheredFileName = fileName[:-4] + '_enciphered' + fileName[-4:]
decipheredFileName = fileName[:-4] + '_deciphered' + fileName[-4:]

print('Forward\n')
enigma.encipherFile(fileName, encipheredFileName)
print('\nBackwards\n')
enigmaCopy.encipherFile(encipheredFileName, decipheredFileName)


