from Data import Data

class Node:
    def __init__(self, value, is_leaf = False):
        self.val = value
        self.is_leaf = is_leaf
        self.next = {}



class ClassifierPriori:
    def __init__(self, data):
        count = {}

        for rating in data.ratings:
            if count.get(rating["Rating"]) == None:
                count[rating["Rating"]] = 1
            else:
                count[rating["Rating"]] = count[rating["Rating"]] + 1
        
        total = 0
        mode = None
        count_mode = 0
        for rate in count:
            total += rate*count[rate]
            if count_mode < count[rate]:
                mode = rate
                count_mode = count[rate]

        self.mode = mode
        self.truncated_median = int(total/len(data.ratings))

class ClassifierDecisionTree:
    def __init__(self, data):
        self.data = data
    
    def CreateTree(self, samples, atrib, default):
        # Verifica se existe exemplos
        if len(samples) == 0:
            return Node(value=default,is_leaf=True)
        # Verifica se todos os exemplos tem a mesma classificacao
        same_classification = True
        classification = samples[0]["Rating"]
        for sample in samples:
            if sample["Rating"] != classification:
                same_classification = False
                break
        if same_classification:
            return Node(value=classification,is_leaf=True)
        # Faz uma nova ramificacao
        best_atr = self.ChooseAtrib(samples,atrib)
        root = Node(value=best_atr)
        new_default = self.GetMode(samples)
        new_atrib = atrib.copy()
        new_atrib.remove(best_atr)
        for v in self.data.atrib[best_atr]:
            new_samples = self.FilterSamples(samples,best_atr,v)
            root.next[v] = self.CreateTree(new_samples, new_atrib, new_default)
        
        return root



    def ChooseAtrib(self,samples,atrib):
        # TO-DO
        # Escolhe o melhor atributo baseado no exemplos
        return None
        

    def GetMode(self,samples):
        # TO-DO
        # Escolhe a moda dos exemplos
        return None
        

    def FilterSamples(self,samples,atrib,value):
        # TO-DO
        # Filtra os exemplos de acordo um uma escolha de determinado atributo
        return None
    

if __name__ == "__main__":
    data = Data()
    classifier_priori = ClassifierPriori(data)
    print(classifier_priori.truncated_median)
    print(classifier_priori.mode)
    pass