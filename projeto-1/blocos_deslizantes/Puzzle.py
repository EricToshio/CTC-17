import random 
import copy
# print(random.randint(0,9))

import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def str_to_matr(state_s):
    a = state_s.split(',')
    a = [int(c) for c in a]
    size = int(len(a)**(1/2))
    state = []
    it = 0
    for i in range(size):
        row = []
        for j in range(size):
            row.append(a[it])
            it += 1
        state.append(row)
    return state

def matr_to_str(state_m):
    a = []
    size = len(state_m)
    for i in range(size):
        for j in range(size):
            a.append(str(state_m[i][j]))
    return ",".join(a)

def next_states(state_s):
    state = str_to_matr(state_s)

    size = len(state)
    vp = (0,0)
    for i in range(size):
        for j in range(size):
            if state[i][j] == 0:
                vp = (i,j)
                break 
    next = []
    for move in 'UDRL':
        origin = vp
        destiny = (0,0)
        if move == 'U':
            destiny = (origin[0]-1,origin[1])
        elif move == 'D':
            destiny = (origin[0]+1,origin[1])
        elif move == 'R':
            destiny = (origin[0],origin[1]+1)
        elif move == 'L':
            destiny = (origin[0],origin[1]-1)
        
        if destiny[0] < 0 or destiny[0] >= size or destiny[1] < 0 or destiny[1] >= size:
            continue
        
        state[destiny[0]][destiny[1]], state[origin[0]][origin[1]] = state[origin[0]][origin[1]], state[destiny[0]][destiny[1]]
        next.append(matr_to_str(state))
        state[destiny[0]][destiny[1]], state[origin[0]][origin[1]] = state[origin[0]][origin[1]], state[destiny[0]][destiny[1]]

    return next

def g(destiny, origin):
    return 1

def h(current_s, goal):
    current = str_to_matr(current_s)
    size = len(current)
    h = 0
    for i in range(size):
        for j in range(size):
            r = c = 0
            if current[i][j] != 0:
                r = (current[i][j] - 1) // size
                c = (current[i][j] - 1) % size
            else:
                r = c = size - 1
            distance = abs(i - r) + abs(j - c)
            h += distance
    return h

class Node:
    def __init__(self, state = None, size = 9, cost = 0, previous_move = "", father = None):
        self.total_cost = cost
        self.size = size
        self.state = copy.deepcopy(state) if state else self.__generate_default_state()
        self.g = self.heuristic()
        self.previous_move = previous_move
        self.father = father
        self.void_position = self.__find_void_position(self.state)
    
    def __generate_default_state(self):
        state = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(i*self.size + j + 1)
            state.append(row)
        state[-1][-1] = 0
        return state

    def do_move(self, move, shuffle = False):
        origin = self.void_position
        destiny = (0,0)
        if move == 'U':
            destiny = (origin[0]-1,origin[1])
        elif move == 'D':
            destiny = (origin[0]+1,origin[1])
        elif move == 'R':
            destiny = (origin[0],origin[1]+1)
        elif move == 'L':
            destiny = (origin[0],origin[1]-1)
        
        if destiny[0] < 0 or destiny[0] >= self.size or destiny[1] < 0 or destiny[1] >= self.size:
            return None 
        
        self.state[destiny[0]][destiny[1]], self.state[origin[0]][origin[1]] = self.state[origin[0]][origin[1]], self.state[destiny[0]][destiny[1]]
        self.void_position = destiny

        if not shuffle:
            new_node = Node(self.state, self.size, self.total_cost + 1, move,  self)
            self.state[destiny[0]][destiny[1]], self.state[origin[0]][origin[1]] = self.state[origin[0]][origin[1]], self.state[destiny[0]][destiny[1]]
            self.void_position = origin

            return new_node

   
    def __find_void_position(self, state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 0:
                    return (i,j)
    
    def shuffle(self):
        available_moves = 'UDRL'
        qty_of_moves = random.randint(10,15)
        moves = []
        for i in range(qty_of_moves):
            move = available_moves[random.randint(0,3)]
            moves.append(move)
            self.do_move(move, shuffle = True)
        self.g = self.heuristic()
    
    def heuristic(self):
        g = 0
        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                r = c = 0
                if self.state[i][j] != 0:
                    r = (self.state[i][j] - 1) // self.size
                    c = (self.state[i][j] - 1) % self.size
                else:
                    r = c = self.size - 1
                distance = abs(i - r) + abs(j - c)
                g += distance
        return g
    
    def __str__(self):
        for row in self.state:
            print(row)
        return ""
    
    def __eq__(self, other):
        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                if other.state[i][j] != self.state[i][j]:
                    return False
        return True
    
    def __gt__(self, other):
        return (self.total_cost + self.g) > (other.total_cost + other.g)
    
    def __ge__(self, other):
        return (self.total_cost + self.g) >= (other.total_cost + other.g)
    
    def __lt__(self, other):
        return (self.total_cost + self.g) < (other.total_cost + other.g)
    
    def __le__(self, other):
        return (self.total_cost + self.g) <= (other.total_cost + other.g)
    


class Puzzle:
    def __init__(self, size = 9):
        self.size = size
        self.initial_node = Node(size = size)
        self.initial_node.shuffle()
        print(self.initial_node)
        self.goal_node = Node(size = size)
    
    def recover_path(self, smaller):
        moves = []
        while smaller.father:
            moves.append(smaller.previous_move)
            smaller = smaller.father
        print(moves[::-1])
    
    def find_solution(self):
        pq = PriorityQueue()
        pq.put(self.initial_node, 0)
        nodes = 0
        while not pq.empty():
            smaller = pq.get()
            if smaller == self.goal_node:
                self.recover_path(smaller)
                return 
            for move in 'UDRL':
                next_node = smaller.do_move(move)
                if next_node:
                    pq.put(next_node, next_node.total_cost + next_node.g)
                    nodes += 1
                    print("open nodes: ",nodes)

# a = Puzzle(9)
# a.find_solution()