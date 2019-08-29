import pygame, sys
from pygame.locals import *

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SIZE_OF_SQUARE = 50

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
                row.append(Block(SIZE_OF_SQUARE-1, state[i][j], self.positions[value]))
                value += 1
            blocks.append(row)
        return blocks


    def __define_positions(self, size):
        positions = []
        for i in range(size):
            for j in range(size):
                positions.append((j*SIZE_OF_SQUARE, i*SIZE_OF_SQUARE))
        return positions
    
    def draw_board(self, surface_destiny):
        for blocks_row in self.blocks:
            for block in blocks_row:
                surface_destiny.blit(block.backSurf, block.blockRect)

class Game:
    def __init__(self, states):
        self.size = int(len(states[0].split(','))**(1/2))
        size_of_window = SIZE_OF_SQUARE * self.size
        # set up pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        # set up the window
        self.windowSurface = pygame.display.set_mode((size_of_window, size_of_window), 0, 32)
        pygame.display.set_caption('Blocos deslizantes')
        self.windowSurface.fill(BLACK)
        state_index = 0
        while True:
            # draw the window onto the screen
            self.board = Board(self.size, states[state_index])
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
    
 