import csv
from math import sqrt 

class Map:
## Classe responsavel por lidar com os dados do "csv"
    def __init__(self, filename: str):
        csv_file = open(filename, mode='r')
        self.paises = list(csv.DictReader(csv_file))
        self.numero_paises = len(self.paises)
        self.next = self.__create_next()

        
    # Verifica se existe conexao direta entre os dois paises
    def is_connected(self, pais1, pais2) -> bool:
        id1 = int(pais1["id"])
        id2 = int(pais2["id"])
        diff = abs(id1-id2)
        if diff > 2:
            return False
        if diff == 2:
            return True
        if min(id1,id2) % 2 == 1:
            return True
        return False
    
    # Calcula distancia entre dois paises
    def distance(self, pais1, pais2) -> float:
        lat = (float(pais1["lat"])-float(pais2["lat"]))**2
        lng = (float(pais1["lng"])-float(pais2["lng"]))**2
        return 1.1*sqrt(lat+lng)

    # Obtem pais a partir do id
    def get_pais(self,id):
        return self.paises[int(id)-1]
    
    # Cria um dicionario de proximos elementos, junto ja adiciona o custo ate eles
    def __create_next(self) -> dict:
        next = {}
        for pais in self.paises:
            id = int(pais["id"])
            # range maximo de possivel conexao de acordo com criterio
            for i in range(-2,3):
                if i != 0 and id+i > 0 and id+i <= self.numero_paises:
                    outro_pais = self.get_pais(id+i)
                    # verifica se estao conectados
                    if self.is_connected(pais, outro_pais):
                        # adiciona ao dicionario
                        if next.get(id) == None:
                            next[id] = [{"id":id+i,"dist":self.distance(pais, outro_pais)}]
                        else:
                            next[id].append({"id":id+i,"dist":self.distance(pais, outro_pais)})
        return next


# Exemplicacao de uso
if __name__ == "__main__":
    mapa = Map('australia.csv')
    for pais in mapa.paises:
        print(pais)

