"""Pieni UI-moduuli (HUD ja muut käyttöliittymäapufunktiot).
"""

def init_enemy_health_bars(base_path: str = None):
    """Alusta vihollisen health-bar -kuvat.
    Palauttaa listan kuva-olioista tai None, jos ei ole ladattu.
    """
    return []


def draw_hud(screen, state: dict, resources: dict):
    """Piirtää yksinkertaisen HUD:n (pisteet, elämät).
    Tämä on paikka, josta myöhemmin tuodaan paremmat esitykset.
    """
    try:
        lives = state.get('lives', 3)
        # Piirrä tekstiä, kuvia yms. (käytetään myöhemmin)
    except Exception:
        pass
