"""Taso 2 wave-rakenne RocketGame.Game:lle.

Sisältää wave 1-4 vihollisaallot ja boss-wave (wave 4).
Voit muokata tätä omilta enemy-kombinaatioilta.
"""

import pygame
import random

def spawn_wave_taso2(
	game,
	wave_num,
	apply_hitbox,
	hitbox_enemy,
	hitbox_boss,
	straight_enemy_cls,
	circle_enemy_cls,
	boss_enemy_cls,
	down_enemy_cls,
	up_enemy_cls,
):
	"""Spawn Level 2 enemies for the requested wave.

	Returns:
		bool: True if wave was handled by this level module, else False.
	"""
	# TODO: Implement Level 2 unique enemy compositions
