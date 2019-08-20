from menor_caminho.Map import Map
mapa = Map('menor_caminho/australia.csv')


def Zero(*args):
    return 0

class Search:
    def __init__(self, initial, next_states, goal, h, g = Zero):
        self.g = g                     #function g          : custo real para chegar ao estado
        self.h = h                     #function h          : custo estimado minimo
        self.goal = goal               #goal state          : estado objetivo
        self.initial = initial          #inital state        : estado inicial
        self.next_states = next_states #function next_states: retorna o array dos proximos estados
        self.path = [initial]          #array path          : vetor do caminho a percorrer 
    

    def execute(self):
        path = self.DFS(self.initial)
        print("Solucao achada:", path)
        return path
    
    def DFS (self, state, path = []):
        new_path = path.copy()
        new_path.append(state)
        if state == self.goal:
            return new_path
        next_states = self.next_states(state)
        next_states.sort(key = lambda new_state: self.h(new_state, self.goal) + self.g(new_state, state))
        for new_state in next_states:
            if new_state not in new_path:
                sol = self.DFS(new_state, new_path)
                if sol != None:
                    return sol
        return None
            


if __name__ == "__main__":
    # menor_caminho Greedy
    Search(initial=mapa.get_pais_city("Alice Springs"), next_states=mapa.next, goal= mapa.get_pais_city("Yulara"), h = mapa.distance).execute()
    # menor_caminho A*
    Search(initial=mapa.get_pais_city("Alice Springs"), next_states=mapa.next, goal= mapa.get_pais_city("Yulara"), h = mapa.distance, g = mapa.distance).execute() 