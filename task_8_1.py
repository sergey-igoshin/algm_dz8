import heapq
from collections import Counter


class HuffmanCoding:
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

    def make_codes(self, root, path=''):
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = path
            self.reverse_codes[path] = root.char
            return

        self.make_codes(root.left, path=f'{path}0')
        self.make_codes(root.right, path=f'{path}1')

    def encode(self):
        frequency = Counter(self.user_string)
        for key in frequency:
            heapq.heappush(self.heap, self.HeapNode(key, frequency[key]))
        self.merge_nodes()
        self.make_codes(heapq.heappop(self.heap))
        encoded_text = ''
        for character in self.user_string:
            encoded_text += self.codes[character]
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
    h = HuffmanCoding(string)

    encode_text = h.encode()
    print(f'Строка кода после кодирования:', encode_text, sep='\n')
    print(f'Таблица кодов:', h.codes, sep='\n')
    print(f'Декодированная строка:', h.decode(encode_text), sep='\n')
