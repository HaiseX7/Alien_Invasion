import pygame
class Settings:
	"""A class to store all settings for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's static settings."""
		# Screen settings
		display = pygame.display.Info()
		self.screen_width = display.current_w
		self.screen_height = display.current_h
		self.bg_color = (230, 230, 230)

		# Ship settings
		self.ship_limit = 3

		# Bullet settings
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 3

		# Alien settings
		self.fleet_drop_speed = 10

		# How quickly the game speeds up
		self.speedup_scale = 1.15

		# Initialize dynamic settings
		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initializes the game's dynamic settings."""
		self.ship_speed = 1.0
		self.bullet_speed = 1.0
		self.alien_speed = 0.5

		# Scoring
		self.alien_points = 50

		# How quickly the alien point value increases
		self.score_scale = 1.5

		# fleet direction of 1 represents right, -1 represents left.
		self.fleet_direction = 1

	def increase_speed(self):
		"""Increase speed settings and alien point values"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)

