import pygame as pg 
from settings import *
import random

vector = pg.math.Vector2

class SpriteSheet():
	def __init__(self,filename):
		self.spritesheet=pg.image.load(filename).convert()

	def get_image(self, x, y, ancho, largo):
		image=pg.Surface((ancho,largo))
		image.blit(self.spritesheet,(0,0),(x,y,ancho,largo))
		image=pg.transform.scale(image,(ancho//2,largo//2)).convert()
		return image

class Player(pg.sprite.Sprite):
	def __init__(self,game):
		self._layer=PLAYER_LAYER
		self.groups = game.all_sprites

		pg.sprite.Sprite.__init__(self, self.groups)
		self.game=game
		self.last_update=0
		self.current_frame=0
		self.delay=0
		self.__load_images()
		self.current_animation_list=self.standing_frames
		self.image=self.standing_frames[0]
		self.rect=self.image.get_rect()
		self.mask=pg.mask.from_surface(self.image)
		self.rect.midbottom=(40,largo-100)
		self.pos=vector(self.rect.midbottom)
		self.vel=vector(0,0)
		self.acc=vector(0,0)
		self.friccion=player_grass_friction
		self.jumping = False
		self.boosting = False
		self.alive=True

	def __load_images(self):
		self.jumping_frames=[self.game.spritesheet.get_image(382, 763, 150, 181)]
		self.jumping_frames[0].set_colorkey(BLACK)

		self.standing_frames=[self.game.spritesheet.get_image(614,1063,121,191),self.game.spritesheet.get_image(690, 406, 120, 201)]
		for frame in self.standing_frames:
			frame.set_colorkey(BLACK)

		self.running_frames_r=[self.game.spritesheet.get_image(678,860,120,201),self.game.spritesheet.get_image(692, 1458, 120, 207)]
		self.running_frames_l=[]
		for frame in self.running_frames_r:
			frame.set_colorkey(BLACK)
			self.running_frames_l.append(pg.transform.flip(frame,True,False))



	def update(self):
		if self.alive ==True:
			self.__animation()

		self.__kinematics()


	def jump_cut(self):
		if self.jumping==True and self.boosting==False:
			if self.vel.y < -11:
				self.vel.y =-11



	def jump(self):
		
		#evalua si hay alguna plataforma debajo (que le permita saltar)(por ello mueve el sprite haci abajo(para que el sprite no tenga que entrar adentro de la plataforma para saltar))
		self.rect.y+=2
		hits = pg.sprite.spritecollide(self,self.game.plattforms,False)
		self.rect.y-=2

		if hits:
			#si cumple las condicones, salta
			if self.jumping==False and self.boosting==False:
				self.game.jump_sound.play()
				self.jumping=True
				self.vel.y=-22


	def __animation(self):
		#detecta en que estado de movimiento se encuentra el sprite player (escoje la secuencia actual de animacion)
		if int(self.vel.y) != 0 :
			self.current_animation_list=self.jumping_frames

		elif int(self.vel.x) < 0:
			self.standing = False
			self.current_animation_list=self.running_frames_l
			

		elif int(self.vel.x) > 0:
			self.standing = False
			self.current_animation_list=self.running_frames_r
			
		else:
			self.standing = True
			self.current_animation_list=self.standing_frames
			
		if self.standing == True:
			self.delay=400


		#proceso de animacion
		now = pg.time.get_ticks()
		if now - self.last_update > self.delay:
			self.last_update=now

			self.current_frame =  (self.current_frame + 1) % len(self.current_animation_list)

			bottom = self.rect.bottom

			self.image=self.current_animation_list[self.current_frame]

			self.rect=self.image.get_rect()
			self.rect.bottom=bottom
			self.mask=pg.mask.from_surface(self.image)




	def __kinematics(self):
		self.acc=vector(0,gravity)
		keys=pg.key.get_pressed()

		if keys[pg.K_a]:
			self.acc.x=-player_acel
		if keys[pg.K_d]:
			self.acc.x=player_acel
			  
		#tomando en cuenta la friccion:
		self.acc.x+=self.vel.x*self.friccion

		#ecuaciones de cinematica:

		#acelerando
		self.vel+=self.acc

		#calculando la posicion
		self.pos+=self.vel+self.acc*0.5

		#moviendo el rectangulo por la pantalla

		if self.pos.x > ancho + self.rect.width / 2:
			self.pos.x = 0 - (self.rect.width / 2)
			
		if self.pos.x < 0 - self.rect.width / 2:
			self.pos.x = ancho + (self.rect.width / 2)

		self.rect.midbottom=self.pos

	def die(self):
		self.vel.y=0
		self.alive=False
		self.vel.y=-20
		#play sound
		self.image=self.game.spritesheet.get_image(382,946,150,174)
		self.image.set_colorkey(BLACK)


class Nube(pg.sprite.Sprite):
	def __init__(self,game):
		self._layer=NUBE_LAYERS
		self.groups= game.all_sprites , game.nubes
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game=game

		self.images_list=[]

		for i in range(1,4):
			self.images_list.append(pg.image.load(path.join(self.game.img_folder,"cloud{}.png".format(i))).convert())

		self.image=random.choice(self.images_list)
		self.image.set_colorkey(BLACK)
		self.rect=self.image.get_rect()

		scale_per = random.randint(50,100)/100

		pg.transform.scale(self.image,(int(self.rect.width*scale_per),int(self.rect.height*scale_per)))
		
		self.rect.x=random.randint(0,ancho-self.rect.width)
		self.rect.y=random.randint(-500,-50)

		self.velx = random.choice([-0.5,0.5,-0.25,0.25,])
		self.pos = self.rect.x

	def update(self):

		self.pos+=self.velx

		self.rect.x = int(self.pos)

		if self.rect.right < 0:
			self.reborn()
			self.pos = ancho 
			

		if self.rect.left > ancho:
			self.reborn()
			self.pos = 0 - self.rect.width
			

		if self.rect.top > largo *2:
			self.kill()

	def reborn(self):
		center=self.rect.center
		self.image=random.choice(self.images_list)
		self.image.set_colorkey(BLACK)
		self.rect=self.image.get_rect()

		scale_per = random.randint(50,100)/100

		pg.transform.scale(self.image,(int(self.rect.width*scale_per),int(self.rect.height*scale_per)))

		self.rect.center = center

class Plattform(pg.sprite.Sprite):
	def __init__(self,game,x,y,mob_spanw=False,terrain_type="grass",broken=False,be_broke=False):
		self._layer=PLAT_LAYER
		self.groups= game.all_sprites , game.plattforms
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game=game

		self.type=terrain_type
		self.broken=broken

		self.type_dic = {"grass":{"image_list":
								 [self.game.spritesheet.get_image(0,288,380,94),
								  self.game.spritesheet.get_image(213,1662,201,100)],
								  "broken_image_list":	
								  [self.game.spritesheet.get_image(0,384,380,94),
								  self.game.spritesheet.get_image(382,204,200,100)]							
								  													},
						"mud":{"image_list":
							   [self.game.spritesheet.get_image(0,960,380,94),
								self.game.spritesheet.get_image(218,1558,200,100)],
								"broken_image_list":	
								[self.game.spritesheet.get_image(0,864,380,94),
								 self.game.spritesheet.get_image(382,0,200,100)]			
							   														}
						}

		if (self.broken == True and random.randint(0,100) <=self.game.broken_plat_controler) or be_broke==True :

			images_list=self.type_dic[self.type]["broken_image_list"]
			self.broken=True
			self.counting=False
			self.counter=0
			self.falling=False

		else:

			images_list=self.type_dic[self.type]["image_list"]
			self.broken=False
			self.falling=False

		self.image=random.choice(images_list)
		self.image.set_colorkey(BLACK)
		self.rect=self.image.get_rect()
		self.rect.x,self.rect.y=x,y

		self.pos = vector(self.rect.center)
		self.vel=vector(0,0)

		if random.randint(0,100) <= POWER_UP_PROBABILITY:
			PowerUp(self.game,self)

		if mob_spanw==True:
			if random.randint(0,200) <= self.game.walker_controler:
				Mob(self.game,"walker",*self.rect.center)

	def update(self):
		if self.broken == True:
			if self.counting==True:
				self.counter+=1

			if self.counter > 30:
				self.falling=True

			self.pos=vector(self.rect.center)

			if self.falling==True:
			
				self.vel.y+=gravity

				self.pos.y+=self.vel.y+(gravity/2)

				self.rect.centery = self.pos.y



class PowerUp(pg.sprite.Sprite):
	def __init__(self,game,plat):
		self._layer=POWER_UP_LAYER
		self.groups= game.all_sprites , game.powerups

		pg.sprite.Sprite.__init__(self, self.groups)
		self.game=game
		self.plat=plat
		type_list=["boost"]

		self.type=random.choice(type_list)
		self.image=game.spritesheet.get_image(820,1805,71,70)
		self.image.set_colorkey(BLACK)
		self.rect=self.image.get_rect()
		self.rect.centerx=self.plat.rect.centerx
		self.rect.bottom=self.plat.rect.top +5 

	def update(self):
		self.rect.bottom=self.plat.rect.top +5 

		if self.game.plattforms.has(self.plat)==False:
			self.kill()

class Mob(pg.sprite.Sprite):
	def __init__(self,game,typex,x=None,y=None):
		self._layer=MOBS_LAYER
		self.groups= game.all_sprites , game.mobs

		pg.sprite.Sprite.__init__(self, self.groups)
		self.game=game

		self.type=typex

		self.type_dic={"flyman":{"image_list":
					   			[self.game.spritesheet.get_image(568,1534,122,135),
								self.game.spritesheet.get_image(566,510,122,139)]
																					},
						"walker":{"image_list":
								 [self.game.spritesheet.get_image(704,1256,120,159),
								  self.game.spritesheet.get_image(812,296,90,155)]
								 													}
								 }

		
		self.image_list=self.type_dic[self.type]["image_list"]

		for image in self.image_list:
			image.set_colorkey(BLACK)

		self.image=self.image_list[0]
		self.mask=pg.mask.from_surface(self.image)
		self.rect= self.image.get_rect()

		if self.type=="flyman":

			self.vx=random.randint(1,4)

			self.rect.centerx=random.choice([-100,ancho+100])

			self.rect.centery=random.randint(-500,largo/2)

			if self.rect.centerx > ancho:
				self.vx*=-1

			self.vy=0
			self.armonic_acel_y=1

		if self.type == "walker":
			self.rect.centerx=x
			self.rect.bottom=y - 10
			self.vel=vector(random.choice([-1,-2,1,2]),0)
			self.pos = vector(self.rect.midbottom)
			self.acc = vector(0,gravity)

			self.image_listR = self.image_list

			self.image_listL = []

			for x in self.image_listR:
				self.image_listL.append(pg.transform.flip(x,True,False))

			if self.vel.x < 0:
				self.image_listA = self.image_listL
			else:
				self.image_listA = self.image_listR

			self.image = self.image_listA[0]

			self.last_update =0
			self.index=0
			

	def update(self):
		if self.type == "flyman":
			self.update_flyman()
		if self.type=="walker":
			self.update_walker()


	def update_flyman(self):
		self.rect.x+=self.vx

		self.vy+=self.armonic_acel_y

		old_center=self.rect.center

		if self.vy > 8 or self.vy < -8:
			self.armonic_acel_y*=-1

		if self.vy < 0:
			self.image = self.image_list[1]
			self.mask=pg.mask.from_surface(self.image)
			self.rect = self.image.get_rect()
		else:
			self.image = self.image_list[0]
			self.mask=pg.mask.from_surface(self.image)
			self.rect = self.image.get_rect()

		
		self.rect.center = old_center

		self.rect.y += self.vy

		if self.rect.right < -100 or \
		self.rect.left > ancho+100 or \
		self.rect.y > ancho+100:
			self.kill()


	def update_walker(self):
		#cinematics
		self.vel+=self.acc

		self.pos+=self.vel+(self.acc/2)

		if self.pos.x > ancho + self.rect.width / 2:
			self.pos.x = 0 - (self.rect.width / 2)
			
		if self.pos.x < 0 - self.rect.width / 2:
			self.pos.x = ancho + (self.rect.width / 2)

		self.rect.midbottom=self.pos

		if self.rect.top > largo:
			self.kill()

		#animation
		now = pg.time.get_ticks()

		if now - self.last_update > 150:
			self.last_update = now 

			center = self.rect.center

			self.index=(self.index+1) % (len(self.image_listA)) 

			self.image = self.image_listA[self.index]

			self.rect = self.image.get_rect()
			self.mask = pg.mask.from_surface(self.image)
			self.rect.center=center

		



		