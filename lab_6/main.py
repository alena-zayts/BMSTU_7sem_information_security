from typing import *
import json
from collections import defaultdict
from treelib import Node, Tree


class RW:
    @staticmethod
    def readBytesFromFile(filename: str) -> bytes:
        with open(filename, 'rb') as f_in:
            text = f_in.read()
        return text

    @staticmethod
    def writeBytesToFile(filename: str, text: bytes):
        with open(filename, 'wb') as f_out:
            f_out.write(text)


def insertion_sort(nodesList: List['TreeNode']):
    for i in range(1, len(nodesList)):
        temp = nodesList[i]
        j = i - 1
        while j >= 0 and temp.frequency < nodesList[j].frequency:
            nodesList[j + 1] = nodesList[j]
            j = j - 1
        nodesList[j + 1] = temp


class TreeNode:
    frequency: int
    symb: bytes
    left: 'TreeNode'
    right: 'TreeNode'

    def __init__(self, frequency=None, symb='+', left=None, right=None):
        self.frequency = frequency
        self.symb = symb
        self.left = left
        self.right = right


class BinaryTree:
    root: TreeNode

    def __init__(self, allNodes: List[TreeNode]):
        while len(allNodes) > 1:
            insertion_sort(allNodes)
            parent = TreeNode(symb=allNodes[0].symb + allNodes[1].symb,
                              frequency=allNodes[0].frequency + allNodes[1].frequency,
                              left=allNodes[0],
                              right=allNodes[1])
            allNodes = allNodes[2:] + [parent]

        self.root = allNodes[0]

    def SaveToJSON(self, filename: str):
        currentNode = self.root
        with open(filename, "wb") as write_file:
            while True:
                write_file.write(currentNode.symb)

        # with open(filename, "w") as write_file:
        #     json.dump(self, write_file)

    @staticmethod
    def LoadFromJSON(filename) -> 'BinaryTree':
        with open(filename, "r") as read_file:
            data = json.load(read_file)
        return data

    def printTree(self):
        self._printNode(self.root)

    @staticmethod
    def _printNode(startNode: TreeNode, space: str = "", side: str = 'r'):
        if startNode is None:
            return

        if startNode.left and startNode.right:
            print(f'{space} [{side}]- {startNode.frequency}')
        elif startNode.left is None and startNode.right is None:
            print(f'{space} [{side}]- {startNode.frequency}, symb={startNode.symb}')
        space += '    '

        BinaryTree._printNode(startNode.left, space, "L")
        BinaryTree._printNode(startNode.right, space, "R")

    def toLibTree(self, filename, tree=None, node=None, parent=None, side=''):
        if tree is None:
            tree = Tree()
            node = self.root

        tree.create_node(side, node.symb, parent=parent.symb if parent else None, data=node.symb)
        if node.left:
            self.toLibTree(filename, tree=tree, node=node.left, parent=node, side='left')
        if node.right:
            self.toLibTree(filename, tree=tree, node=node.right, parent=node, side='right')

        if node == self.root:
            with open(filename, 'w') as f:
                f.write(tree.to_json(with_data=True))
                print(tree.to_json(with_data=True))
                #json.dump(tree.to_json(with_data=True), f)
            # print(tree.to_json(with_data=True))
            # tree.save2file(filename)
            return tree

    @staticmethod
    def fromLibTree(filename, data=None, tree=None, side=''):
        if data is None:
            with open(filename) as f:
                data = json.load(f)
                print(data)

        node_symb = data[side]['data']
        node = TreeNode(symb=node_symb)

        if 'children' in data[side]:
            node.left = BinaryTree.fromLibTree(filename, data=data[side]['children'][0], tree=tree, side='left')
            node.right = BinaryTree.fromLibTree(filename, data=data[side]['children'][1], tree=tree, side='right')

        return node




