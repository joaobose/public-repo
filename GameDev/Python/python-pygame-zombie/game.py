import pygame as pg
import random
from os import path
from settings import *
from sprites import *
from tilemap import *
vec = pg.math.Vector2

#HUD functions
def draw_player_health(surface, x, y, health):
	if health < 0:
		health = 0

	pct = health * 100 / PLAYER_HEALTH

	r = 255/(PLAYER_HEALTH/2)

	if health > 50:
		c = (health * r) - (PLAYER_HEALTH/2 * r)
		red = 255 - c
		color = (red,255,0)
	elif health <= 50:
		c = health * r
		color = (255,c,0)



	ancho_barra = 100
	largo_barra = 10

	fill = pct * ancho_barra / 100

	outline = pg.Rect(x,y,ancho_barra,largo_barra)
	fill_rect = pg.Rect(x,y,fill,largo_barra)

	pg.draw.rect(surface,color,fill_rect)
	pg.draw.rect(surface,GREY,outline,2)

#used to show weapons and inventory
def draw_item_inventory_bar(game,surf,items,actual_item,x,y,imgs,selection_img,show_amount=False):
	distance = 40
	posx = x - distance
	posy = y

	if len(items) > 0:
		for item in items:
			posx += distance

			#create a teporal surface to blit all the elements in
			temp_surf = pg.Surface((64,64))

			#set the image
			image = imgs[item]

			#if the image is bigger than the usual, then it will be scaled
			if image.get_width() > 40 or image.get_height() > 40:
				image = pg.transform.scale(image,(32,32))

			#set image coordinates inside the temp surf (centered)
			image_rect = image.get_rect()
			image_rect.center = (32,32)

			#set the selection image coordinates inside the temp surf (centered)
			selection_img_rect = selection_img.get_rect()
			selection_img_rect.center = (32,32)

			#blit the map (backgruond) on the temp surf
			temp_surf.blit(surf,(-posx,-posy))

			#if the item is the selected item (actual item), then blit the selection image on the temp surf (before the item img)
			if item == actual_item:
				temp_surf.blit(selection_img,selection_img_rect)

			#blit the image on the temp surf
			temp_surf.blit(image,image_rect)

			#if show_amount its set, entonces:
			if show_amount == True:
				try:
					#intenta dibujar el texto para mostrar cantidad de items disponibles
					draw_text(temp_surf,str(items[item]),game.title_font_dic[12],40,40,WHITE)

				except:
					#si no puede (ya que el objeto items, puede ser una lista), no lo dibuja
					pass

			#blit the temp surf on the screen
			surf.blit(temp_surf,(posx,posy))

def draw_bullets(surf,player,font,x,y,bullet_img):
	surf.blit(bullet_img,(x - TILE_SIZE,y - TILE_SIZE/4))
	draw_text(surf," - " + str(player.all_ammo[player.weapon])+"/"+str(player.charged_ammo[player.weapon]),font,x,y,WHITE)

def draw_buffs(game,x,y):
	distance = 50
	posx = x
	posy = y - distance

	for buff in game.player.buffs:
		if game.player.buffs[buff] > 0:
			posy += distance

			temp_surf = pg.Surface((TILE_SIZE,TILE_SIZE))

			temp_surf.blit(game.ventana,(-posx,-posy))

			image = game.consum_img[buff]
			rect = image.get_rect()

			rect.center = (TILE_SIZE/2,TILE_SIZE/2)

			temp_surf.blit(image,rect)

			draw_text(temp_surf,str(int(game.player.buffs[buff]/1000)),game.title_font_dic[15],40,40,WHITE)

			game.ventana.blit(temp_surf,(posx,posy))

def blit_with_opacity(screen, image, position_rect, opacity):
	temp = pg.Surface((image.get_width(),
					   image.get_height())).convert()

	temp.blit(screen,(-position_rect.x,-position_rect.y))
	temp.blit(image,(0,0))
	temp.set_alpha(opacity)
	screen.blit(temp,(position_rect.x,position_rect.y))

def draw_text(surf,text,font_object,x,y,color):
	text_surf = font_object.render(text,True,color)
	text_rect = text_surf.get_rect()
	text_rect.center = (x,y)
	surf.blit(text_surf,text_rect)


