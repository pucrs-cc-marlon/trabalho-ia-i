#!/usr/bin/env python
# coding=utf-8
# Four spaces as indentation [no tabs]
import sys
from queue import PriorityQueue

from common import *


# ==========================================
# PathFinder A Star
# ==========================================

class PathFinder_A_Star:
    def __init__(self):
        # TODO initialize your attributes here if needed
        pass

    # ------------------------------------------
    # Cost
    # ------------------------------------------

    def function(self, _map):
        # TODO priority function to use with the PriorityQueue
        # You are free not to use this function
        # (it is not tested in the unit test)
        queue = PriorityQueue()  # Fila de Prioridade
        queue.put(_map.start, 0)  # Adiciona o ponto de partida na fila
        custo = {_map.start: 0}  # Custo inicial do ponto de partida
        chegou_no_destino = False  # Variável de controle para identificar se o algoritmo chegou no destino
        caminho = {}  # Dicionário para armazenar o caminho percorrido
        while not queue.empty():  # Enquanto a fila não estiver vazia
            point = queue.get()  # Remove e pega o elemento da fila
            if point == _map.goal:  # Se ponto for o destino, para a recursão
                chegou_no_destino = True  # E sinaliza a variável de controle
                break
            for proximo in _map.successors(point.x, point.y):  # Pega os pontos sucessores do point
                n_custo = custo[point] + self.heuristic(point, proximo)  # f(n) = g(n) + h(n)
                if proximo not in custo or n_custo < custo[proximo]:  # Se o elemento não estiver no dicionário
                    # custo (ele não foi percorrido) OU se o custo atual for menor do custo armazenado
                    custo[proximo] = n_custo  # Armazena o custo do próximo nó
                    prioridade = n_custo + self.heuristic(_map.goal, proximo)  #
                    queue.put(proximo, prioridade)  # Adiciona o nó na fila
                    caminho[proximo] = point  # Adiciona o nó no dicionário do caminho apontando para o próximo nó
        return caminho if chegou_no_destino else None, \
               custo[_map.goal] if chegou_no_destino else None

    # ------------------------------------------
    # Heuristic
    # ------------------------------------------

    def heuristic(self, p1, p2):
        # Here, you must use Manhattan distance
        # (it is graded in the unit test)
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)

    # ------------------------------------------
    # Solve
    # ------------------------------------------

    def solve(self, _map):
        # TODO returns a list of movements (may be empty)
        # if plan found, otherwise return None
        caminho, custo = self.function(_map)  # Executa o método de busca A*
        caminho_final = []  # Lista contendo o caminho
        node = _map.goal  # O dicionário que é retornado começa do destino até a origem
        # (mas na pesquisa é feito da origem até o destino), então é armazenado o destino como ponto de partida
        if caminho is not None:  # Se o caminho for Nulo então não foi encontrado uma solução
            while node is not None and node in caminho:  # Enquanto o nó node não for nulo
                # (lembrando que vem de trás para frente) e o nó estiver no dicionário
                # (isso acontece no caso do ponto de partida já que ele não tem nó node a ele)
                atual = node  # Armazena o nó node
                node = caminho[node]  # armazena
                caminho_final.insert(0, direction(node.x, node.y, atual.x, atual.y))  # Pega a direção de movimento
                # que o agente deve realizar através do método
                # auxiliar e armazena sempre no começo da lista
        return caminho_final if caminho is not None else None

    # ------------------------------------------
    # Get solvable
    # ------------------------------------------

    def get_solvable(self, _map):
        # TODO returns True if plan found,
        # otherwise returns False
        return False if self.solve(_map) is None else True

    # ------------------------------------------
    # Get max tree height
    # ------------------------------------------

    def get_max_tree_height(self, _map):
        # TODO returns max tree height if plan found,
        # otherwise, returns None
        path, custo = self.function(_map=_map)
        return custo if custo is not None else None

    # ------------------------------------------
    # Get min moves
    # ------------------------------------------

    def get_min_moves(self, _map):
        # TODO returns size of minimal plan to reach goal if plan found,
        # otherwise returns None
        path = self.solve(_map=_map)
        return len(path) if path is not None else None


# ------------------------------------------
# Main
# ------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) == 2:
        map_name = sys.argv[1]
    else:
        map_name = DEFAULT_MAP
    print("Loading map: " + map_name)
    plan = PathFinder_A_Star().solve(read_map(map_name))
    if plan is None:
        print("No plan was found")
    else:
        print("Plan found:")
        for i, move in enumerate(plan):
            if move == MOVE_UP:
                print(i, ": Move Up")
            elif move == MOVE_DOWN:
                print(i, ": Move Down")
            elif move == MOVE_LEFT:
                print(i, ": Move Left")
            elif move == MOVE_RIGHT:
                print(i, ": Move Right")
            else:
                print(i, ": Movement unknown = ", move)
