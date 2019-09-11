import random
import math
import copy

class Chessboard:
    def __init__(self, size):
        self.size = size
        # Cria tabuleiro
        ## 0 => sem rainha
        ## 1 => com rainha
        self.board = []
        for _ in range(self.size):
            self.board.append([0]*self.size)

        # Coloca as rainhas em posicoes aleatorias
        self.random()

    def random(self):
        queens = 0
        while queens != self.size:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.board[x][y] == 0:
                self.board[x][y] = 1
                queens +=1


    def next_boards(self, board):
        # Faz um conjunto com as posicoes das rainhas
        queens = set()
        for x in range(self.size):
            for y in range(self.size):
                if board[x][y] == 1:
                    queens.add((x,y))
        # Encontra todos os possiveis proximos estados
        # onde se muda a posicao de uma rainha somente
        next_states = []
        for queen in queens:
            new_board = copy.deepcopy(board)
            new_board[queen[0]][queen[1]] = 0

            for x in range(self.size):
                for y in range(self.size):
                    if (x,y) not in queens:
                        new_board_queen = copy.deepcopy(new_board)
                        new_board_queen[x][y] = 1
                        next_states.append(new_board_queen)
        return next_states

    def update_board(self, board):
        self.board = board
        self.queens = set()
        for x in range(self.size):
            for y in range(self.size):
                if board[x][y] == 1:
                    self.queens.add((x,y))

    def evaluate(self, board):

        cost = 0
        queens = set()
        for x in range(self.size):
            for y in range(self.size):
                if board[x][y] == 1:
                    queens.add((x,y))
        
        for queen in queens:
            cost += self.__evaluateIteration__(queen, [1,0], board)
            cost += self.__evaluateIteration__(queen, [-1,0], board)
            cost += self.__evaluateIteration__(queen, [0,1], board)
            cost += self.__evaluateIteration__(queen, [0,-1], board)
            cost += self.__evaluateIteration__(queen, [1,1], board)
            cost += self.__evaluateIteration__(queen, [1,-1], board)
            cost += self.__evaluateIteration__(queen, [-1,1], board)
            cost += self.__evaluateIteration__(queen, [-1,-1], board)
        return -cost
    
    def higest_next(self, actual_board):
        nexts_boards = self.next_boards(actual_board)
        best = None
        value_best = -math.inf
        for next_board in nexts_boards:
            next_value = self.evaluate(next_board)
            if next_value > value_best:
                best = next_board
                value_best = next_value
        return best 
    
    def __evaluateIteration__(self, queen, add, board):
        add_x = add[0]
        add_y = add[1]
        cost = 0
        while queen[0]+add[0] >= 0 and queen[0]+add[0] < self.size and queen[1]+add[1] >= 0 and queen[1]+add[1] < self.size:
            cost += board[queen[0]+add[0]][queen[1]+add[1]]
            add[0]+=add_x
            add[1]+=add_y
        return cost

        


if __name__ == "__main__":
    a = Chessboard(5)
    for i in range(a.size):
        for j in range(a.size):
            print(a.board[i][j], end=" ")
        print() 

    print(a.evaluate(a.board))
    p = a.next_boards(a.board)[0]
    p = [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 1, 1], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0]]
    p = [[0, 1, 0, 0, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 0], [1, 0, 0, 0, 0], [0, 0, 1, 0, 0]]
    for i in range(a.size):
        for j in range(a.size):
            print(p[i][j], end=" ")
        print() 


