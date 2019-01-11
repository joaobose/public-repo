import pygame as pg
from settings import *
from premade import *



class LifeGrid():
	def __init__(self):
		self.aliveNodes = []#nodes that are currently alive on the grid
		self.deathNodes = []#deaths nodes explored every frame
		self.connections = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]#all permitted connections between neighbors
		self.last_update = 0 #variable for control of the artificial delay


	def find_neighbors(self,node):#returns the neighbors of a node
		neighbors = [(node[X] + connection[X],node[Y] + connection[Y]) for connection in self.connections]
		return neighbors


	def update(self):
		if pg.time.get_ticks() - self.last_update > LIFEGRID_DELAY:#putting some delay
			self.last_update = pg.time.get_ticks()

			todie = list(filter(self.checkAlives, self.aliveNodes))#getting the nodes that are about to die (while filtering the aliveNodes)

			bornedNodes = list(filter(self.checkDeaths, self.deathNodes))#getting the nodes that are about to born (while filtering the deathNodes)

			self.aliveNodes.extend(bornedNodes)#adding the nodes that are about to live to the aliveNodes

			self.aliveNodes = list(set(self.aliveNodes) - set(todie))#removing the nodes that are about to die from the aliveNodes

			del self.deathNodes[:]#cleanning the deathNodes explored in this actual frame

	def checkAlives(self,node):#filter function for alive nodes

		n = self.find_neighbors(node)#gets the neighbors of the node

		#split neighbors into alive and death neighbors
		alivesNeighbors = list(set(n) & set(self.aliveNodes))
		deathNeighbors = list(set(n) - set(self.aliveNodes))


		if len(deathNeighbors) > 0:
			#adds the death neighbors to the deathNodes (excluding the ones that are already there)
			self.deathNodes.extend(list(set(deathNeighbors) - set(self.deathNodes)))

		#finnaly, if the node doesnt have 2 or 3 live neighbors, then the node its about to die
		if len(alivesNeighbors) not in [2,3]:
			return True

	def checkDeaths(self,node):#filter function for death nodes

		#gets the alive neighbors of the node
		n = self.find_neighbors(node)
		alivesNeighbors = list(set(n) & set(self.aliveNodes))

		#finnaly if the node have exactly 3 alive neighbors, then the node its about to born
		if len(alivesNeighbors) == 3:
			return True

