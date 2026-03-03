"""Pääsilmukan runko esimerkinomaisesti.
Käytä tätä mallina, kun siirrämme loogisia paloja alkuperäisestä `RocketGame.py`-tiedostosta.
"""
import pygame

from .assets import load_assets
from .game_state import init_game_state, reset_game
from .input_handler import handle_events
from .update import update_entities, handle_collisions
from .render import render_frame


def main():
    """Esimerkkirunko — ei pipelöi kaikkea automaattisesti.
    Suorita ja laajenna vaiheittain, älä yritä kerralla siirtää koko pelilogiikkaa.
    """
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    resources = load_assets('..')
    state = init_game_state(resources, world_rect=None)

    running = True
    clock = pygame.time.Clock()
    while running:
        dt = clock.tick(60)
        ev = handle_events()
        if ev.get('quit'):
            running = False
        if ev.get('pause'):
            # Näytä valikko tai käsittele pause
            pass

        update_entities(dt, state)
        handle_collisions(state)
        render_frame(screen, state, resources, 0, 0)
        pygame.display.flip()

if __name__ == '__main__':
    main()
