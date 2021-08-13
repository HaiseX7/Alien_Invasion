import pygame
import sys
from settings import Settings

class GameOverScreen:
	"""A class for the starting screen of the game."""
	def __init__(self, ai_game):
		# print(pygame.font.get_fonts())
		self.ai_game = ai_game

		self.settings = ai_game.settings

		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		self.title_font = pygame.font.SysFont('Futura', 120)
		self.title = self.title_font.render('Game Over', True, 
			(0, 0, 0), self.settings.bg_color)
		self.title_rect = self.title.get_rect()

		self.title_rect.center = self.screen_rect.center

		self.instructions_font = pygame.font.SysFont(None, 25)
		self.instructions = self.instructions_font.render('Press any key to return to home screen', 
			True, (0, 0, 0), self.settings.bg_color)
		self.instructions_rect = self.instructions.get_rect()

		self.instructions_rect.center = self.screen_rect.center
		self.instructions_rect.y += 200

		self.game_over = False

	def game_over_screen(self):
		while self.game_over:
			self.screen.fill(self.settings.bg_color)
			self.screen.blit(self.title, self.title_rect)
			self.screen.blit(self.instructions, self.instructions_rect)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						sys.exit()
					else:
						print("key")
						self.game_over = False
						self.ai_game.start_screen.finished = False
