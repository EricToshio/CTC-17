import World
import Utility
import actions
import actionProbability
from constants import discountFactor
import GUI

def maxFunc(pair):
    return pair[1]

def maxActions(state, utilities):
    result = []
    maximum = max(utilities, key=maxFunc)
    for i in utilities:
        if i[1] == maximum[1]:
            result.append((state, i[0]))
    return result

def determinePolicy(utility):
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
                sigmaSum += p*utility.getUtilityOfState(nextState)
            tempUtilities.append((action,sigmaSum))
        bestActions = maxActions(state, tempUtilities)
        policy.extend(bestActions)
    return policy

def runRL(discountFactor = 0.7):
    world = World.World()
    states = world.getStatesArray()
    utility = Utility.Utility()

    convergence = False
    while not convergence:
        for state in states:
            tempUtilities = []
            for action in actions.actionsArray:
                probabilities = actionProbability.defineProbabilityArray(action)
                sigmaSum = 0
                for actionToNewState, p in probabilities:
                    nextState = world.getNextState(state, actionToNewState)
                    sigmaSum += p*utility.getUtilityOfState(nextState)
                sigmaSum *= discountFactor
                if world.need_restart(state):
                    sigmaSum = 0 
                sigmaSum += world.getReward(state, action)
                tempUtilities.append(sigmaSum)
            maxUtility = max(tempUtilities)
            utility.updateUtility(state, maxUtility)
        utility.showUtility()
        convergence = utility.updateUtilityMatrixIteration()
    policy = determinePolicy(utility)
    GUI.drawWorldWithPolicy(policy, world.wumpusList, world.pitList, world.goldList)

# qual eh o fator de desconto?
runRL(discountFactor)