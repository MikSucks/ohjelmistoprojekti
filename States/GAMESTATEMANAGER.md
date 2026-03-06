# States-kansion selitys

Tama kansio sisaltaa pelin tilakoneen (state machine) kaikki tilat.
Tilat vaihtuvat `GameStateManager`-luokan kautta, jolloin pelin eri nakymat
ja logiikka pysyvat selkeasti erotettuina.

## Mitä tiedostot tekevat

- `GameState.py`
  - Yhteinen perusluokka kaikille tiloille.
  - Maarittelee rungon (`update`, `draw`, mahdolliset tapahtumakasittelijat).

- `GameStateManager.py`
  - Hallitsee aktiivista tilaa ja tilasiirtymia.
  - Kutsuu joka framella aktiivisen tilan `update`- ja `draw`-metodeja.

- `MainMenuState.py`
  - Paa valikko, josta peli aloitetaan.

- `PlayState.py`
  - Varsinainen pelitila.
  - Kayttaa `Tasot/LevelManager.py`-luokkaa tasojen paivitykseen ja piirtoon.

- `PauseState.py`
  - Taukovalikko pelin aikana.

- `LevelCompleteState.py`
  - Naytetaan, kun nykyinen taso on suoritettu.
  - Paattaa, siirrytaanko seuraavaan tasoon vai takaisin paavalikkoon.

- `GameOverState.py`
  - Naytetaan, kun pelaaja haviaa.

## Tyypillinen tilavirta

`MainMenuState` -> `PlayState` -> (`PauseState` / `LevelCompleteState` / `GameOverState`)

## Miksi taman rakenne on hyodyllinen

- Eri nakymat pysyvat erillaan (valikko, peli, game over).
- Tilasiirtymat ovat keskitetty yhdelle managerille.
- Uusien tilojen lisaaminen on helppoa (esim. asetukset tai credits).
