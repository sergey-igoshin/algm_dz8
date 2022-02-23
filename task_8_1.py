"""
Задание 1.

Реализуйте кодирование строки по алгоритму Хаффмана.
У вас два пути:
1) тема идет тяжело? тогда вы можете, опираясь на примеры с урока,
 сделать свою версию алгоритма
Разрешается и приветствуется изменение имен переменных,
выбор других коллекций, различные изменения
и оптимизации.

2) тема понятна? постарайтесь сделать свою реализацию.
Вы можете реализовать задачу, например,
через ООП или предложить иной подход к решению.
"""
import heapq
from collections import Counter


class HuffmanCode:
    def __init__(self, user_string=None):
        self.user_string = user_string
        self.heap = []
        self.codes = dict()
        self.reverse_codes = dict()

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    def make_heap(self, frequency):
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        if len(self.heap) == 1:
            return
        node1 = heapq.heappop(self.heap)
        node2 = heapq.heappop(self.heap)
        merged = self.HeapNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(self.heap, merged)
        return self.merge_nodes()

    def make_codes(self, root=None, path=None):
        if root is None and path is None:
            root, path = heapq.heappop(self.heap), ''

        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = path
            self.reverse_codes[path] = root.char
            return

        self.make_codes(root.left, path=f'{path}0')
        self.make_codes(root.right, path=f'{path}1')

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def encode(self):
        self.make_heap(Counter(self.user_string))
        self.merge_nodes()
        self.make_codes()
        encoded_text = self.get_encoded_text(self.user_string)
        return encoded_text

    def decode(self, encoded_text, count=1, decoded_text=""):
        if len(encoded_text) < 1:
            return decoded_text
        if encoded_text[:count] in self.reverse_codes:
            d = self.reverse_codes[encoded_text[:count]]
            decoded_text += d
            return self.decode(encoded_text[count:], 1, decoded_text)
        return self.decode(encoded_text, count+1, decoded_text)


if __name__ == '__main__':
    string = input('Введите строку: ')
    h = HuffmanCode(string)

    encode_text = h.encode()
    print(f'Строка кода после кодирования:', encode_text, sep='\n')
    print(f'Таблица кодов:', h.codes, sep='\n')
    print(f'Декодированная строка:', h.decode(encode_text), sep='\n')
