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
    def __init__(self, initial_node, higest_next, evaluate, real):
        self.node = initial_node
        self.higest_next = higest_next
        self.evaluate = evaluate
        self.real = real
    @timeit
    def find_best(self):
        found  = False
        while not found:
            next = self.higest_next(self.node)
            if self.evaluate(next) > self.evaluate(self.node):
                self.node = next
            else:
                if self.real(self.node)==0:
                    found = True
                else:
                    self.node = next
        return self.node


if __name__ == "__main__":
    board = Chessboard(25,super_optimization=True)
    sol = HillClimbing(initial_node=board.board, higest_next=board.higest_next, evaluate=board.evaluate,real =board.real_cost).find_best()
    
    board.print_board(sol)
    print("custo:",board.real_cost(sol))