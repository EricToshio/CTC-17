import World
import Utility
import actions
import actionProbability
import GUI
import sys

def maxFunc(pair):
    return pair[1]

def maxActions(state, utilities):
    result = []
    maximum = max(utilities, key=maxFunc)
    for i in utilities:
        if i[1] == maximum[1]:
            result.append((state, i[0]))
    return result

def determinePolicy(utility, discountFactor):
    world = World.World()
    states = world.getStatesArray()

    policy = []
    
    for state in states:
        tempUtilities = []
        for action in actions.actionsArray:
            probabilities = actionProbability.defineProbabilityArray(action)
            sigmaSum = 0

            for actionToNewState, p in probabilities:
                nextState = world.getNextState(state, actionToNewState)
                sigmaSum += p*(world.getReward(state, nextState)+utility.getUtilityOfState(nextState)*discountFactor)
            tempUtilities.append((action,sigmaSum))
        bestActions = maxActions(state, tempUtilities)
        policy.extend(bestActions)
    return policy

def runRL(discountFactor = 0.7):
    world = World.World()
    states = world.getStatesArray()
    utility = Utility.Utility()
    print("Valores utilidades obtidos a cada iteração")
    print('*'*64)

    convergence = False
    while not convergence:
        for state in states:
            if world.need_restart(state):
                maxUtility = 0
                dimension = utility.getDimesion()
                utilitys = utility.getAllUtilitys()
                for i in range(dimension[0]):
                    for j in range(dimension[1]):
                        maxUtility +=  world.getReward(state, (i,j), restart=True) + discountFactor*utilitys[i][j] 
                maxUtility /= (dimension[0]*dimension[1])
            else:
                tempUtilities = []
                for action in actions.actionsArray:
                    probabilities = actionProbability.defineProbabilityArray(action)
                    sigmaSum = 0

                    for actionToNewState, p in probabilities:
                        nextState = world.getNextState(state, actionToNewState)
                        sigmaSum += p*(world.getReward(state, nextState)+utility.getUtilityOfState(nextState)*discountFactor)
                    tempUtilities.append(sigmaSum)
                maxUtility = max(tempUtilities)
            utility.updateUtility(state, maxUtility)
        utility.showUtility()
        convergence = utility.updateUtilityMatrixIteration()
    policy = determinePolicy(utility, discountFactor)
    GUI.drawWorldWithPolicy(policy, world.wumpusList, world.pitList, world.goldList)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        runRL(float(sys.argv[1]))
    else:
        runRL(0.99)