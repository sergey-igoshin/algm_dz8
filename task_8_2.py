"""
Задание 2.

Доработайте пример структуры "дерево", рассмотренный на уроке.

Предложите варианты доработки и оптимизации
(например, валидация значений узлов в соответствии
 с требованиями для бинарного дерева). При валидации приветствуется генерация
 собственного исключения

Поработайте с оптимизированной структурой,
протестируйте на реальных данных - на клиентском коде.
"""

from string import ascii_lowercase
import re


def create_lines(nodes, lines, s, e, w, check):
    r = (s + e) // 2
    if check:
        r += 1
        nodes.extend([' ' * (r + 1), '_' * (w - r)])
        lines.extend([' ' * r + '/', ' ' * (w - r)])
    else:
        nodes.extend(['_' * r, ' ' * (w - r + 1)])
        lines.extend([' ' * r + '\\', ' ' * (w - r)])
    return nodes, lines


def create_bt(lw, rw, ls, rs, lz, rz, n, node):
    nodes, lines = [], []
    s = 0
    r = n
    if lw > 0:
        nodes, lines = create_lines(nodes, lines, ls, lz, lw, True)
        n += 1
        s = lw + 1
    nodes.append(node)
    lines.append(' ' * r)
    if rw > 0:
        nodes, lines = create_lines(nodes, lines, rs, rz, rw, False)
        n += 1
    return nodes, lines, s, ' ' * n


def print_color(arg):
    format_color = {
        'GREEN': '\x1b[38;5;46m',
        'RED': '\x1b[38;5;160m',
        'END': '\x1b[0m',
    }
    return format_color[arg]


RED = print_color('RED')
GREEN = print_color('GREEN')
END = print_color('END')


def red(text):
    return RED + str(text) + END


def green(text):
    return GREEN + str(text) + END


#  Обход бинарного дерева
def go_bt(bt, el=None, path=''):
    if el is None:
        print(green('***** Обход дерева *****'))
        el = input('Введите какой элемент найти?: ')
        if el.isdigit():
            el = int(el)
    if bt.root == el:
        return f'Корень{path} {green(el)}'
    if el < bt.root and bt.left_child is not None:
        return go_bt(bt.left_child, el, f'{path} {green(bt.root)} \nШаг влево')
    if el > bt.root and bt.right_child is not None:
        return go_bt(bt.right_child, el, f'{path} {green(bt.root)} \nШаг вправо')
    return red(f'Элемент "{el}" отсутствует')


