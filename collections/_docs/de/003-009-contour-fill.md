---
title: "Konturfüllung"
permalink: /de/docs/stitches/contour-fill/
excerpt: ""
last_modified_at: 2023-02-12
toc: true
---
## Beschreibung

![Konturfüllung Detail](/assets/images/docs/contour-fill-detail.jpg)

Konturfüllung füllt eine Fläche der Kontur folgend.

### Funktionsweise

Erstelle einen geschlossenen Pfad mit einer Füllfarbe.

### Anfangs- und Endpunkt festlegen

Ink/Stitch erlaubt es über visuelle Befehle den [Anfangs- und Endpunkt eines Füllobjekts](/de/docs/commands) zu kennzeichnen.

### Parameter

Öffne `Erweiterungen > Ink/Stitch > Parameter`. Setze die Füllmethode auf `Konturfüllung` und passe die restlichen Einstellungen den jeweiligen Bedürfnissen an.

Einstellung                     ||Beschreibung
---|---|---
Automatisch geführte Füllstiche | ☑ |Muss aktiviert sein, damit diese Einstellungen wirksam werden.
Füllmethode                     | Konturfüllung | Contour Fill must be selected to sew spiral lines of the contour
Methode                         | ![Von Innen nach Außen](/assets/images/docs/contour-fill-innertoouter-bottlenecks.jpg)<br>![Konturspiralen](/assets/images/docs/contour-fill-spirals.jpg)|**Von Innen nach Außen** (Standard) kann auch Formen mit Engpässen füllen<br>**Einfach Spirale** füllt eine Fläche mit einer einfachen Spirale von außen nach innen<br>**Doppelte Spirale** füllt eine Fläche mit einer doppelten Spirale, die Außen beginnt und endet.
Stil der Verbindungen           | rund, spitz, abgeschrägt|Method to handle the edges when the size the contour is reduced for the inner spirals
Selbstüberschneidungen vermeiden| ![Avoid self crossing effect](/assets/images/docs/contour-fill-self-crossing.jpg)|Wheter inner to outer is allowed to cross itself or not
Uhrzeigersinn                   || Bestimmt die Richtung in der die Kontur gestickt wird
Maximale Füllstichlänge         || Die Stichlänge in einer Reihe. Ein kürzerer Stich kann am Anfang oder am Ende einer Reihe verwendet werden.
Reihenabstand                   || Abstand zwischen den Stichreihen.
Geradstich-Toleranz             || Alle Stiche müssen innerhalb dieses Abstandes zum Pfad befinden. Ein niedrigerer Toleranzwert führt zu kürzeren Stichen. Ein höherer Wert könnte Ecken abrunden.
Vernähen erzwingen              || Vernäht den Faden nach diesem Element, auch dann, wenn der Abstand zum Folgeobjekt geringer ist als in den [Ink/Stitch Einstellungen](/de/docs/preferences/) definiert.
Fadenschnitt                    || Schneidet den Faden nachdem dieses Objekt genäht wurde
Stopp                           || Stoppt die Maschine nachdem dieses Objekt genäht wurde und springt zur Stopp-Position (sofern vorhanden)

### Unterlage

Die Unterlage einer Konturfüllung folgt nicht der Kontur, aber nutzt den Stickwinkel, der in den [Parametern der Unterlage](/de/docs/params/#füllung-unterlage) eingestellt werden kann.

### Beispieldateien für Konturfüllung

{% include tutorials/tutorial_list key="stichart" value="Konturfüllung" %}
