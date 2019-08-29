from menor_caminho.Map import Map
import heapq
from blocos_deslizantes import Puzzle as puzzle_logic
from blocos_deslizantes import GUI as puzzle_gui
from menor_caminho.GUI import *

mapa = Map('menor_caminho/australia.csv')

def Zero(*args):
    return 0

class Node:
    def __init__(self, state, g, h):
        self.state = state
        self.g = g
        self.h = h
        self.f = g + h
        self.previous = None
    def __lt__(self, other_node):
        return self.f < other_node.f


class Search:
    def __init__(self, initial, next_states, goal, h, g = None):
        self.type = "A star"
        if not g:
            g = Zero
            self.type = "Greedy"
        self.g = g                      #function g          : custo real para chegar ao estado
        self.h = h                      #function h          : custo estimado minimo
        self.goal = goal                #goal state          : estado objetivo
        self.initial = initial          #inital state        : estado inicial
        self.next_states = next_states  #function next_states: retorna o array dos proximos estados
        self.path = [initial]           #array path          : vetor do caminho a percorrer 
    

    def execute(self):
        # Salva os estados ja visitados
        closed_states = set()
        # Dicionario estado->no
        direct = {}
        # Cria o no do estado inicial e adiciona ao heap
        new_node = Node(state = self.initial,g = 0, h = self.h(self.initial,self.goal))
        direct[self.initial] = new_node
        open_node_heap = [new_node]
        # Enquanto o estado final nao e visitado
        while self.goal not in closed_states:
            # Pega o no de menor valor e o estado dele
            actual_node = heapq.heappop(open_node_heap)
            actual_state = actual_node.state
            # Adiciona o estado de menor valor aos estados visitados
            closed_states.add(actual_state)
            # Analisa o estados vizinhos
            for state in self.next_states(actual_node.state):
                # Verifica se eles ja foram visitados
                if state not in closed_states:
                    # Calcula o valor de 'g' e 'h' dos vizinhos
                    new_g = actual_node.g + self.g(state, actual_state)
                    new_h = self.h(state, self.goal)
                    # Verifica se ja foram adicionados ao heap
                    if direct.get(state) == None:
                        # Caso nao tenham sido adicionados
                        new_node = Node(state = state,g = new_g, h = new_h)
                        new_node.previous = actual_node
                        direct[state] = new_node
                        # Adiciona na heap
                        heapq.heappush(open_node_heap, new_node)
                    else:
                        # Caso tenham sido adicionados, compara os valores
                        if new_g + new_h < direct[state].f:
                            # Modifica os valores
                            direct[state].g = new_g
                            direct[state].h = new_h
                            direct[state].f = new_g + new_h
                            direct[state].previous = actual_node
                            # Atualiza a heap
                            heapq.heapify(open_node_heap)
        # Caminho gerado
        path = []
        actual_node = direct[self.goal]
        while actual_node.previous != None:
            path.append(actual_node.state)
            actual_node = actual_node.previous
        path.append(actual_node.state)
        path.reverse()
        print("Solucao achada({}): {}".format(self.type, len(path)))

        return path


if __name__ == "__main__":
    # ------ inicio menor caminho --------------------
    # 1) Menor caminho utilizando Greedy
    # path = Search(initial=mapa.get_id_city_name("Alice Springs"), next_states=mapa.next, goal= mapa.get_id_city_name("Yulara"), h = mapa.distance).execute()
    # print("Custo total:", mapa.path_cost(path))
    # print("Caminho achado:\n",mapa.show_path(path))
    # MapDraw(mapa.cidades, path)
    #
    # 2) Menor caminho utilizando A*
    # path = Search(initial=mapa.get_id_city_name("Alice Springs"), next_states=mapa.next, goal= mapa.get_id_city_name("Yulara"), h = mapa.distance, g = mapa.cost).execute() 
    # print("Custo total:", mapa.path_cost(path))
    # print("Caminho achado:\n",mapa.show_path(path))
    # MapDraw(mapa.cidades, path)
    #
    # ------ fim menor caminho -----------------------
    # ------ inicio blocos deslizantes ---------------
    node = puzzle_logic.Node() # passe no construtor o tamanho do board. O padrao eh 9
    goal_state = node.get_state()
    print(goal_state)
    # node.shuffle() # passe no construtor uma tupla indicando minimo e maximo do numero de movimentos. O padrao eh (30, 50)
    # initial_state = node.get_state()
    ### TESTE FACIL
    #initial_state = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,0,61,62,63,64,65,66,67,68,60,71,79,72,73,74,75,76,77,69,78,70,80"
    ### TESTE NAO TAO FACIL
    initial_state = "10,44,27,28,61,8,14,17,0,22,6,16,43,48,51,36,2,68,24,38,37,45,18,41,70,34,46,55,4,1,30,50,58,32,12,9,3,23,60,56,40,15,72,54,20,7,25,11,47,5,74,29,35,26,52,57,73,65,49,42,77,78,21,31,67,13,53,62,66,80,33,69,39,75,64,19,59,76,63,79,71"
    (g,h,next_states) = node.get_evaluation_functions()
    # solution = Search(initial=initial_state, next_states=next_states, goal=goal_state, h=h, g=g).execute() 
    # puzzle_gui.Game(solution)
    solution = Search(initial=initial_state, next_states=next_states, goal=goal_state, h=h).execute() 
    puzzle_gui.Game(solution)
    # ------ fim blocos deslizantes ------------------
    pass