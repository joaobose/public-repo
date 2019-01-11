import pygame as pg 
import random
from os import path 
from settings import *

vec = pg.math.Vector2



class Black_hole(pg.sprite.Sprite):
	def __init__(self,game,x,y):
		self.game = game
		self.layer = 0
		self.groups = self.game.all_sprites , self.game.black_holes

		pg.sprite.Sprite.__init__(self,self.groups)

		self.image = pg.Surface((BLACK_HOLE_SIZE,BLACK_HOLE_SIZE))
		self.rect = self.image.get_rect()
		pg.draw.circle(self.image,GREY,(self.rect.width//2,self.rect.height//2),BLACK_HOLE_SIZE//2)
		self.rect.center = (x,y)
		self.pos = vec(x,y)
		self.external_forces = vec(0,0)
		self.mass = BLACK_HOLE_MASS


	def update(self):
		for x in self.game.all_sprites:
			if x not in self.game.black_holes:
				distance = vec(self.pos - x.pos)
				angle = distance.angle_to(vec(1,0))
				force = (self.mass * x.mass) 
				gravitational_force = vec(force,0).rotate(-angle)
				apply_force(x,gravitational_force)

		

class Planet(pg.sprite.Sprite):
	def __init__(self,game,x,y,size,mass,vel,notMove=False):
		self.game = game
		self.layer = 0
		self.groups = self.game.all_sprites , self.game.planets

		pg.sprite.Sprite.__init__(self,self.groups)

		self.image = pg.Surface((size,size))
		self.rect = self.image.get_rect()
		pg.draw.circle(self.image,GREY,(self.rect.width//2,self.rect.height//2),size//2)
		self.rect.center = (x,y)
		self.pos = vec(x,y)
		self.acc = vec(0,0)
		self.vel = vel
		self.external_forces = vec(0,0)
		self.mass = mass
		self.notMove = notMove



	def update(self):

		self.calculate_gravity()

		if self.mass != 0 and not self.notMove:
		
			self.acc = (self.external_forces/self.mass)

		#apply_black_hole_effect(self,self.game.black_holes)

		self.pos += (self.vel * self.game.dt) + ((self.acc * (self.game.dt ** 2))/2)

		self.vel += self.acc * self.game.dt

		self.rect.center = self.pos

		self.external_forces = vec(0,0)

	def calculate_gravity(self):
		for planet in self.game.planets:
			if planet != self:
				distance = vec(planet.pos - self.pos)
				angle = distance.angle_to(vec(1,0))
				force = (self.mass * planet.mass ) / ((get_vec_magnitude(distance))**2) 
				gravitational_force = vec(force,0).rotate(-angle)
				apply_force(self,gravitational_force)