class BinaryTree:
    def __init__(self, root_obj=None, left=None, right=None):
        self.root = root_obj                            # корень
        self.left_child = left                          # левый потомок
        self.right_child = right                        # правый потомок
        self.array = []

    def __str__(self):
        lines = self.write_bt(self, 0, False, False)[0]
        return str('\n'.join((line.rstrip() for line in lines)))

    # добавить левого потомка
    def insert_left(self, new_node):
        if self.left_child is None:                     # если у узла нет левого потомка
            self.left_child = BinaryTree(new_node)      # то узел вставляется в дерево формируется новое поддерево
        else:                                           # если у узла есть левый потомок
            tree_obj = BinaryTree(new_node)             # то вставляем новый узел
            tree_obj.left_child = self.left_child       # и спускаем имеющегося потомка на один уровень ниже
            self.left_child = tree_obj

    # добавить правого потомка
    def insert_right(self, new_node):
        if self.right_child is None:                    # если у узла нет правого потомка
            self.right_child = BinaryTree(new_node)     # то узел вставляется в дерево формируется новое поддерево
        else:                                           # если у узла есть правый потомок
            tree_obj = BinaryTree(new_node)             # то вставляем новый узел
            tree_obj.right_child = self.right_child     # и спускаем имеющегося потомка на один уровень ниже
            self.right_child = tree_obj

    # метод доступа к правому потомку
    def get_right_child(self):
        return self.right_child

    # метод доступа к левому потомку
    def get_left_child(self):
        return self.left_child

    # метод установки корня
    def set_root_val(self, obj):
        self.root = obj

    # метод доступа к корню
    def get_root_val(self):
        return self.root

    #  Проверяем тип данных для добавления узлов
    def insert(self, data):
        if isinstance(data, (list, str)):
            self.bt_values(sorted(data))
            for i in self.array:
                self.insert_node(i)
        elif isinstance(data, (int, float)):
            self.insert_node(data)

    #  Добавляем узел
    def insert_node(self, data):
        if not self.root:
            self.root = data

        if data < self.root:
            if not self.left_child:
                self.left_child = BinaryTree(data)
            return self.left_child.insert_node(data)

        if data > self.root:
            if not self.right_child:
                self.right_child = BinaryTree(data)
            return self.right_child.insert_node(data)

    #  Проверяем тип данных для удаления узлов
    def delete(self, data):
        if isinstance(data, (list, str)):
            for num in data:
                self.delete_node(num)
        elif isinstance(data, (int, float)):
            self.delete_node(data)

    #  Удаляем узел
    def delete_node(self, data):
        if self is None:
            return self

        if data < self.root:
            if self.left_child:
                self.left_child = self.left_child.delete_node(data)
            return self

        if data > self.root:
            if self.right_child:
                self.right_child = self.right_child.delete_node(data)
            return self

        if self.right_child is None:
            return self.left_child

        if self.left_child is None:
            return self.right_child

        node = self.right_child
        while node.left_child:
            node = node.left_child

        self.root = node.root
        self.right_child = self.right_child.delete_node(node.root)
        return self

    #  Подготавливаем массив
    def bt_values(self, data):
        if len(data) < 1:
            return
        val = len(data) // 2
        self.array.append(data[val])
        self.bt_values(data[:val])
        self.bt_values(data[val + 1:])
        return

    #  выводим визуально дерево
    def write_bt(self, bt, this, s=False, e=False):
        if bt is None:
            return [], 0, 0, 0

        node = str(bt.root)
        left, lw, ls, lz = self.write_bt(bt.left_child, 2 * this + 1, s, e)
        right, rw, rs, rz = self.write_bt(bt.right_child, 2 * this + 2, s, e)
        nodes, lines, start, size = create_bt(lw, rw, ls, rs, lz, rz, len(node), node)
        end = start + len(node) - 1
        box = [''.join(nodes), ''.join(lines)]

        for item in range(max(len(left), len(right))):
            ll = left[item] if item < len(left) else ' ' * lw
            rl = right[item] if item < len(right) else ' ' * rw
            box.append(ll + size + rl)
        return box, len(box[0]), start, end


def main():
    # r = BinaryTree(8)
    # print(r.get_root_val())
    # print(r.get_left_child())
    # r.insert_left(40)
    # print(r.get_left_child())
    # print(r.get_left_child().get_root_val())
    # r.insert_right(12)
    # print(r.get_right_child())
    # print(r.get_right_child().get_root_val())
    # r.get_left_child().set_root_val(16)
    # print(r.get_right_child().get_root_val())

    n = BinaryTree()
    MIN_NUM = 8
    MAX_NUM = 37
    N_DATA = list(range(MIN_NUM, MAX_NUM + 1))
    print(green('***** Создаем дерево *****'), f'{N_DATA = }', sep='\n')
    n.insert(N_DATA)
    print(n)

    N_EL_ADD = 38
    print(green('***** Добавляем один элемент *****'), f'{N_EL_ADD = }', sep='\n')
    n.insert(N_EL_ADD)
    print(n)

    N_DATA_ADD = [1, 2, 3, 4, 5, 6, 7]
    print(green('***** Добавляем элементы пакетом *****'), f'{N_DATA_ADD = }', sep='\n')
    n.insert(N_DATA_ADD)
    print(n)

    N_EL_DEL = 19
    print(green('***** Удаляем один элемент *****'), f'{N_EL_DEL = }', sep='\n')
    n.delete(N_EL_DEL)
    print(n)

    N_DATA_DEL = [5, 3, 4, 1]
    print(green('***** Удаляем элементы пакетом *****'), f'{N_DATA_DEL = }', sep='\n')
    n.delete(N_DATA_DEL)
    print(n)
    print(go_bt(n), '\n')

    s = BinaryTree()
    S_DATA = ascii_lowercase
    print(green('***** Тоже самое создаем дерево со строковыми данными *****'), f'{S_DATA = }', sep='\n')
    s.insert(S_DATA)
    print(s)
    print(go_bt(s), '\n')

    w = BinaryTree()
    W_DATA = 'Умом Россию не понять, ' \
            'Аршином общим не измерить: ' \
            'У ней особенная стать — ' \
            'В Россию можно только верить.'
    print(green('***** Тоже самое создаем дерево с текстовыми данными *****'), f'{W_DATA = }', sep='\n')
    w_list = re.sub(r'[^\w\s]', '', W_DATA.lower()).split()
    w.insert(w_list)
    print(w)
    print(go_bt(w), '\n')


if __name__ == "__main__":
    main()
