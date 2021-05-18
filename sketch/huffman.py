from operator import attrgetter


class Node:
    def __init__(self, freq, char=None):
        self.freq = freq
        self.char = char
        self.left = None
        self.right = None
    
    def is_leaf(self):
        return (self.left is None) and (self.right is None)
    
    def __str__(self):
        return f'freq: {self.freq}, char: {self.char}, leaf:{self.is_leaf()}'

    def __add__(self, rhs):
        father = Node(self.freq + rhs.freq)
        father.left = self
        father.right = rhs
        return father

def calculate_frequency(data):
    frequency = dict()
    for i in data:
        frequency.setdefault(i, 0)
        frequency[i] += 1
    return frequency

def create_tree(frequency):
    nodes = [Node(j,i) for i,j in frequency.items()]
    func = lambda x: x.freq
    root = None

    while len(nodes) > 1:
        a = min(nodes, key=func)
        nodes.remove(a)        
        b = min(nodes, key=func)
        nodes.remove(b)

        root = a+b
        nodes.append(root)
    
    return root

def get_code(node, char):
    if node.is_leaf():
        return ''

    if node.left.char == char:
        return '0' 

    if node.right.char == char:
        return '1'

    lc = get_code(node.left, char)
    rc = get_code(node.right, char)

    if lc:
        code = '0' + lc
    elif rc:
        code = '1' + rc
    else:
        code = ''
    
    return code 

def encode(data, frequency):
    tree = create_tree(frequency)
    code = ''

    for char in data:
        code += get_code(tree, char)
    return code

def decode(code, frequency):
    tree = create_tree(frequency)
    data = ''

    temp = tree
    for i in range(len(code)):
        if code[i] == '0':
            temp = temp.left
        else:
            temp = temp.right 
        
        if temp.is_leaf():
            data += temp.char
            temp = tree
    return data