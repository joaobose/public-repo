from os import path
import json

with open(path.join(path.dirname(__file__),"settings.txt"),"r+") as f:
    data = ""
    for line in f:
        data += line
    settings = json.loads(data)

TILESIZE = settings["tilesize"]

width,height = settings["width"], settings["height"]
FPS = settings["maxFPS"]
NAME = "GameOfLife"

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
GREY=(155,155,155)
MEDGREY=(80,80,80)
DARKGREY=(20,20,20)

CAMERA_VEL = settings["camera_vel"]
LIFEGRID_DELAY = settings["lifeGrid_delay"]

#keyvalues definitions for vectors
X = 0
Y = 1

IMAGE = 0
RECT = 1
