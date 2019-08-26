import csv
from math import sqrt 

class Map:
## Classe responsavel por lidar com os dados do "csv"
    def __init__(self, filename: str):
        csv_file = open(filename, mode='r')
        self.cidades = list(csv.DictReader(csv_file))
        self.numero_cidades = len(self.cidades)
        self.next_dict = self.__create_next()

        
    # Verifica se existe conexao direta entre os duas cidades
    def is_connected(self, id1: int, id2: int) -> bool:
        diff = abs(id1-id2)
        if diff > 2:
            return False
        if diff == 2:
            return True
        if min(id1,id2) % 2 == 1:
            return True
        return False
    
    # Calcula distancia real entre duas cidades
    def distance(self, id1, id2) -> float:
        cidade1 = self.get_cidade_id(id1)
        cidade2 = self.get_cidade_id(id2)
        lat = (float(cidade1["lat"])-float(cidade2["lat"]))**2
        lng = (float(cidade1["lng"])-float(cidade2["lng"]))**2
        return sqrt(lat+lng)
    
    # Calcula o custo do caminho
    def path_cost(self,path:list)-> float:
        total = 0
        num_city = len(path)
        for i in range(num_city-1):
            total += self.cost(path[i], path[i+1])
        return total

    # Custo do caminho, caso exista
    def cost(self, id1, id2) -> float:
        return 1.1*self.distance(id1,id2)

    # Obtem cidade a partir do id
    def get_cidade_id(self,id):
        return self.cidades[int(id)-1]
    
    # Cria um dicionario de proximos id
    def __create_next(self) -> dict:
        next = {}
        for cidade in self.cidades:
            id = int(cidade["id"])
            # range maximo de possivel conexao de acordo com criterio
            for i in range(-2,3):
                if i != 0 and id+i > 0 and id+i <= self.numero_cidades:
                    outro_cidade = self.get_cidade_id(id+i)
                    # verifica se estao conectados
                    if self.is_connected(int(cidade["id"]), int(outro_cidade["id"])):
                        # adiciona ao dicionario
                        if next.get(id) == None:
                            next[id] = [int(outro_cidade["id"])]
                        else:
                            next[id].append(int(outro_cidade["id"]))
        return next

    # Obtem id do cidade a partir do nome
    def get_id_city_name(self, nome_cidade):
        for cidade in self.cidades:
            if cidade["city"] == nome_cidade:
                return int(cidade["id"])
        return None

    # Todos os cidades conectados
    def next(self, id):
        return self.next_dict[id]


# Exemplicacao de uso
if __name__ == "__main__":
    mapa = Map('australia.csv')
    for cidade in mapa.cidades:
        print(cidade)

