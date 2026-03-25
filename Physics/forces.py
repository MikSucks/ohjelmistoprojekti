
"""
Physics/forces.py - Voimahierarkia RigidBody-fysiikoille

Tarjoaa yleisimmät voimatyypit:
- Painovoima (Gravity): Vetovoima tiettyä pistettä kohti
- Ilmanvastus/Kitka (Drag): Nopeudesta riippuva vastus
- Magnetismi (Magnetism): Suunnattu vetovoima (tekoälylle)
- Työntövoima (Thrust): Suunnattu kiihtyvyys (pelaajan liikkumiseen)
"""
import pygame
import math


class Force:
    """
    Voimien kantaluokka.
    Ylikirjoita get_force() toteuttaaksesi kustomoidun voiman käyttäytymisen.
    Kaikki voimat palauttavat pygame.Vector2-olion, joka edustaa voimavektoria.
    """
    
    def get_force(self, body, dt):
        """
        Laske voima tälle framelle.
        Args:
            body (RigidBody): Kappale, johon voima kohdistuu
            dt (float): Delta-aika sekunteina
        
        Returns:
            pygame.Vector2: Voimavektori yksiköissä pikseliä/sekunti^2
        """
        return pygame.Vector2(0, 0)


class Gravity(Force):
    """
    Säteittäinen painovoima kohti keskipistettä.
    Käyttää yksinkertaistettua kääntäen verrannollisuutta etäisyyden neliöön: F = strength / distance^2
    Attributes:
        center (pygame.Vector2): Vetovoiman keskipiste
        strength (float): Painovoiman voimakkuusparametri
    """
    
    def __init__(self, center, strength=500):
        """
        Alusta painovoimakenttä.
        Args:
            center (tuple|pygame.Vector2): Painovoimakentän keskipiste
            strength (float): Mitä suurempi, sitä vahvempi veto (oletus 500)
        """
        self.center = pygame.Vector2(center)
        self.strength = float(strength)
    
    def get_force(self, body, dt):
        """
        Laske painovoima: F = strength / distance^2
        Returns:
            pygame.Vector2: Voima kohti keskipistettä
        """
        direction = self.center - body.pos
        distance = max(1, direction.length())
        
        # Etäisyyden neliön laki (approksimaatio)
        force_magnitude = self.strength / (distance * distance)
        
        try:
            return direction.normalize() * force_magnitude
        except ValueError:
            return pygame.Vector2(0, 0)


class Drag(Force):
    """
    Lineaarinen, nopeudesta riippuva ilmanvastus.
    Vastustaa liikettä: F = -coefficient * velocity
    Luo luonnollisen hidastuvuuden ja vauhdin vaimennuksen.
    
    Attributes:
        coefficient (float): Vastuskerroin (tyypillisesti välillä 0-1)
    """
    
    def __init__(self, coefficient=0.1):
        """
        Alusta vastusvoima. 
        Args:
            coefficient (float): Vastuksen voimakkuus (0.0-1.0, suurempi = enemmän vastusta)
        """
        self.coefficient = float(coefficient)
    
    def get_force(self, body, dt):
        """
        Laske nopeutta vastustava voima. 
        Returns:
            pygame.Vector2: Voima vastakkaiseen suuntaan kuin nopeus
        """
        return -body.vel * self.coefficient


class Magnetism(Force):
    """
    Vetovoima kohti kohdetta (yleensä pelaajaa).
    Käytetään vihollisten tekoälyssä luomaan "hakeutuva" käyttäytyminen.
    Voima skaalautuu etäisyyden mukaan dynaamisemman liikkeen saamiseksi.
    Attributes:
        target (RigidBody): Kohde, jota kohti vedetään
        strength (float): Perusvetovoiman voimakkuus
        min_distance (float): Minimietäisyys, jolloin voima alkaa vaikuttaa
    """
    
    def __init__(self, target, strength=200, min_distance=50):
        """
        Alusta magnetismivoima kohti kohdetta.
        Args:
            target (RigidBody): Kohde-entiteetti (yleensä pelaaja)
            strength (float): Vetovoiman voimakkuus (oletus 200)
            min_distance (float): Minimietäisyys vedon alkamiselle (oletus 50)
        """
        self.target = target
        self.strength = float(strength)
        self.min_distance = float(min_distance)
    
    def get_force(self, body, dt):
        """
        Laske vetovoima kohti kohdetta.
        Skaalautuu etäisyyden mukaan (lähempänä = voimakkaampi).
        Returns:
            pygame.Vector2: Voima kohti kohdetta
        """
        if self.target is None:
            return pygame.Vector2(0, 0)
        
        direction = self.target.pos - body.pos
        distance = direction.length()
        
        if distance < self.min_distance:
            return pygame.Vector2(0, 0)
        
        # Skaalaa voima etäisyyden mukaan (lähempänä = vahvempi)
        force_magnitude = self.strength * (distance / 500.0)
        
        try:
            return direction.normalize() * force_magnitude
        except ValueError:
            return pygame.Vector2(0, 0)


class Thrust(Force):
    """
    Suunnattu kiihdytysvoima.
    
    Käytetään pelaajan työntövoimaan ja vihollisten liikkeeseen.
    Kohdistaa vakiovoiman määritettyyn suuntaan.
    Attributes:
        direction (pygame.Vector2): Normalisoitu suuntavektori
        magnitude (float): Voiman voimakkuus
    """
    
    def __init__(self, direction, magnitude):
        """
        Alusta työntövoima tiettyyn suuntaan.
        Args:
            direction (tuple|pygame.Vector2): Suunta, johon voima kohdistetaan
            magnitude (float): Voiman voimakkuus (pikseliä/sekunti^2)
        """
        dir_vec = pygame.Vector2(direction)
        try:
            self.direction = dir_vec.normalize()
        except ValueError:
            self.direction = pygame.Vector2(1, 0)
        self.magnitude = float(magnitude)
    
    def get_force(self, body, dt):
        """
        Palauta vakio työntövoima haluttuun suuntaan.
        Returns:
            pygame.Vector2: Voima määritettyyn suuntaan
        """
        return self.direction * self.magnitude


class Spring(Force):
    """
    Jousimainen palautusvoima.
    
    Vetää entiteettiä kohti ankkuripistettä: F = -k * displacement
    Hyödyllinen heilahteluihin ja kiertoratoihin.
    
    Attributes:
        anchor (pygame.Vector2): Lepoasema
        stiffness (float): Jousivakio (suurempi = jäykempi)
        damping (float): Vaimennuskerroin (stabiloi heilahtelua)
    """
    
    def __init__(self, anchor, stiffness=100, damping=0.1):
        """
        Alusta jousivoima.
        
        Args:
            anchor (tuple|pygame.Vector2): Lepoasema
            stiffness (float): Jousivakio (oletus 100)
            damping (float): Energiahäviö per askel (oletus 0.1)
        """
        self.anchor = pygame.Vector2(anchor)
        self.stiffness = float(stiffness)
        self.damping = float(damping)
    
    def get_force(self, body, dt):
        """
        Laske jousivoima: F = -k*x - b*v
        
        Returns:
            pygame.Vector2: Palauttava voima kohti ankkuria
        """
        displacement = self.anchor - body.pos
        spring_force = displacement * self.stiffness
        damping_force = body.vel * (-self.damping)
        return spring_force + damping_force