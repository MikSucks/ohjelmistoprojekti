"""
Fysiikkamoduuli - Yhtenäinen fysiikkamoottori RocketGame-pelille

Tarjoaa:
- RigidBody: Fysiikan kantaluokka kaikille entiteeteille (pelaaja, viholliset, ammukset)
- Forces (Voimat): Painovoima, ilmanvastus, magnetismi, työntövoima
- Animations (Animaatiot): Vaimennettu värähtelijä (DampedOscillator) törmäyspompuille
- Presets (Esiasetukset): Ennalta määritetyt fysiikkaprofiilit eri vihollistyypeille
- Box2D-integraatio: Valinnaiset edistyneet fysiikkasimulaatiot Box2D-kirjastolla
- Collision Categories (Törmäyskategoriat): Määrittele, mitkä objektit voivat törmätä keskenään
- Yhtenäinen API: Kaikki fysiikkaobjektit ja -toiminnot on keskitetty tähän moduuliin, mikä helpottaa ylläpitoa, 
  laajennettavuutta ja johdonmukaisuutta pelin fysiikkalogiikassa.
  
"""


from Physics.core import RigidBody
from Physics.forces import Force, Gravity, Drag, Magnetism, Thrust
from Physics.animation import DampedOscillator
from Physics.presets import ENEMY_PRESETS, create_enemy_physics
from Physics.box2d_config import PHYSICS_PROFILES, PhysicsProfile, get_physics_profile
from Physics.box2d_world import Box2DPhysicsWorld, CollisionCategory

__all__ = [
    'RigidBody',
    'Force',
    'Gravity',
    'Drag',
    'Magnetism',
    'Thrust',
    'DampedOscillator',
    'ENEMY_PRESETS',
    'create_enemy_physics',
    'PHYSICS_PROFILES',
    'PhysicsProfile',
    'get_physics_profile',
    'Box2DPhysicsWorld',
    'CollisionCategory',
]
