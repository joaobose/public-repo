#pathfinding
import pygame as pg
from collections import deque
import heapq
from os import path
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
LIGHTGREY = (150,150,150)
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

water = [(12, 6), (14, 6), (13, 6), (15, 6), (16, 6), (17, 6), (18, 6), (19, 6), (19, 7), (17, 7),
(18, 7), (16, 7), (15, 7), (13, 7), (12, 7), (13, 5), (14, 4), (15, 4), (15, 3), (17, 3), (16, 3),
(18, 4), (19, 5), (20, 6), (20, 7), (19, 8), (18, 9), (17, 10), (16, 10), (15, 10), (14, 9), (13, 8),
(14, 5), (15, 5), (16, 4), (17, 4), (18, 5), (17, 5), (16, 5), (14, 8), (15, 8), (15, 9), (16, 9),
(16, 8), (17, 8), (17, 9), (18, 8), (27, 2), (26, 4), (27, 3), (26, 3), (26, 2), (27, 4), (28, 3),
(25, 3), (25, 4), (25, 2), (28, 2), (28, 4), (28, 5), (27, 5), (26, 5), (25, 5), (24, 4), (24, 3),
(29, 3), (29, 4), (27, 6), (26, 6), (26, 1), (27, 1), (11, 9), (12, 10), (13, 11), (14, 12), (13, 12),
(12, 12), (12, 11), (11, 10), (11, 11), (10, 9), (9, 10), (8, 11), (7, 12), (8, 12), (9, 12), (10, 12),
(11, 12), (10, 11), (10, 10), (9, 11), (7, 13), (7, 14), (7, 15), (8, 15), (8, 14), (8, 13), (9, 13),
(9, 14), (9, 15), (10, 15), (10, 14), (10, 13), (11, 13), (11, 14), (11, 15), (12, 15), (12, 13), (12, 14),
(13, 13), (13, 14), (13, 15), (14, 15), (14, 14), (14, 13), (15, 13), (16, 14), (17, 15), (16, 15), (15, 15),
(15, 14), (9, 9), (8, 9), (8, 10), (7, 9), (7, 10), (6, 10), (5, 11), (4, 12), (3, 13), (2, 14), (1, 15),
(7, 11), (6, 11), (6, 12), (5, 12), (5, 13), (6, 13), (4, 13), (3, 14), (4, 14), (5, 14), (6, 14), (6, 15),
(5, 15), (4, 15), (3, 15), (2, 15), (2, 6), (2, 5), (2, 7), (1, 6), (2, 4), (1, 4), (2, 8), (4, 6), (4, 7),
(2, 9), (3, 9), (1, 9), (2, 10), (0, 6), (0, 5), (1, 5), (3, 5), (3, 7), (3, 6), (3, 8), (4, 8), (0, 10),
(1, 10), (1, 8), (1, 7), (0, 7), (0, 8), (0, 9), (1, 11), (0, 12), (0, 11), (1, 3), (0, 2), (0, 3), (0, 4),
(8, 0), (9, 1), (10, 2), (11, 2), (12, 1), (13, 0), (12, 0), (11, 0), (10, 0), (9, 0), (10, 1), (11, 1),
(5, 3), (4, 3), (4, 2), (5, 2), (6, 2), (6, 3), (25, 11), (26, 11), (27, 11), (26, 10), (26, 12), (24, 13),
(24, 12), (23, 13), (28, 12), (29, 13), (28, 13), (27, 13), (27, 12), (25, 12), (25, 13), (26, 13), (22, 14),
(21, 15), (22, 15), (23, 15), (23, 14), (24, 14), (24, 15), (25, 15), (25, 14), (26, 14), (26, 15), (27, 15),
(27, 14), (28, 14), (28, 15), (29, 15), (29, 14), (30, 14), (30, 15), (31, 15), (5, 4), (5, 1), (14, 7)]

pg.init()
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
running = True

