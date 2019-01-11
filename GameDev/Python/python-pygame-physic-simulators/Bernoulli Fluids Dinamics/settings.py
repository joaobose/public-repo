from os import path
import pygame as pg
ancho,largo=1200,800
FPS=200
NAME="Bernoulli Ecuation"

pg.init()

vec = pg.math.Vector2

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
GREY=(155,155,155)

game_folder=path.dirname(__file__)
img_folder=path.join(game_folder,"pngs")
snd_folder=path.join(game_folder,"snds")

def lerp(a,b,t):
		return a + (b-a)*(t)

def cuadratic_interpolation(a,b,c,t):
	p0 = lerp(a,b,t)
	p1 = lerp(b,c,t)
	return lerp(p0,p1,t)

def cubic_interpolation(a,b,c,d,t):
	p0 = cuadratic_interpolation(a,b,c,t)
	p1 = cuadratic_interpolation(b,c,d,t)
	return lerp(p0,p1,t)

def vecToInt(vec):
	return (int(vec.x),int(vec.y))

def get_dir_between_curves(segment1,segment2,x,h):
	if (x in segment1.region and (x + 1 in segment1.region)) and (x in segment2.region and (x + 1 in segment2.region)):
		return (lerp(segment1.get_tangent_vec(x),segment2.get_tangent_vec(x),h)).normalize()
	else:
		return vec(0,0)