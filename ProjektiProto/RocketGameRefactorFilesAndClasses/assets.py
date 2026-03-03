"""Resurssien lataus ja yksinkertainen cache.
Tässä modulissa keskitetään kuvat, äänet ja muut resurssit.
Pidetään API pieni ja testattava: `load_assets(base_path)` palauttaa sanakirjan.
"""
import os


def load_assets(base_path: str) -> dict:
    """Lataa peliresurssit ja palauta sanakirja, josta muut modulit hakevat.

    - `base_path` on polku projektiin (yleensä dirname(__file__) tai vastaava)
    """
    assets = {}

    # TODO: Lisää varsinainen lataus myöhemmin. Pidä placeholder-arvot nyt.
    try:
        imgs_path = os.path.join(base_path, '..', 'images')
        assets['base_path'] = base_path
        assets['images_path'] = imgs_path
        assets['enemy_images'] = []  # täytetään myöhemmin
    except Exception:
        # Älä peitä virheitä lopullisessa versiossa; tässä palautetaan tyhjä sanakirja
        assets = {}

    return assets
