#pathfinding
import pygame as pg
vec = pg.math.Vector2

TILESIZE = 32
TILEWIDTH = 32
TILEHEIGHT = 16

WIDTH = TILEWIDTH  * TILESIZE
HEIGHT = TILEHEIGHT * TILESIZE

FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
GREY = (100,100,100)
DARKGREY = (40,40,40)
YELLOW = (255,255,0)

premade_lab = [(0, 2), (1, 2), (2, 2), (2, 3), (2, 4), (2, 5), (5, 0), (5, 2), (5, 1), (5, 3), (6, 3), (7, 3), (8, 3), (8, 4),
(8, 5), (5, 8), (5, 9), (4, 9), (3, 9), (2, 9), (2, 10), (2, 11), (2, 12), (1, 12), (0, 12), (3, 6), (2, 6), (6, 14), (7, 14),
(8, 14), (9, 14), (10, 14), (10, 13), (10, 12), (10, 11), (10, 10), (10, 9), (10, 8), (11, 8), (12, 8), (13, 8), (6, 15),
(12, 5), (12, 4), (12, 3), (12, 2), (13, 1), (12, 1), (14, 1), (15, 1), (11, 5), (16, 1), (17, 1), (18, 1), (19, 1), (20, 1),
(20, 2), (20, 3), (20, 5), (20, 4), (19, 5), (18, 5), (17, 5), (16, 5), (16, 4), (16, 3), (23, 0), (23, 1), (24, 1), (25, 1),
(25, 2), (25, 3), (26, 3), (27, 3), (28, 3), (28, 2), (31, 5), (30, 5), (29, 5), (29, 6), (29, 7), (28, 7), (27, 7), (12, 15),
(12, 14), (13, 14), (13, 13), (13, 12), (13, 11), (14, 11), (15, 11), (16, 11), (16, 10), (16, 9), (16, 8), (16, 7), (17, 7),
(18, 7), (21, 9), (20, 9), (20, 10), (20, 11), (20, 12), (19, 13), (20, 13), (18, 13), (18, 14), (18, 15), (17, 15), (28, 1),
(26, 7), (26, 8), (26, 9), (26, 10), (27, 11), (26, 11), (28, 11), (29, 11), (29, 10), (31, 13), (30, 13), (29, 13), (29, 14),
(26, 15), (26, 14), (26, 13), (25, 13), (24, 13), (23, 13), (21, 15), (22, 15), (24, 11), (24, 10), (24, 9), (24, 8), (24, 7),
(23, 7), (22, 7), (21, 7), (20, 7), (22, 3), (22, 4), (22, 5), (23, 5), (24, 5), (4, 15), (4, 14), (4, 13), (4, 12), (5, 12),
(6, 12), (7, 12), (7, 11), (7, 10), (7, 9), (7, 8), (8, 0), (8, 1), (9, 1), (10, 1), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9)]

pg.init()
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
running = True

def draw_grid():
    for x in range(0,WIDTH,TILESIZE):
        pg.draw.line(screen,GREY,(x,0),(x,HEIGHT))
    for y in range(0,HEIGHT,TILESIZE):
        pg.draw.line(screen,GREY,(0,y),(WIDTH,y))

#mapa que es conformado por cuadrados de igual area (tilemap)
class Squaregrid():
    def __init__(self, width, height):
        self.width = width #tile width of the map
        self.height = height #tile height of the map
        self.directions = [vec(1,0), vec(-1,0), vec(0,1), vec(0,-1)]#allowed directions to move between nodes
        self.walls = []#all non passable nodes (tiles)

    def in_bounds(self, node):#check if a node is inside the grid
        if 0 <= node.x < self.width and 0 <= node.y < height:
            return True

    def passable(self, node):#check if a node is passable (is not a wall)
        if node not in self.walls:
            return True

    def find_neighbors(self, node):#find all the possible neighbors of a node
        neighbors = [node + direction for direction in self.directions]
        #fitrando los vecinos del nodo:
        neighbors = filter(self.in_bounds,neighbors)#verificando que los vecino esten dentro del mapa (in-bound (dentro de las esquinas))
        neighbors = filter(self.passable,neighbors)#verificando que se pueda pasar por los vecinos (que no sean walls)
        return neighbors

    def draw_walls(self):
        for wall in self.walls:
            rect = pg.Rect(wall * TILESIZE,(TILESIZE,TILESIZE))
            pg.draw.rect(screen,GREY,rect)

G = Squaregrid(TILEWIDTH,TILEHEIGHT)
G.walls = [vec(cord) for cord in premade_lab]

while running:
    clock.tick(FPS)
    #events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        #adding walls by clicking
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = vec(pg.mouse.get_pos()) // TILESIZE #getting the tile coordinates of the mouse_pos

            #spawning or destroying a wall
            if mouse_pos in G.walls:
                G.walls.remove(mouse_pos)
            else:
                G.walls.append(mouse_pos)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                if len(G.walls) > 0:
                    G.walls = []
                else:
                    G.walls = [vec(cord) for cord in premade_lab]

            if event.key == pg.K_m:
                print([(int(wall.x),int(wall.y)) for wall in G.walls])
    #update

    #drawing
    screen.fill(DARKGREY)
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    draw_grid()
    G.draw_walls()

    pg.display.flip()

pg.quit()
