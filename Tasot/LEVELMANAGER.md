# Monitasonhallinnan toteutus - Yhteenveto

## Yleiskuva

Peliin on toteutettu toimiva monitason etenemisjarjestelma, joka siirtyy sujuvasti viiden pelattavan tason (Taso1-Taso5) valilla. Jarjestelma hallitsee erillisia pelinstansseja tasokohtaisesti, mutta sailyttaa yhtenaisen etenemislogiikan.

---

## Keskeiset komponentit

### 1. `Tasot/LevelManager.py` (UUSI)

Kaikkien viiden tason keskitetty koordinaattori.

**Luokka: `LevelManager`**

```python
def __init__(self, screen, num_levels=5)
    # Luo 5 Game-instanssia (yksi per taso)
    # Yllapitää current_level_index-arvoa (0-4)

def next_level() -> bool
    # Siirtyy seuraavaan tasoon; True jos onnistuu, False jos kaikki tasot suoritettu

def is_level_complete() -> bool
    # Tarkistaa onko nykyisen tason level_completed-lippu paalla

def is_game_over() -> bool
    # Tarkistaa onko nykyisen tason game_over-lippu paalla

def update(events)
    # Delegoi paivityksen aktiiviselle tasolle

def draw(target_screen)
    # Delegoi piirron aktiiviselle tasolle

def get_current_level_number() -> int
    # Palauttaa 1-indeksoidun tasonumeron (1-5)

def reset_current_level()
    # Nollaa aktiivisen tason reset_game()-metodilla
```

**Keskeiset attribuutit:**

- `self.levels`: lista viidesta `Game`-instanssista
- `self.current_level_index`: aktiivisen tason indeksi 0-4
- `self.current_level`: viite aktiiviseen `Game`-instanssiin
- `self.all_levels_completed`: lippu, joka asetetaan kun kaikki viisi tasoa on suoritettu

---

### 2. `RocketGame.py` (MUOKATTU)

Paivitetty tukemaan tasokohtaista wave-dispatchia.

**Muutokset `Game.__init__`-metodiin:**

```python
def __init__(self, screen, level_number=1):
    self.level_number = level_number  # Tassa instanssissa pelattava taso (1-5)
    # ... muu alustus ennallaan
```

**Muutokset `Game.spawn_wave()`-metodiin:**

- Kutsuu oikeaa Taso-moduulia `self.level_number`-arvon perusteella.
- Tuo valinnaisesti `spawn_wave_taso2-5`-funktiot.
- Toimii hallitusti, vaikka jotkin tasomoduulit puuttuisivat.

---

### 3. `States/PlayState.py` (MUOKATTU)

Kayttaa nyt `LevelManager`-luokkaa suoran `RocketGame.Game`-instanssin sijaan.

**Keskeinen muutos:**

```python
def __init__(self, manager, level_manager=None):
    self.level_manager = level_manager if level_manager else LevelManager(manager.screen)
    # Hyvaksyy ulkoisen level_managerin etenemisen jatkamista varten
```

**Paivityslogiikka:**

- Delegoi paivityksen `level_manager.update(events)`-kutsulle.
- Tarkistaa `level_manager.is_level_complete()` ja siirtyy `LevelCompleteState`-tilaan.
- Tarkistaa pelaajan HP:n `level_manager.current_level.player.health`-arvosta.
- Valittaa `level_manager`-instanssin `LevelCompleteState`-tilaan, jotta eteneminen jatkuu oikein.

---

### 4. `States/LevelCompleteState.py` (MUOKATTU)

Paivitetty monitason etenemista varten.

**Keskeinen muutos:**

```python
def __init__(self, manager, level_manager=None):
    self.level_manager = level_manager
    # Nayttaa nykyisen tason ja seuraavan tason tiedot valikossa
```

**"Next Level" -painikkeen logiikka:**

```python
if isinstance(result, int):
    has_next = self.level_manager.next_level()
    if has_next:
        # Luodaan uusi PlayState samalla level_managerilla
        self.manager.set_state(PlayState(self.manager, level_manager=self.level_manager))
    else:
        # Kaikki tasot suoritettu -> takaisin paavalikkoon
        self.manager.set_state(MainMenuState(self.manager))
```

---

### 5. `Tasot/Taso2.py`, `Taso3.py`, `Taso4.py`, `Taso5.py` (UUSI)

Tasopohjat valmiina jatkokehitysta varten.

**Jokainen moduuli vie ulos:**

```python
def spawn_wave_taso#(game, wave_num, apply_hitbox, ...):
    # Palauttaa True jos kasitelty, muuten False
    # Talla hetkella placeholderina samankaltainen wave-rakenne kuin Taso1:ssa
```

**TODO per taso:**