#dibuja la cuadricula de tiles
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
        self.directions = [vec(1,0), vec(-1,0), vec(0,1), vec(0,-1)] + [vec(-1,-1), vec(1,-1), vec(-1,1), vec(1,1)]#allowed directions to move between nodes
        self.walls = []#all non passable nodes (tiles)

    def in_bounds(self, node):#check if a node is inside the grid
        if 0 <= node.x < self.width and 0 <= node.y < self.height:
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

class WeigthedGrid(Squaregrid):
    def __init__(self,width,height):
        super().__init__(width,height)
        self.weigth_tiles = {}#diccionario que contiene los tiles que son "pesados" (dificiles de transitar) como keys
                              #y como respuesta a el respectivo costo adicional de transitar sobre ellos

    def cost(self, from_node, to_node):
        if (from_node - to_node).length_squared() == 1:
            return self.weigth_tiles.get(vec2int(to_node),0) + 10
        else:
            return self.weigth_tiles.get(vec2int(to_node),0) + 14

class PriorityQueue():#es una cola que posee prioridades (sus elementos se ordenan por un parametro "cost", el cual es tomado en cuenta a la hora de agregar o sacar elementos de la cola)
    def __init__(self):
        self.nodes = []#lista de los elementos de la cola

    def put(self,node,cost):
        heapq.heappush(self.nodes,(cost,node)) #agrega el elemento (node) a la cola (tomando en cuenta "cost")

    def get(self):
        data = heapq.heappop(self.nodes) #se guarda la tupla de heapQ (priory_order, elemento)
        return data[1]#retorna el elemento

    def empty(self):#chequea se la PriorityQueue esta vacia o no
        return len(self.nodes) == 0


def vec2int(vector):#converts a vector object into a int tuple
    return (int(vector.x),int(vector.y))

def breadth_first_search(graph,goal,start):#encuentra el camino desde el nodo start hacia el goal(BFS ALGORITHM)
    #nota: el BFS hace la busqueda desde el goal hasta el start es decir al reves
    frontier = deque()
    frontier.append(goal)
    path = {}
    path[vec2int(goal)] = None

    while len(frontier) > 0:
        current = frontier.popleft()
        if current == start:
            break
        for next in graph.find_neighbors(current):
            if vec2int(next) not in path:
                frontier.append(next)
                path[vec2int(next)] = current - next
    return path

def dijkstras_search(graph,goal,start):#encuentra el camino desde el nodo start hacia el goal(DIJKSTRAS ALGORITHM)
    frontier = PriorityQueue()#cola que da prioridad a los elementos que tengan menor "costo" (a menor costo, mayor prioridad)
    path = {}
    cost = {}

    frontier.put(vec2int(goal),0)#mi objetivo es por donde empiezo (agrego mi goal al frontier, con 0 de costo)
    path[vec2int(goal)] = None
    cost[vec2int(goal)] = 0

    while not frontier.empty():#mientras el frontier no este vacio
        current = frontier.get()#define el nodo actual

        if current == start:#si ya llego a el star(ya encontro el camino)
            break#se rompe el ciclo

        for next in graph.find_neighbors(vec(current)):#itera por los vecino del nodo actual
            next = vec2int(next)

            next_cost = cost[current] + graph.cost(vec(current),vec(next))#calcula el costo (lo que me costo llegar a donde estoy(current) + lo que me cuesta caminar a mi vecino (next))

            if next not in cost or next_cost < cost[next]:#si no he pasado por next o consegui una ruta mas economica que pasa por next

                priority = next_cost#defino la prioridad de next en el frontier (costo)
                frontier.put(next,priority)#agrego "next" a mi frontier (tomando en cuenta el costo)

                cost[next] = next_cost #guardo lo que me costo llegar a next

                path[next] = vec(current) - vec(next) #guardo el vertor que me regresa de next a current (mi camino a goal)

    return path

#loading graphics
img_folder = path.join(path.dirname(__file__),"icons")

