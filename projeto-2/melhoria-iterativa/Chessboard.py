import random

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
    
    def next(self):
        pass


if __name__ == "__main__":
    a = Chessboard(10)
    print(a.board) 

