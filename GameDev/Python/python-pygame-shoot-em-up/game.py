#music from Frozen Jam by tgfcoder <https://twitter.com/tgfcoder>
#licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
#art by Kenney.nl
import pygame,random,os
from os import path
from sett import *
import serial
pygame.init()
pygame.mixer.init()

ancho,largo=800,600
FPS=60

BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
RED=(255,0,0)
GREY=(155,155,155)
WHITE=(255,255,255)
YELLOW=(255,255,0)
DARK_RED=(180,0,0)


class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.transform.scale(player_img,(50,38))
		self.image.set_colorkey(BLACK)
		self.rect=self.image.get_rect()
		self.radius=int((self.rect.width * 0.78)/2)
		#pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
		self.rect.centerx=ancho/2
		self.rect.bottom=largo-10
		self.Vx=0
		self.shield=100
		self.shoot_delay=200
		self.last_shoot=pygame.time.get_ticks()
		self.hidden=False
		self.hide_time=800
		self.hide_clock=pygame.time.get_ticks()
		self.life=3

		self.untouchable=False
		self.untouchable_statesList=["hidden","visible"]
		self.untouchable_state = 1
		self.untouchable_time=3000
		self.last_update_untouchable=pygame.time.get_ticks()
		self.untouchable_clock=pygame.time.get_ticks()


		self.double=False
		self.clock_double=pygame.time.get_ticks()
		self.double_time=3000


	def update(self):
		#evaluando si esta en power up de tipo "gun"

		if self.double==True:
			nowP=pygame.time.get_ticks()
			if nowP - self.clock_double >self.double_time:
				self.double=False

		#evaluando y calculando el timepo de regreso del player del estado hide
		nowH = pygame.time.get_ticks()
		if self.hidden==True and nowH - self.hide_clock > self.hide_time:
			self.hidden=False
			self.rect.centerx=ancho/2
			self.rect.bottom=largo-10


		#si el player esta en estado respawn (intocable)
		nowV=pygame.time.get_ticks()
		if self.hidden==False and self.untouchable==True:
			if nowV- self.untouchable_clock <self.untouchable_time:

				nowC=pygame.time.get_ticks()
				if nowC -self.last_update_untouchable>75:
					self.last_update_untouchable=nowC
					self.untouchable_state+=1

					if self.untouchable_state>=len(self.untouchable_statesList):
						self.untouchable_state=0

					if self.untouchable_statesList[self.untouchable_state]=="hidden":
						self.rect.centery=largo+200
					else:
						self.rect.bottom=largo-10
			else:
				self.rect.bottom=largo-10
				self.untouchable_state=1
				self.untouchable=False


		self.__movement()

	def __movement(self):
		control = 4 #2 = joystick, #4 Gx
		self.Vx=0
		keystate= pygame.key.get_pressed()
		if keystate[pygame.K_a] or control_variables[control] == "50":
			if self.rect.left>0:
				self.Vx=-5
		if keystate[pygame.K_d] or control_variables[control] == "49":
			if self.rect.right<ancho:
				self.Vx=5
		if keystate[pygame.K_SPACE] or control_variables[0] != "48" or control_variables[1] != "48":
			if self.hidden==False and self.untouchable_state!=0:
				self.shoot()
		self.rect.centerx += self.Vx

	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shoot>self.shoot_delay:
			self.last_shoot=now
			shoot_snd.play()
			if self.double==False:
				B = Bullet(self.rect.centerx,self.rect.top)
				all_sprites.add(B)
				bullets.add(B)
			else:
				xa=self.rect.left
				ya=self.rect.centery
				for x in range(1,3):
					B = Bullet(xa,ya)
					all_sprites.add(B)
					bullets.add(B)
					xa+=self.rect.width

	def hide(self):
		self.hidden=True
		self.untouchable=True
		self.untouchable_clock=pygame.time.get_ticks()
		self.untouchable_state=0
		self.hide_clock=pygame.time.get_ticks()
		self.rect.center=(ancho/2,largo+200)

class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=bullet_img
		self.image.set_colorkey(BLACK)
		self.rect=self.image.get_rect()
		self.rect.centerx=x
		self.rect.bottom=y
		self.Vy=-10

	def update(self):
		self.rect.y+=self.Vy

		if self.rect.bottom < 0:
			self.kill()

