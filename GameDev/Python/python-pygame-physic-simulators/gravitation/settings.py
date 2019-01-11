from os import path
ancho,largo=1200,600
FPS=60
NAME="gravity simulation"

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
GREY=(155,155,155)
YELLOW=(255,255,0)

game_folder=path.dirname(__file__)
img_folder=path.join(game_folder,"pngs")
snd_folder=path.join(game_folder,"snds")

def get_vec_magnitude(vec):
	return (((vec.x)**2) + ((vec.y)**2))**(1/2)

def apply_force(entity,force_vec):
	entity.external_forces += force_vec

def apply_black_hole_effect(entity,black_hole_group):
	if len(black_hole_group) > 0:
		entity.acc += entity.vel * BLACK_HOLE_FR


BLACK_HOLE_MASS = 100000
BLACK_HOLE_SIZE = 5
BLACK_HOLE_FR = -10