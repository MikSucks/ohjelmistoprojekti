import os
import pygame


class SpriteSettings:
    """Apuluokka vihollisspritesien lataukseen ja ryhmittelyyn.

    Tämän luokan tarkoitus on tarjota helppo tapa ladata ja pitää järjestyksessä
    vihollisten (alusten) kehykset, pakokaasu-animaatiot ja luotikehykset.
    Luokka ei käynnistä `pygame`-kirjastoa automaattisesti; `pygame.init()` tulee
    kutsua ennen `load_all()`-metodin käyttöä.
    """

    def __init__(self, base_path: str = 'enemy-sprite', ship: str = 'Ship2'):
        self.base = base_path
        self.ship = ship

        self.ship_frames: list[pygame.Surface] = []
        self.exhaust_turbo: list[pygame.Surface] = []
        self.exhaust_normal: list[pygame.Surface] = []
        self.shot_frames: list[pygame.Surface] = []

        # call load when pygame is ready (pygame.init() must be called first)
        # We do not auto-initialize pygame here to keep this module pure.

    def _load_images_from(self, path: str) -> list:
        """Palauttaa listan `pygame.Surface`-olioita polusta.

        Jos `path` on tiedosto, palautetaan yhden kuvan lista. Jos se on kansio,
        palautetaan kaikki kansiossa olevat .png-tiedostot (lajiteltuna).
        Paluuarvo on tyhjä lista jos polku ei ole olemassa tai kuvia ei voida ladata.
        """
        if not os.path.exists(path):
            return []

        if os.path.isfile(path):
            try:
                return [pygame.image.load(path).convert_alpha()]
            except Exception:
                return []

        # Jos annettu polku on kansio, etsi sen .png-tiedostot
        images = []
        for dirpath, _, files in os.walk(path):
            pngs = sorted(f for f in files if f.lower().endswith('.png'))
            for f in pngs:
                full = os.path.join(dirpath, f)
                try:
                    images.append(pygame.image.load(full).convert_alpha())
                except Exception:
                    continue
        return images

    def load_all(self):
        """Lataa kaikki yleisesti tarvittavat sprite-resurssit.

        Metodi yrittää ladata seuraavia ryhmiä suhteessa `self.base`-polkuun:
        - aluksen kehykset (ship frames)
        - pakokaasu/afterburner -kehykset (turbo/normal)
        - luotien kehykset (start/flight/explode)

        Palauttaa sanakirjan, joka sisältää listoja ladatuista kuvista.
        """
        ship_folder = os.path.join(self.base, 'PNG_Parts&Spriter_Animation', self.ship, self.ship)
        self.ship_frames = self._load_images_from(ship_folder)

        turbo_folder = os.path.join(self.base, 'PNG_Parts&Spriter_Animation', self.ship, 'Exhaust', 'Turbo_flight', 'Exhaust1')
        self.exhaust_turbo = self._load_images_from(turbo_folder)

        normal_folder = os.path.join(self.base, 'PNG_Parts&Spriter_Animation', self.ship, 'Exhaust', 'Normal_flight', 'Exhaust1')
        self.exhaust_normal = self._load_images_from(normal_folder)

        # check both PNG_Animations and PNG_Parts&Spriter_Animation locations for Shot4
        candidate_shot_paths = [
            os.path.join(self.base, 'PNG_Animations', 'Shots', 'Shot4'),
            os.path.join(self.base, 'PNG_Parts&Spriter_Animation', 'Shots', 'Shot4'),
            os.path.join(self.base, 'PNG_Parts&Spriter_Animation', 'Shot4'),
        ]

        # Kerää luotikehysten alikansiot kategorioihin: start, flight, explode
        shots = {'start': [], 'flight': [], 'explode': []}
        for shots_folder in candidate_shot_paths:
            if not os.path.isdir(shots_folder):
                continue
            for dirpath, dirnames, files in os.walk(shots_folder):
                name = os.path.basename(dirpath).lower()
                pngs = sorted(f for f in files if f.lower().endswith('.png'))
                imgs = []
                for f in pngs:
                    full = os.path.join(dirpath, f)
                    try:
                        imgs.append(pygame.image.load(full).convert_alpha())
                    except Exception:
                        continue
                if not imgs:
                    continue
                # Luokan nimi kertoo mihin kategoriaan kuvat kuuluvat
                if 'start' in name or 'shotstart' in name:
                    shots['start'].extend(imgs)
                elif 'exp' in name or 'expl' in name:
                    shots['explode'].extend(imgs)
                else:
                    # Oletuksena käsitellään kuvaa lentovaiheen kehyksenä
                    shots['flight'].extend(imgs)

        self.shot_frames = shots

        # Jos tietyt Shot4-lentokehykset löytyvät osakansiosta, käytä niitä ensisijaisesti
        preferred = os.path.join(self.base, 'PNG_Parts&Spriter_Animation', 'Shots', 'Shot4', 'shot4', 'shot4_asset', '000_shot4_asset_0.png')
        if os.path.isfile(preferred):
            try:
                img = pygame.image.load(preferred).convert_alpha()
                shots['flight'] = [img]
                self.shot_frames = shots
            except Exception:
                pass

        return {
            'ship': self.ship_frames,
            'exhaust_turbo': self.exhaust_turbo,
            'exhaust_normal': self.exhaust_normal,
            'shots': self.shot_frames,
        }


__all__ = ['SpriteSettings']
