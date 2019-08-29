import random 

MIN_OF_MOVES = 30
MAX_OF_MOVES = 50

class Node:
    def __init__(self, size = 9):
        self.size = size
        self.state = self.__generate_goal_state()
        self.void_position = self.__find_void_position(self.state)

    def __generate_goal_state(self):
        state = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(i*self.size + j + 1)
            state.append(row)
        state[-1][-1] = 0
        print(state)
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

    def get_state(self):
        return self.matr_to_str(self.state)

    def __find_void_position(self, state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 0:
                    return (i,j)
    
    def shuffle(self, range_shuffle = None):
        min_of_moves = MIN_OF_MOVES
        max_of_moves = MAX_OF_MOVES
        if range_shuffle:
            min_of_moves = range[0]
            max_of_moves = range[1]
        available_moves = 'UDRL'
        qty_of_moves = random.randint(MIN_OF_MOVES, MAX_OF_MOVES)
        moves = []
        for _ in range(qty_of_moves):
            move = available_moves[random.randint(0,3)]
            moves.append(move)
            self.do_move(move, shuffle = True)
        print("Embaralhado com {} movimento(s)".format(qty_of_moves))

    def str_to_matr(self, state_s):
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

    def matr_to_str(self, state_m):
        a = []
        size = len(state_m)
        for i in range(size):
            for j in range(size):
                a.append(str(state_m[i][j]))
        return ",".join(a)

    def next_states(self, state_s):
        state = self.str_to_matr(state_s)

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
            next.append(self.matr_to_str(state))
            state[destiny[0]][destiny[1]], state[origin[0]][origin[1]] = state[origin[0]][origin[1]], state[destiny[0]][destiny[1]]

        return next

    # the cost between any state and its successors is 1 move
    def g(self, destiny, origin):
        return 1

    # use Manhattan distance as heuristic
    def h(self, current_s, goal):
        current = self.str_to_matr(current_s)
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
    
    def get_evaluation_functions(self):
        return (self.g, self.h, self.next_states)
