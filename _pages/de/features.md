---
title: "Ink/Stitch Features"
permalink: /de/features/
excerpt: "Ink/Stitch features"
last_modified_at: 2019-03-15
sidebar:
  nav: pages
toc: true
---
## Features
* Digitalisiere Motive für Maschinenstickerei mit Inkscape (SVG)
* Platformübergreifen
  * alle Code-Bibliotheken werden mitgeliefert, es muss nichts weiter installiert werden!
* Benutzeroberfläche in verschiedenen Sprachen ([Übersetzungsvorschläge willkommen](https://crowdin.com/project/inkstitch)!)
* Unterstützung vieler Dateiformate
    * einschließlich Batch-Export (viele Dateiformate gleichzeitig exportieren)
* Fadenschneide- und Stop-Befehle
* Stickreihenfolge ändern
* Nullpunkt (0, 0) in der Stickdatei festlegen
* Animierte Vorschau
  * Inklusive einer Live-Vorschau während Stick-Parameter geändert werden wie z.B. Unterlage, Zeilenabstand, etc.
* PDF-Ausdruck
  * realistische und schematische Vorschau
  * Layout für den Nutzer mit Farbblock, Garnnamen, Stichanzahl und individuellen Notizen
  * Layout für Klienten
  * im Webbrowser individuell anpassbar
* Garnhersteller Paletten von über 60 Herstellern
  * automatische Installation der Inkscape-Paletten für den Gebrauch in deinen Motiven
  * Garnnamen und Katalog-Nummern im PDF-Ausdruck
* Lettering

## Unterstützte Sticharten

### Füllstitch
* automatische Füllung von ausgefallenen Formen mit Stichen
* Anpassung von Stichlänge, Zeilenabstand und Winkel
* Unterlage

### Satinstich
* Individuelle Satinkolumnen mit variierender Breite
* Automatische Führung (mit verstecktem Laufstich, falls nötig)
* verwende von bis zu 3 verschiedenen Arten von Unterlage
    * Mitellinie
    * Kontur
    * Zick-Zack

* E-Stich

### Linienförmige Stiche

* Laufstitch
* Bohnenstich
* Manueller Stich
  * jeder Stitch genau dort, wo du ihn haben willst

## Unterstützte Datei-Formate

### Schreiben
CSV, **DST**, **EXP**, **JEF**, PEC, **PES**, SVG, TXT (G-CODE), U01, **VP3**

### Lesen
100, 10o, BRO, DAT, DSB, **DST**, DSZ, EMD, **EXP**, EXY, FXY, GT, INB, **JEF**, JPX, KSM, MAX, MIT, NEW, PCD, PCM, PCQ, PCS, PEC, **PES**, PHB, PHC, SEW, SHV, STC, STX, TAP, TBF, TXT (G-CODE), U01, **VP3**, XXX, ZXY

## Ausschau

Hier sind Funktionen, die wir hoffen hinzufügen zu können (nicht unbedingt in dieser Reihenfolge):

* Gradient Fill (already realised as a [hidden feature](https://github.com/inkstitch/inkstitch/pull/108#issuecomment-369444197))
* Pattern Fill [#33](https://github.com/inkstitch/inkstitch/issues/33)
* Multi-Decoration Support [#371](https://github.com/inkstitch/inkstitch/issues/371)
* Automatic splitting of designs for small machines [#182](https://github.com/inkstitch/inkstitch/issues/182)
* Multiple Underlay for Fill [#110](https://github.com/inkstitch/inkstitch/issues/110)
* Split satins [#77](https://github.com/inkstitch/inkstitch/issues/77)
* Running Stitch Autoroute [#373](https://github.com/inkstitch/inkstitch/issues/373)
* 32-bit Linux support (build engineers needed!)

