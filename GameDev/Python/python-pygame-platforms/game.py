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
		self.load_data()


	def load_data(self):
		#loading folders
		self.game_folder = game_folder
		self.img_folder = img_folder
		self.snd_folder =  snd_folder

		#getting saved highscore
		with open(path.join(self.game_folder,HIGH_SCORE_FILE_NAME),"r+") as f:
			try:
				self.HighScore=int(f.read())
			except:
				self.HighScore=0
				f.write(str(0))

		#craeting spritesheet
		self.spritesheet=SpriteSheet(path.join(self.img_folder,SPRITESHEET_NAME))

		#loading sounds
		self.jump_sound=pg.mixer.Sound(path.join(self.snd_folder,"Jump33.wav"))
		self.boost_sound= pg.mixer.Sound(path.join(self.snd_folder,"Boost16.wav"))


	def new_game(self):
		#inicia un nuevo juego
		self.playing=True
		self.score=0
		self.mobs=pg.sprite.Group()
		self.all_sprites=pg.sprite.LayeredUpdates()
		self.plattforms=pg.sprite.Group()
		self.powerups = pg.sprite.Group()
		self.nubes=pg.sprite.Group()
		self.mob_timer=0
		self.walker_controler=WALKER_PROBABILITY
		self.flyman_spanw=-100
		self.broken_plat_controler=BROKEN_PLAT_PBT
		self.act_lvl = 0
		self.invencible = False

		for i in range(0,6):
			N = Nube(self)
			N.rect.y+=500

		#genera las plataformas de inicio (especificadas en settings.py)
		for plat in PLAT_LIST:
			Plattform(self,*plat)

		self.player=Player(self)

		pg.mixer.music.load(path.join(self.snd_folder,"Happy Tune.ogg"))


	def run(self):
		#game loop
		pg.mixer.music.play(-1)
		while self.playing:
			self.Clock.tick(FPS)
			self.events()
			self.update()
			self.drawing()
		pg.mixer.music.fadeout(500)


	def events(self):
		#game loop events
		for event in pg.event.get():
			if event.type== pg.QUIT:
				if self.playing==True:
					self.playing=False
				self.running=False
			if event.type == pg.KEYDOWN:
				if event.key==pg.K_SPACE:
					self.player.jump()
				if event.key == pg.K_ESCAPE:
					self.pause()
				if event.key == pg.K_p:
					self.__invencible()
				if event.key == pg.K_0:
					self.__superjump()
			if event.type == pg.KEYUP:
				if event.key==pg.K_SPACE:
					self.player.jump_cut()


	def update(self):
		#game loop update
		self.all_sprites.update()

		lvl = self.score//20

		if self.act_lvl < lvl:
			self.act_lvl += (lvl - self.act_lvl)

			set_dificulty(self,self.act_lvl,self.flyman_spanw,self.walker_controler,self.broken_plat_controler)


		#spanw a mob?
		now=pg.time.get_ticks()
		if now - self.mob_timer > 10000 + self.flyman_spanw:
			self.mob_timer=now
			Mob(self,"flyman")


		#detecta colisiones entre el player y las plataformas
		collisions_player_plattforms=pg.sprite.spritecollide(self.player,self.plattforms,False)

		if collisions_player_plattforms:

			#detecta cual de las plataformas con la que colisionamos es la que esta mas baja
			lowest = collisions_player_plattforms[0]

			for plat in collisions_player_plattforms:
				if plat.rect.y > lowest.rect.y:
					lowest = plat


			#detecta si el player se puede parar en una plataforma , si puede hacerlo (velocidad positiva),
			#se pregunta si ha llegado lo suficientemente alto para pararse en la plataforma, si lo hizo,
			#se para en la plataforma (velocidad en Y = 0 y posicion = al top de la plataforma)

			if self.player.vel.y>=0 and self.player.alive==True:
				if self.player.pos.y < lowest.rect.centery and \
				self.player.pos.x +10 > lowest.rect.left and \
				self.player.pos.x -10 < lowest.rect.right and \
				lowest.falling == False:

					#detecta si la plataforma es de lodo o de grama y modifica la friccion
					if lowest.type == "mud":
						self.player.friccion=player_mud_friction
						if self.player.standing == False:
							self.player.delay=200
					else:
						self.player.friccion=player_grass_friction
						if self.player.standing == False:
							self.player.delay=100

					if lowest.broken==True:
						lowest.counting=True

					self.player.pos.y=lowest.rect.top+1
					self.player.vel.y=0
					self.player.jumping = False
					self.player.boosting = False



		#colision entre los walkers y las plataformas

		collisions_enemies_plats=pg.sprite.groupcollide(self.mobs,self.plattforms,False,False)

		for hit in collisions_enemies_plats:

			lowest = collisions_enemies_plats[hit][0]

			for plat in collisions_enemies_plats[hit]:
				if plat.rect.y > lowest.rect.y:
					lowest = plat

			if hit.type == "walker":

				if hit.pos.y < lowest.rect.centery and\
				   hit.pos.x < lowest.rect.right and\
				   hit.pos.x > lowest.rect.left:

					hit.pos.y=lowest.rect.top+1
					hit.vel.y=0


		#colision con enemigos
		collisions_player_enemies = pg.sprite.spritecollide(self.player,self.mobs,False)

		for enemy in collisions_player_enemies:

			if pg.sprite.collide_mask(self.player,enemy):

				if self.player.boosting==False and self.player.alive==True and self.player.pos.y > (largo*1/4) and self.invencible==False:
					self.player.die()

		#colision entre powerups y player
		collisions_player_powerups = pg.sprite.spritecollide(self.player, self.powerups,True)

		if collisions_player_powerups:
			if collisions_player_powerups[0].type == "boost" and self.player.alive==True:
				if self.player.boosting==False:
					self.player.vel.y = -BOOST_SIZE
					self.player.jumping = False
					self.boost_sound.play()
					self.player.boosting = True

		#subiendo (moviendo la camara hacia arriba)
		if self.player.pos.y<=largo*1/4:

			if random.randint(0,100) < 10:
				Nube(self)

			self.player.pos.y+=max(abs(self.player.vel.y),2)

			for mob in self.mobs:

				if mob.type == "walker":

					mob.pos.y+=max(abs(self.player.vel.y),2)

				else:

					mob.rect.y+=max(abs(self.player.vel.y),2)

			for nube in self.nubes:

				nube.rect.y+=max(abs(int(self.player.vel.y/random.choice([1,2,3,4]))),2)


			for plat in self.plattforms:

				plat.rect.y+=max(abs(self.player.vel.y),2)

				if plat.rect.top>=largo:
					self.score+=10
					plat.kill()

		#callendo y muriendo
		if self.player.rect.bottom >= largo :

			for sprite in self.all_sprites:

				if sprite == self.player:
					sprite.pos.y-=sprite.vel.y
				elif sprite in self.mobs and sprite.type == "walker":
					sprite.pos.y-=self.player.vel.y

				else:

					sprite.rect.y -= self.player.vel.y

				if sprite.rect.y <=0:
					sprite.kill()

			if self.player.rect.top>largo:
				self.playing=False



		#si hay menos de 6 plataformas, crea una nueva (encima de la pantalla)
		while len(self.plattforms) <7:

			Plattform(self,random.randint(0,(ancho-100)),random.randint(-100,-50),True,random.choice(PLATS_TYPE_PROBABILITY),True)

		#detecta si dos plataformas colisionan entre ellas (estan superpuestas),
		#si lo estan elimina a una de ellas (la que este mas alto)


		for plat1 in self.plattforms:
			for plat2 in self.plattforms:
				if plat1.rect.center == plat2.rect.center:
					continue
				elif plat1.rect.colliderect(plat2.rect):
					higher= plat1
					if higher.rect.centery>plat2.rect.centery:
						higher = plat2

					if plat1.falling==False and plat2.falling==False:
						higher.kill()




	def drawing(self):
		#game loop draw
		self.ventana.fill(BG_COLOR)
		self.all_sprites.draw(self.ventana)
		self.draw_text(str(self.score),30,WHITE,ancho/2,20)

		pg.display.flip()


	def draw_new_game_screen(self):
		#draw the new game screen
		pg.mixer.music.load(path.join(self.snd_folder,"Yippee.ogg"))
		pg.mixer.music.play(-1)
		self.ventana.fill(BG_COLOR)
		self.draw_text(NAME,50,WHITE,ancho/2,largo/4)
		self.draw_text("A and D to move, Space to jump",30,WHITE,ancho/2,largo/2)
		self.draw_text("press any key to start",30,WHITE,ancho/2,largo*3/4)
		self.draw_text("Escape to pause the game",25,WHITE,ancho/2,largo-(largo/2 -25))
		self.draw_text("High Score: " + str(self.HighScore),25,WHITE,ancho/2,50)
		pg.display.flip()
		self.wait_for_key()
		pg.mixer.music.fadeout(500)


	def draw_game_over_screen(self):
		#draw the game over screen
		if self.running == True:
			pg.mixer.music.load(path.join(self.snd_folder,"Yippee.ogg"))
			pg.mixer.music.play(-1)
			self.ventana.fill(BG_COLOR)
			self.draw_text("GAME OVER",50,WHITE,ancho/2,largo/4)
			self.draw_text("score: " + str(self.score),30,WHITE,ancho/2,largo/2)
			self.draw_text("press any key to try again",30,WHITE,ancho/2,largo*3/4)

			if self.score>self.HighScore:

				self.HighScore=self.score

				with open(path.join(self.game_folder,HIGH_SCORE_FILE_NAME),"r+") as f:
					f.write(str(self.HighScore))

				self.draw_text("NEW HIGH SCORE",25,WHITE,ancho/2,largo/2+40)

			else:
				self.draw_text("High Score: " + str(self.HighScore),25,WHITE,ancho/2,largo/2+40)

			pg.display.flip()
			self.wait_for_key()
			pg.mixer.music.fadeout(500)


	def pause(self):
		self.draw_text("PAUSE",50,WHITE,ancho/2,largo/2)
		pg.display.flip()
		self.wait_for_key(pg.K_ESCAPE,"keydown")
		if self.running==False:
			self.playing=False



	def draw_text(self,text,size,color,x,y):
		font = pg.font.Font(FONT_NAME,size)
		text_surface=font.render(text,True,color)
		text_rect=text_surface.get_rect()
		text_rect.midtop=(x,y)
		self.ventana.blit(text_surface,text_rect)


	def wait_for_key(self, key_ = None, type_ = "keyup"):
		waiting=True
		while waiting:
			self.Clock.tick(FPS)

			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.running=False
					waiting=False

				if type_ == "keyup":
					if event.type == pg.KEYUP:
						if key_==None:
							waiting=False
						elif event.key== key_:
							waiting=False
				else:
					if event.type == pg.KEYDOWN:
						if key_==None:
							waiting=False
						elif event.key== key_:
							waiting=False

	def __invencible(self):
		if self.invencible == False:
			self.invencible = True
			print ("invencible mode ON")

		elif self.invencible == True:
			self.invencible = False
			print ("invencible mode OFF")

	def __superjump(self):
		self.player.vel.y = -1000
		self.player.boosting=True


#ciclo del programa
game = Game()
game.draw_new_game_screen()
while game.running:
	game.new_game()
	game.run()
	game.draw_game_over_screen()

pg.quit()
