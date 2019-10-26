class Utility:
    def __init__(self):
        self.dimension = (4,8)
        self.utilityMatrix = self.__fillUtilityMatrix()
        self.nextIterationUtilityMatrix = None
        self.convergenceCriterium = 0.01
    
    def __fillUtilityMatrix(self):
        # default value = 0
        matrix = []
        for i in range(self.dimension[0]):
            matrix.append([0]*self.dimension[1])
        return matrix
    
    def getUtilityOfState(self, state):
        return self.utilityMatrix[state[0]][state[1]]
    
    def updateUtility(self, state, newUtilityValue):
        if self.nextIterationUtilityMatrix == None:
            self.nextIterationUtilityMatrix = self.__fillUtilityMatrix()
        self.nextIterationUtilityMatrix[state[0]][state[1]] = newUtilityValue
    
    def updateUtilityMatrixIteration(self):
        maxDiff = 0
        for i in range(self.dimension[0]):
            for j in range(self.dimension[1]):
                diff = abs(self.utilityMatrix[i][j] - self.nextIterationUtilityMatrix[i][j])
                if diff > maxDiff:
                    maxDiff = diff
                self.utilityMatrix[i][j] = self.nextIterationUtilityMatrix[i][j]
        if maxDiff <= self.convergenceCriterium:
            return True
        return False


