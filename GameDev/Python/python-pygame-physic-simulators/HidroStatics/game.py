import pygame as pg
import random
from os import path
from settings import *
from sprites import *

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
		self.all_volume = 0

		#density[m] initial depth [m] drag_constant[none] y depende de la forma, en este caso, los cuerpos son cilindros entonces = 1.2
		self.fluid = Fluid(self,1000,400,2.5)


		#posx [m] posy[m] volume[m^3] height[m] density[kg/m^3]
		Object(self,ancho//2 - 400,400,1000,100,100)
		Object(self,ancho//2 - 300,-100,1000,100,200)
		Object(self,ancho//2 - 200,400,1000,100,600)
		Object(self,ancho//2 - 100,-100,1000,100,600)
		Object(self,ancho//2, 400, 1000,100,800)
		Object(self,ancho//2 + 200,400 -100,1000,100,1050)
		Object(self,ancho//2 + 400,400,1000,100,5000)

	def run(self):
		#game loop
		while self.playing:
			self.dt = self.Clock.tick(FPS)/1000
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
		#game loop update+
		self.all_volume = 0
		self.all_sprites.update()
		self.fluid.update()


	def drawing(self):
		#game loop draw
		self.ventana.fill(BLACK)
		self.all_sprites.draw(self.ventana)
		pg.draw.line(self.ventana, BLUE, (0,self.fluid.lvl) , (ancho,self.fluid.lvl) , 5)

		for s in self.all_sprites:
			s.show_data()


		pg.display.flip()

	def draw_new_game_screen(self):
		#draw the new game screen
		pass

	def draw_game_over_screen(self):
		#draw the game over screen
		pass

	def draw_text(self, surf, text, size, x, y):
	    font = pg.font.Font(pg.font.match_font("times new"), size)
	    text_surface = font.render(text, True, WHITE)
	    text_rect = text_surface.get_rect()
	    text_rect.midtop = (x, y)
	    surf.blit(text_surface, text_rect)

game = Game()
game.draw_new_game_screen()
while game.running:
	game.new()
	game.run()
	game.draw_game_over_screen()

pg.quit()
