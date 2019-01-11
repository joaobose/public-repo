import pygame as pg
import pytmx
from settings import *
from sprites import *


def collide_with_camera_obstacles( sprite, group):
	hits = pg.sprite.spritecollide(sprite,group,False,collide_hit_rect)
	for hit in hits:
		if hit.collide_orientation == "x":
			if sprite.hit_box.centerx < hit.rect.centerx:
				sprite.pos.x = hit.rect.x - sprite.hit_box.width/2

			if sprite.hit_box.centerx > hit.rect.centerx:
				sprite.pos.x = hit.rect.right + sprite.hit_box.width/2
			sprite.vel.x = 0
			sprite.hit_box.centerx = sprite.pos.x

		if hit.collide_orientation == "y":
			if sprite.hit_box.centery < hit.rect.centery:
				sprite.pos.y = hit.rect.top - sprite.hit_box.height/2

			if sprite.hit_box.centery > hit.rect.centery:
				sprite.pos.y = hit.rect.bottom + sprite.hit_box.height/2
			sprite.vel.y = 0
			sprite.hit_box.centery = sprite.pos.y

class Map():
	def __init__(self,filename):
		self.data=[]

		with open(path.join(game_folder,filename)) as f:
			for line in f:
				self.data.append(line.strip())

		self.ancho_tiles = len(self.data[0])
		self.largo_tiles = len(self.data)

		self.ancho_pixels = self.ancho_tiles * TILE_SIZE
		self.largo_pixels = self.largo_tiles * TILE_SIZE

class TiledMap():
	def __init__(self, filename):
		self.tiled_data = pytmx.load_pygame(filename,pixelalpha=True)

		self.ancho_pixels = self.tiled_data.width * self.tiled_data.tilewidth
		self.largo_pixels = self.tiled_data.height * self.tiled_data.tileheight

	def render(self, surface):
		get_tile_image = self.tiled_data.get_tile_image_by_gid

		for layer in self.tiled_data.visible_layers:
			if isinstance(layer,pytmx.TiledTileLayer):#si el layer es de tipo tilelayer entonces...
				for x, y, gid, in layer:#obtiene las coordenadas y la id de cada tile en el layer
					imagen_del_tile = get_tile_image(gid)#define la imagen del tile
					if imagen_del_tile:#si el tile contiene una imagen
						surface.blit(imagen_del_tile,((x * self.tiled_data.tilewidth),
													  (y * self.tiled_data.tileheight)))#entonces dibuja el tile en la superficie

	def make_map_surface(self):
		map_surface = pg.Surface((self.ancho_pixels,self.largo_pixels))
		self.render(map_surface)
		return map_surface

class Camera():
	def __init__( self, ancho_mapa , largo_mapa ):
		self.off_set_rect = pg.Rect(0,0,ancho_mapa,largo_mapa)
		self.ancho_mapa = ancho_mapa
		self.largo_mapa = largo_mapa

	def apply( self, entidad ):
		return entidad.rect.move(self.off_set_rect.x , self.off_set_rect.y)

	def apply_rect( self , rect):
		return rect.move(self.off_set_rect.x , self.off_set_rect.y)

	def apply_scrolling_parallax(self, entidad, coeficent):

		return entidad.rect.move(self.off_set_rect.x/coeficent,self.off_set_rect.y/coeficent)


	def update( self, target ):
		offset_x = -(target.rect.centerx) + int(ancho/2)
		offset_y = -(target.rect.centery) + int(largo/2)

		#limites del scrolling de la camara
		offset_x = min(0, offset_x)#left
		offset_y = min(0, offset_y)#top
		offset_x = max(-(self.ancho_mapa-ancho),offset_x)#right
		offset_y = max(-(self.largo_mapa-largo),offset_y)#bottom

		self.off_set_rect = pg.Rect(offset_x,offset_y,self.ancho_mapa,self.largo_mapa)


class VisibleArea(pg.sprite.Sprite):#sprite que representa el area visible de la camera
	def __init__( self , game ):
		self.game = game

		pg.sprite.Sprite.__init__(self)

		self.rect = pg.Rect(0,0,ancho,largo)
		self.pos = vec(self.rect.center)
		self.vel = vec(0,0)
		self.hit_box = self.rect.copy()
		self.player = self.game.player
		self.actual_room = None
		self.in_room = False

	def collide_player_with_rooms(self):
		hits = pg.sprite.spritecollide(self.player,self.game.rooms,False,collide_hit_rect)

		if hits:
			self.actual_room = hits[0]
			self.in_room = True

		else:
			self.actual_room = None
			self.in_room = False


	def update(self):
		self.pos = vec(self.player.pos)

		self.hit_box.center = self.pos

		self.collide_player_with_rooms()

		if self.in_room == True:

			if self.actual_room.rect.width < self.rect.width:
			#si el ancho del cuarto es mas pequeno que el ancho de la area visible (pantalla)
			#entonces la posicion del area visible en x es el centro del cuarto actual
				self.pos.x = self.actual_room.rect.centerx
				self.hit_box.centerx = self.pos.x

			if self.actual_room.rect.height < self.rect.height:#si el largo del cuarto es mas pequeno que el largo de la area visible (pantalla)
			#entonces la posicion del area visible en y es el centro del cuarto actual
				self.pos.y = self.actual_room.rect.centery
				self.hit_box.centery = self.pos.y

			#si esta en un cuarto, detecta colisiones con los camera obstacles (paredes del cuarto)
			collide_with_camera_obstacles(self,self.game.camera_obstacles)


		self.rect.center = self.hit_box.center

class CameraObstacle(pg.sprite.Sprite):
	def __init__( self , game , x , y , width , height):
		self.game = game
		self.groups = self.game.camera_obstacles

		pg.sprite.Sprite.__init__(self,self.groups)

		self.rect = pg.Rect(x,y,width,height)

		self.collide_orientation = ""

		if width < height:
			self.collide_orientation = "x"#solo detecta colisiones en el eje x

		else:
			self.collide_orientation = "y"#solo detecta colisiones en el eje y

class Room(pg.sprite.Sprite):
	def __init__( self , game , x , y , width , height):
		self.game = game
		self.groups = self.game.rooms

		pg.sprite.Sprite.__init__(self,self.groups)

		self.rect = pg.Rect(x,y,width,height)
