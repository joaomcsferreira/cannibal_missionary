from re import search


class Node:
    def __init__(self, value, father) -> None:
        self.value = value
        self.father = father

    def __str__(self) -> str:
        return self.value


class Graph:
    def __init__(self) -> None:
        self.border = list()
        self.nodes = list()

    def push(self, elem):
        self.border.append(elem)

    def pop(self):
        elem = self.border.pop(0)
        self.nodes.append(elem)

        return elem

    def get_node(self, elem):
        for i in self.nodes:
            if i.value == elem:
                return i
    
    def is_valid(self, path):
        return (False if search(r'[4-9]', path) else True) \
                and ((int(path[0]) + int(path[3]) == 3) and (int(path[1]) + int(path[4]) == 3)) \
                and (int(path[0]) <= int(path[1]) if int(path[1]) != 0 else True) \
                and (int(path[3]) <= int(path[4]) if int(path[4]) != 0 else True)

    def step(self, origin, path):
        if origin[2] == 'r':
            return str(f"{path[0] + int(origin[0])}{path[1] + int(origin[1])}l{int(origin[3]) - path[0]}{int(origin[4]) - path[1]}")
        return str(f"{int(origin[0]) - path[0]}{int(origin[1]) - path[1]}r{path[0] + int(origin[3])}{path[1] + int(origin[4])}")

    def get_adjacents(self, node):
        steps = [(1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]
        adjacents = list()

        for step in steps:
            adjacent = self.step(node, step)
            if self.is_valid(adjacent):
                adjacents.append(adjacent)

        return adjacents

    def get_path(self):
        last = self.nodes[-1]

        path = list()

        while last.value != str(self.nodes[0]):
            path.append(last.value)
            last = self.get_node(last.father)

        path.append('00r33')

        return list(reversed(path))

        
def bfs(origin, destiny):
    path = Graph()
    path.push(Node(origin, ''))

    while True:
        if not path.border:
            return "ERRO! Something's wrong."

        current_node = path.pop()

        if current_node.value == destiny:
            return path.get_path()

        adjacents = sorted(path.get_adjacents(current_node.value))

        for adjacent in adjacents:
            path.push(Node(adjacent, current_node.value))