class Game():
	def __init__(self):
		pg.mixer.pre_init(44100, -16, 4, 1024)
		pg.init()
		pg.mixer.init()
		self.ventana = pg.display.set_mode(( ancho , largo ))
		pg.display.set_caption( NAME )
		pg.key.set_repeat( 500 , 100 )
		self.Clock = pg.time.Clock()
		self.running = True
		self.load_data()

	def load_data(self):
		self.lvl_name = "map1.tmx"
		self.map = TiledMap(path.join(map_folder, self.lvl_name))

		self.player_image = pg.image.load(path.join(img_folder,PLAYER_IMG)).convert_alpha()
		self.base_tile_img = pg.image.load(path.join(img_folder,"tileGreen_39.png")).convert_alpha()
		self.base_tile_img = pg.transform.scale(self.base_tile_img,(TILE_SIZE,TILE_SIZE)).convert_alpha()
		self.mob_img = pg.image.load(path.join(img_folder,MOB_IMG)).convert_alpha()
		self.bullet_img = pg.image.load(path.join(img_folder,BULLET_IMG)).convert_alpha()
		self.splat_image = pg.image.load(path.join(img_folder,SPLAT)).convert_alpha()
		self.splat_image = pg.transform.scale(self.splat_image,(64,64))
		self.gun_flashes = []
		self.items_img = {}
		self.consum_img ={}

		for img in FLASHES_FILENAMES:
			self.gun_flashes.append(pg.image.load(path.join(img_folder,img)).convert_alpha())

		for img in ITEM_FILENAMES:
			self.items_img[img] = pg.image.load(path.join(img_folder,ITEM_FILENAMES[img])).convert_alpha()

		for img in CONSUM_IMG:
			self.consum_img[img] = pg.image.load(path.join(img_folder,CONSUM_IMG[img])).convert_alpha()


		self.black_alpha_surf = pg.Surface((self.ventana.get_size())).convert_alpha()
		self.black_alpha_surf.fill((0,0,0,180))

		self.selection_img = pg.image.load(path.join(img_folder,"light_350_soft.png")).convert_alpha()
		self.selection_img = pg.transform.scale(self.selection_img,(64,64))

		self.bullet_icon = pg.image.load(path.join(img_folder,"bullet_icon.png")).convert_alpha()

		#sounds
		pg.mixer.music.load(path.join(music_folder,BG_MUSIC))

		self.player_pain_sounds = []

		for x in range(9,14):
			s = pg.mixer.Sound(path.join(snd_folder,"pain/{}.wav".format(x)))
			s.set_volume(1)
			self.player_pain_sounds.append(s)

		self.sound_effects = {}

		for type in SOUND_EFFECTS:
			sound = pg.mixer.Sound((path.join(snd_folder,SOUND_EFFECTS[type])))
			sound.set_volume(0.6)
			self.sound_effects[type] = sound

		self.zombie_splat_sound = pg.mixer.Sound(path.join(snd_folder,ZOMBIE_HIT_SOUNDS[0]))
		self.zombie_splat_sound.set_volume(0.3)

		self.weapon_sounds = {}

		for type in WEAPON_SOUNDS:
			self.weapon_sounds[type] = []
			for index in range(len(WEAPON_SOUNDS[type])):
				s = pg.mixer.Sound(path.join(snd_folder,WEAPON_SOUNDS[type][index]))
				s.set_volume(0.2)
				self.weapon_sounds[type].append(s)

		self.zombie_roar_sound = []

		for snd in ZOMBIE_ROAR_SOUNDS:
			s = pg.mixer.Sound(path.join(snd_folder,snd))

			s.set_volume(0.1)
			self.zombie_roar_sound.append(s)

		self.reloading_sound = pg.mixer.Sound(path.join(snd_folder,"reloading.wav"))

		self.reloaded_sound = pg.mixer.Sound(path.join(snd_folder,"reloaded.wav"))

		self.no_ammo_sound = pg.mixer.Sound(path.join(snd_folder,"no_ammo.wav"))

		#fonts
		combat_font_name = path.join(img_folder,"ZOMBIE.TTF")
		self.combat_font_dic = {}
		#all sizes for "combat" font
		for key in ["NORMAL_SIZE","BIG_SIZE"]:
			if key == "NORMAL_SIZE":
				self.combat_font_dic[key] = pg.font.Font(combat_font_name,NORMAL_SIZE)
			else:
				self.combat_font_dic[key] = pg.font.Font(combat_font_name,BIG_SIZE)


		title_font_name = path.join(img_folder,"Impacted2.0.ttf")
		self.title_font_dic = {}
		#all sizes for "title" font
		for key in [12,15,20,30,60,100]:
			self.title_font_dic[key] = pg.font.Font(title_font_name,key)



	def new(self):
		#inicia un nuevo juego
		self.playing = True
		self.paused = False
		self.all_sprites = pg.sprite.LayeredUpdates()
		self.walls = pg.sprite.Group()
		self.mobs = pg.sprite.Group()
		self.items = pg.sprite.Group()
		self.bullets = pg.sprite.Group()
		self.camera_obstacles = pg.sprite.Group()
		self.rooms = pg.sprite.Group()
		self.texts = pg.sprite.Group()

		self.map_image = self.map.make_map_surface()
		self.map_rect = self.map_image.get_rect()

		self.all_mobs_data = []


		#charging old map
		#for pos_y , fila in enumerate(self.map.data):
		#	for pos_x , columna in enumerate(fila):
		#		if columna == "1":
		#			Wall(self, pos_x, pos_y)
		#		if columna == "p":
		#			self.player = Player(self, pos_x, pos_y)
		#		if columna == "m":
		#			Mob(self,pos_x,pos_y)

		for tile_object in self.map.tiled_data.objects:
			object_center = vec(tile_object.x + (tile_object.width/2),
								tile_object.y + (tile_object.height/2))

			if tile_object.name == "player":
				self.player = Player(self,object_center.x,object_center.y)

			if tile_object.name == "wall":
				Obstacle(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height)

			if tile_object.name == "zombie":
				data = vec(object_center.x,object_center.y)
				self.all_mobs_data.append(data)
				Mob(self,object_center.x,object_center.y)

			if tile_object.name == "camera_obstacle":
				CameraObstacle(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height)

			if tile_object.name == "room":
				Room(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height)

			if tile_object.name in ["health","shotgun","machine_gun","ammo","consumible"]:
				Item(self,(object_center.x,object_center.y),tile_object.name)

		self.see_invisible_colliders = False

		self.camera = Camera(self.map.ancho_pixels,self.map.largo_pixels)

		self.visible_area = VisibleArea(self)


	def run(self):
		#game loop
		self.sound_effects["level_start"].play()
		pg.mixer.music.play(-1)
		while self.playing:
			self.dt = self.Clock.tick(FPS) / 1000
			self.fps = self.Clock.get_fps()
			self.events()
			if not self.paused:
				self.update()
			self.drawing()

	def events(self):
		#game loop events
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.playing = False
				self.running = False
			if event.type == pg.KEYDOWN:

				if event.key == pg.K_m:
					self.see_invisible_colliders = not self.see_invisible_colliders


				if event.key == pg.K_k:
					for mob in self.mobs:
						mob.kill()
					print("all mobs killed")


				if event.key == pg.K_u:
					self.player.inmune = not self.player.inmune
					print("player inmunity set to: " + str(self.player.inmune))


				if event.key == pg.K_ESCAPE:
					self.paused = not self.paused


				if event.key == pg.K_f:
					if self.player.reloading == False:
						self.player.weapon_index += 1


				if event.key == pg.K_c:
					self.player.inventory_index += 1


				if event.key == pg.K_e:
					self.player.use_item(self.player.actual_item)


				if event.key == pg.K_l:
					if len(self.mobs) == 0:
						for mob_data in self.all_mobs_data:
							Mob(self,mob_data.x,mob_data.y)

						print("all mobs respawned")

	def update(self):
		#game loop update
		self.all_sprites.update()
		self.visible_area.update()
		self.camera.update(self.visible_area)

		if len(self.mobs) == 0:
			#self.playing = False
			pass

		#hits player mob
		hits = pg.sprite.spritecollide(self.player,self.mobs,False,collide_hit_rect)
		for hit in hits:
			#aplicando efecto visual de daño
			self.player.damage_effect_on()

			#el mob ataca
			hit.attack()

			if random.random() < 0.3:
				if self.player.inmune == False:
					random.choice(self.player_pain_sounds).play()

			if self.player.health < 0:
				self.playing = False

		#hits bullets mobs
		hits = pg.sprite.groupcollide(self.mobs,self.bullets,False,True,collide_hit_rect)

		#por cada mob
		for hit in hits:
			total_dmg = 0
			crit_strike = False

			#por cada bala que golpeo al mob
			for bullet in hits[hit]:
				#danando a la salud del mob
				hit.health -= bullet.damage
				total_dmg += bullet.damage

				#detectando si fue critico
				if bullet.critical_strike != 0:
					crit_strike = True

				#aplicando fuerza de impacto
				impact_force = vec((bullet.impact_force * self.fps / MAX_FPS),0).rotate(-hit.rot)
				apply_force(impact_force,hit)

			#spawning text
			if crit_strike == True:
				CombatText(self,hit,str(int(total_dmg))," CRITICAL",(155,0,0),"BIG_SIZE")
			else:
				CombatText(self,hit,str(int(total_dmg)),"",WHITE,"NORMAL_SIZE")

		#hits player items
		hits = pg.sprite.spritecollide(self.player,self.items,False)

		for hit in hits:
			if hit.type == "health" and self.player.health < PLAYER_HEALTH:
				hit.kill()
				self.sound_effects["health_up"].play()
				self.player.add_health(HEALTH_PACK_AMOUNT)

			if hit.type in ["shotgun","machine_gun"]:
				if hit.type not in self.player.weapon_inventory:
					self.player.weapon_inventory.append(hit.type)
					self.player.all_ammo[hit.type] = WEAPONS[hit.type]["INITIAL_BULLETS"]
					self.player.charged_ammo[hit.type] = WEAPONS[hit.type]["CHARGER_SIZE"]
					self.sound_effects["pickup"].play()
					hit.kill()

			if hit.type == "ammo":
				#agrega al inventario de municion mas balas (a un arma aleatoria del inventario)
				random_ammo = random.choice(self.player.weapon_inventory)
				self.player.all_ammo[random_ammo] += (WEAPONS[random_ammo]["CHARGER_SIZE"] * 2)
				self.sound_effects["pickup"].play()
				hit.kill()

				#spawning informative text
				CombatText(self,self.player,"","ADDED " + str((WEAPONS[random_ammo]["CHARGER_SIZE"] * 2)) + " " + random_ammo ,
						   (20,20,20),"BIG_SIZE")

			if hit.type == "consumible":
				self.player.add_item(hit.consum_type)
				self.sound_effects["pickup"].play()
				hit.kill()


		#combat text visual optimization (para evitar que los textos se sobre pongan (se monten uno arriba del otro haciendo que no se lean))
		hits = pg.sprite.groupcollide(self.texts,self.texts,False,False,collide_double_hit_rect)

		if hits:
			#si existe un choque entre textos de combate (solapamiento)

			#escojes cualquiera de los textos
			combat_text = self.choose_any(hits)
			#una vez seleccionado el texto
			for hit in hits[combat_text]:#se itera por los textos que chocan con el
				if combat_text != hit and (combat_text.target == hit.target):#se verifica si pertenecen al mismo target
					#si al menos uno de los elementos considerados (combat text y hit)es critico:
					if combat_text.text == " CRITICAL" or hit.text == " CRITICAL":
						combat_text.text = " CRITICAL"
						combat_text.color = (155,0,0)
						combat_text.size = "BIG_SIZE"
						#entonces se modifica el texto inicial (combat text) para que sea critico (visualmente)

					#se suma la cantidad de daño total entre el texto original y el iterado
					total_amount = combat_text.int_amount + hit.int_amount

					#y editas la data del texto original (combat text)
					combat_text.int_amount = total_amount
					combat_text.re_render_data()

					#finalmente destruyes el texto (hit) iterado
					hit.kill()

	#escoje una key aleatoria en un dic
	def choose_any(self,dic_obj):
		keys = []
		for key in dic_obj:
			keys.append(key)

		return random.choice(keys)

	def draw_grid(self):
		for x in range(0,ancho,TILE_SIZE):
			pg.draw.line(self.ventana,GREY,(x , 0),(x , largo))

		for y in range(0,largo,TILE_SIZE):
			pg.draw.line(self.ventana,GREY,(0 , y),(ancho , y))

	def drawing(self):
		#game loop draw
		pg.display.set_caption("{:.0f}".format(self.Clock.get_fps()))
		self.ventana.blit(self.map_image,self.camera.apply_rect(self.map_rect))
		#self.draw_grid() #dibuja la cudricula
		#self.layered_drawing()
		self.draw_sprites()
		#pg.draw.rect(self.ventana,WHITE,self.camera.apply_rect(self.player.hit_box),2)
		#pg.draw.rect(self.ventana,RED,self.camera.apply_rect(self.player.rect),2)
		#self.draw_mobs_detect_area()
		self.draw_invisible_colliders()

		#hud drawing
		self.player.draw_reloading_bar()
		draw_text(self.ventana,"ZOMBIES: {}".format(len(self.mobs)),self.title_font_dic[30], ancho - 100, 10, WHITE)
		draw_player_health(self.ventana,10,10,self.player.health)
		draw_item_inventory_bar(self,self.ventana,self.player.weapon_inventory,self.player.weapon,2,15,self.items_img,self.selection_img)
		draw_item_inventory_bar(self,self.ventana,self.player.inventory,self.player.actual_item,2,90,self.consum_img,self.selection_img,True)
		draw_bullets(self.ventana,self.player,self.title_font_dic[20],70,80,self.bullet_icon)
		draw_buffs(self,2,170)


		if self.paused:
			self.ventana.blit(self.black_alpha_surf,(0,0))
			draw_text(self.ventana,'pause',self.title_font_dic[100],ancho/2,largo/2,(155,0,0))


		pg.display.flip()

	def draw_invisible_colliders(self):
		if self.see_invisible_colliders == True:
			for wall in self.walls:
				pg.draw.rect(self.ventana,RED,self.camera.apply_rect(wall.rect),2)
			for sprite in self.all_sprites:
				if isinstance(sprite,Mob) or isinstance(sprite,Player):
					pg.draw.rect(self.ventana,RED,self.camera.apply_rect(sprite.hit_box),2)

	def draw_sprites(self):
		for sprite in self.all_sprites:
			if isinstance(sprite,Player):
				#efecto visual para el daño hacia el player (tiene que ver con la funcion damage_effect_on)
				if sprite.damaged:
					try:
						sprite.image.fill((255,50,0,next(sprite.alpha_sequence)),special_flags=pg.BLEND_RGBA_MULT)
					except:
						sprite.damaged = False


			if isinstance(sprite,Mob):
				sprite.draw_health()

			if (isinstance(sprite,Flash)) or (isinstance(sprite,Player) and self.player.inmune == True) or \
				(isinstance(sprite,CombatText)):

				blit_with_opacity(self.ventana,sprite.image,self.camera.apply(sprite),sprite.opacity)

			else:
				self.ventana.blit(sprite.image,self.camera.apply(sprite))

	def layered_drawing(self):
		layers = {0:[] , 1:[], 2:[] , 3:[] , 4:[] , 5:[] , 6:[] , 7:[] , 8:[] , 9:[] , 10:[]}

		for sprite in self.all_sprites:
			for key in layers:
				if sprite.layer == key:
					layers[key].append(sprite)

		layer_order = []
		for key in layers:
			layer_order += layers[key]

		for sprite in layer_order:
			if isinstance(sprite,Mob):
				sprite.draw_health()

			if (isinstance(sprite,Flash)) or (isinstance(sprite,Player) and self.player.inmune == True) or \
				(isinstance(sprite,CombatText)):

				blit_with_opacity(self.ventana,sprite.image,self.camera.apply(sprite),sprite.opacity)

			else:
				self.ventana.blit(sprite.image,self.camera.apply(sprite))

	def draw_mobs_detect_area(self):
		for mob in self.mobs:
			pg.draw.circle(self.ventana,RED,self.camera.apply_rect(mob.rect).center,mob.detect_radius,2)

	def draw_new_game_screen(self):
		#draw the new game screen
		self.ventana.fill(BLACK)
		draw_text(self.ventana,'TILED ZOMBIE',self.title_font_dic[100],ancho/2,largo/2,(155,0,0))
		draw_text(self.ventana,'press any key to start',self.title_font_dic[60],ancho/2,largo * 3/4,(155,0,0))

		pg.display.flip()

		self.wait_for_key()

	def draw_game_over_screen(self):
		#draw the game over screen

		if self.player.health <= 0:
			string = "GAME OVER"

		else:
			string = "LEVEL COMPLETE"

		self.ventana.fill(BLACK)
		draw_text(self.ventana,string,self.title_font_dic[100],ancho/2,largo/2,(155,0,0))
		draw_text(self.ventana,'press any key to start again',self.title_font_dic[60],ancho/2,largo * 3/4,(155,0,0))

		pg.display.flip()

		self.wait_for_key()

	def wait_for_key(self):
		pg.event.wait()
		waiting = True
		while waiting:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.playing = False
					self.running = False
					waiting = False
				if event.type == pg.KEYUP:
					waiting = False

game = Game()
game.draw_new_game_screen()
while game.running:
	game.new()
	game.run()
	if game.running:
		game.draw_game_over_screen()

pg.quit()
