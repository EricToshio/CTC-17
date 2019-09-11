class Chessboard:
    def __init__(self, size):
        self.size = size
        # Cria tabuleiro
        ## 0 => sem rainha
        ## 1 => com rainha
        self.board = []
        for _ in range(self.size):
            self.board.append([0]*self.size)
        