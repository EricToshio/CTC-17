from Data import Data
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




if __name__ == "__main__":
    data = Data()
    classifier_priori = ClassifierPriori(data)
    print(classifier_priori.truncated_median)
    print(classifier_priori.mode)
    pass