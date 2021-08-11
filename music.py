import pygame
import pygame.mixer

class Music:
	"""A class to play music while running the game."""

	def __init__(self):
		pygame.mixer.init()

	def play_music(self):
		pygame.mixer.Channel(0).play(pygame.mixer.Sound('alien_invasion.mp3'), -1)

	def button_click(self):
		pygame.mixer.Channel(1).play(pygame.mixer.Sound('menu_ok.wav'))