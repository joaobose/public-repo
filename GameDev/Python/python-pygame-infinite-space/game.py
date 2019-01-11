import pygame
from os import path
import math
vec = pygame.math.Vector2

pygame.init()

main_folder=path.dirname(__file__)
img_folder=path.join(main_folder,"pngs")

ancho,largo=1300,600
FPS=60

clock = pygame.time.Clock()
running=True
ventana=pygame.display.set_mode((ancho,largo))
all_sprites=pygame.sprite.Group()
bullets=pygame.sprite.Group()
fondos=pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#image and rect
		self.image_O=pygame.image.load(path.join(img_folder,"nave.png")).convert_alpha()
		#cabiando el tamano de la imagen original proporcionalmente al tamano de la ventana
		self.image_original=pygame.transform.scale(self.image_O,(int((ancho*7)/130),int((largo*26)/300)))
		self.image=self.image_original.copy()
		self.rect=self.image.get_rect()
		self.rect.center=(ancho/2,largo/2)
		#movimiento rotacional
		self.rot=0
		self.accR=0
		self.velR=0
		self.frccR=-0.03
		self.max_Rspeed=0
		self.mov_stateR=""
		#movimiento translacional
		self.acc=vec(0,0)
		self.vel=vec(0,0)
		self.frcc=-0.01
		self.pos=vec(self.rect.center)
		#shooting
		self.last_shoot=pygame.time.get_ticks()
		self.shoot_delay=150

	def update(self):

		self.__movement()

		self.__rotation()


		key_events2=pygame.key.get_pressed()

		if key_events2[pygame.K_SPACE]:
			self.__shoot()


	def __rotation(self):
		key_events=pygame.key.get_pressed()

		self.accR=0
		self.mov_stateR=""

		if key_events[pygame.K_a]:
			self.accR=0.25
			self.max_Rspeed=3
			self.mov_stateR="pos"

		if key_events[pygame.K_d]:
			self.accR=-0.25
			self.max_Rspeed=-3
			self.mov_stateR="neg"

		#tomando en cuenta a la friccion

		self.accR+=self.velR*self.frccR

		#modificando la velocidad en funcion de la aceleracion
		self.velR+=self.accR

		#verificando si la velocidad no es la maxima (ya sea en sentido positivo o negativo)
		#en caso de que si la sea, se mantendra en esa velocidad hasta que se deje de acelerar

		if (self.mov_stateR=="pos" and self.velR >=self.max_Rspeed) or (self.mov_stateR=="neg" and self.velR <=self.max_Rspeed):
			self.velR=self.max_Rspeed


		#calculando la rotacion tomando en cuenta la aceleracion (y por ende la friccion) y la velocidad angular
		self.rot+=(self.velR+(self.accR*1/2))


		#rotating process
		self.rot=self.rot%360

		old_pos=self.rect.center

		self.image=pygame.transform.rotate(self.image_original,self.rot)

		self.rect=self.image.get_rect()

		self.rect.center=old_pos


	def __movement(self):

		key_events=pygame.key.get_pressed()
		self.acc=vec(0,0)

		#aplicando el vector aceleracion en el angulo en el que se mueve la nave (siempre hacia delante y apuntando hacia el angulo de rotacion)
		if key_events[pygame.K_w]:
			self.acc=vec(-0.2*math.sin(math.radians(self.rot)),-0.2*math.cos(math.radians(self.rot)))


		#tomando en cuenta la friccion
		self.acc+=self.vel * self.frcc

		#acelerando la velocidad
		self.vel+=self.acc

		#limitando el movimento a que no se salga de la pantalla
		if (self.rect.centery <=0 and self.vel.y <0) or (self.rect.centery >=largo and self.vel.y >0) or(self.rect.centerx<=0 and self.vel.x <0) or(self.rect.centerx >=ancho and self.vel.x >0):
			self.vel=vec(0,0)

		else:

			#calculando posicion
			self.pos+=(self.vel + (self.acc*1/2))

			#moviendo el rectangulo segun el vector posicion
			self.rect.center=self.pos


	def __shoot(self):
		now = pygame.time.get_ticks()
		#disparando con delay (cada cierto tiempo)
		if now - self.last_shoot > self.shoot_delay:
			self.last_shoot=now
			m = Bullet(self.rect.centerx,self.rect.centery,self.rot)
			bullets.add(m)


