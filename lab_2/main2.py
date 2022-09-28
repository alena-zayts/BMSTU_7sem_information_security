from random import shuffle, seed
import copy
import os

seed(0)
SYMBOLS_COUNT = 256
SYMBOLS_FOR_ENIGMA = [i for i in range(SYMBOLS_COUNT)]
SYMBOLS = [chr(i) for i in range(SYMBOLS_COUNT)]


class Rotor:
    def __init__(self):
        self.__countShift = 0
        self.__values = SYMBOLS_FOR_ENIGMA.copy()
        shuffle(self.__values)

    def __str__(self):
        s = ''
        for i in range(SYMBOLS_COUNT):
            s += f'{self.__values[i]}'
        return s

    def getValue(self, index: int) -> int:
        return self.__values[index]

    def getIndex(self, value: int) -> int:
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
        self.__values = SYMBOLS_FOR_ENIGMA.copy()
        shuffle(self.__values)

    def __str__(self):
        s = ''
        for i in range(SYMBOLS_COUNT // 2):
            s += f'({self.__values[i * 2]},{self.__values[i * 2 + 1]})'
        return s

    def getReflectedValue(self, value: int) -> int:
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

    def __encipherSymbol(self, symbol: chr) -> chr:
        cur = ord(symbol)
        for i in range(self.__rotorsAmount):
            cur = self.__rotors[i].getValue(cur)

        cur = self.__reflector.getReflectedValue(cur)

        for i in range(self.__rotorsAmount - 1, -1, -1):
            cur = self.__rotors[i].getIndex(cur)

        cur = SYMBOLS[cur]

        return cur

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


enigma = Enigma(rotorsAmount=4, with_print=True)
enigmaCopy = copy.deepcopy(enigma)

fileName = "dist\main2\main2.rar"
encipheredFileName = fileName[:-4] + '_enciphered' + fileName[-4:]
decipheredFileName = fileName[:-4] + '_deciphered' + fileName[-4:]

print('Forward\n')
enigma.encipherFile(fileName, encipheredFileName)
print('\nBackwards\n')
enigmaCopy.encipherFile(encipheredFileName, decipheredFileName)


