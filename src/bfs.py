from re import search


class Node:
    def __init__(self, value, father) -> None:
        """
            Utilizando o codigo de estado (canibal, missionario, posicao da jangada, canibal, missionario) 
            temos o estado inicial -> 00r33; E os estado final -> 33l00
            Cada Nó tera o seu valor e conhecera o nó acima dele, dessa forma
            é possivel recriar o caminho até a origem
        """
        self.value = value
        self.father = father

    def is_valid(self, path):
        """
            a primeira condiconal verifica se o calculo do passo extrapolou a quantidade de canibais e missionarios
            a segunda verifica se a quantidade total de canibais ou missionarios continua sendo 3
            a terceira e quarta verifica se ha mais canibais que missionarios nos dois lados do rio

            path -> representa o estado atual do jogo, exemplo: o estado original -> 00r33
        """
        return (False if search(r'[4-9]', path) else True) \
                and ((int(path[0]) + int(path[3]) == 3) and (int(path[1]) + int(path[4]) == 3)) \
                and (int(path[0]) <= int(path[1]) if int(path[1]) != 0 else True) \
                and (int(path[3]) <= int(path[4]) if int(path[4]) != 0 else True)

    def get_name(self, origin, step):
        """
            realiza o calculo para encontrar o novo codigo de estado
            sempre fica variando com o barco, ou seja, 
            sempre que a entrada contiver o valor 'r' a saida sera com 'l'
        """
        if origin[2] == 'r':
            return str(f"{step[0] + int(origin[0])}{step[1] + int(origin[1])}l{int(origin[3]) - step[0]}{int(origin[4]) - step[1]}")
        return str(f"{int(origin[0]) - step[0]}{int(origin[1]) - step[1]}r{step[0] + int(origin[3])}{step[1] + int(origin[4])}")

    def get_adjacents(self):
        """
            responsavel por criar uma lista com todas os passos possiveis,
            levando em conta se o passo é valido.
        """
        steps = [(1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]
        adjacents = list()

        for step in steps:
            adjacent = self.get_name(self.value, step)
            if self.is_valid(adjacent):
                adjacents.append(adjacent)

        return adjacents

    def __str__(self) -> str:
        return self.value


class Graph:
    def __init__(self) -> None:
        """
            Utilizamos uma lista simples para criar a fronteira e os nós visitados
        """
        self.border = list()
        self.visited = list()

    def push(self, elem):
        """
            Adiciona o no na fronteira
        """
        self.border.append(elem)

    def pop(self):
        """
            remove o primeiro elemento da fronteira e adiciona nos visitados
        """
        elem = self.border.pop(0)
        self.visited.append(elem)

        return elem

    def get_path(self, origin):
        """
            faz a chamada reversa, quando estiver no destino realiza a pesquisa
            pelo pai de cada nó e retorna esse caminho em uma lista
        """
        last = self.visited[-1]

        path = list()

        while last.value != str(self.visited[0]):
            path.append(last.value)
            last = last.father

        path.append(origin)

        return list(reversed(path))

        
def bfs(origin, destiny):
    path = Graph()
    path.push(Node(origin, ''))

    while True:
        if not path.border:
            return "ERRO! Something's wrong."

        current_node = path.pop()

        if current_node.value == destiny:
            return path.get_path(origin)

        adjacents = sorted(current_node.get_adjacents())

        for adjacent in adjacents:
            path.push(Node(adjacent, current_node))