class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y,rot):
		pygame.sprite.Sprite.__init__(self)
		#cambiando el tamano de la imagen proporcionalmente al tamano de la ventana
		self.image_original=pygame.transform.scale(pygame.image.load(path.join(img_folder,"laserBlue05.png")).convert_alpha(),(int((ancho*9)/1300),int((largo*37)/600)))
		#rotando la imagen del proyectil (en direccion al lanzamiento)
		self.image=pygame.transform.rotate(self.image_original,rot)
		self.rect=self.image.get_rect()
		self.rect.center=(x,y)
		#calculando la velocidad tomando en cuenta el angulo de lanzamiento
		self.vx=-15*(math.sin(math.radians(rot)))
		self.vy=-15*(math.cos(math.radians(rot)))

	def update(self):
		#moviendo el proyectil
		self.rect.move_ip(self.vx,self.vy)

		#si se sale de pantalla muere el sprite
		if self.rect.left > ancho or self.rect.right <0 or self.rect.bottom <0 or self.rect.top >largo:
			self.kill()

class Fondo(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=fondo
		self.rect=self.image.get_rect()
		self.rect.x,self.rect.y = x,y


player=Player()
all_sprites.add(player)

#graphics
fondo_original=pygame.image.load(path.join(img_folder,"background.png")).convert_alpha()

fondo= pygame.transform.scale(fondo_original,(ancho,largo))
fondo_rect = fondo.get_rect()

#creando diccionario para los fondos (para organizarlos mejor)
fondos_dics={"A":Fondo(0,0),"B":Fondo(0,largo-(2*fondo_rect.height)),"C":Fondo(ancho-(2*fondo_rect.width),0),"D":Fondo(ancho-(2*fondo_rect.width),largo-(2*fondo_rect.height))}

#agregando los fondos a su grupo de sprites
for fnd in fondos_dics:
	fondos.add(fondos_dics[fnd])


while running ==True:
	clock.tick(FPS)

	#inputs (eventos)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running=False

	#update
	all_sprites.update()
	bullets.update()


	#moviendo la camara

	#eje Y
	if player.pos.y>=largo*3/4:
		player.pos.y+=-player.vel.y

		for i in fondos:

			i.rect.y+=-int(player.vel.y)

	if player.pos.y<=largo*1/4:
		player.pos.y+=abs(player.vel.y)

		for i in fondos:

			i.rect.y+=abs(int(player.vel.y))


	#eje X
	if player.pos.x>=ancho*3/4:
		player.pos.x+=-player.vel.x

		for i in fondos:

			i.rect.x+=-int(player.vel.x)

	if player.pos.x<ancho*1/4:
		player.pos.x+=abs(player.vel.x)

		for i in fondos:

			i.rect.x+=abs(int(player.vel.x))



	#haciendo el fondo infinito (moviendo los fondos de manera que siempre esten corriendo en la pantalla)
	for x in ["A","B","C","D"]:
		if fondos_dics[x].rect.y>=largo:
			fondos_dics[x].rect.y=largo-(2*fondo_rect.height)

		if fondos_dics[x].rect.y<largo-(2*fondo_rect.height):
			fondos_dics[x].rect.y=largo

		if fondos_dics[x].rect.x>ancho:
			fondos_dics[x].rect.x=ancho-(2*fondo_rect.width)

		if fondos_dics[x].rect.x<ancho-(2*fondo_rect.width):
			fondos_dics[x].rect.x=ancho



	#draw
	ventana.fill((0,0,0))
	fondos.draw(ventana)
	bullets.draw(ventana)
	all_sprites.draw(ventana)


	pygame.display.flip()

pygame.quit()