class Game():
	def __init__(self):#initial settings for window
		pg.init()
		self.ventana = pg.display.set_mode((width,height))
		pg.display.set_caption(NAME)
		self.Clock = pg.time.Clock()
		self.font = pg.font.SysFont(pg.font.match_font("times new"),30)

	def new(self):#initial setting for a new game
		self.playing = True

		#creates the lifeGrid (grid that contains the game of life logic)
		self.lifeGrid = LifeGrid()
		self.lifeGrid.aliveNodes = premade[0]#create a few default nodes of the lifeGrid
		self.index = 0

		#sets the camera initial settings
		self.camera_pos = [0,0]
		self.camera_offset = [0,0]
		self.camera_vel = [0,0]

		#pre-render the graphic grid to store it as an image
		self.grid = self.renderGrid(TILESIZE,(width//2,height//2))


	def run(self):#Runs the game
		#game loop
		while self.playing:
			self.dt = self.Clock.tick(FPS)/1000
			self.events()
			self.update()
			self.drawing()

	def events(self):
		#game loop events
		for event in pg.event.get():
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False

			if event.type == pg.KEYDOWN:
				if event.key == pg.K_p:
					self.camera_offset = [0,0]
					self.camera_pos = [0,0]

			self.cameraEvents(event)

	def update(self):#update the virtual elements of the game
		self.lifeGrid.update()
		self.cameraUpdate()


	def drawing(self):#draws everything on the screen
		#game loop draw
		self.ventana.fill(DARKGREY)
		self.draw_nodes(self.lifeGrid,self.ventana)
		self.ventana.blit(self.grid[IMAGE],self.grid[RECT])

		pg.display.flip()

	def draw_text(self,x,y,text,color):
		text_surf = self.font.render(text,True,color)
		text_rect = text_surf.get_rect()
		text_rect.topleft = (x,y)
		self.ventana.blit(text_surf,text_rect)

	def renderGrid(self,tilesize,center):#renders the grid image
		#creates the surface (empty image), gets his rect and put its center position to the given center argument
		surf = pg.Surface((width,height))
		r = surf.get_rect()
		r.center = (center)

		#draws the grid on the empty image
		for x in range(-tilesize,width + tilesize,tilesize):
			pg.draw.line(surf,MEDGREY,(x,0),(x,height))

		for y in range(-tilesize,height + tilesize,tilesize):
			pg.draw.line(surf,MEDGREY,(0,y),(width,y))

		#sets all black pixels alpha value to zero (excludes all black pixels of the image)
		surf.set_colorkey(BLACK)

		#finnaly returns an array with the image itself and its rect
		return [surf,r]

	def draw_nodes(self,lifeGrid,screen):#draes the alive nodes on the screen
		for node in lifeGrid.aliveNodes:
			rect = pg.Rect((node[X] * TILESIZE) + width//2 + int(self.camera_offset[X]),
						   (node[Y] * TILESIZE) + height//2 + int(self.camera_offset[Y]),
						   TILESIZE,TILESIZE)

			pg.draw.rect(screen,GREY,rect)

	def cameraEvents(self,event):
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_a:
				self.camera_vel[X] = CAMERA_VEL

			if event.key == pg.K_d:
				self.camera_vel[X] = -CAMERA_VEL

			if event.key == pg.K_w:
				self.camera_vel[Y] = CAMERA_VEL

			if event.key == pg.K_s:
				self.camera_vel[Y] = -CAMERA_VEL

		if event.type == pg.KEYUP:
			if event.key == pg.K_a or event.key == pg.K_d:
				self.camera_vel[X] = 0

			if event.key == pg.K_w or event.key == pg.K_s:
				self.camera_vel[Y] = 0

	def cameraUpdate(self):#updates the camera offset
		#updates the camera position
		self.camera_pos = [self.camera_pos[X] + ((self.camera_vel[X] * self.dt)),
						   self.camera_pos[Y] + ((self.camera_vel[Y] * self.dt))]

		#updates the camera offset
		self.camera_offset = [(self.camera_pos[X]//TILESIZE)*TILESIZE,
							  (self.camera_pos[Y]//TILESIZE)*TILESIZE]


	#loop to set the initial state of the lifeGrid system
	def set_initial_state(self):
		waiting = True

		while waiting:
			self.dt = self.Clock.tick(FPS)/1000

			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()

				if event.type == pg.MOUSEBUTTONDOWN:#if the player clicks the window
					#gets the mouse coordinates on the world
					mouse_pos = ((pg.mouse.get_pos()[X] - width//2 - int(self.camera_offset[X]))//TILESIZE,
								(pg.mouse.get_pos()[Y] - height//2 - int(self.camera_offset[Y]))//TILESIZE )

					#spawning or destroying a cell
					if mouse_pos in self.lifeGrid.aliveNodes:
						self.lifeGrid.aliveNodes.remove(mouse_pos)
					else:
						self.lifeGrid.aliveNodes.append(mouse_pos)

				if event.type == pg.KEYDOWN:

					if event.key == pg.K_SPACE:#if the player press space, the the game start
						waiting = False

					if event.key == pg.K_p:#if the player press P, then reset the camera pos and offset
						self.camera_offset = [0,0]
						self.camera_pos = [0,0]

					if event.key == pg.K_o:
						print(self.lifeGrid.aliveNodes)

					if event.key == pg.K_m:
						self.index += 1
						if self.index == len(premade):
							self.index = 0

						self.lifeGrid.aliveNodes = premade[self.index]

				self.cameraEvents(event)#updating the camera

			#updates and draw the needed elements
			self.cameraUpdate()
			self.ventana.fill(DARKGREY)
			self.draw_nodes(self.lifeGrid,self.ventana)
			self.ventana.blit(self.grid[IMAGE],self.grid[RECT])
			self.draw_text(10,10,"click to add cells",WHITE)
			self.draw_text(10,40,"W,A,S,D to move arround the map",WHITE)
			self.draw_text(10,70,"SPACE to start the simulation",WHITE)
			self.draw_text(10,100,"press P to go back to the origin",WHITE)
			self.draw_text(10,130,"press M to change the initial pattern",WHITE)


			pg.display.flip()


game = Game()
game.new()
game.set_initial_state()
game.run()

pg.quit()
