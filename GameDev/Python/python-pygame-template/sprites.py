import pygame as pg 
import random
from os import path 
from settings import *

class Sprite(pg.sprite.Sprite):
	def __init__(self,game):
		self.game = game
		self.layer = 0
		self.groups = self.game.all_sprites

		pg.sprite.Sprite.__init__(self,self.groups)

	def update(self):
		pass