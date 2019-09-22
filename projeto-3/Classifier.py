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
        self.count = 0
    
    def CreateTree(self, samples, atrib, default):
        # Verifica se existe exemplos
        if len(samples) == 0:
            self.count += 1
            return Node(value=default,is_leaf=True)
        # Verifica se todos os exemplos tem a mesma classificacao
        same_classification = True
        classification = samples[0]["Rating"]
        for sample in samples:
            if sample["Rating"] != classification:
                same_classification = False
                break
        if same_classification:
            self.count += 1
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
        return atrib[0]
        

    def GetMode(self,samples):
        # Escolhe a moda dos exemplos
        count = [0]*6
        for sample in samples:
            count[sample["Rating"]] += 1
        maxi = 0
        best_rate = 0
        for rate in range(1,6):
            if count[rate] > maxi:
                maxi = count[rate]
                best_rate = rate
        return best_rate
        

    def FilterSamples(self,samples,atrib,value):
        # Filtra os exemplos de acordo um uma escolha de determinado atributo
        new_samples = []
        for sample in samples:
            if sample[atrib] == value:
                new_samples.append(sample)
        return new_samples
    

def show_tree(tree,intern=0):
    print("*"*intern,tree.val)
    if not tree.is_leaf:
        for son in tree.next:
            show_tree(tree.next[son],intern+1)

if __name__ == "__main__":
    data = Data()
    training_set, teste_set = data.generate_samples()
    ###########################################
    # classifier_priori = ClassifierPriori(data)
    # print(classifier_priori.truncated_median)
    # print(classifier_priori.mode)
    ###########################################
    classifier_tree = ClassifierDecisionTree(data)
    tree = classifier_tree.CreateTree(training_set,data.key_atrib,0)
    # show_tree(tree)