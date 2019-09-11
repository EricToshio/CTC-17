from Chessboard import Chessboard
class HillClimbing:
    def __init__(self, initial_node, higest_next, evaluate):
        self.node = initial_node
        self.higest_next = higest_next
        self.evaluate = evaluate
    
    def find_best(self):
        found  = False
        while not found:
            next = self.higest_next(self.node)
            if self.evaluate(next) > self.evaluate(self.node):
                self.node = next
            else:
                found = True
        return self.node


if __name__ == "__main__":
    board = Chessboard(5)
    sol = HillClimbing(initial_node=board.board, higest_next=board.higest_next, evaluate=board.evaluate).find_best()
    print(sol,board.evaluate(sol))