class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_original=random.choice(meteor_imgs)
		self.image_original.set_colorkey(BLACK)
		self.image=self.image_original.copy()
		self.image.set_colorkey(BLACK)
		self.rect=self.image.get_rect()
		self.radius=int((self.rect.width*0.9)/2)
		#pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
		self.rect.y=random.randint(-200,-100)
		self.rect.x=random.randint(0,ancho-self.rect.width)
		self.Vx=random.randint(-3,3)
		self.Vy=random.randint(1,8)
		self.rot=0
		self.rot_speed=random.randint(-8,8)
		self.last_update=pygame.time.get_ticks()


	def update(self):
		self.__rotate()
		self.__movement()

	def __movement(self):
		#move
		self.rect.move_ip(self.Vx,self.Vy)
		#re-random
		if self.rect.top>largo or self.rect.right<-20 or self.rect.left>ancho+50:
			self.rect.y=random.randint(-200,-100)
			self.rect.x=random.randint(0,ancho-self.rect.width)
			self.Vx=random.randint(-3,3)
			self.Vy=random.randint(1,8)
			self.rot_speed=random.randint(-8,8)

	def __rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_update >50:
			self.last_update=now
			self.rot = self.rot + self.rot_speed % 360
			self.old_center = self.rect.center
			self.image=pygame.transform.rotate(self.image_original,self.rot)
			self.rect=self.image.get_rect()
			self.rect.center=self.old_center

class Explosion(pygame.sprite.Sprite):
	def __init__(self,center,size):
		pygame.sprite.Sprite.__init__(self)
		self.size=size
		self.image=explosions_imgs[self.size][0]
		self.rect=self.image.get_rect()
		self.rect.center=center
		self.imagen_actual=0
		self.frame_animation_delay=35
		self.last_update=pygame.time.get_ticks()

	def update(self):
		now = pygame.time.get_ticks()
		if now- self.last_update>self.frame_animation_delay:
			self.last_update=now
			self.imagen_actual+=1
			if self.imagen_actual >= len(explosions_imgs[self.size]):
				self.kill()
			else:
				old_center=self.rect.center
				self.image=explosions_imgs[self.size][self.imagen_actual]
				self.rect=self.image.get_rect()
				self.rect.center=old_center

class Pow(pygame.sprite.Sprite):
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self)
		self.posibilities=["extra_life"]+["gun"for g in range(7)]+["shield"for s in range(7)]
		self.type=random.choice(self.posibilities)
		self.image=pow_images[self.type]
		self.rect=self.image.get_rect()
		self.rect.center=center
		self.Vy=5

	def update(self):
		self.rect.y+=self.Vy

		if self.rect.top > largo:
			self.kill()


def new_mob():
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)

def draw_shield_bar(surface,x,y,escudo,almost_dead):
	if escudo<0:
		escudo=0

	if almost_dead==True:
		color=DARK_RED
	else:
		color=GREY

	ancho_barra=200
	alto_barra=10

	percent=(escudo*100)/100
	fill=(percent*ancho_barra)/100


	rect_fill=pygame.Rect(x,y,float(fill),alto_barra)

	rect_fondo=pygame.Rect(x,y,ancho_barra,alto_barra)

	pygame.draw.rect(surface,GREEN,rect_fill)

	pygame.draw.rect(surface,color,rect_fondo,2)


def draw_text(surface,text,size,x,y):
	font=pygame.font.Font(font_name,size)
	text=font.render(text,True,WHITE)
	text_rect=text.get_rect()
	text_rect.midtop=(x,y)
	surface.blit(text,text_rect)

def draw_lives(surface,img,x,y,vidas):
	rect=img.get_rect()
	for i in range(vidas):
		rect.centery=y
		rect.left=x+(i*35)
		surface.blit(img,rect)

def draw_buff(surface,bol,x,y):
	image=pow_images["gun"]
	rect=image.get_rect()
	rect.centerx,rect.top=(x,y)
	if bol ==True:
		surface.blit(image,rect)

