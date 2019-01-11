import pygame as pg
import math
import random
import pytweening as tweening
from os import path
from settings import *
import itertools

vec = pg.math.Vector2

def collide_double_hit_rect(one,other):
	return one.hit_box.colliderect(other.hit_box)

def collide_hit_rect(one,other):
	return one.hit_box.colliderect(other.rect)

def apply_force(force,entity):
	entity.external_forces += force

def collide_with_walls( sprite, dirc ,group):
	hits = pg.sprite.spritecollide(sprite,group,False,collide_hit_rect)
	if hits:
		if dirc == "x":
			if sprite.hit_box.centerx < hits[0].rect.centerx:
				sprite.pos.x = hits[0].rect.x - sprite.hit_box.width/2

			if sprite.hit_box.centerx > hits[0].rect.centerx:
				sprite.pos.x = hits[0].rect.right + sprite.hit_box.width/2
			sprite.vel.x = 0
			sprite.hit_box.centerx = sprite.pos.x

		if dirc == "y":
			if sprite.hit_box.centery < hits[0].rect.centery:
				sprite.pos.y = hits[0].rect.top - sprite.hit_box.height/2

			if sprite.hit_box.centery > hits[0].rect.centery:
				sprite.pos.y = hits[0].rect.bottom + sprite.hit_box.height/2
			sprite.vel.y = 0
			sprite.hit_box.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
	def __init__( self , game , x , y):
		self.game = game
		self._layer = PLAYER_LAYER
		self.groups = self.game.all_sprites

		pg.sprite.Sprite.__init__( self , self.groups )

		self.image = self.game.player_image
		self.rect = self.image.get_rect()
		self.hit_box = PLAYER_HIT_BOX
		self.x = x
		self.y = y
		self.rect.x,self.rect.y = self.x, self.y
		self.hit_box.center = self.rect.center
		self.pos = vec(self.rect.center)
		self.vel = vec(0,0)
		self.acc = vec(0,0)
		self.fr = PLAYER_FR
		self.health = PLAYER_HEALTH
		self.inmune = False
		#self.inmune_time = 2000

		self.rot_acc = 0
		self.rot_speed = 0
		self.rot_fr = PLAYER_FR_ROT
		self.rot = 0

		self.external_forces = vec(0,0)

		#bobbing opacity
		self.step = 0
		self.dir = 1
		self.easing_function = tweening.easeInOutSine
		self.opacity = 255

		#ammo and weapons
		self.weapon = "pistol"
		self.last_shoot = pg.time.get_ticks()
		self.weapon_inventory = [self.weapon]
		self.weapon_index = 0
		self.all_ammo = {"pistol" : WEAPONS["pistol"]["INITIAL_BULLETS"],
						"shotgun" : 0,
						"machine_gun" : 0}
		self.critical_chance = CRITICAL_CHANCE
		self.extra_bullet_impact = False


		self.charged_ammo = {"pistol" : WEAPONS["pistol"]["CHARGER_SIZE"],
							"shotgun" : 0,
							"machine_gun" : 0}

		self.reloading = False
		self.reload_time = 0

		#reloding bar animation
		self.easing_function = tweening.easeInOutSine

		#inventory and buffs
		self.inventory = {}
		self.inventory_index = 0
		self.selectable_items = []
		self.actual_item = ""

		self.buffs = {"Adrenaline" : 0,
			  		 "Spectral Flasck" : 0,
			  		 "Titan Aiming": 0}

		#damage effect
		self.damaged = False
		self.alpha_sequence = itertools.chain([0])


	def update(self):
		#self.inmune_tracking()
		self.movement()
		self.external_forces = vec(0,0)
		self.set_bobbing_opacity()
		self.inventory_manager()
		self.buff_manager()
		self.ammo_manager()

	def set_keys(self):
		self.acc = vec(0,0)
		self.rot_acc = 0
		keys = pg.key.get_pressed()

		if keys[pg.K_a]:
			self.rot_acc = PLAYER_ACC_ROT

		if keys[pg.K_d]:
			self.rot_acc = -PLAYER_ACC_ROT

		if keys[pg.K_w]:
			self.acc = vec(PLAYER_ACC,0).rotate(-self.rot)

		if keys[pg.K_s]:
			self.acc = vec(-PLAYER_ACC/2,0).rotate(-self.rot)

		if keys[pg.K_SPACE]:
			self.pull_trigger()

	def pull_trigger(self):
		now = pg.time.get_ticks()
		if (now - self.last_shoot > WEAPONS[self.weapon]["SHOOTING_VEL"]) and self.reloading == False:
			self.last_shoot = now

			#si tienes municion cargada en la arma actual
			if self.charged_ammo[self.weapon] > 0:
				self.shoot()
				self.charged_ammo[self.weapon] -= 1

			#si no
			else:
				#pero si tienes municion del arma actual en inventario
				if self.all_ammo[self.weapon] > 0:
					#entonces recargas
					self.reloading = True
					self.reload_time += WEAPONS[self.weapon]["RELOAD_TIME"]
					self.game.reloading_sound.play()

				#si no, no tienes balas, asi que no disparas
				else:
					#play no ammo sound
					snd = self.game.no_ammo_sound

					snd.play()


	def shoot(self):
		#spawn bullet
		pos = self.pos + CORDENADAS_DE_LANZAMIENTO.rotate(-self.rot)

		#por cada bala que dispare el arma
		for bullet in range(WEAPONS[self.weapon]["BULLET_COUNT"]):
			#calcula un angulo de spread (desviacion)
			spread = random.uniform(-WEAPONS[self.weapon]["SPREAD"],WEAPONS[self.weapon]["SPREAD"])
			#define la direcion para que apunte hacia donde mire el player (tomando en cuenta el spread)
			dir = vec(1,0).rotate(-self.rot + spread)
			#y spanwnea la bala
			Bullet(self.game,pos,dir,self.weapon)

		#spawn muzzle flash
		flash_pos = self.pos + CORDENADAS_DE_FLASH.rotate(-self.rot)
		Flash(self.game,flash_pos)

		#apply knockback force
		culatazo = vec((WEAPONS[self.weapon]["CULATAZO"] * self.game.fps / MAX_FPS),0).rotate(-self.rot)
		apply_force(culatazo,self)

		#sonido
		snd = random.choice(self.game.weapon_sounds[self.weapon])
		if snd.get_num_channels() > 2:
			snd.stop()
		snd.play()

	def movement(self):
		self.set_keys()

		#translational
		self.acc += self.external_forces

		self.acc += self.vel * self.fr

		self.pos += (self.vel * self.game.dt) + ((self.acc * (self.game.dt**2))/2)

		self.vel += self.acc * self.game.dt

		self.hit_box.centerx = self.pos.x

		collide_with_walls(self,"x",self.game.walls)

		self.hit_box.centery = self.pos.y

		collide_with_walls(self,"y",self.game.walls)

		#rotational

		self.rot_acc += self.rot_speed * self.rot_fr

		self.rot = (self.rot + (self.rot_speed * self.game.dt ) + ((self.rot_acc * (self.game.dt**2))/2)) % 360

		self.rot_speed += self.rot_acc * self.game.dt

		old_center = self.hit_box.center

		self.image = pg.transform.rotate(self.game.player_image,self.rot).convert_alpha()

		self.rect = self.image.get_rect()

		self.rect.center = old_center

	def set_bobbing_opacity(self):
		if self.inmune == True:
			offset = 255 * (self.easing_function(self.step/255) - 0.5)

			self.opacity = (255/2) + (offset * self.dir)

			self.step += PLAYER_BOBBIN_OP_SPEED * (MAX_FPS/self.game.fps)

			if self.step >= 255:
				self.step = 0
				self.dir *= -1

		else:
			self.step = 0
			self.dir = 1
			self.opacity = 255

	def inventory_manager(self):
		#seleccion de items
		if self.inventory_index >= len(self.selectable_items):
			self.inventory_index = 0

		if len(self.inventory) > 0:
			#definiendo el item actual
			self.actual_item = self.selectable_items[self.inventory_index]

			#limpiando el inventario de items vacios
			for_kill = []

			for item in self.inventory:
				if self.inventory[item] <= 0:
					for_kill.append(item)

			for empty_item in for_kill:
				del self.inventory[empty_item]
				self.selectable_items.remove(empty_item)

		else:
			self.actual_item = None


	def add_item(self,item):
		if item in self.inventory:
			self.inventory[item] += 1
		else:
			self.inventory[item] = 1
			self.selectable_items.append(item)


	def use_item(self,item):
		if item in self.inventory:
			self.inventory[item] -= 1
			self.buffs[item] = CONSUM_TIMES[item]


	def buff_manager(self):
		#por cada buff
		for buff in self.buffs:
			#le restamos el tiempo pasado
			self.buffs[buff] -= self.game.dt * 1000

			#si al buff todavia le queda tiempo activo
			if self.buffs[buff] > 0:
				#activas los efectos de los buffs
				if buff == "Adrenaline":
					self.critical_chance = 100/100

				if buff == "Spectral Flasck":
					self.inmune = True

				if buff == "Titan Aiming":
					self.extra_bullet_impact = True

			else:
				#si no, desactivas dichos efectos
				if buff == "Adrenaline":
					self.critical_chance = CRITICAL_CHANCE

				if buff == "Spectral Flasck":
					self.inmune = False

				if buff == "Titan Aiming":
					self.extra_bullet_impact = False

				self.buffs[buff] = 0



	def ammo_manager(self):
		#seleccion de armas
		if self.weapon_index >= len(self.weapon_inventory):
			self.weapon_index = 0

		self.weapon = self.weapon_inventory[self.weapon_index]

		#reloading manager
		if self.reloading:

			self.reload_time -= (self.game.dt*1000)

			#si estas a punto de terminar
			if self.reload_time <= 350:

				#entonces reproduces el sonido de "..."
				snd = self.game.reloaded_sound

				if snd.get_num_channels() < 1:
					snd.play()


			#si tu tiempo de recarga es cero
			if self.reload_time <= 0:
				#terminas de recargar
				self.reload_time = 0
				self.reloading = False

				#y recargas tu arma (municion)
				municion_disponible = self.all_ammo[self.weapon]

				if municion_disponible >= WEAPONS[self.weapon]["CHARGER_SIZE"]:

					self.charged_ammo[self.weapon] += WEAPONS[self.weapon]["CHARGER_SIZE"]
					self.all_ammo[self.weapon] -= WEAPONS[self.weapon]["CHARGER_SIZE"]

				else:
					self.charged_ammo[self.weapon] += municion_disponible
					self.all_ammo[self.weapon] -= municion_disponible


	def draw_reloading_bar(self):
		if self.reloading:
			ancho_barra = 50
			largo_barra = 5
			pos_x = self.pos.x - ancho_barra/2
			pos_y = self.pos.y - 25

			offset = ancho_barra * self.easing_function(self.reload_time/WEAPONS[self.weapon]["RELOAD_TIME"])

			ancho_fill = ancho_barra - offset

			fill_rect = pg.Rect(pos_x,pos_y,ancho_fill,largo_barra)
			fondo_rect = pg.Rect(pos_x,pos_y,ancho_barra,largo_barra)

			pg.draw.rect(self.game.ventana,GREY,self.game.camera.apply_rect(fill_rect))
			pg.draw.rect(self.game.ventana,DARKGREY,self.game.camera.apply_rect(fondo_rect),2)

	def add_health(self, amount):
		self.health += amount
		if self.health > PLAYER_HEALTH:
			self.health = PLAYER_HEALTH

	def damage_effect_on(self):
		if self.damaged != True:
			self.damaged = True
			self.alpha_sequence = itertools.chain(DAMAGE_ALPHA_VALUES * 2)


