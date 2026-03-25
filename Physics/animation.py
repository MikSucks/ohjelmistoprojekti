"""
Physics/animation.py - Fysiikkapohjainen animointi värähtelyille

Tarjoaa DampedOscillator-luokan törmäyksien jälkeiseen pomppimiseen ja muihin fysiikkaohjattuihin animaatioihin.
Käyttää eksponentiaalista vaimennusta ja sinimuotoista värähtelyä luonnollisen liikkeen aikaansaamiseksi.
"""

import pygame
import math


class DampedOscillator:
    """
    Vaimennettu harmoninen värähtelijä fysiikkapohjaisiin animaatioihin.
    
    Mallintaa pomppuja ja värinää kaavalla:
    $$position = base + initial\_displacement \cdot e^{-\frac{damping \cdot t}{T}} \cdot \cos(\omega \cdot t)$$
    
    Tämä luo luonnollisen tuntuisen fysiikan: alkuperäinen pomppu, joka asettuu vähitellen.
    Käytetään korvaamaan Enemy-luokan collision_bounce_*-logiikka.
    
    Attribuutit:
        base (pygame.Vector2): Lepoasema, jota kohti liike konvergoi
        initial_disp (pygame.Vector2): Alkuperäinen poikkeama lepoasemasta
        duration (float): Animaation kokonaiskesto sekunteina
        oscillations (float): Värähdysjaksojen määrä keston aikana
        damping (float): Vaimennuskerroin (suurempi = nopeampi vaimennus)
        active (bool): Onko värähtely parhaillaan käynnissä?
        timer (float): Tässä värähtelyssä jäljellä oleva aika
    """
    
    def __init__(self, base_pos, initial_displacement, duration=2.0, 
                 oscillations=2.0, damping=2.2):
        """
        Alusta vaimennettu värähtelijä.
        
        Args:
            base_pos (tuple|pygame.Vector2): Keskipiste/lepoasema
            initial_displacement (tuple|pygame.Vector2): Alkupoikkeama lepoasemasta
            duration (float): Animaation kokonaisaika sekunteina (oletus 2.0)
            oscillations (float): Jaksojen määrä (oletus 2.0)
            damping (float): Eksponentiaalinen vaimennuskerroin (oletus 2.2)
        
        Esimerkki:
            # Pomputa vihollista 30 pikseliä 1 sekunnin ajan kahdella värähdyksellä
            osc = DampedOscillator((100, 100), (30, 0), duration=1.0, oscillations=2.0)
        """
        self.base = pygame.Vector2(base_pos)
        self.initial_disp = pygame.Vector2(initial_displacement)
        self.duration = max(0.01, float(duration))
        self.oscillations = float(oscillations)
        self.damping = float(damping)
        
        self.timer = self.duration
        self.active = True
    
    def update(self, dt):
        """
        Päivitä värähtelijä ja palauta nykyinen sijainti.
        
        Sijainti vaimenee eksponentiaalisesti samalla kun se värähtelee sinimuotoisesti.
        Kun ajastin kuluu loppuun, värähtelijä muuttuu inaktiiviseksi ja palauttaa lepoaseman.
        
        Args:
            dt (float): Delta-aika sekunteina
        
        Returns:
            pygame.Vector2: Nykyinen sijainti tässä framessa
        """
        self.timer -= dt
        
        # Animaatio valmis
        if self.timer <= 0:
            self.active = False
            return self.base
        
        # Laske kulunut aika
        elapsed = self.duration - self.timer
        T = self.duration
        
        # Värähtelytaajuus: omega = 2*pi * (värähdykset / kesto)
        omega = 2.0 * math.pi * (self.oscillations / T)
        
        # Eksponentiaalinen vaippakäyrä: e^(-vaimennus * t / T)
        # Vaimenee arvoon ~0.1 kun t=T ja vaimennus=2.2
        envelope = math.exp(-(self.damping * elapsed) / T)
        
        # Kosinivärähtely: alkaa arvosta 1, värähtelee
        osc = math.cos(omega * elapsed)
        
        # Lopullinen sijainti: lepoasema + alkupoikkeama * vaippakäyrä * värähtely
        displacement = self.initial_disp * (envelope * osc)
        
        return self.base + displacement
    
    def is_active(self):
        """Tarkista, onko värähtely vielä käynnissä."""
        return self.active
    
    def __repr__(self):
        return (f"DampedOscillator(base={self.base}, "
                f"remaining={self.timer:.2f}s, active={self.active})")


class BounceAnimator:
    """
    Hallintatyökalu useille samanaikaisille vaimennetuille värähtelijöille.
    
    Hyödyllinen, kun entiteetti tarvitsee useita pomppupisteitä (esim. eri ruumiinosat).
    Seuraa kaikkia aktiivisia värähtelijöitä ja tarjoaa yhden päivitysrajapinnan.
    """
    
    def __init__(self):
        """Alusta tyhjä animaattori."""
        self.oscillators = {}
    
    def add_oscillation(self, name, base_pos, initial_disp, duration=2.0,
                        oscillations=2.0, damping=2.2):
        """
        Lisää uusi värähtelijä.
        
        Args:
            name (str): Yksilöllinen tunniste tälle värähtelylle
            base_pos (tuple|pygame.Vector2): Lepoasema
            initial_disp (tuple|pygame.Vector2): Alkupoikkeama
            duration (float): Animaation kesto
            oscillations (float): Jaksojen määrä
            damping (float): Vaimennusnopeus
        """
        self.oscillators[name] = DampedOscillator(
            base_pos, initial_disp, duration, oscillations, damping
        )
    
    def update(self, dt):
        """
        Päivitä kaikki aktiiviset värähtelijät ja poista inaktiiviset.
        
        Args:
            dt (float): Delta-aika sekunteina
        
        Returns:
            dict: {nimi: nykyinen_sijainti} kaikille aktiivisille värähtelijöille
        """
        result = {}
        
        # Päivitä ja suodata pois inaktiiviset
        names_to_remove = []
        for name, osc in self.oscillators.items():
            pos = osc.update(dt)
            if osc.is_active():
                result[name] = pos
            else:
                names_to_remove.append(name)
        
        # Poista inaktiiviset
        for name in names_to_remove:
            del self.oscillators[name]
        
        return result
    
    def has_active(self):
        """Tarkista, onko mikään värähtelijöistä vielä aktiivinen."""
        return any(osc.is_active() for osc in self.oscillators.values())
    
    def clear(self):
        """Tyhjennä kaikki värähtelijät."""
        self.oscillators.clear()