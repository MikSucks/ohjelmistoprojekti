Tässä kansiossa on pienet skeletontiedostot RocketGame-refaktorointia varten.

Tavoite:
- Pilkkoa `RocketGame.py` pienempiin vastuisiin: assets, input, update, render, enemies, ui, game_state
- Pitää tiedostot yksinkertaisina ja helposti luettavina

Seuraavat tiedostot on luotu:
- `assets.py`  : resurssien lataus
- `enemies.py` : vihollisten luonti / spawn
- `game_state.py`: pelitilan alustukset ja reset
- `input_handler.py`: tapahtumakäsittely
- `update.py`  : päivityslogiikka (entiteetit, fysiikka)
- `render.py`  : piirtäminen
- `ui.py`      : UI-apufunktiot
- `main.py`    : pääsilmukan runko

Aloitetaan pienin askelin: täydennän moduuleja tarpeen mukaan kun siirrämme logiikkaa pääsilmukasta.