class Mob(pg.sprite.Sprite):
	def __init__( self , game , x , y ):
		self.game = game
		self._layer = MOBS_LAYER
		self.groups = self.game.all_sprites , self.game.mobs

		pg.sprite.Sprite.__init__(self,self.groups)

		self.image = self.game.mob_img.copy()
		self.rect = self.image.get_rect()
		self.rect.x,self.rect.y = x, y
		self.pos = vec(self.rect.center)
		self.rot = 0
		self.distance_player_mob = vec(0,0)
		#self.original_pos = vec(self.pos)
		#self.detect_radius = 400
		self.follow_player = False
		self.vel = vec(0,0)
		self.attack_range = 35
		self.hit_box = pg.Rect(0,0,40,40)
		self.hit_box.center = self.rect.center
		self.health = MOB_HEALTH
		self.max_health = MOB_HEALTH
		self.external_forces = vec(0,0)
		self.fr = MOB_FR
		self.acc = vec(0,0)
		self.acc_value = random.choice(MOB_ACCS)
		self.last_attack = 0

		self.drop_list = ["consumible"for x in range(0,2)] + ["ammo" for x in range(0,4)] + ["health"]

	def __same_room_as_player(self):
		hits_with_rooms = pg.sprite.spritecollide(self,self.game.rooms,False)

		if hits_with_rooms:
			actual_room = hits_with_rooms[0]
		else:
			actual_room = None

		if actual_room == self.game.visible_area.actual_room:
			return True

	def __collide_with_visible_game_area(self):
		#si el mob esta dentro del area visible retorna True
		if self.rect.colliderect(self.game.visible_area.rect):
			return True

	def update(self):
		#define el estado de movimiento del mob
		self.__set_movement_state()

		#si mob esta persiguiendo al player
		if self.follow_player == True:
			#iddle sound effect
			if random.random() < 0.002:
				random.choice(self.game.zombie_roar_sound).play()

			#ecuaciones de cinematica del mob
			self.__kinematics()

			#rotacion del mob (imagen) para que apunte al player
			self.__rotate_img()

			#killing the mob and spawning splat (on map image)
			if self.health <= 0:
				self.kill()
				self.game.zombie_splat_sound.play()
				self.game.map_image.blit(self.game.splat_image,self.pos - (32,32))
				if random.random() < 0.8:
					Item(self.game,self.pos,random.choice(self.drop_list))

	def __set_movement_state(self):
		self.acc = vec(0,0)
		self.distance_player_mob = vec(self.game.player.pos - self.pos)

		#si el mob esta en la area visible y en el mismo cuarto que el player o esta herido, entonces sigue al player
		if self.follow_player == False:
			if ((self.__collide_with_visible_game_area() and self.__same_room_as_player()) or self.health < MOB_HEALTH):
				self.follow_player = True

		#si el mob esta siguiendo al player
		if self.follow_player == True:
			#el angulo de rotacion es el angulo con el eje x del vector distance_player_mob
			self.rot = self.distance_player_mob.angle_to(vec(1,0))

			#si el mob no ha llegado a su rango de ataque se mueve hacia el player (aplica aceleracion)
			if self.distance_player_mob.length_squared() > self.attack_range**2:
				self.acc = vec(1,0).rotate(-self.rot)
			else:
				#si no, no se mueve
				self.acc = vec(0,0)


	def __kinematics(self):
		if self.follow_player == True:

			#evita a los demas mobs (los esquiva)
			self.__avoid_mobs()

			#multiplica el vector acc (resultante de avoid mobs(), es decir un vector unitario) con el valor de la aceleracion (modulo)
			self.acc *= self.acc_value

			#suma la fuerzas externas
			self.acc += self.external_forces

			#toma en cuenta la friccion
			self.acc += self.vel * self.fr

			#cinematica
			self.pos += (self.vel * self.game.dt) + ((self.acc * (self.game.dt**2))/2)

			self.vel += self.acc * self.game.dt

			#coloca al hit_box en la posicion virtual del mob y detecta colisiones con los obstaculos en ambos ejes (por separado)
			self.hit_box.centerx = self.pos.x

			collide_with_walls(self,"x",self.game.walls)

			self.hit_box.centery = self.pos.y

			collide_with_walls(self,"y",self.game.walls)

			#al finalizar coloca la fuerzas externas en cero
			self.external_forces = vec(0,0)

	def __avoid_mobs(self):
		#por cada mob
		for mob in self.game.mobs:
			#si el mob no es el actual
			if mob != self:
				#calcula la distancia desde el mob iterado al actual
				distance = vec(self.pos - mob.pos)
				#si el mob iterado esta dentro del rango de deteccion
				if 0 < distance.length_squared() < AVOID_RADIUS**2:
					#entonces el vector acc del mob actual cambia de direccion (se le suma el vector distancia normalizado)
					self.acc += distance.normalize()

	def __rotate_img(self):
		if self.rot != 0:
			self.image = pg.transform.rotate(self.game.mob_img,self.rot).convert_alpha()

			self.rect = self.image.get_rect()

			self.rect.center = self.pos

	def attack(self):
		now = pg.time.get_ticks()
		if now - self.last_attack > MOB_ATTACK_SPEED:
			self.last_attack = now

			#segun su velocidad de ataque, el mob cada cierto tiempo ataca al player
			if self.game.player.inmune == False:
				self.game.player.health -= MOB_DAMAGE

		#cada vez que lo toque (aun asi no le haga daño) le aplica una fuerza al player (empuje o knockback)
		knockback = vec((MOB_KNOCKBACK * self.game.fps / MAX_FPS),0).rotate(-self.rot)
		apply_force(knockback,self.game.player)

	def draw_health(self):
		if self.health < 0:
			self.health = 0

		pct = self.health * 100/self.max_health
		width = int(pct * self.rect.width/100)

		color = (255,255,0)

		r = 255/(MOB_HEALTH/2)

		if self.health > 50:
			c = (self.health * r) - (MOB_HEALTH/2 * r)
			red = 255 - c
			color = (red,255,0)
		elif self.health < 50:
			c = self.health * r
			color = (255,c,0)

		outline = pg.Rect(0,0,self.rect.width,7)
		health_bar = pg.Rect(0,0,width,7)

		if self.health < self.max_health:
			pg.draw.rect(self.image,color,health_bar)
			pg.draw.rect(self.image,GREY,outline,2)


