# Scripted Siege

Jednoduchý 2D Tower Defense projekt napísaný v Pythone (Pygame).

## O projekte
Scripted Siege rozdeľuje kód na jadro hry (engine) a herný obsah (game). Hráč umiestňuje veže pozdĺž cesty a bráni sa proti vlnám nepriateľov.

## Požiadavky
- Python 3.8+ (alebo novší)
- Pygame

Inštalácia závislostí:

```bash
pip install pygame
```

## Spustenie

Spusti hru z koreňového adresára:

```bash
python src/main.py
```

## Základné ovládanie
- Ľavé tlačidlo myši: výber a umiestnenie veží, interakcia s UI
- ESC: návrat do hlavného menu
- Prepínanie rýchlosti hry a ovládanie zvuku v menu

## Štruktúra projektu (vybrané súbory)
- `src/main.py` – vstupný bod a hlavná slučka
- `src/engine/` – jadro (okno, sound manager, správa stavu)
- `src/game/` – herná logika (úrovne, nepriatelia, veže, konfigurácia)
- `assets/` – zvuky a obrázky

