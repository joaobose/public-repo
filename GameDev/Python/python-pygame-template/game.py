import pygame as pg
import random
from os import path
from settings import *

class Game():
	def __init__(self):
		pg.init()
		pg.mixer.init()
		self.ventana=pg.display.set_mode((ancho,largo))
		pg.display.set_caption(NAME)
		self.Clock=pg.time.Clock()
		self.running=True


	def new(self):
		#inicia un nuevo juego
		self.playing=True
		self.all_sprites=pg.sprite.Group()

	def run(self):
		#game loop
		while self.playing:
			self.Clock.tick(FPS)
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

	def update(self):
		#game loop update
		self.all_sprites.update()


	def drawing(self):
		#game loop draw
		self.ventana.fill(BLACK)
		self.all_sprites.draw(self.ventana)


		pg.display.flip()

	def draw_new_game_screen(self):
		#draw the new game screen
		pass

	def draw_game_over_screen(self):
		#draw the game over screen
		pass

game = Game()
game.draw_new_game_screen()
while game.running:
	game.new()
	game.run()
	game.draw_game_over_screen()

pg.quit()