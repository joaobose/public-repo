import pygame as pg
import random
from os import path
from settings import *

vec = pg.math.Vector2

class Object(pg.sprite.Sprite):
	def __init__(self,game,x,y,Vo,h,density):
		self.game = game
		self.layer = 0
		self.groups = self.game.all_sprites

		pg.sprite.Sprite.__init__(self,self.groups)

		self.image = pg.Surface(((Vo//(h)),h))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.topleft = (x,y)

		self.Vo = Vo
		self.h = h
		self.density = density

		self.acc = vec(0,0)
		self.external_forces = vec(0,0)
		self.vel = vec(0,0)
		self.pos = vec(x,y)



	def update(self):

		self.external_forces = self.calculate_force()

		self.acc = (self.external_forces/(self.density * self.Vo))

		self.pos += (self.vel * self.game.dt) + ((self.acc * (self.game.dt ** 2))/2)

		self.vel += self.acc * self.game.dt

		self.rect.topleft = self.pos

		self.external_forces = vec(0,0)

		if self.rect.bottom >= largo:
			self.pos = vec(self.pos.x,largo - self.rect.height)
			self.vel.y = 0



	def calculate_force(self):

		W = self.density * self.Vo * GRAVITY

		if self.rect.y < self.game.fluid.lvl:
			if self.rect.bottom > self.game.fluid.lvl:
				hs = self.h + self.rect.y - self.game.fluid.lvl
			else:
				hs = 0

		else:
			hs = self.h

		E = self.game.fluid.density * ((hs * self.Vo)/self.h) * GRAVITY

		if self.rect.bottom < self.game.fluid.lvl:

			Fr = 0

		else:

			Fr = (self.game.fluid.drag_constant * 0.5 * self.game.fluid.density * self.vel.length_squared() * (self.Vo / self.h))



		self.game.all_volume += hs

		if self.vel.y > 0:

			forceSum = vec(0,W - E - Fr)

		else:
			forceSum = vec(0,W - E + Fr)

		return forceSum


	def show_data(self):
		self.game.draw_text(self.game.ventana, str(int(self.vel.y)) + "m/s" , 22, self.rect.centerx, self.rect.top - 10)
		self.game.draw_text(self.game.ventana, str(int(self.acc.y)) + "m/s^2" , 22, self.rect.centerx, self.rect.top + 10)

class Fluid(pg.sprite.Sprite):
	def __init__(self,game,density,Lo,drag):
		self.game = game
		self.layer = 0

		pg.sprite.Sprite.__init__(self)

		self.Lo = Lo
		self.density = density

		self.lvl = Lo
		self.drag_constant = drag

	def update(self):
		self.lvl = self.Lo - (self.game.all_volume/10)
