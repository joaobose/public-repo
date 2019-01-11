import pygame as pg
import random
from os import path
from settings import *
from sprites import *
from collections import deque

class Game():
	def __init__(self):
		pg.init()
		pg.mixer.init()
		self.ventana = pg.display.set_mode((ancho,largo))
		pg.display.set_caption(NAME)
		self.Clock=pg.time.Clock()
		self.running=True


	def new(self):
		#inicia un nuevo juego
		self.playing=True
		self.all_sprites=pg.sprite.Group()

		self.generate_dungeon()

	def generate_dungeon(self):

		#definimos la lista de todos los cuartos de la mazmorra
		self.rooms = []

		#definimos la lista de corredores de la mazmorra
		self.corridors = []

		#definimos el cuarto inicial y lo seleccionamos como el cuarto actual
		self.actual_room = Room(self,ancho/2, largo/2, 10, 10)
		self.rooms.append(self.actual_room)

		#mientras la cantidad de cuartos en la mazmorra sea menor que la cantidad de cuartos deseada
		while len(self.rooms) < N_ROOMS:

			#definimos como nula la direccion en la cual construiremos el siguiente cuarto
			dir = None

			#nos aseguramos de obtener una direccion valida
			while True:

				#obtenemos una direccion aleatoria dentro de las direcciones permitidas del cuarto actual (una vez que ya la usamos la quitamos de las opciones)
				if len(self.actual_room.allowed_connections) != 0:
					dir = random.choice(self.actual_room.allowed_connections)
					self.actual_room.allowed_connections.remove(dir)

				#escojemos un cuarto aleatorio

				#si encontramos una direcion (es decir que el desde el cuarto actual se puede construir otro cuarto)
				if dir != None:

					#entonces definimos el cuarto a construir
					corridor_lenght = random.randint(4,20)
					preliminar_room = self.generate_room(self.actual_room,dir, corridor_lenght,random.choice([10,16,10,25]))

					#si el cuarto a construir es el ultimo por construir, entonces ese cuarto es un boss rooms
					if len(self.rooms) == N_ROOMS - 1:
						preliminar_room = self.generate_room(self.actual_room,dir, corridor_lenght,100)

					#verificamos si el cuarto a construir colisiona con los otros cuartos  de la mazmorra
					for room in self.rooms:
						if room.hit_rect.colliderect(preliminar_room.hit_rect):
							#si lo hace, entonces no es posible construir en esa direcion
							dir = None
							break

					#verificamos si el cuarto a construir colisiona con los corredores de la mazmorra
					for corridor in self.corridors:
						if corridor.rect.colliderect(preliminar_room.hit_rect):
							#si lo hace, entonces no es posible construir en esa direcion
							dir = None
							break

					#luego, si nuestra direccion es valida, entonces rompemos el ciclo (ya conseguimos la direccion deseada)
					if dir != None:
						break
					else:
						#si no provamos con las otras direcciones disponibles
						continue

				#si no logramos conseguir alguna direccion en la cual construir, rompemos el ciclo (no es posible construir mas desde el cuarto actual)
				else:
					break

			#si la direcion que tuvimos es valida (distinta de nula)
			if dir != None:
				#entonces instanciamos el cuarto previamente predefinido, y generamos el corredor desde el cuarto actual hasta el nuevo cuarto
				instance = preliminar_room
				self.rooms.append(instance)
				corridor = self.make_corridor(self.actual_room,instance,dir)

			#si no pudimos encontrar una direccion valida, entonces cambiamos de cuarto actual (pues desde este ya no se puede construir mas)
			else:
				self.actual_room = random.choice(self.rooms)

	#dado un cuarto, y una direcion, contruye otro cuarto
	def generate_room(self,actual_room,dir, corridor_lenght, size):

		if dir == "up":
			w = size
			h = size

			r = Room(self,actual_room.rect.centerx - w/2, actual_room.rect.y - corridor_lenght - h, w, h)

		if dir == "down":
			w = size
			h = size

			r = Room(self,actual_room.rect.centerx - w/2, actual_room.rect.y + corridor_lenght + actual_room.rect.height, w, h)

		if dir == "left":
			w = size
			h = size

			r = Room(self,actual_room.rect.x - corridor_lenght - w, actual_room.rect.centery - h/2, w, h)

		if dir == "right":
			w = size
			h = size

			r = Room(self,actual_room.rect.x + corridor_lenght + actual_room.rect.width, actual_room.rect.centery - h/2, w, h)

		return r

	#construye un corredor entre dos cuartos dada una direccion
	def make_corridor(self,actual_room,r,dir):

		if dir == "up":
			c = Corridor(self,actual_room.rect.centerx - 2, r.rect.bottom , 4 , actual_room.rect.top - r.rect.bottom, BLUE )
			self.corridors.append(c)

		if dir == "down":
			c = Corridor(self,actual_room.rect.centerx - 2, actual_room.rect.bottom  , 4 ,r.rect.top - actual_room.rect.bottom , BLUE )
			self.corridors.append(c)

		if dir == "left":
			c = Corridor(self,r.rect.right, r.rect.centery - 2  , actual_room.rect.x - r.rect.right , 4 , BLUE )
			self.corridors.append(c)

		if dir == "right":
			c = Corridor(self,actual_room.rect.right, actual_room.rect.centery - 2  , r.rect.x - actual_room.rect.right , 4 , BLUE )
			self.corridors.append(c)

		#verificamos que el corredor no colisone con cualquier otro elemento de la mazmorra, si lo hace, destruimos el corredor y el cuarto SECUNDARIO asociado a el (pues no hay manera de conectarlo con la red-mazmorra)
		for room in self.rooms:
			if room.rect.colliderect(c.rect):
				self.corridors.remove(c)
				if r in self.rooms:
					self.rooms.remove(r)
				break

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
			if event.type == pg.QUIT:
				if self.playing==True:
					self.playing=False
				self.running=False

			#new code
			if event.type == pg.MOUSEBUTTONDOWN:
				mouse_pos = pg.mouse.get_pos()


	def update(self):
		#game loop update
		self.all_sprites.update()

	def drawing(self):
		#game loop draw
		self.ventana.fill(BLACK)
		self.all_sprites.draw(self.ventana)

		for room in self.rooms:
			room.draw(self.ventana)

		for corridor in self.corridors:
			corridor.draw(self.ventana)

		pg.display.flip()


game = Game()
while game.running:
	game.new()
	game.run()

pg.quit()
