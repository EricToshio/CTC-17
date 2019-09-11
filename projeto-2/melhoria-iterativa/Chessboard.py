import random
import math
import copy

class Chessboard:
    def __init__(self, size, optimization = False, super_optimization = False):
        self.size = size
        # preferencia da super otimizacao
        self.optimization = optimization and not super_optimization
        self.super_optimization = super_optimization
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
        if self.optimization:
            # Somente 1 rainha por linha 
            while queens != self.size:
                y = random.randint(0, self.size - 1)
                self.board[queens][y] = 1
                queens +=1

        elif self.super_optimization:
            # Somente 1 rainha por linha e por coluna
            used = set()
            while queens != self.size:
                y = random.randint(0, self.size - 1)
                if y not in used:
                    self.board[queens][y] = 1
                    queens +=1
                    used.add(y)

        else:
            # Qualquer posicao
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
        next_states = []
        used = set()
        for queen in queens:
            new_board = copy.deepcopy(board)
            new_board[queen[0]][queen[1]] = 0

            if self.optimization:
                # Possiveis estados mudando somente uma rainha
                # As mudancas sao feitas somentes pelas linhas
                x = queen[0]
                for y in range(self.size):
                    if y != queen[1]:
                        new_board_queen = copy.deepcopy(new_board)
                        new_board_queen[x][y] = 1
                        next_states.append(new_board_queen)
            elif self.super_optimization:
                # Possiveis estados mudando duas rainha
                # As mudancas sao feitas de forma a rainhas
                # continuarem no mesma linha porem trocam o
                # valor da coluna
                used.add(queen)
                x = queen[0]
                for other_queen in queens:
                    if other_queen not in used:
                        new_board_queen = copy.deepcopy(new_board)
                        new_board_queen[other_queen[0]][other_queen[1]] = 0
                        new_board_queen[other_queen[0]][queen[1]] = 1
                        new_board_queen[x][other_queen[1]] = 1
                        next_states.append(new_board_queen)
                    
            else:
                # Encontra todos os possiveis proximos estados
                # onde se muda a posicao de uma rainha somente
                # para qualque posicao
                for x in range(self.size):
                    for y in range(self.size):
                        if (x,y) not in queens:
                            new_board_queen = copy.deepcopy(new_board)
                            new_board_queen[x][y] = 1
                            next_states.append(new_board_queen)
        return next_states


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
    
    def print_board(self, board):
        for x in range(self.size):
            for y in range(self.size):
                print(board[x][y], end=" ")
            print() 
    
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


