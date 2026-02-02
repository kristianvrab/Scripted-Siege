# Scripted Siege

Jednoduchý 2D Tower Defense projekt napsaný v Pythonu (Pygame).

## O projektu
Scripted Siege rozděluje kód na jádro hry (engine) a herní obsah (game). Hráč umisťuje věže podél cesty a brání se proti vlnám nepřátel.

## Požadavky
- Python 3.8+ (nebo novější)
- Pygame

Instalace závislostí:

```bash
pip install pygame
```

## Spuštění

Spusť hru z kořenového adresáře:

```bash
python src/main.py
```

## Základní ovládání
- Levé tlačítko myši: výběr a umístění věží, interakce s UI
- ESC: návrat do hlavního menu
- Přepínání rychlosti hry a ovládání zvuku v menu

## Struktura projektu (vybrané soubory)
- `src/main.py` – vstupní bod a hlavní smyčka
- `src/engine/` – jádro (okno, sound manager, správa stavu)
- `src/game/` – herní logika (úrovně, nepřátelé, věže, konfigurace)
- `assets/` – zvuky a obrázky

## Přispění
Pokud chceš přispět, otevři issue nebo vytvoř pull request s popisem změn.

---
Pokud chceš, mohu přidat stručný obsah (TOC), KaTeX podporu nebo rozšířené instrukce pro vývoj.