class Bullet(pg.sprite.Sprite):
	def __init__(self , game , pos , dir, weapon):
		self.game = game
		self._layer = BULLET_LAYER
		self.groups = game.all_sprites , game.bullets

		pg.sprite.Sprite.__init__(self,self.groups)

		self.image = game.bullet_img.copy()
		self.image = pg.transform.scale(self.image,(9,9))
		self.weapon = weapon

		self.rect = self.image.get_rect()
		self.pos = vec(pos)
		self.rect.center = self.pos

		self.vel = dir * (WEAPONS[self.weapon]["BULLET_SPEED"] * random.uniform(0.6, 1.1))

		self.impact_force = WEAPONS[self.weapon]["IMPACT"]
		self.impact_force += WEAPONS[self.weapon]["IMPACT"] * (int(self.game.player.extra_bullet_impact) * 2)


		self.spanw_time = pg.time.get_ticks()

		self.critical_strike = 0

		if random.random() <= self.game.player.critical_chance:
			self.critical_strike = WEAPONS[self.weapon]["DAMAGE"] * 2

		self.damage = WEAPONS[self.weapon]["DAMAGE"] + self.critical_strike

	def update(self):
		self.pos += self.vel * self.game.dt
		self.rect.center = self.pos

		now = pg.time.get_ticks()
		if now - self.spanw_time > WEAPONS[self.weapon]["BULLET_LIFETIME"]:
			self.kill()

		if pg.sprite.spritecollideany(self,self.game.walls):
			self.kill()