arrows = {}
arrow = pg.image.load(path.join(img_folder,"arrowRight.png"))
arrow = pg.transform.scale(arrow,(50,50))
for dir in [(1,0), (-1,0), (0,1), (0,-1), (-1,-1), (1,-1), (-1,1), (1,1)]:
    arrows[dir] = pg.transform.rotate(arrow, vec(dir).angle_to(vec(1,0)))

goal_img = pg.image.load(path.join(img_folder,"home.png"))
goal_img = pg.transform.scale(goal_img,(50,50))
goal_img_rect = goal_img.get_rect()

start_img = pg.image.load(path.join(img_folder,"cross.png"))
start_img = pg.transform.scale(start_img,(50,50))
start_img_rect = start_img.get_rect()

def draw_visited_nodes_to_find_path():
    for node in path:
        rect = pg.Rect(vec(node) * TILESIZE,(TILESIZE,TILESIZE))
        pg.draw.rect(screen,LIGHTGREY,rect)

def draw_weigth_tiles(graph):
    for node in graph.weigth_tiles:
        rect = pg.Rect(vec(node) * TILESIZE,(TILESIZE,TILESIZE))
        pg.draw.rect(screen,(0,155,200),rect)

#charging graph (map of nodes)
G = WeigthedGrid(TILEWIDTH,TILEHEIGHT)
G.walls = [vec(cord) for cord in premade_lab]

#or node in water:
 #  G.weigth_tiles[node] = 80

#calculando el path desde el start al goal
goal = vec(5,6)
start = vec(7,4)
path = dijkstras_search(G,goal,start)

while running:
    clock.tick(FPS)
    #events
    for event in pg.event.get():
        if event.type == pg.QUIT: 
            running = False

        #adding walls by clicking
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = vec(pg.mouse.get_pos()) // TILESIZE #getting the tile coordinates of the mouse_pos
            if event.button == 1:
                #spawning or destroying a wall
                if mouse_pos in G.walls:
                    G.walls.remove(mouse_pos)
                else:
                    G.walls.append(mouse_pos)
            if event.button == 3:
                #change the current goal of the path
                goal = mouse_pos
            #recalculating the path
            path = dijkstras_search(G,goal,start)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                if len(G.walls) > 0:
                    #elimina todas las paredes
                    G.walls = []
                else:
                    #spawnea las paredes del mapa incial
                    G.walls = [vec(cord) for cord in premade_lab]
                #recalculation the path
                path = dijkstras_search(G,goal,start)

            if event.key == pg.K_m:
                #print the list of all the walls
                print([(int(wall.x),int(wall.y)) for wall in G.walls])

            #chage the staring point
            if event.key == pg.K_q:
                mouse_pos = vec(pg.mouse.get_pos()) // TILESIZE
                start = mouse_pos

                #recalculating the path
                path = dijkstras_search(G,goal,start)
    #update

    #drawing
    screen.fill(DARKGREY)
    draw_visited_nodes_to_find_path()
    draw_weigth_tiles(G)
    pg.display.set_caption("{:.0f}".format(clock.get_fps()))
    draw_grid()
    G.draw_walls()

    #drawing goal and start points
    x = (goal.x * TILESIZE) + TILESIZE//2
    y = (goal.y * TILESIZE) + TILESIZE//2
    goal_img_rect.center = (x,y)
    screen.blit(goal_img,goal_img_rect)

    x = (start.x * TILESIZE) + TILESIZE//2
    y = (start.y * TILESIZE) + TILESIZE//2
    start_img_rect.center = (x,y)
    screen.blit(start_img,start_img_rect)

    #drawing path from start to goal
    if vec2int(start) in path:
        current = start + vec(path[vec2int(start)])#dibuja flechas a partir del siguiente nodo al start
        while current != goal:
            x = (current.x * TILESIZE) + TILESIZE//2
            y = (current.y * TILESIZE) + TILESIZE//2
            image = arrows[vec2int(path[vec2int(current)])]
            rect = image.get_rect(center=(x,y))

            screen.blit(image,rect)

            current += path[vec2int(current)]



    pg.display.flip()

pg.quit()
