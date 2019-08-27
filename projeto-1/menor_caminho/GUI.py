import pygame, sys
from pygame.locals import *

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class City:
    def __init__(self, lat, lng, name, id, is_goal = False):
        self.lat = lat
        self.lng = lng
        self.name = name
        self.id = id
        self.position = self.__define_position_on_screen()
        if is_goal:
            self.color = RED 
        else:
            self.color = BLACK

    def __define_position_on_screen(self):
        x = int(self.lat+45)
        y = int(self.lng-110)
        return (x*28,y*18)

class MapDraw:
    def __init__(self, cities, path):
        self.cities = cities 
        self.path = path
        self.goal = path[-1]
        self.number_of_cities = len(cities)
        self.map_cities = {}
        self.__load_cities()
        self.__init_pygame()
    
    def __load_cities(self):
        for city in self.cities:
            lt = float(city["lat"])
            ln = float(city["lng"])
            id = int(city["id"])
            name = city["city"]
            is_goal = False
            if id == self.goal:
                is_goal = True 
            self.map_cities[id] = City(lt,ln,name,id,is_goal)
    
    def __init_pygame(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        # set up the window
        self.windowSurface = pygame.display.set_mode((1024, 900), 0, 32)
        pygame.display.set_caption('Caminho entre cidades')

        self.windowSurface.fill(WHITE)

        while True:
            # draw the window onto the screen
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            self.__draw_cities()
            self.__draw_path()
            pygame.display.update()
            self.clock.tick(1)
    
    def __draw_cities(self):
        for i in range(self.number_of_cities):
            pygame.draw.circle(self.windowSurface, self.map_cities[i+1].color, self.map_cities[i+1].position, 3, 3)
    
    def __draw_path(self):
        for i in range(1,len(self.path)):
            pygame.draw.line(self.windowSurface, BLACK, self.map_cities[self.path[i]].position, self.map_cities[self.path[i-1]].position, 2)