from Chessboard import Chessboard
import time
import sys

soma = 0

def timeit(method):
    def timed(*args, **kw):
        global soma
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%2.2f ms' % ((te - ts) * 1000))
        soma += ((te - ts) * 1000)
        return result
    return timed

class HillClimbing:
    def __init__(self, initial_node, higest_next, evaluate,real_cost,random):
        self.node = initial_node
        self.higest_next = higest_next
        self.evaluate = evaluate
        self.real =real_cost
        self.random = random
    
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
    solucao_otima = 0
    for _ in range(int(sys.argv[2])):

        board = Chessboard(int(sys.argv[1]),super_optimization=True)
        sol = HillClimbing(initial_node=board.board, higest_next=board.higest_next, evaluate=board.real_cost,real_cost=board.real_cost,random=board.random_initial ).find_best()
        
        board.print_board(sol)
        custo = board.real_cost(sol)
        print("custo:",custo)
        if custo == 0:
            solucao_otima+=1
    
    print("tempo medio de todas execucoes: %2.2f ms" % (soma/int(sys.argv[2])))
    print("encontrou solucao ótima", solucao_otima,"vezes em",int(sys.argv[2]),"tentativas")