- Muokkaa vihollistyypit, maarat ja liikekuviot wave-kohtaisesti.
- Sääda vaikeusasteen eteneminen tasolta toiselle.

---

## Pelin etenemisvirta

```text
MainMenuState
    -> PlayState.__init__()
        -> Luo uuden LevelManagerin (jos sita ei annettu)
            -> LevelManager luo 5 Game-instanssia
                -> Jokainen Game.__init__(level_number=1-5)
                    -> Game.spawn_wave(1) -> Taso#.spawn_wave_taso#()

PlayState paivittaa joka framella:
    -> level_manager.update(events)
        -> game.update() kasittelee wave-etenemisen
            -> Kun wave 4 (boss) kaatuu:
                level_completed = True

PlayState havaitsee level_completed-tilan:
    -> LevelCompleteState(manager, level_manager)
        -> Kayttaja valitsee "Next Level"
            -> level_manager.next_level()
                -> jos tasoja jaljella: PlayState samalla level_managerilla
                -> jos viimeinen taso: MainMenuState (peli suoritettu)
```

---

## Testatut asiat

- Syntax-tarkistus: kaikki muokatut tiedostot kaantyvat ilman virheita.
- LevelManagerin alustus: luo oikein 5 tasoa ja oikeat tasonumerot.
- Eteneminen: `next_level()` etenee tasolta 1 tasolle 5 oikeassa jarjestyksessa.
- Rajatapaus: viimeisen tason jalkeen `all_levels_completed = True`.
- Instanssieristys: jokaisella tasolla oma pelaaja-, vihollis- ja pistejarjestelma.

---

## Arkkitehtuurin hyodyt

1. Eristys: jokainen taso on oma `Game`-instanssi.
2. Etenemisen jatkuvuus: sama `LevelManager` kulkee tilasiirtymien mukana.
3. Laajennettavuus: Taso6+ voidaan lisata helposti.
4. Yhteensopivuus: `PlayState` toimii myos ilman ulkoista `level_manager`-instanssia.

---

## Seuraavat kehitysaskeleet

### Nopeat parannukset

1. Tasokohtainen vaikeus: muokkaa `Tasot/Taso2-5.py` wave-funktioita.
2. Lopputila: lisaa `States/GameCompleteState.py` kaikkien tasojen suorittamisen jalkeen.

### Keskitason parannukset

3. Tasokohtaiset taustat/musiikit.
4. Vaikeusasteen skaalautuminen myohempiin tasoihin.
5. Kumulatiivinen pisteytys kaikkien tasojen yli.

### Edistyneet parannukset

6. Pelaajan jatkuvuus tasojen valilla (HP/ammo).
7. Lukituksen avausjarjestelma myöhemmille tasoille.

---

## Tiedostokooste

| Tiedosto | Tila | Tarkoitus |
|----------|------|-----------|
| `Tasot/LevelManager.py` | UUSI | Monitason keskitetty hallinta |
| `RocketGame.py` | MUOKATTU | Tasotietoinen wave-dispatch |
| `States/PlayState.py` | MUOKATTU | Eteneminen LevelManagerin kautta |
| `States/LevelCompleteState.py` | MUOKATTU | Seuraava taso -siirtymat |
| `Tasot/Taso1.py` | OLEMASSA | Tason 1 wave-logiikka |
| `Tasot/Taso2-5.py` | UUSI | Tasopohjat jatkokehitykseen |
| `States/MainMenuState.py` | OLEMASSA | Paavalikko |
| `States/PauseState.py` | OLEMASSA | Taukovalikko |
| `States/GameOverState.py` | OLEMASSA | Haviotila |

---

## Varmennuskomennot

```bash
# Testaa LevelManagerin import
py -c "from Tasot.LevelManager import LevelManager; print('OK: import toimii')"

# Testaa eteneminen
py -c "
from Tasot.LevelManager import LevelManager
import pygame
pygame.init()
lm = LevelManager(pygame.display.set_mode((1600,800)))
for i in range(4):
    lm.next_level()
print(f'Tasoja: {lm.num_levels}, kaikki suoritettu: {lm.all_levels_completed}')
"

# Syntax-tarkistus
py -m py_compile RocketGame.py Tasot/LevelManager.py States/PlayState.py
```

---

## Yhteenveto

Monitasonhallinta on toiminnassa ja valmiina jatkokehitykseen. Peli pystyy:

- aloittamaan uudella `LevelManager`-instanssilla
- etenemaan tasoilla 1-5 wave-rakenteen mukaan
- siirtymaan seuraavaan tasoon bossin kaaduttua
- palaamaan paavalikkoon, kun kaikki tasot on suoritettu
- sailyttamaan etenemistilan tilasiirtymien yli

Jarjestelma on valmis pelitestaukseen ja tasokohtaiseen sisallon viimeistelyyn.
