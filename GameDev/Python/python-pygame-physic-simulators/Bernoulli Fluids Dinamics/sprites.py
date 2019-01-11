import pygame as pg 
import random
from os import path 
from settings import *
vec = pg.math.Vector2

class Segment():
	def __init__(self,game,ABCD,COLOR):
		self.game = game
		self.points = ABCD
		self.initial_points = ABCD
		self.selected_point = None
		self.color = COLOR

		self.region = {}


	def update(self):
		pos = pg.mouse.get_pos()
		rel = pg.mouse.get_rel()
		

		for point in self.points:

			i = self.points.index(point)

			if i == 0:
				rect = pg.Rect(point.x - 5 + 100, point.y - 5, 40, 40)

			elif i == 3:
				rect = pg.Rect(point.x - 5 - 100, point.y - 5, 40, 40)

			else:
				rect = pg.Rect(point.x - 5, point.y - 5, 40, 40)

			if rect.collidepoint(pos) and (not i in [0,3]):
				self.selected_point = point



		if (pg.mouse.get_pressed()[0] == True) and self.selected_point != None and not self.game.selected:
			
			i = self.points.index(self.selected_point)

			if i in [0,3]:
				self.selected_point = vec(self.initial_points[i].x,pos[1])

			else: 
				self.selected_point = vec(pos[0],pos[1])

			self.points[i] = self.selected_point
			self.game.selected = True

		else:
			self.selected_point = None
			self.game.selected = False


	def draw(self):
		t = 0
		while t <= 1:
			p = cubic_interpolation(self.points[0],self.points[1],self.points[2],self.points[3],t)
			t += 0.0005
			pg.draw.circle(self.game.ventana,BLUE,vecToInt(p),1)

			self.region[vecToInt(p)[0]] = p

		for point in self.points:
			

			i = self.points.index(point)

			if i == 0:
				pg.draw.circle(self.game.ventana,self.color,(vecToInt(point)[0] + 100,vecToInt(point)[1]),10)

			elif i == 3:
				pg.draw.circle(self.game.ventana,self.color,(vecToInt(point)[0] - 100,vecToInt(point)[1]),10)

			else:
				pg.draw.circle(self.game.ventana,self.color,vecToInt(point),10)

	def get_tangent_vec(self,x):
		return (self.region[x + 1] - self.region[x]).normalize()

class Particle(pg.sprite.Sprite):
	def __init__( self , game , x , y, DATA):
		self.game = game
		self.groups = self.game.all_sprites

		pg.sprite.Sprite.__init__(self,self.groups)

		self.image = pg.Surface((10,10))
		self.image.set_colorkey(BLACK)
		pg.draw.circle(self.image,GREY,(5,5),5)
		self.rect = self.image.get_rect()

		self.rect.center = (x,y)

		self.pos = vec(x, y)
		self.vel = vec(DATA[0],0)
		self.initial_pos = (x,y)

		self.h = 0.5 
		self.data = DATA

	def update(self):
		self.last_vel = vec(self.vel.x,self.vel.y)
		self.vel = vec(0,0)

		if (self.rect.x in self.game.s1.region and self.rect.x in self.game.s2.region):

			self.h = (self.rect.centery - self.game.s1.region[self.rect.x].y)/(self.game.s2.region[self.rect.x].y - self.game.s1.region[self.rect.x].y)

		self.dir = get_dir_between_curves(self.game.s1,self.game.s2,self.rect.centerx,self.h)

		if self.dir == vec(0,0):
			self.vel = self.last_vel

		else:

			self.vel = self.dir * self.calcutate_vel()

		self.pos += self.vel * self.game.dt

		self.rect.center = vecToInt(self.pos)

		if self.rect.left > ancho:
			self.kill()

	def calcutate_vel(self):

		vmax = self.data[0] * (self.data[1]**2)/((self.game.s2.region[self.rect.centerx].y - self.game.s1.region[self.rect.centerx].y)**2) 

		Maxradius = self.game.s2.region[self.rect.centerx].y - self.game.s1.region[self.rect.centerx].y

		j = self.pos.y - self.game.s1.region[self.rect.centerx].y

		v = vmax * (1  - (((abs(Maxradius/2 - j))**2)/(Maxradius**2)))
		
		return v
		

		