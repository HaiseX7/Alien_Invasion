# Python Modules
import sys
import pygame
from pygame.sprite import Sprite
from time import sleep
import json

# My Modules
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from music import Music


class AlienInvasion:
	"""Class to manage game assets and behavior."""

	def __init__(self):
		"""Initialize the game, and create game resources."""
		pygame.init()
		self.settings = Settings()

		# Initialize the screen
		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.screen_rect = self.screen.get_rect()
		pygame.display.set_caption("Alien Invasion")

		# Instance of game statistics
		self.stats = GameStats(self)

		# Instance of ship
		self.ship = Ship(self)

		# Groups
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		# Create the fleet of aliens
		self._create_fleet()

		# Make the Play Button
		self.w = self.settings.screen_width
		self.h = self.settings.screen_height
		self.play_button = Button(self, "Play", self.screen_rect.center)

		# Make the Easy, Normal, and Hard buttons
		self.play_easy = Button(self, "Easy", (self.w // 4, self.h // 2))
		self.play_normal = Button(self, "Normal", (self.screen_rect.center))
		self.play_hard = Button(self, "Hard", (self.w // (1 / (3/4)), self.h // 2))
		self.difficulty_selected = False

		# Make the scoreboard
		self.sb = Scoreboard(self)

		# Initiate the music
		self.music = Music()
		self.music.play_music()	

	def run_game(self):
		"""Starts the main loop for the game."""
		while True:
			# Watch for keboard and mouse events
			self._check_events()

			if self.stats.game_active:
				# Update Ships position
				self.ship.update()

				# Updates the bullets
				self._update_bullets()
				
				# Updates the aliens
				self._update_aliens()

			# Redraw the screen during each pass through the loop.
			self.update_screen()

	def _check_events(self):
		"""Respond to keypresses and mouse events."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.sb.write_high_score()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_keydown_events(self, event):
		"""Respond to keypresses."""
		if event.key == pygame.K_RIGHT:
			# Move the ship to the right.
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			# Move the ship to the left.
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			self.sb.write_high_score()
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_p and not self.stats.game_active:
			self._start_game()
		elif event.key == pygame.K_r and self.stats.game_active:
			self.stats.game_active = False
			self.difficulty_selected = False
			self.stats.reset_stats()
			pygame.mouse.set_visible(True)

	def _check_keyup_events(self, event):
		"""Respond to key releases."""
		if event.key == pygame.K_RIGHT:
			# Stops the ship
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			# Stops the ship
			self.ship.moving_left = False

	def _check_difficulty_selected(self, mouse_pos):
		self.check_difficulty_selected = [
			self.play_easy.rect.collidepoint(mouse_pos), 
			self.play_normal.rect.collidepoint(mouse_pos), 
			self.play_hard.rect.collidepoint(mouse_pos)
			]
		if any(self.check_difficulty_selected):
			self.music.button_click()
			self.difficulty_selected = True
			self._set_difficulty(self.check_difficulty_selected)
			return True
		else:
			self.difficulty_selected = False
			return False

	def _set_difficulty(self, difficulties):
		if difficulties[0]:
			self.settings.initialize_easy()
		elif difficulties[1]:
			self.settings.initialize_normal()
		else:
			self.settings.initialize_hard()

	def _draw_difficulties(self):
		self.play_easy.draw_button()
		self.play_normal.draw_button()
		self.play_hard.draw_button()

	def _check_play_button(self, mouse_pos):
		"""Starts a new game when the player clicks a difficulty and hits start."""
		if self._check_difficulty_selected(mouse_pos) and not self.stats.game_active:
			play_button_click = self.play_button.rect.collidepoint(mouse_pos)
			if play_button_click:
				# start game
				self.music.button_click()
				self._start_game()

	def _start_game(self):
		# Reset game statistics
		self.stats.reset_stats()
		self.sb.prep_score()
		self.stats.game_active = True

		# Get rid of any remaining aliens and bullets
		self.aliens.empty()
		self.bullets.empty()

		# Create a new fleet and center the ship 
		self._create_fleet()
		self.ship.center_ship()

		# Hide the mouse
		pygame.mouse.set_visible(False)

		# Show the scoreboard
		self.sb.prep_score()
		self.sb.prep_level()
		self.sb.prep_ships()

		# Define the dynamic settings
		self.settings.initialize_dynamic_settings()

	def _fire_bullet(self):
		"""Create a new bullet and add it to the bullets group."""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Update position of bullets and get rid of the old bullets."""
		# Updates bullet position
		self.bullets.update()

		# Get rid of bullets that're off the screen
		self._remove_bullet()

		self._check_bullet_alien_collisions()

	def _remove_bullet(self):
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

	def _check_bullet_alien_collisions(self):
		# Check for any bullets that have hit aliens.
		# If so, get rid of the bullet and the alien.
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()  
			self.sb.check_high_score()

		if not self.aliens:
			self._new_level()

	def _new_level(self):
		# Destroy existing bullets and create new fleet.
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			# Increase level
			self.stats.level += 1
			self.sb.prep_level()

	def _create_fleet(self):
		"""Create the fleet of aliens."""
		# Create the full fleet of aliens
		number_rows, number_aliens_x = self._alien_fleet_calculations()
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	def _alien_fleet_calculations(self):
		# Make an alien.
		# Find the number of aliens in a row and define their spacing
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		self.number_aliens_x = available_space_x // (2 * alien_width)

		# Determing the number of rows of aliens that fit on the screen.
		ship_height = self.ship.rect.height 
		available_space_y = (self.settings.screen_height - 0.45 * self.settings.screen_height)
		self.number_rows = int(available_space_y // (2 * alien_height))

		return (self.number_rows, self.number_aliens_x)

	def _create_alien(self, alien_number, row_number):
		"""Create an alien and place it in the row."""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = (alien_height * 2) + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _update_aliens(self):
		"""Update the positions of all aliens in the fleet."""
		self._check_fleet_edges()
		self.aliens.update()

		# Check for aliens hitting the ship
		self._check_ship_collision()

		# Look for aliens hitting the bottom of the screen
		self._check_aliens_bottom()

	def _check_fleet_edges(self):
		"""Respond appropriately if any aliens have reached an edge."""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleet's direction."""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _check_aliens_bottom(self):
		"""Check if any aliens have reached the bottom of the screen."""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# Treat this the same as if the ship got hit
				self._ship_hit()
				break

	def _check_ship_collision(self):
		# Look for alien-ship collisions.
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			print("Ship hit!!!")
			self._ship_hit()

	def _ship_hit(self):
		""" Respond to the ship being hit."""
		if self.stats.ships_left > 1:
			# Decrement ships left.
			self.stats.ships_left -= 1
			print(self.stats.ships_left)
			self.sb.prep_ships()

			# Get rid of any remaining aliens and bullets.
			self.aliens.empty()
			self.bullets.empty()

			# Create a new fleet and center the ship.
			self._create_fleet()
			self.ship.center_ship()

			# Pause.
			sleep(0.5)
		else:
			self.stats.game_active = False
			self.difficulty_selected = False
			pygame.mouse.set_visible(True)

	def update_screen(self):
		# Fill the screen with color
		self.screen.fill(self.settings.bg_color)

		# Draw the ship to the screen
		self.ship.blitme()

		# Draw the bullets
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()

		# Draw the alien
		self.aliens.draw(self.screen)

		# Draw the score information
		self.sb.show_score()

		# Draw the difficulties if one hasn't been selected and if the
		# game isn't active
		if (not self.stats.game_active) and (not self.difficulty_selected):
			self._draw_difficulties()

		# Draw the play button if the game is inactive and a difficulty 
		# has been selected
		if (not self.stats.game_active) and (self.difficulty_selected):
			self.play_button.draw_button()

		#Make the recently drawn screen visible.
		pygame.display.flip()


if __name__ == '__main__':
	# Make a game instance, and run the game.
	ai = AlienInvasion()
	ai.run_game()

