from os import path
import pygame
pygame.init()

game_folder=  path.dirname(__file__)
image_folder = path.join(game_folder,"pngs")
sounds_folder = path.join(game_folder,"sounds")
font_name = pygame.font.match_font("times new")
