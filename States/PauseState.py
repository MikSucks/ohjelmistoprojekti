from States.GameState import GameState
from Valikot.PauseMenu import PauseMenu
from SaveGame import SaveGameManager


class PauseState(GameState):

	def __init__(self, manager, previous_state, background_surface=None):
		super().__init__(manager)
		self.previous_state = previous_state
		self.background_surface = background_surface
		self.pause_menu = PauseMenu(screen=manager.screen)

	def update(self, events):
		action = self.pause_menu.handle_events_from(events)
		result = self.pause_menu.resolve_action(action)

		if result == "continue":
			self.manager.set_state(self.previous_state)
			return

		if result == "save_quit":
			# Tallenna peli
			level_manager = getattr(self.manager, "level_manager", None)
			if level_manager and self.previous_state:
				# Lataa GameState (PlayState) että pääsee Game-instanssiin
				if hasattr(self.previous_state, 'level_manager'):
					game_instance = level_manager.current_level
					
					# Kerää pelaajan tila
					current_level_num = level_manager.get_current_level_number()
					wave_num = getattr(game_instance, 'current_wave', 1)
					
					# Pisteet: nykyisen tason pisteet + level_managerin kertyneet pisteet
					current_level_score = 0
					if game_instance.pistejarjestelma:
						current_level_score = getattr(game_instance.pistejarjestelma, 'pisteet', 0)
					total_score = level_manager.total_score + current_level_score
					
					# Pelaajan health
					player_health = 3
					if game_instance.player:
						player_health = getattr(game_instance.player, 'health', 3)
					
					# Pelaajan ammo
					ammo_type1 = 100
					ammo_type2 = 50
					if game_instance.player and hasattr(game_instance.player, 'weapons'):
						ammo_type1 = getattr(game_instance.player.weapons, 'ammo_type1', 100)
						ammo_type2 = getattr(game_instance.player.weapons, 'ammo_type2', 50)
					
					# Pelaajan nimi
					player_name = "Player"
					try:
						with open('player_name.txt', 'r') as f:
							player_name = f.read().strip()
					except:
						pass
					
					SaveGameManager.save_game(
						current_level_num, 
						wave_num, 
						total_score, 
						player_health,
						ammo_type1,
						ammo_type2,
						player_name
					)
			
			# Palaa päävalikkoon
			from States.MainMenuState import MainMenuState
			self.manager.set_state(MainMenuState(self.manager))
			return

		if result == "quit":
			self.manager.running = False
			return

	def draw(self, screen):
		if self.background_surface is None and self.previous_state is not None:
			self.previous_state.draw(screen)
		self.pause_menu.draw(self.background_surface)
