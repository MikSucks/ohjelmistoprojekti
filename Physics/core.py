"""
Physics/core.py - Perus RigidBody-luokka fysiikkaolioille

Tarjoaa yhtenäisen fysiikkasimulaation kaikille pelin objekteille (pelaaja, viholliset, ammukset).
Jokainen olio ylläpitää sijaintia, nopeutta, kiihtyvyyttä, massaa ja niihin voidaan kohdistaa voimia.
"""

import pygame
import math


class RigidBody:
    """
    Perusluokka kaikille pelin fysiikkaolioille.
    
    Vastaa seuraavista:
    - Sijainnin ja nopeuden seuranta
    - Voimien kerääminen ja soveltaminen
    - Nopeusrajoitukset (maksiminopeus)
    - Integraatio: voimat -> kiihtyvyys -> nopeus -> sijainti
    
    Attribuutit:
        pos (pygame.Vector2): Sijainti maailmassa
        vel (pygame.Vector2): Nopeusvektori (pikseliä/sekunti)
        acc (pygame.Vector2): Kertyvä kiihtyvyys (nollataan joka ruudun jälkeen)
        mass (float): Massa (kg vastaava)
        inv_mass (float): Esilaskettu 1/massa optimointia varten
        collision_radius (float): Säde törmäyksentunnistukseen
        max_speed (float|None): Valinnainen maksiminopeus
        forces (list): Lista Force-olioista, jotka sovelletaan joka ruutu
        is_dynamic (bool): Voiko tähän kappaleeseen vaikuttaa voimat?
    """
    
    def __init__(self, x=0, y=0, mass=1.0):
        """
        Alustaa fysiikkaolion.
        
        Parametrit:
            x (float): Alkusijainti X-akselilla
            y (float): Alkusijainti Y-akselilla
            mass (float): Massa (oletus 1.0)
        
        Poikkeukset:
            ValueError: Jos massa on nolla tai negatiivinen
        """
        if mass <= 0:
            raise ValueError("Mass must be positive")
            
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        
        self.mass = float(mass)
        self.inv_mass = 1.0 / self.mass
        
        self.collision_radius = 1.0
        self.max_speed = None  # No limit by default
        
        self.forces = []
        self.is_dynamic = True
    
    def add_force(self, force):
        """
        Lisää voima, joka sovelletaan seuraavassa update()-kutsussa.
        
        Parametrit:
            force (Force): Force-olio, jolla on get_force(body, dt) -metodi
        """
        if force is not None:
            self.forces.append(force)
    
    def apply_forces(self, dt):
        """
        Summaa kaikki voimat ja muuntaa ne kiihtyvyydeksi.
        
        F = ma => a = F/m (kaikkien voimien summa jaettuna massalla)
        Tyhjentää voimien listan käytön jälkeen.
        
        Parametrit:
            dt (float): Aikaväli sekunneissa
        """
        self.acc = pygame.Vector2(0, 0)
        
        for force in self.forces:
            try:
                f = force.get_force(self, dt)
                if f is not None:
                    self.acc += f * self.inv_mass
            except Exception:
                # Silently skip invalid forces
                pass
        
        self.forces = []  # Clear for next frame
    
    def apply_velocity_constraints(self):
        """
        Soveltaa maksiminopeusrajoituksen, jos asetettu.
        
        Rajaa nopeuden max_speed-arvoon skaalaamalla nopeusvektoria.
        """
        if self.max_speed is not None and self.max_speed > 0:
            speed = self.vel.length()
            if speed > self.max_speed:
                self.vel.scale_to_length(self.max_speed)
    
    def update_velocity(self, dt):
        """
        Päivittää nopeuden kiihtyvyydestä: v += a*dt
        
        Soveltaa myös nopeusrajoitukset.
        
        Parametrit:
            dt (float): Aikaväli sekunneissa
        """
        self.vel += self.acc * dt
        self.apply_velocity_constraints()
    
    def update_position(self, dt):
        """
        Päivittää sijainnin nopeudesta: pos += v*dt
        
        Parametrit:
            dt (float): Aikaväli sekunneissa
        """
        self.pos += self.vel * dt
    
    def update(self, dt):
        """
        Suorittaa koko fysiikka-askeleen:
        1. Soveltaa voimat -> kiihtyvyys
        2. Päivittää nopeuden kiihtyvyydellä
        3. Päivittää sijainnin nopeudella
        
        Parametrit:
            dt (float): Aikaväli sekunneissa
        """
        if not self.is_dynamic:
            return
            
        self.apply_forces(dt)
        self.update_velocity(dt)
        self.update_position(dt)
    
    def set_velocity(self, vx, vy):
        """Aseta nopeus suoraan."""
        self.vel = pygame.Vector2(vx, vy)
        self.apply_velocity_constraints()
    
    def get_speed(self):
        """Palauttaa nykyisen nopeuden suuruuden."""
        return self.vel.length()
    
    def __repr__(self):
        return (f"RigidBody(pos={self.pos}, vel={self.vel}, "
                f"mass={self.mass}, speed={self.get_speed():.1f})")
