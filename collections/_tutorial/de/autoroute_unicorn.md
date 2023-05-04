---
permalink: /de/tutorials/autoroute_unicorn/
title: "Einhorn mittels automatisch geführtem Geradstich"
language: de
last_modified_at: 2022-07-08
excerpt: "fichier exemple licorne en points droits"
image: "/assets/images/tutorials/tutorial-preview-images/autoroute_unicorn.jpg"
tutorial-typ:
  - Beispieldatei
stichart: 
  - Geradstich
  - Mehrfach-Geradstich
tool:
  - Linie
techniken:
schwierigkeitsgrad: 
  - leicht
---

## Einhorn mittels Geradstich
Starte mit diesem Bild, lade es als `.png` herunter [Einhorn](https://freesvg.org/1539642047)
<a title="Public Domain" href="https://freesvg.org/1539642047"><img width="512" alt="Unicorn" src="https://freesvg.org/img/1539642047.png"></a>

gestickte Version:

![Brodée](/assets/images/tutorials/tutorial-preview-images/autoroute_unicorn.jpg)

Und alles mit geringem Aufwand....

in dem svg [Download](/assets/images/tutorials/samples/autoroute_unicorn.svg){: download="autoroute_unicorn.svg" } findest du alle Arbeitsschritte:

- Image (Bild) : Bild mit dem man startet

- Step 1 (Schritt 1): Vektorisierung des Startbildes mittels `Pfad > Bitmap nachzeichnen` 

Hier stellt man die Parameter ein :

![Parameter](/assets/images/tutorials/autoroute/autoroute_unicorn_parameters.jpg)

Das allerwichtigste ist bei der Auswahl des `Erkennungsmodus` die Wahl der Option `Strichzeichnung vektorisieren(autotrace)` 

- Step 2 (Schritt 2): Optimierung der Pfade für die Stickerei
  - `Pfad > Zerlegen` 
  - als nächstes  `Erweiterungen > Ink/Stitch  > Fehlerbehebung > Dokument bereinigen...` das löscht alle Mini-Pfade, Standardeinstellung ist < 20px

 
- Step 3 (Schritt 3): Einstellung der Stickparameter 
  - Alle Pfade als Geradstich einstellen (`Objekt > Füllung und Kontur > Muster der Kontur`) eine unterbrochene Linie wählen (egal welche)
  - Festlegen der Stickparameter mittels `Erweiterungen > Ink/Stitch  > Parameter`. 
  - Dies ist der Zeitpunkt, um die Länge des Stichs zu wählen und ob man einen Mehrfachgeradstich wünscht oder nicht

Nun sieht man in der Simulation sehr viele Sprungstiche.

![Sauts de fil](/assets/images/tutorials/autoroute/autoroute_unicorn_embroidery_params.jpg)

- Step 4 (Schritt 4)
   Ausführung der automatischen Anordnung von Geradstichen nach Auswahl aller Pfade
  `Erweiterungen > Ink/Stitch  > Werkzeuge: Linie > Automatisch Geführter Geradstich` mit der Option "Knoten an Schnittpunkten hinzufügen".
  
  Geradstiche zur Verbindung werden automatisch eingefügt um Sprungstiche zu vermeiden. Im Dokument sind diese Französisch benannt, nicht wudnern, wenn du das mit der Deutschen Version machst, stehts auf Deutsch da.
  
Führe `Erweiterungen > Ink/Stitch  > Visualieren und Exportieren > Simulator / Realistische Vorschau` aus, um zu überprüfen, dass es nur noch zwei Fadensprünge gibt, zwischen dem Auge und dem Körper.
   
   ![ohne Sprungstiche](/assets/images/tutorials/autoroute/autoroute_unicorn_embroidery_preview.jpg)
 

Hinweis: Hier ist das Ausgangsbild von sehr guter Qualität, wenn es weniger gut ist, kannst du vor der Anwendung des Werkzeugs `Automatisch Geführter Geradstich`
diese Erweiterungen von Ellen Wasbo (https://inkscape.org/cs/~EllenWasbo/resources/) verwenden.
- remove duplicate nodes
- remove duplicate lines

die noch nützlicher sein können, als ihr Name vermuten lässt, um das Bild zu verbessern.

Eine Vereinfachung der Pfade, kann auch eine gute Idee sein.

![SVG](/assets/images/tutorials/samples/autoroute_unicorn.svg)

[Download](/assets/images/tutorials/samples/autoroute_unicorn.svg){: download="autoroute_unicorn.svg" }