def show_menu(typex):

	ventana.blit(fondo,fondo_rect)

	if typex == "menu":
		draw_text(ventana,"SMUP!",64,ancho/2,largo/4)
		draw_text(ventana,"A and D to move , and SPACE for shoting",32, ancho/2, largo/2)
		draw_text(ventana, "press any key to start",32,ancho/2,largo*3/4)

	elif typex == "over":
		draw_text(ventana,"GAME OVER!",64,ancho/2,largo/2)
		draw_text(ventana, "press any key to start",32,ancho/2,largo*3/4)

	pygame.display.flip()

	waiting=True

	while waiting:
		clock.tick(FPS)

		if arduino != None:
			data = arduino.readline()
			try:
				raw_string = (str(data[0])) + ',' + str(data[1]) + ',' + str(data[2]) + ',' + str(data[3]) + ',' + str(data[4]) + ',' + str(data[5])
			except:
				pass

			h = raw_string.split(',')
			control_variables = h;

		else:
			control_variables = ["48","48","48","48","48"]

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting=False

			if control_variables[0] != "48" or control_variables[1] != "48" or control_variables[2] != "48" or control_variables[3] != "48":
				waiting = False




ventana=pygame.display.set_mode((ancho,largo))

#loading graphics
explosions_imgs={}
explosions_imgs["big1s"]=[]
explosions_imgs["player"]=[]
explosions_imgs["small1s"]=[]
for i in range(0,9):
	nombre_archivo="regularExplosion0{}.png".format(i)
	img = pygame.image.load(path.join(image_folder,nombre_archivo)).convert()
	img.set_colorkey(BLACK)
	img_big=pygame.transform.scale(img,(75,75))
	explosions_imgs["big1s"].append(img_big)
	img_small=pygame.transform.scale(img,(32,32))
	explosions_imgs["small1s"].append(img_small)
	nombre_archivo2="sonicExplosion0{}.png".format(i)
	img = pygame.image.load(path.join(image_folder,nombre_archivo2)).convert()
	img.set_colorkey(BLACK)
	explosions_imgs["player"].append(img)


meteor_list=["meteorBrown_big1.png","meteorBrown_big2.png","meteorBrown_big3.png","meteorBrown_big4.png",
			 "meteorBrown_med1.png","meteorBrown_med3.png","meteorBrown_small1.png","meteorBrown_small2.png",
			 "meteorBrown_tiny1.png","meteorBrown_tiny2.png"]
meteor_imgs=[]
fondo=pygame.image.load(path.join(image_folder,"background.png")).convert_alpha()
fondo_rect=fondo.get_rect()
bullet_img=pygame.image.load(path.join(image_folder,"laserRed01.png")).convert_alpha()
player_img=pygame.image.load(path.join(image_folder,"playerShip1_red.png")).convert_alpha()
player_lives=pygame.image.load(path.join(image_folder,"playerLife1_red.png")).convert_alpha()

for meteor in meteor_list:
	meteor_imgs.append(pygame.image.load(path.join(image_folder,meteor)).convert())

pow_images={}
pow_images["shield"]=pygame.image.load(path.join(image_folder,"shield_gold.png")).convert_alpha()
pow_images["gun"]=pygame.image.load(path.join(image_folder,"bolt_gold.png")).convert_alpha()
pow_images["extra_life"]=player_lives

#loading sounds
power_ups_snds={}
power_ups_snds["shield"]=pygame.mixer.Sound(path.join(sounds_folder,"Pow4.wav"))
power_ups_snds["gun"]=pygame.mixer.Sound(path.join(sounds_folder,"Pow5.wav"))
power_ups_snds["extra_life"]=pygame.mixer.Sound(path.join(sounds_folder,"Pow6.wav"))

shoot_snd=pygame.mixer.Sound(path.join(sounds_folder,"sfx_laser1.ogg"))
explosions=[]
player_dead_sound=pygame.mixer.Sound(path.join(sounds_folder,"rumble1.ogg"))

for i in range(1,11):
	sounds="Explosion{}.wav".format(i)
	snd =pygame.mixer.Sound(path.join(sounds_folder,sounds))
	snd.set_volume(1)
	explosions.append(snd)

pygame.mixer.music.load(path.join(sounds_folder,"music.ogg"))
pygame.mixer.music.set_volume(0.5)

