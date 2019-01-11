from os import path
import pygame as pg
vec = pg.math.Vector2

FPS = 125
NAME = "tILeZOmBIe"
MAX_FPS = 125 #fps en los que fue desarrollado el juego
#NOTA: el juego usa un sistema de proporciones entre los fps ingame y los fps en los que fue
#desarrollado el juego para ajustar proporcionalmente los efectos aplicados (fuerza...) de manera
#que sea cual sea el fps in game, el efecto ocasionado por el efecto aplicado (fuerza..) sea el mismo


TILE_SIZE = 64  # CANTIDAD DE PIXELES EN CADA SQUARE


ancho = (TILE_SIZE//2) * 32  #cantidad de cuadros de ancho
largo = (TILE_SIZE//2) * 21 #cantidad de cuadros de alto

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
GREY = (100,100,100)
DARKGREY = (40,40,40)
YELLOW = (255,255,0)

game_folder = path.dirname(__file__)
img_folder = path.join( game_folder , "pngs" )
snd_folder = path.join( game_folder , "snds" )
map_folder = path.join( game_folder , "maps" )
music_folder = path.join( game_folder , "music" )

ANCHO_DE_CUADRICULA = ancho / TILE_SIZE

LARGO_DE_CUADRICULA = largo / TILE_SIZE

#player settings
PLAYER_ACC = 2240  #maximum vel = acc / friction
PLAYER_FR = -8
PLAYER_ACC_ROT = 2000
PLAYER_FR_ROT = -8
PLAYER_HIT_BOX = pg.Rect(0,0,35,35)
PLAYER_HEALTH = 100
#player opacity bobbing
PLAYER_BOBBIN_OP_SPEED = 10
CRITICAL_CHANCE = 5/100

#WEAPONS SETTINGS
BULLET_IMG = "bullet.png"
CORDENADAS_DE_LANZAMIENTO = vec(18,10) #con respecto al centro del player

WEAPONS = {"pistol" : {"BULLET_SPEED" : 500,
					   "BULLET_LIFETIME" : 1000,
					   "SHOOTING_VEL" : 350,
					   "BULLET_COUNT" : 1,
					   "CULATAZO" : -3800, #FUERZA
					   "IMPACT" : -25000 ,#FUERZA
					   "SPREAD" : 5,
					   "DAMAGE" : 10,
					   "CHARGER_SIZE":10,
					   "INITIAL_BULLETS":100,
					   "RELOAD_TIME":1000},

		   "shotgun" : {"BULLET_SPEED" : 400,
					   "BULLET_LIFETIME" : 500,
					   "SHOOTING_VEL" : 1000,
					   "BULLET_COUNT" : 12,
					   "CULATAZO" : -3800*4, #FUERZA
					   "IMPACT" : -25000/4, #FUERZA
					   "SPREAD" : 20,
					   "DAMAGE" : 5,
					   "CHARGER_SIZE":6,
					   "INITIAL_BULLETS":12,
					   "RELOAD_TIME":2000},

		"machine_gun" : {"BULLET_SPEED" : 800,
					   "BULLET_LIFETIME" : 1000,
					   "SHOOTING_VEL" : 100,
					   "BULLET_COUNT" : 1,
					   "CULATAZO" : -3800/2,#FUERZA
					   "IMPACT" : -25000/2, #FUERZA
					   "SPREAD" : 5,
					   "DAMAGE" : 5,
					   "CHARGER_SIZE":30,
					   "INITIAL_BULLETS":80,
					   "RELOAD_TIME":800}
}


#layer settings
EFFECTS_LAYER = 4
BULLET_LAYER = 1
MOBS_LAYER = 2
PLAYER_LAYER = 2
ITEMS_LAYER = 1
WALLS_LAYER = 1
FONDO_LAYER = 0

#graphics
PLAYER_IMG = "manBlue_gun.png"
MOB_IMG = "zombie1_hold.png"

#mobs setting
MOB_ACCS = [1000, 1800, 1200, 1600, 900]
MOB_HEALTH = 100
MOB_FR = -10
MOB_KNOCKBACK = 18000  #fuerza
MOB_DAMAGE = 5
AVOID_RADIUS = 50
MOB_ATTACK_SPEED = 50

#visual effects settings
FLASHES_FILENAMES = ["WhitePuff15.png", "WhitePuff16.png", "WhitePuff17.png", "WhitePuff18.png"]
FLASH_STEP = 12.75 * MAX_FPS #per second
SPLAT = "splat green.png"
CORDENADAS_DE_FLASH = vec(30,10)
DAMAGE_ALPHA_VALUES = [i for i in range(0,255,125)]

#combat text settings
TEXT_RANGE = 60
TEXT_VEL = 150 #per second
OPACITY_VEL = 637.5 #per second
NORMAL_SIZE = 18
BIG_SIZE = 25
TEXT_HIT_BOX = pg.Rect(0,0,20,20)


#item settings
ITEM_FILENAMES = {"health" : "health_pack.png",
				  "shotgun" : "obj_shotgun.png",
				  "machine_gun" : "uzi_gun-512.png",
				  "pistol": "pistol.png",
				  "ammo" : "Ammo_Box.png"}

HEALTH_PACK_AMOUNT = 30
BOBBING_SPEED = 37.5 #per second
BOBBING_RANGE = 20.0

#items consumibles settings
ALL_CONSUM = ["Adrenaline","Spectral Flasck","Titan Aiming"]

CONSUM_IMG = {"Adrenaline" : "Adrenaline.png",
			   "Spectral Flasck" : "Spectral Flasck.png",
			   "Titan Aiming": "Titan Aiming.png"}

CONSUM_TIMES = {"Adrenaline" : 30000,
			   "Spectral Flasck" : 10000,
			   "Titan Aiming": 30000}

#sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']

ZOMBIE_ROAR_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']

ZOMBIE_HIT_SOUNDS = ['splat-15.wav']

WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav'],
                 'machine_gun' : ['sfx_weapon_singleshot2.wav']}

SOUND_EFFECTS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'pickup': 'gun_pickup.wav'}
