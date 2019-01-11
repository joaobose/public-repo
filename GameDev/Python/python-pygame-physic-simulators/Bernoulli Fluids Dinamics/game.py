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
		pg.display.set_caption(NAME)
		self.Clock=pg.time.Clock()
		self.running=True

	

	def new(self):
		#inicia un nuevo juego
		self.playing=True
		self.all_sprites=pg.sprite.Group()
		self.selected = False

		A = vec(-50,100)
		B = vec(ancho/2 - 100,100)
		C = vec(ancho/2 + 100,100)
		D = vec(ancho + 50,100)

		points1 = [A,B,C,D]

		self.s1 = Segment(self,points1,RED)

		E = vec(-50,400)
		F = vec(ancho/2 - 100,400)
		G = vec(ancho/2 + 100,400)
		H = vec(ancho + 50,400)

		points2 = [E,F,G,H]

		self.s2 = Segment(self,points2,GREEN)

		
		#physics properties
		self.dPressure = 0.5#pa
		self.viscosity = 0.015 #pa/seg
		self.initial_radius = 150 #m
		self.lenght = ancho #m
		self.Simulateviscosity = True

		self.Vo = (self.dPressure * self.initial_radius**2)/(4 * self.viscosity * self.lenght)
		self.flujo = (3.14*self.initial_radius**2)*self.Vo  #m^3/seg
		


		self.simulate = False
		self.burst = False
		self.last_burst = 0
		self.burst_timer = 10000/self.flujo

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

			if event.type == pg.KEYDOWN:
				if event.key == pg.K_u:
					self.simulate = not self.simulate

				if event.key == pg.K_h:
					self.burst = not self.burst

			
				if event.key == pg.K_k:
					self.all_sprites.empty()

	def update(self):
		#game loop update
		if self.simulate and not self.burst:
			for i in range(0,int(self.flujo * self.dt/100000)):
				if len(self.s1.region) > 0 and len(self.s2.region) > 0:
					x = -5
					y =  random.randint(int(self.s1.region[x].y) + 10,int(self.s2.region[x].y) - 10)
					Particle(self,x,y,(self.Vo,self.s2.region[x].y - self.s1.region[x].y))

		if self.simulate and self.burst :
			now = pg.time.get_ticks()
			if now - self.last_burst > self.burst_timer:
				self.last_burst = now

				for i in range(1,10):

					if len(self.s1.region) > 0 and len(self.s2.region) > 0:
						x = -5
						y =  ((i/10) * (self.s2.region[x].y - self.s1.region[x].y)) + self.s1.region[x].y
						Particle(self,x,y,(self.Vo,self.s2.region[x].y - self.s1.region[x].y))


		self.all_sprites.update()
		self.s1.update()
		self.s2.update()




	def drawing(self):
		#game loop draw
		pg.display.set_caption("{:.0f}".format(self.Clock.get_fps()))
		self.ventana.fill(BLACK)
		self.all_sprites.draw(self.ventana)
		self.s1.draw()
		self.s2.draw()
		                        
		self.draw_tangent_line(self.s1) 
		self.draw_tangent_line(self.s2) 

		pg.display.flip()

	def draw_tangent_line(self,segment):
		pos = pg.mouse.get_pos()

		if pos[0] in segment.region and (pos[0] + 1 in segment.region):

			O = (pos[0],segment.region[pos[0]].y)
			tangent_vec = segment.get_tangent_vec(pos[0])
			Sp = vecToInt(vec(O) + (500 * tangent_vec))
			Ep = vecToInt(vec(O) - (500 * tangent_vec))

			pg.draw.line(self.ventana,GREEN,Sp,Ep,2)

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