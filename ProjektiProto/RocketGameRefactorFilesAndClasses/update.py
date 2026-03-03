"""Päivityslogiikka: entiteettien ja fysiikan päivitys.
Tämä tiedosto tarjoaa pieniä apufunktioita `main`-silmukkaa varten.
"""

def update_entities(dt, state: dict):
    """Päivitä kaikki entiteetit (pelaaja, viholliset, luodit).
    dt on millisekunteina.
    """
    for e in list(state.get('enemies', [])):
        try:
            e.update(dt, state.get('player'), state.get('world_rect'))
        except Exception:
            # Poista virheellinen entiteetti mieluummin kuin peitä virhe
            try:
                state['enemies'].remove(e)
            except Exception:
                pass


def handle_collisions(state: dict):
    """Yksinkertainen kollisiosilmukka; vain paikka varataan tässä.
    Tarkempi logiikka siirretään myöhemmin moduuliin `collisions.py`.
    """
    # TODO: siirrä ja laajenna
    return