class Wall(pg.sprite.Sprite):
	def __init__( self , game , x , y ):
		self.game = game
		self._layer = WALLS_LAYER
		self.groups = self.game.all_sprites , self.game.walls

		pg.sprite.Sprite.__init__(self,self.groups)

		self.image = self.game.base_tile_img
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TILE_SIZE
		self.rect.y = y * TILE_SIZE

class Obstacle(pg.sprite.Sprite):
	def __init__( self , game , x , y , width , height):
		self.game = game
		self._layer = WALLS_LAYER
		self.groups = self.game.walls

		pg.sprite.Sprite.__init__(self,self.groups)

		self.rect = pg.Rect(x,y,width,height)

class Flash(pg.sprite.Sprite):
	def __init__(self, game, pos):
		self.game = game
		self.groups = game.all_sprites
		self._layer = EFFECTS_LAYER

		pg.sprite.Sprite.__init__(self,self.groups)

		size = random.randint(20,40)
		self.image = pg.transform.scale(random.choice(self.game.gun_flashes),(size,size))
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.spanw_time = pg.time.get_ticks()
		self.opacity = 255

	def update(self):
		self.opacity -= FLASH_STEP * self.game.dt

		if self.opacity <= 0:
			self.kill()

class Item(pg.sprite.Sprite):
	def __init__(self, game, pos, typex):
		self.game = game
		self._layer = ITEMS_LAYER
		self.groups = game.all_sprites, game.items

		pg.sprite.Sprite.__init__(self,self.groups)

		if typex == "consumible":
			self.consum_type = random.choice(ALL_CONSUM)
			self.image = self.game.consum_img[self.consum_type]

		else:
			self.image = self.game.items_img[typex]

		if typex == "machine_gun":
			self.image = pg.transform.scale(self.game.items_img[typex],(32,32))

		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.pos = vec(pos)
		self.type = typex

		self.easing_function = tweening.easeInOutSine
		self.step = 0.0
		self.dir = 1

	def update(self):

		offset = BOBBING_RANGE * (self.easing_function(self.step/BOBBING_RANGE)- 0.5)

		self.rect.centery = (offset * self.dir) + self.pos.y

		self.step += BOBBING_SPEED * self.game.dt

		if self.step >= BOBBING_RANGE:
			self.step = 0
			self.dir *= -1

