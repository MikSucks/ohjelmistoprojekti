"""Piirtotoiminnot.
Sisältää yksinkertaisen `render_frame`-funktion, joka kutsuu entiteettien `draw`-metodeja.
"""

def render_frame(screen, state: dict, resources: dict, camera_x: int, camera_y: int):
    # Piirrä kaikki pelikomponentit tässä järjestyksessä
    # 1) tausta (resurssit voivat sisältää sen)
    # 2) planeetat / koristeet
    # 3) viholliset
    # 4) pelaaja
    # 5) UI
    try:
        for e in state.get('enemies', []):
            try:
                e.draw(screen, camera_x, camera_y)
            except Exception:
                pass
    except Exception:
        pass
