import pygame as pg
import random
from os import path
from settings import *

class Room():
	def __init__(self,game,x,y,width,height,color = GREY):
		self.hit_rect = pg.Rect(x - 1,y - 1,width + 2,height + 2)
		self.rect = pg.Rect(x,y,width,height)
		self.allowed_connections = ["up","down","left","right"]
		self.color = color

	def draw(self,surface):
		pg.draw.rect(surface,self.color,self.rect)

class Corridor():
	def __init__(self,game,x,y,width,height,color = GREY):
		self.rect = pg.Rect(x,y,width,height)
		self.color = color

	def draw(self,surface):
		pg.draw.rect(surface,self.color,self.rect)