class CombatText(pg.sprite.Sprite):
	def __init__(self, game, target, int_text, text, color, size):
		self.game = game
		self.groups = game.all_sprites, game.texts
		self._layer = EFFECTS_LAYER

		pg.sprite.Sprite.__init__(self,self.groups)

		#self.font_name = font_name
		self.size = size
		self.color = color
		self.target = target
		self.text = text

		#self.font = pg.font.Font(self.font_name,self.size)
		self.font = self.game.combat_font_dic[self.size]
		self.image = self.font.render(int_text + text,True,color)
		self.rect = self.image.get_rect()
		self.hit_box = TEXT_HIT_BOX.copy()
		self.hit_box.center = self.target.pos
		self.rect.center = self.hit_box.center

		try:
			self.int_amount = int(int_text)
		except:
			self.int_amount = int_text


		self.easing_function = tweening.easeInOutSine
		self.trans_step = 0

		self.opacity = 255
		self.opacity_step = 255

	def re_render_data(self):
		self.font = self.game.combat_font_dic[self.size]
		self.image = self.font.render(str(self.int_amount) + self.text,True,self.color)
		self.rect = self.image.get_rect()

	def update(self):
		#translational easing animation
		offset = TEXT_RANGE * self.easing_function(self.trans_step/TEXT_RANGE)


		self.hit_box.centery = self.target.pos.y - offset
		self.hit_box.centerx = self.target.pos.x
		self.rect.center = self.hit_box.center

		self.trans_step += TEXT_VEL * self.game.dt

		if self.trans_step > TEXT_RANGE:
			self.trans_step = 0

		#opacity easing animation
		offset = 255 * self.easing_function(self.opacity_step/255)

		self.opacity = offset

		self.opacity_step -= OPACITY_VEL * self.game.dt

		if self.opacity_step < 0:
			self.opacity_step = 255
			self.kill()
