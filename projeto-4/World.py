import rewards

class World:
    def __init__(self):
        self.dimensions = (4,8)
        self.wumpusList = []
        self.__addWumpus()
        self.pitList = []
        self.__addPit()
        self.goldList = []
        self.__addGold()

    def getReward(self, state, action):
        currentReward = self.__getRewardOfCurrentState(state)
        # next state is a wall
        if not self.__isPossibleMove(state, action):
            return currentReward + rewards.COLISION
        if self.__nextStateIsEmpty(state, action):
            return currentReward + rewards.MOVE
        return currentReward + rewards.MOVE + rewards.RESET 

    def __addWumpus(self):
        self.wumpusList.append((1,0))
        self.wumpusList.append((2,4))
    
    def __addPit(self):
        self.pitList.append((0,1))
        self.pitList.append((0,6))
        self.pitList.append((1,2))
        self.pitList.append((1,6))
        self.pitList.append((3,6))
        self.pitList.append((3,2))
    
    def __addGold(self):
        self.goldList.append((1,1))
        self.goldList.append((2,5))
    
    def __isPossibleMove(self, state, action):
        next_state = (state[0] + action[0], state[1] + action[1])
        if next_state[0] < 0 or next_state[0] >= self.dimensions[0]:
            return False
        if next_state[1] < 0 or next_state[1] >= self.dimensions[1]:
            return False
        return True
    
    def __nextStateIsEmpty(self, state, action):
        next_state = (state[0] + action[0], state[1] + action[1])
        return not ((next_state in self.wumpusList) or (next_state in self.pitList) or (next_state in self.goldList))
        
    def __getRewardOfCurrentState(self, state):
        if state in self.wumpusList:
            return rewards.WUMPUS
        if state in self.goldList:
            return rewards.GOLD
        if state in self.pitList:
            return rewards.PIT
        return 0 
        # [TODO] verify if this is correct
    
    def getNextState(self, state, action):
        if self.__isPossibleMove(state, action):
            return (state[0] + action[0], state[1] + action[1])
        return state
    
    def getStatesArray(self):
        states = []
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                states.append((i,j))
        return states