#game loop local variables
pygame.display.set_caption("Sm'up!")
clock=pygame.time.Clock()
running=True
menu=True
game_over=False

control_variables = ["48","48","48","48","48"]
#B1,B2,Jx,Jy,Gx,Gy

#music init
pygame.mixer.music.play(-1)

arduino = None
try:
	arduino = serial.Serial('COM6',9600)
except:
	print("no control connected to the port")

#gameloop
while running==True:
	clock.tick(FPS)

	#gameStates
	if menu==True:
		menu=False
		show_menu("menu")
		all_sprites=pygame.sprite.Group()
		mobs=pygame.sprite.Group()
		powers=pygame.sprite.Group()
		bullets=pygame.sprite.Group()

		almost_dead=False
		score=0
		nextlvl=1000

		player=Player()
		all_sprites.add(player)

		#enemies - mobs spanw
		for i in range(0,16):
			new_mob()
		cant_mobs=16

	if game_over==True:
		game_over=False
		show_menu("over")
		all_sprites=pygame.sprite.Group()
		mobs=pygame.sprite.Group()
		powers=pygame.sprite.Group()
		bullets=pygame.sprite.Group()

		almost_dead=False
		score=0
		nextlvl=1000

		player=Player()
		all_sprites.add(player)

		#enemies - mobs spanw
		for i in range(0,16):
			new_mob()
		cant_mobs=16

	#events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running=False

	if arduino != None:
			data = arduino.readline()
			try:
				raw_string = (str(data[0])) + ',' + str(data[1]) + ',' + str(data[2]) + ',' + str(data[3]) + ',' + str(data[4])
			except:
				pass

			h = raw_string.split(',')
			control_variables = h
	else:
		control_variables = ["48","48","48","48","48"]


	#updates:

	#collision bullets mobs
	hits_bullets_mobs=pygame.sprite.groupcollide(mobs,bullets,True,True)


	for hit in hits_bullets_mobs:
		score+=60- hit.radius
		if random.random()>0.9:
			P = Pow(hit.rect.center)
			all_sprites.add(P)
			powers.add(P)


		explosion= Explosion(hit.rect.center,"big1s")
		all_sprites.add(explosion)
		random.choice(explosions).play()


	#collision player mobs
	hits_player_mobs=pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)

	for hit in hits_player_mobs:
		explosion= Explosion(hit.rect.center,"small1s")
		all_sprites.add(explosion)
		if player.untouchable==False:
			player.shield-=hit.radius * 2


			if player.shield<0:
				player_dead_sound.play()
				player_explo=Explosion(player.rect.center,"player")
				all_sprites.add(player_explo)
				player.hide()
				player.life-=1
				if player.life>0:
					player.shield=100

	if player.shield < 30:
		almost_dead=True
	if player.shield>30:
		almost_dead=False



	if player.life==0 and not player_explo.alive():
		game_over=True

	#evaluando si el player colisiona con un power-up

	hits_player_pow=pygame.sprite.spritecollide(player,powers,True)

	for hit in hits_player_pow:
		power_ups_snds[hit.type].play()
		if hit.type=="shield":
			player.shield+=random.randint(10,30)
			if player.shield >=100:
				player.shield=100

		if hit.type=="extra_life":
			if player.life <13:
				player.life+=1

		if hit.type=="gun":
			if player.double!=True:
				player.double=True
				player.clock_double=pygame.time.get_ticks()

	#evaluando la cantidad de mobs en la pantalla y creando nuevos si faltan
	while len(mobs) < cant_mobs:
		new_mob()

	# evaluando si el player subio de nivel
	if score > nextlvl:
		nextlvl*=2
		cant_mobs+=5


	#all update
	all_sprites.update()
	#drawing
	ventana.fill(BLACK)
	ventana.blit(fondo,fondo_rect)
	all_sprites.draw(ventana)
	draw_shield_bar(ventana,5,15,player.shield,almost_dead)
	draw_text(ventana,str(score),30,(ancho/2),10)
	draw_lives(ventana,player_lives,5,45,player.life)
	draw_buff(ventana,player.double,ancho-35,5)

	#buffering
	pygame.display.flip()


print ("score:" + str(score) )
print ("Nro de meteoritos presentes:" + str(cant_mobs))
if arduino != None:
	arduino.close()