class Huffman:
    @staticmethod
    def _createTree(data: bytes) -> BinaryTree:
        def _createFrequencyDict(data: bytes) -> Dict:
            res = defaultdict(int)
            for sym in data:
                res[chr(sym)] += 1
            return res

        def _createNodesWithTheirFrequency(frequencyDict: Dict) -> List[TreeNode]:
            res = []
            for symb, frequency in frequencyDict.items():
                node = TreeNode(symb=symb, frequency=frequency)
                res.append(node)
            return res

        frequencyDict = _createFrequencyDict(data)
        allNodes = _createNodesWithTheirFrequency(frequencyDict)
        tree = BinaryTree(allNodes)
        return tree

    @staticmethod
    def _createCodeForNodeOrChildren(node: TreeNode, codeArr: Dict, currentCode: str = ''):
        if node.left is None and node.right is None:
            codeArr[node.symb] = currentCode
        else:
            Huffman._createCodeForNodeOrChildren(node.left, codeArr, currentCode + '1')
            Huffman._createCodeForNodeOrChildren(node.right, codeArr, currentCode + '0')
            # if node.left is not None:
            #     Huffman._createCodeForNodeAndChildren(node.left, codeArr, currentCode + '1')
            #
            # if node.right is not None:
            #     Huffman._createCodeForNodeAndChildren(node.right, codeArr, currentCode + '0')


    @staticmethod
    def Encode(data: bytes, symbolCodes: dict) -> (bytes, int):
        encodedBits = ''
        for symb in data:
            encodedBits += symbolCodes[chr(symb)]

        addedNulls = 8 - (len(encodedBits) % 8)
        encodedBits += '0' * addedNulls

        encodedBytes = b''
        for i in range(len(encodedBits) // 8):
            #print((int(encodedBits[i * 8: (i + 1) * 8], 2)).to_bytes(1, byteorder='big'))
            encodedBytes += ((int(encodedBits[i * 8: (i + 1) * 8], 2)).to_bytes(1, byteorder='big'))

        return encodedBytes, encodedBits, addedNulls

    @staticmethod
    def Compress(fileSrc: str, fileDest: str) -> (BinaryTree, int):
        text = RW.readBytesFromFile(fileSrc)
        tree = Huffman._createTree(text)

        symbolCodes = {}
        Huffman._createCodeForNodeOrChildren(tree.root, symbolCodes)

        encodedBytes, encodedBits, addedNulls = Huffman.Encode(text, symbolCodes)
        RW.writeBytesToFile(fileDest, encodedBytes)
        print('Compressor')
        print(f'Original size  : 8 bits per symbol, {len(text)} symbols. Total: {8 * len(text)} bit')
        print(f'Compressed size: {len(symbolCodes)} unique symbols, {len(text)} symbols. Total: {len(encodedBits) + addedNulls} bit (with addedNulls)')
        print('original  :', text)
        print('compressed:', encodedBytes)
        print('in bits   :', encodedBits)
        print('added null:', addedNulls)
        print()
        return tree, addedNulls

    @staticmethod
    def Decompress(fileSrc: str, fileDest: str, tree: BinaryTree, addedNulls: int):
        dataBytes = RW.readBytesFromFile(fileSrc)
        dataBits = ''
        for byte in dataBytes:
            dataBits += format(byte, f'08b')
        dataBits = dataBits[:-addedNulls]

        res = b''
        node = tree.root
        for bool_bit in dataBits:
            if bool_bit == '0' and node.right is not None:
                node = node.right

            elif bool_bit == '1' and node.left is not None:
                node = node.left

            if node.left is None and node.right is None:
                res += ord(node.symb).to_bytes(length=1, byteorder='big')
                node = tree.root

        RW.writeBytesToFile(fileDest, res)

        print('Decompressor')
        print('original  :', dataBytes)
        print('in bits   :', dataBits)
        print('decompressed:', res)
        print('added null:', addedNulls)


def main():
    fileTree = 'tree.json'

    # fileSrc = "text.txt"
    # fileCom = 'compressed_version.txt'
    # fileRes = 'decompressed_version.txt'

    fileSrc = "img.jpeg"
    fileCom = 'compressed_version.jpeg'
    fileRes = 'decompressed_version.jpeg'


    tree, addedNulls = Huffman.Compress(fileSrc, fileCom)
    tree.toLibTree(fileTree)
    #tree.printTree()

    # tree.printTree()
    # tmp = tree.toLibTree(fileTree)
    # tmp.show()

    treeRoot = BinaryTree.fromLibTree(fileTree)
    tree = BinaryTree([treeRoot])
    #tree.printTree()
    Huffman.Decompress(fileCom, fileRes, tree, addedNulls)



main()
