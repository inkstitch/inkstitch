---
title: "Manual Setup"
permalink: /da/developers/inkstitch/manual-setup/
last_modified_at: 2021-10-13
toc: true
---
En manuel installering giver dig mulighed for at redigere koden, mens du kører udvidelsen.

Hvis du sigter efter at fejlsøge udvidelser og kører på Windows, er nogle supplerende instruktioner (på engelsk) tilgængelige på: [windows-manual-setup](/developers/inkstitch/windows-manual-setup/)

## Hvordan Installere Ink/Stitch manuelt

### 1. Klon udvidelseskilden

```
git clone https://github.com/inkstitch/inkstitch
```

### 2. Installering af Pyembroidery

```
git clone https://github.com/inkstitch/pyembroidery.git
pip install -e pyembroidery/
```

We recommend to use `pyenv` with python 3.8.

### 3. Python afhængigheder

Et par python-moduler mere er nødvendige.
I nogle tilfælde bruger denne udvidelse funktioner, der ikke er tilgængelige i versionerne af modulerne, der er færdigpakket i distributioner, så vi anbefaler at installere dem direkte med pip.

Da vi allerede har installeret pyembroidery, kan du kun kommenter det midlertidigt, før du kører disse kommandoer.

```
cd inkstitch
pip install -r requirements.txt
```

### 4. Installering af Electron afhængigheder

Ink/Stitch GUI bruger Electron. Du skal bruge en fungerende NodeJS-installation af version 10 eller nyere. Hvis du ikke har kommandoen `yarn`, skal du installere den med `npm install yarn`.

Installer Electron og dets afhængigheder:

```
cd electron
yarn install
cd ..
```

### 5. Forberedelse af INX files

Nu skal vi oprette filerne til Inkscape-menuen.

```
make inx
```

### 6. Link symbolsk til Inkscape-udvidelsesbiblioteket

```
cd ~/.config/inkscape/extensions
ln -s /path/to/inkstitch
```

### 7. Kør Inkscape.

Ændringer til Python-koden træder i kraft næste gang udvidelsen køres. Ændringer af udvidelsesbeskrivelsesfilerne (`*.inx`) træder i kraft, næste gang Inkscape genstartes.

## Problemløsning

### ImportError: Intet modul er navngivet  shapely

Hvis Ink/Stitch returnerer `ImportError: No module named shapely`, så er det sandsynligvis den version af Python, der bruges af Inkscape, og den version, du installerede Python-afhængighederne for ovenfor, er forskellige.

* Åbne fil præferencer: `preferences.xml`.<br>
 Placeringen kan findes under  `Edit > Preferences > System > User preferences`
* Luk Inkscape, før du redigerer filen.<br>
  Ellers vil det blive overskrevet, når Inkscape lukker
* Søg efter udtrykket `<group id="extensions" />` og opdater til den korrekte Python-fortolker..

  **Eksempel:** Brug `<group id="extensions" python-interpreter="/usr/local/bin/python3" />` hvor `/usr/local/bin/python3` værdien er returneret af `which python3`.
