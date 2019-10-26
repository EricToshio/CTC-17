from Data import Data
from itertools import permutations
import sys
import random


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

        # sum = 0
        # for rating in data.ratings:
        #     sum += rating["Rating"]
        # self.average = int(sum/len(data.ratings))
    
    def PredictRating(self, sample):
        return self.average

class ClassifierDecisionTree:
    def __init__(self, data):
        self.data = data
        self.count = 0
        self.tree = None
        self.atribOrder = []
    
    def CreateTree(self, samples, atrib, default=0):
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

def calculate_kappa(matrix):
    rows_sum = [0]*5
    total = 0
    for i,el in enumerate(matrix):
        rows_sum[i] = sum(el)
        total += rows_sum[i]
    cols_sum = [0]*5
    for i in range(5):
        cols_sum[i] = sum([matrix[j][i] for j in range(5)])
    p0 = sum([matrix[i][i] for i in range(5)])/total
    pe = sum([rows_sum[i]*cols_sum[i] for i in range(5)])/(total**2)
    k = (p0-pe)/(1-pe)
    print("kappa: ",k)
    return k

def quadratic_error(matrix):
    total_ele = 0
    diff = [0]*6
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            total_ele += matrix[i][j]
            diff[abs(i-j)]+= matrix[i][j]
    total = 0
    for i in range(len(diff)):
        total+= (i**2)*diff[i]
    print("quadratic error:{:.4}".format(total/total_ele))

def suggestion(age):
    print("Gerando sugestoes... (isso pode demorar um pouco)\n")
    data_age = 1
    if age >= 18:
        data_age = 18
    if age >= 25:
        data_age = 25
    if age >= 35:
        data_age = 35
    if age >= 45:
        data_age = 45
    if age >= 50:
        data_age = 50
    if age >= 56:
        data_age = 56
    
    data = Data()
    atrib = ["Year","GenderMovie","Age"]
    classifier_tree = ClassifierDecisionTree(data)
    training_set, _ = data.generate_samples(1)
    classifier_tree.CreateTree(training_set,atrib)

    movie_samples = data.generate_sample_with_age(data_age)
    movie_by_rate = {0:[],1:[],2:[],3:[],4:[],5:[]}
    for movie_sample in movie_samples:
        rate = classifier_tree.PredictRating(movie_sample)
        movie_by_rate[rate].append(movie_sample)
    
    for movie in random.choices(movie_by_rate[5],k=3):
        print(movie["Title"])




if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "sugestao":
        age = int(sys.argv[2])
        suggestion(age)
    else:
        # Obtem os dados
        data = Data()
        # Seleciona os atributos a serem utilizados
        atrib = ["Year","GenderMovie","Age"]
        # Gera o subconjuntos de treinamento e teste
        training_set, test_set = data.generate_samples(30)
        #######################################################
        print("CLASSIFICADOR A PRIORI")
        # Gera classificador a priori
        classifier_priori = ClassifierPriori(data)
        # Analise do classificador a priori
        mat = []
        for i in range(5):
            mat.append([0]*5)
        right = wrong = 0
        for test in test_set:
            predictedRating = classifier_priori.PredictRating(test)
            if predictedRating == test["Rating"]:
                right += 1
            else:
                wrong += 1
            mat[test["Rating"]-1][predictedRating-1] += 1
        print("matriz de confusao")
        for i in range(5):
            print(mat[i])
        calculate_kappa(mat)
        quadratic_error(mat)
        print("correct predicts: {}".format(right))
        print("wrong predicts: {}".format(wrong))
        print("hit rate (%): {}".format(right/(right+wrong)*100))
        print("TESTE COM OS NOVOS DADOS")
        right = wrong = 0
        for test in test_set[-14:]:
            predictedRating = classifier_priori.PredictRating(test)
            if predictedRating == test["Rating"]:
                right += 1
            else:
                wrong += 1
        print("correct predicts: {}".format(right))
        print("wrong predicts: {}".format(wrong))
        print("hit rate (%): {}".format(right/(right+wrong)*100))
        

        #######################################################
        print("********************************************")
        print("CLASSIFICADOR POR MEIO DA ARVORE DE DECISAO")
        # Gera o classificador de arvore de decisao
        classifier_tree = ClassifierDecisionTree(data)
        # Analise do da arvore de decisao
        mat = []
        for i in range(5):
            mat.append([0]*5)
        classifier_tree.CreateTree(training_set,atrib)
        right = wrong = 0
        for test in test_set:
            predictedRating = classifier_tree.PredictRating(test)
            if predictedRating == test["Rating"]:
                right += 1
            else:
                wrong += 1
            mat[test["Rating"]-1][predictedRating-1] += 1
        print("matriz de confusao")
        for i in range(5):
            print(mat[i])
        calculate_kappa(mat)
        quadratic_error(mat)
        print("correct predicts: {}".format(right))
        print("wrong predicts: {}".format(wrong))
        print("hit rate (%): {}".format(right/(right+wrong)*100))
        print("TESTE COM OS NOVOS DADOS")
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