"""Pelitilan alustukset ja reset-logiikka.
Tämä moduuli pitää pelitilan rakenteen yksinkertaisena ja testattavana.
"""
from typing import Dict


def init_game_state(resources: dict, world_rect) -> Dict:
    """Luo ja palauta pelitila-sanakirja.

    Rakenne on yksinkertainen dict: {
      'player': obj, 'enemies': [], 'bullets': [], 'score': 0, ...
    }
    """
    state = {
        'player': None,
        'enemies': [],
        'enemy_bullets': [],
        'muzzles': [],
        'score': 0,
        'lives': 3,
        'world_rect': world_rect,
    }
    return state


def reset_game(state: dict, resources: dict) -> None:
    """Nollaa pelitilan perusasetukset (kutsutaan esim. play again).

    Tämä funktio käyttää `enemies.spawn_wave` myöhemmin kun integroimme moduulit.
    """
    state['enemies'].clear()
    state['enemy_bullets'].clear()
    state['muzzles'].clear()
    state['score'] = 0
    state['lives'] = 3
    # spawn_wave voidaan kutsua ulkopuolelta

