import json
class GameStats:
	"""Track statistics for Alien Invasion."""

	def __init__(self, ai_game):
		"""Initialize statistics."""
		self.settings = ai_game.settings
		self.reset_stats()

		# Start Alien Invasion in an active state.
		self.game_active = False

		# High score should never be reset
		try: 
			filename = 'high_score.json'
			with open(filename) as f:
				self.high_score = json.load(f)
		except FileNotFoundError:
			self.high_score = 0

	def reset_stats(self):
		"""Initializes statistics that can change in game."""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1
