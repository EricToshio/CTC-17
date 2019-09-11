from Chessboard import Chessboard
import time

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed

class HillClimbing:
    def __init__(self, initial_node, higest_next, evaluate):
        self.node = initial_node
        self.higest_next = higest_next
        self.evaluate = evaluate
    @timeit
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
    board = Chessboard(10,super_optimization=True)
    sol = HillClimbing(initial_node=board.board, higest_next=board.higest_next, evaluate=board.evaluate).find_best()
    
    board.print_board(sol)
    print("custo:",board.evaluate(sol))