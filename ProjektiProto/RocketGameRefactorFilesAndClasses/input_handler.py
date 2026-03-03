"""Yksinkertainen tapahtumankäsittely funktio.
Tämä moduuli pitää `handle_events` pienenä ja puhtaan testaamisen mahdollistavana.
"""
import pygame


def handle_events():
    """Käsittele pygame-tapahtumat ja palauta tila.

    Palauttaa sanakirjan esim. {'quit': bool, 'pause': bool}
    """
    state = {'quit': False, 'pause': False}
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state['quit'] = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                state['pause'] = True
    return state
