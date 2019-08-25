import pygame, sys
from pygame.locals import *

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Block:
    def __init__(self, dimension, value, initial_position):
        basicFont = pygame.font.SysFont(None, 64)
        number = basicFont.render(str(value), True, BLACK, WHITE)
        self.backSurf = pygame.Surface((dimension, dimension))
        if value == 0:
            self.backSurf.fill(BLACK)
        else:
            self.backSurf.fill(WHITE)
        self.blockRect = self.backSurf.get_rect()
        left_corner = (self.blockRect.centerx - number.get_width()/2 , self.blockRect.centery - number.get_height()/2)
        if value != 0:
            self.backSurf.blit(number, left_corner)
        self.blockRect.topleft = initial_position
    
    def go_to(self, new_position):
        self.blockRect.topleft = new_position
    

class Board:
    def __init__(self, size, state):
        self.positions = self.__define_positions(size)
        self.blocks = self.__create_matrix(size, state)
        self.void_position = (0,0)
        self.size = size

    def __create_matrix(self, size, state_s):
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
        
        blocks = []
        value = 0
        for i in range(size):
            row = []
            for j in range(size):
                row.append(Block(99, state[i][j], self.positions[value]))
                value += 1
            blocks.append(row)
        return blocks


    def __define_positions(self, size):
        positions = []
        for i in range(size):
            for j in range(size):
                positions.append((j*100, i*100))
        return positions
    
    def draw_board(self, surface_destiny):
        for blocks_row in self.blocks:
            for block in blocks_row:
                surface_destiny.blit(block.backSurf, block.blockRect)

class Game:
    def __init__(self, states):
        # set up pygame
        pygame.init()

        self.clock = pygame.time.Clock()

        # set up the window
        self.windowSurface = pygame.display.set_mode((900, 900), 0, 32)
        pygame.display.set_caption('Hello world!')

        self.windowSurface.fill(BLACK)

        state_index = 0
        self.board = Board(9, states[state_index])

        while True:
            # draw the window onto the screen
            self.board = Board(9,states[state_index])
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            self.draw()
            # pygame.time.wait(1000)
            self.clock.tick(1)
            state_index = state_index + 1 if state_index < len(states)-1 else state_index
        
    def draw(self):
        self.board.draw_board(self.windowSurface)
        pygame.display.update()
    
 