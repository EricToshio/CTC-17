from Data import Data
from itertools import permutations, combinations

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
        self.average = self.truncated_median

    
    def PredictRating(self, sample):
        return self.average

class ClassifierDecisionTree:
    def __init__(self, data):
        self.data = data
        self.count = 0
        self.tree = None
        self.atribOrder = []
    
    def CreateTree(self, samples, atrib, default):
        # Verifica se existe exemplos
        if len(samples) == 0 or len(atrib) == 0:
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
        self.atribOrder.append(best_atr)
        root = Node(value=best_atr)
        new_default = self.GetMode(samples)
        new_atrib = atrib.copy()
        new_atrib.remove(best_atr)
        for v in self.data.atrib[best_atr]:
            new_samples = self.FilterSamples(samples,best_atr,v)
            root.next[v] = self.CreateTree(new_samples, new_atrib, new_default)
        
        self.tree = root
        return root
    
    def PredictRating(self, sample):
        root = self.tree
        atribInd = 0
        while not root.is_leaf:
            
            a = sample[self.atribOrder[atribInd]]
            root = root.next[a]
            atribInd += 1
        
        return root.val

    def ChooseAtrib(self,samples,atrib):
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

def calculate_kappa(matrix):
    rows_sum = [0]*5
    total = 0
    for i,el in enumerate(matrix):
        rows_sum[i] = sum(el)
        total += rows_sum[i]
    cols_sum = [0]*5
    for i in range(5):
        cols_sum[i] = sum([matrix[j][i] for j in range(5)])
    print(rows_sum)
    print(cols_sum)
    p0 = sum([matrix[i][i] for i in range(5)])/total
    pe = sum([rows_sum[i]*cols_sum[i] for i in range(5)])/(total**2)
    k = (p0-pe)/(1-pe)
    print("kappa: ",k)
    return k

if __name__ == "__main__":
    data = Data()
    training_set, test_set = data.generate_samples(30)
    ###########################################
    # classifier_priori = ClassifierPriori(data)
    # print(classifier_priori.truncated_median)
    # print(classifier_priori.mode)
    ###########################################
    subsets = []
    for i in range(1,len(data.key_atrib)+1):
        subsets+=list(map(list, combinations(data.key_atrib, i)))
    best = None
    value_best = 0


    
    for subset in subsets:
        atribs = list(permutations(subset))

        for atrib in atribs:
            mat = []
            for i in range(5):
                mat.append([0]*5)
            classifier_tree = ClassifierDecisionTree(data)
            print(list(atrib))
            tree = classifier_tree.CreateTree(training_set,list(atrib),0)
            # show_tree(tree)
            right = 0
            wrong = 0
            for test in test_set:
                predictedRating = classifier_tree.PredictRating(test)
                if predictedRating == test["Rating"]:
                    right += 1
                else:
                    wrong += 1
                mat[test["Rating"]-1][predictedRating-1] += 1
            # print("matriz de confusao")
            # for i in range(5):
            #     for j in mat[i]:
            #         print("{:10d}".format(j),end=' ')
            #     print()
            #calculate_kappa(mat)
            #print("correct predicts: {}".format(right))
            #print("wrong predicts: {}".format(wrong))
            print("hit rate (%): {}".format(right/(right+wrong)*100))

            if right/(right+wrong)*100> value_best:
                value_best = right/(right+wrong)*100
                best = atrib

    print("BEST",best)
    print("hit rate",value_best)
    '''        
    print("teste >>>>>>>>>>")
    for atrib in atribs:
        classifier_tree = ClassifierDecisionTree(data)
        tree = classifier_tree.CreateTree(training_set,list(atrib),0)
        # show_tree(tree)
        right = wrong = 0
        for test in test_set[-14:]:
            predictedRating = classifier_tree.PredictRating(test)
            if predictedRating == test["Rating"]:
                right += 1
            else:
                wrong += 1
        print("correct predicts: {}".format(right))
        print("wrong predicts: {}".format(wrong))
        print("hit rate (%): {}".format(right/(right+wrong)*100))
    '''
    