from os import path
import pygame as pg
pg.init()
ancho,largo=480,600
FPS=60
NAME="Jumpy!"

FONT_NAME=pg.font.match_font("times new")

HIGH_SCORE_FILE_NAME= "HS.txt"

SPRITESHEET_NAME="spritesheet_jumper.png"

game_folder=path.dirname(__file__)
img_folder=path.join(game_folder,"pngs")
snd_folder=path.join(game_folder,"snds")

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
GREY=(155,155,155)
LIGHTBLUE=(0,180,210)
BG_COLOR=LIGHTBLUE

#gameplay settings
BOOST_SIZE=70
POWER_UP_PROBABILITY=7
WALKER_PROBABILITY=2
BROKEN_PLAT_PBT=4

PLATS_TYPE_PROBABILITY=["grass" for i in range(0,5)]+["mud"]


#layer settings
PLAYER_LAYER=3
MOBS_LAYER=2
PLAT_LAYER=1
POWER_UP_LAYER=1
NUBE_LAYERS=0


#initial platforms
PLAT_LIST= [(0,largo-60),
			(ancho/2-50,largo*3/4,False,"grass",True,True),
			(100,250),
			((ancho/2)+50,100),
			(ancho-120,175)]

#player settings
player_acel=0.5
player_grass_friction=-0.12
player_mud_friction=-0.48

#map settings
gravity=0.8

def set_dificulty(game,lvl,flyman_spanw,walker_controler,broken_plat_controler=None):

	if lvl!=0:

		if lvl % 5 == 0:
			if game.walker_controler < 120:
				game.walker_controler +=2

		elif lvl % 2 == 0:
			if game.broken_plat_controler < 100:
				game.broken_plat_controler +=1

		elif lvl % 3 == 0:
			if game.flyman_spanw>-9000:
				game.flyman_spanw-=1000

			


