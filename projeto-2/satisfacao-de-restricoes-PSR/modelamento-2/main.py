import itertools 
nos_expandidos = 0
class State:
    def __init__(self, default='position'):
        self.numOfRows = 6
        self.numOfColumns = 5
        self.state = {
            "nacionality": [None for c in range(self.numOfColumns)],
            "color": [None for c in range(self.numOfColumns)],
            "animal": [None for c in range(self.numOfColumns)],
            "cigarrete": [None for c in range(self.numOfColumns)],
            "beverage": [None for c in range(self.numOfColumns)],
            "position": [c+1 for c in range(self.numOfColumns)]
        }
    
    def reset(self):
        self.state = {
            "position": [c+1 for c in range(self.numOfColumns)],
            "nacionality": [None for c in range(self.numOfColumns)],
            "color": [None for c in range(self.numOfColumns)],
            "animal": [None for c in range(self.numOfColumns)],
            "cigarrete": [None for c in range(self.numOfColumns)],
            "beverage": [None for c in range(self.numOfColumns)],
        }
    
    def printState(self):
        order = ['position','nacionality','beverage','cigarrete','animal','color']
        for key in order:
            print("%15s | %15s | %15s | %15s | %15s | %15s" % (key, self.state[key][0], self.state[key][1], self.state[key][2], self.state[key][3], self.state[key][4]))
    
    def resetRow(self, variable):
        self.state[variable] = [None for c in range(self.numOfColumns)]

    def addValue(self, variable, position, value):
        # if self.state[variable][position]:
            # print("WARN: overwrite value")
        self.state[variable][position] = value
    
    def removeValue(self, variable, position, value):
        # if not self.state[variable][position]:
            # print("WARN: empty value")
        self.state[variable][position] = None
    
    def isValidState(self):
        for j in range(self.numOfColumns):
            if not self.state['nacionality'][j] or not self.state['color'][j]:
                continue
            if (self.state['nacionality'][j] == 'ingles' and self.state['color'][j] != 'vermelha') or (self.state['nacionality'][j] != 'ingles' and self.state['color'][j] == 'vermelha'):
                return False

        for j in range(self.numOfColumns):
            if not self.state['nacionality'][j] or not self.state['animal'][j]:
                continue
            if (self.state['nacionality'][j] == 'espanhol' and self.state['animal'][j] != 'cachorro') or (self.state['nacionality'][j] != 'espanhol' and self.state['animal'][j] == 'cachorro'):
                return False
        
        for j in range(self.numOfColumns):
            if not self.state['position'][j] or not self.state['nacionality'][j]:
                continue
            if (self.state['position'][j] == 1 and self.state['nacionality'][j] != 'noruegues') or (self.state['position'][j] != 1 and self.state['nacionality'][j] == 'noruegues'):
                return False
        
        for j in range(self.numOfColumns):
            if not self.state['cigarrete'][j] or not self.state['color'][j]:
                continue
            if (self.state['cigarrete'][j] == 'Kool' and self.state['color'][j] != 'amarela') or (self.state['cigarrete'][j] != 'Kool' and self.state['color'][j] == 'amarela'):
                return False
        
        for j in range(self.numOfColumns):
            if not self.state['cigarrete'][j] or not self.state['animal'][j]:
                continue
            if (self.state['cigarrete'][j] == 'Winston' and self.state['animal'][j] != 'caramujos') or (self.state['cigarrete'][j] != 'Winston' and self.state['animal'][j] == 'caramujos'):
                return False
        
        for j in range(self.numOfColumns):
            if not self.state['cigarrete'][j] or not self.state['beverage'][j]:
                continue
            if (self.state['cigarrete'][j] == 'Lucky' and self.state['beverage'][j] != 'suco de laranja') or (self.state['cigarrete'][j] != 'Lucky' and self.state['beverage'][j] == 'suco de laranja'):
                return False
        
        for j in range(self.numOfColumns):
            if not self.state['nacionality'][j] or not self.state['beverage'][j]:
                continue
            if (self.state['nacionality'][j] == 'ucraniano' and self.state['beverage'][j] != 'cha') or (self.state['nacionality'][j] != 'ucraniano' and self.state['beverage'][j] == 'cha'):
                return False
        
        for j in range(self.numOfColumns):
            if not self.state['nacionality'][j] or not self.state['cigarrete'][j]:
                continue
            if (self.state['nacionality'][j] == 'japones' and self.state['cigarrete'][j] != 'Parliament') or (self.state['nacionality'][j] != 'japones' and self.state['cigarrete'][j] == 'Parliament'):
                return False
        
        for j in range(self.numOfColumns):
            if not self.state['color'][j] or not self.state['beverage'][j]:
                continue
            if (self.state['color'][j] == 'verde' and self.state['beverage'][j] != 'cafe') or (self.state['color'][j] != 'verde' and self.state['beverage'][j] == 'cafe'):
                return False
            
        for j in range(self.numOfColumns):
            if not self.state['position'][j] or not self.state['beverage'][j]:
                continue
            if (self.state['position'][j] == 3 and self.state['beverage'][j] != 'leite') or (self.state['position'][j] != 3 and self.state['beverage'][j] == 'leite'):
                return False
        
        for j in range(self.numOfColumns):
            a = True
            b = True
            if self.state['animal'][j] and self.state['animal'][j] == 'raposa':
                if j < self.numOfColumns - 1 and self.state['cigarrete'][j+1]:
                    if self.state['cigarrete'][j+1] != 'chester':
                        a = False
                if j > 0 and self.state['cigarrete'][j-1]:
                    if self.state['cigarrete'][j-1] != 'chester':
                        b = False
            if j == 0 and not a:
                return False
            if j == self.numOfColumns - 1 and not b:
                return False
            if not a and not b:
                return False
        

        for j in range(self.numOfColumns):
            a = True
            b = True
            if self.state['color'][j] and self.state['color'][j] == 'azul':
                if j < self.numOfColumns - 1 and self.state['nacionality'][j+1]:
                    if self.state['nacionality'][j+1] != 'noruegues':
                        a = False
                if j > 0 and self.state['nacionality'][j-1]:
                    if self.state['nacionality'][j-1] != 'noruegues':
                        b = False
            if j == 0 and not a:
                return False
            if j == self.numOfColumns - 1 and not b:
                return False
            if not a and not b:
                return False

        for j in range(self.numOfColumns):
            a = True
            b = True
            if self.state['animal'][j] and self.state['animal'][j] == 'cavalo':
                if j < self.numOfColumns - 1 and self.state['cigarrete'][j+1]:
                    if self.state['cigarrete'][j+1] != 'Kool':
                        a = False
                if j > 0 and self.state['cigarrete'][j-1]:
                    if self.state['cigarrete'][j-1] != 'Kool':
                        b = False
            if j == 0 and not a:
                return False
            if j == self.numOfColumns - 1 and not b:
                return False
            if not a and not b:
                return False

        for j in range(self.numOfColumns - 1):
            if self.state['color'][j] and self.state['color'][j+1]:
                if (self.state['color'][j] == 'marfim' and self.state['color'][j+1] != 'verde') or (self.state['color'][j] != 'marfim' and self.state['color'][j+1] == 'verde'):
                    return False
            if self.state['color'][self.numOfColumns-1] and self.state['color'][self.numOfColumns-1]=='marfim':
                return False
        
        return True

if __name__=='__main__':
    aa = State()

    order = ['beverage','nacionality','cigarrete','color','animal']
    domains = {
        'color': list(itertools.permutations(['vermelha','amarela','azul','verde','marfim'])),
        'nacionality': list(itertools.permutations(['ingles','espanhol','noruegues','ucraniano','japones'])),
        'cigarrete': list(itertools.permutations(['chester','Kool','Winston','Lucky','Parliament'])),
        'animal': list(itertools.permutations(['cachorro','raposa','caramujos','cavalo','zebra'])),
        'beverage': list(itertools.permutations(['agua','suco de laranja','cha','cafe','leite'])),
    }

    nodes = [0]
    def solveCSP(depth):
        global nos_expandidos
        nos_expandidos += 1
        if depth == len(order):
            return aa.isValidState()
        domain = domains[order[depth]]
        for value in domain:
            for i in range(len(value)):
                aa.addValue(order[depth],i,value[i])
            nodes[0] += 1
            if aa.isValidState():
                res = solveCSP(depth+1)
                if res:
                    return True
            else:
                aa.resetRow(order[depth])
        return False

    solveCSP(0)
    print(aa.isValidState())
    print(nodes[0])
    aa.printState()
    print("total de nos expandidos", nos_expandidos)
