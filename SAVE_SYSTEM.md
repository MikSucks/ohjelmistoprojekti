## Pelin Tallennusjärjestelmä - Käyttäjän Opas

###  Ominaisuudet

1. **Automaattinen Tallentaminen Taukovalikosta**  
   - Kun painat `ESC` pelissä ja valitse **"SAVE & QUIT"**, peli tallentaa:
     - Nykyinen taso (1-5)
     - Nykyinen aalto (1-4) levyssä
     - Kerätyt pisteet
     - Pelaajan terveystila (HP)
     - Pelaajan ammo määrät

2. **Continue-Nappi Päävalikossa**  
   - Päävalikossa ilmestyy **"CONTINUE"** -nappi jos tallennusta on
   - Klikkaamalla CONTINUE, peli jatkaa juuri siitä mihin jäit
   - Aalto generoidaan uudestaan samalla vihollisten asetuksella
   - Pelaajasi stats (HP, ammo, pisteet) palautetaan

3. **Tallennustiedosto**
   - Tallentuu tiedostoon: `savegame.json`
   - Formaatti: JSON (helppo lukea ja muokata)
   - Sijainti: Projektin pääkansio

###  Tallennetut Tiedot

```json
{
    "level_number": 2,
    "wave_number": 3,
    "total_score": 4200,
    "player_health": 4,
    "player_ammo_type1": 85,
    "player_ammo_type2": 40,
    "player_name": "Pelaaja"
}
```

###  Käyttö

1. **Pelaa peliä normaalisti**
2. **Paina ESC** kesken pelissä
3. **Valitse "SAVE & QUIT"** → peli tallennetaan
4. **Käynnistä peli uudestaan**
5. **Päävalikossa klikkaa "CONTINUE"** → jatka juuri siitä mihin jäit!

###  Tallennuksen Poistaminen

Jos haluat aloittaa alusta:
- Poista `savegame.json` -tiedosto projektin pääkansiosta
- Tai valitse "START GAME" → aloitat uudesta

###  Tekninen Toteutus

- **Moduuli**: `SaveGame.py` - hallinnoi tallennusta/lataamista
- **Integraatio**: 
  - `MainMenuState.py` - lataa tallennetun pelin
  - `PauseState.py` - tallentaa pelin "SAVE & QUIT":lle
  - `MainMenu.py` - näyttää CONTINUE-napin jos tallennus on olemassa
  - `PauseMenu.py` - lisää "SAVE & QUIT" -nappi

###  Huomioitavaa

- Aalto generoidaan **uudestaan alusta**, mutta viholliset ovat samat
- Pelaajan **sijaintia ei tallenneta** (pelaaja spawna levyn keskelle)
- Jos haluat **edistyneempää tallennusta** (pelaajan sijainti, vihollisten tila), se vaatii laajempia muutoksia
