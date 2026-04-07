import pygame

from States.GameState import GameState
from Valikot.MainMenu import MainMenu
from SaveGame import SaveGameManager


class MainMenuState(GameState):

    def __init__(self, manager=None):
        super().__init__(manager)
        self.menu = MainMenu()

    def update(self, events):

        action = self.menu.handle_events(events)

        if action == "continue":
            try:
                from States.PlayState import PlayState
                from Tasot.LevelManager import LevelManager
                
                # Lataa tallennettu peli
                save_data = SaveGameManager.load_game()
                if save_data:
                    level_number = save_data["level_number"]
                    wave_number = save_data["wave_number"]
                    total_score = save_data["total_score"]
                    player_health = save_data["player_health"]
                    player_ammo_type1 = save_data["player_ammo_type1"]
                    player_ammo_type2 = save_data["player_ammo_type2"]
                    
                    # Luo level manager aloittaen tallennetusta levelista
                    level_manager = LevelManager(self.manager.screen, level_numbers=[level_number])
                    
                    # Aseta pelaajan tila
                    game_instance = level_manager.current_level
                    if game_instance.player:
                        game_instance.player.health = player_health
                        # Aseta ammo jos pelaajalla on weapons-objekti
                        if hasattr(game_instance.player, 'weapons'):
                            if hasattr(game_instance.player.weapons, 'ammo_type1'):
                                game_instance.player.weapons.ammo_type1 = player_ammo_type1
                            if hasattr(game_instance.player.weapons, 'ammo_type2'):
                                game_instance.player.weapons.ammo_type2 = player_ammo_type2
                    
                    # Aseta pisteet: tallennettu kokonaisscore asetetaan suoraan
                    if hasattr(game_instance, "pistejarjestelma"):
                        game_instance.pistejarjestelma.pisteet = total_score
                    level_manager.total_score = 0  # Resetoidaan total_score koska nykyisen tason pisteet ovat jo total_score:ssa
                    
                    # Aseta aalto ja spawnaa se
                    game_instance.current_wave = int(wave_number)
                    game_instance.spawn_wave(int(wave_number))
                    
                    self.manager.set_state(PlayState(self.manager, level_manager=level_manager))
            except Exception as exc:
                print(f"Virhe pelin jatkamisessa: {exc}")

        elif action == "start":
            try:
                from States.PlayState import PlayState
                self.manager.set_state(PlayState(self.manager))
            except Exception as exc:
                # Keep the menu active if gameplay state is not yet wired.
                print(f"Could not start PlayState: {exc}")

        elif action == "settings":
            try:
                from Valikot.SettingsMenu import main as settings_menu_main
                from States.PlayState import PlayState
                from Tasot.LevelManager import LevelManager

                settings_action = settings_menu_main()
                current_surface = pygame.display.get_surface()
                if current_surface is not None:
                    self.manager.screen = current_surface
                if settings_action == "start_test_level":
                    test_level_manager = LevelManager(self.manager.screen, level_numbers=[0])
                    self.manager.set_state(PlayState(self.manager, level_manager=test_level_manager))
                elif settings_action == "start_test2_level":
                    test_level_manager = LevelManager(self.manager.screen, level_numbers=[6])
                    self.manager.set_state(PlayState(self.manager, level_manager=test_level_manager))
            except Exception as exc:
                print(f"Could not open settings menu: {exc}")

        elif action == "quit":
            self.manager.running = False

    def draw(self, screen):
        self.menu.draw(screen)