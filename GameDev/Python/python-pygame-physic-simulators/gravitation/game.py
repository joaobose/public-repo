import pygame as pg
import random
from os import path
from settings import *
from sprites import *

vec = pg.math.Vector2

class Game():
	def __init__(self):
		pg.init()
		pg.mixer.init()
		self.ventana=pg.display.set_mode((ancho,largo))
		self.buffer = pg.Surface((ancho,largo))
		pg.display.set_caption(NAME)
		self.Clock=pg.time.Clock()
		self.running=True


	def new(self):
		#inicia un nuevo juego
		self.playing=True
		self.all_sprites=pg.sprite.Group()
		self.planets = pg.sprite.Group()
		self.black_holes = pg.sprite.Group()

		#sistema de dos masas iguales (M = m) que inicialmente estan a distacia r y tienen un
		#momento angular inicial dado por las velocidades iniciales aplicadas y r

		#si r = 100
		#Vmin = 61 #Vmax=86

		#self.M = Planet(self,550,300,10,1500000,vec(0,-70))
		#self.m = Planet(self,750,300,10,1500000,vec(0,70))

		#sistema de dos masas M y m con M>>m que inicialmente estan a una distacia r y tienen un
		#angular inicial dado por la velocidad de m con respecto a M (que se aproxima a la velocidad de m
		#con respeto al CM) y r

		#si r = 100
		#Vmin = 38  #Vmax =54


		#self.M = Planet(self,600+200,300,50,150000,vec(0,0))
		#self.m = Planet(self,600+300,300,10,1,vec(0,50))


		#sistema de dos mas masas m1 y m2, separados inicialmente por una distacia d y que tinen cada uno de ellos,
		#una velocidad v1 y v2 iniciales. si ri es la distancia de mi con respecto al centro de masas

		#r1 = m2d/(m1+m2)
		#r2 = d - r1

		#si d = 100
		#y si m1 = 3000000 y m2 = 900000
		#r1 = 23.0769
		#r2 = 76.9231

		#v1min = 45.57 #v1max = 64.45

		#v2 = (m1/m2)v1

		#v2min = 151.9 #v2max = 214.8

		#600, 200


		self.m = Planet(self,650,300,20,3000000,vec(0,45.57))
		self.M = Planet(self,550,300,10,900000,vec(0,-151.9))





		self.drawRadius = False
		self.drawOrbit = True




	def run(self):
		#game loop
		while self.playing:
			self.dt = (self.Clock.tick(1000000)/1000)/3
			self.events()
			self.update()
			self.drawing()

	def events(self):
		#game loop events
		for event in pg.event.get():
			if event.type== pg.QUIT:
				if self.playing==True:
					self.playing=False
				self.running=False

			if event.type == pg.KEYDOWN:
				if event.key == pg.K_m:
					self.drawRadius = not self.drawRadius

				if event.key == pg.K_n:
					self.drawOrbit = not self.drawOrbit

	def update(self):
		#game loop update
		self.all_sprites.update()




	def drawing(self):
		#game loop draw
		self.ventana.fill(BLACK)



		self.all_sprites.draw(self.ventana)
		self.all_sprites.draw(self.buffer)

		if self.drawOrbit:
			self.ventana.blit(self.buffer,(0,0))

		if self.drawRadius:
			pg.draw.line(self.ventana,RED,(int(self.M.pos.x),int(self.M.pos.y)),(int(self.m.pos.x),int(self.m.pos.y)),5)


		pg.display.flip()


game = Game()
while game.running:
	game.new()
	game.run()

pg.quit()
