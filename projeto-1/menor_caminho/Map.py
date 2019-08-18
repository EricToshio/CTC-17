import csv
from math import sqrt 

class Map:
## Classe responsavel por lidar com os dados do "csv"
    def __init__(self):
        csv_file = open('australia.csv', mode='r')
        self.paises = list(csv.DictReader(csv_file))
        self.size = len(self.paises)

        
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


# Exemplicacao de uso
if __name__ == "__main__":
    mapa = Map()
    for pais in mapa.paises:
        print(pais)
