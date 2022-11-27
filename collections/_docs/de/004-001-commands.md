---
title: "Visuelle Befehle"
permalink: /de/docs/commands/
excerpt: ""
last_modified_at: 2022-11-27
toc: true
---
Visuelle Befehle können genutzt werden, um zusätzliche Informationen darüber festzulegen, wie das Design gestickt werden soll. Sie können z.B. der Maschine mitteilen, dass der Faden nach einem Stickobjekt geschnitten werden soll oder definieren, wann und wo die Maschine pausieren soll, so dass man für eine Applikation bequem ein Stück Stoff hinzufügen kann.

Nicht jede Maschine kann diese zusätzliche Informationen umsetzen und verstehen. In diesem Fall wird ein Befehl einfach ignoriert.
{: .notice--warning }

### Visuelle Befehle über die Erweiterung anhängen

* Wähle ein Objekt oder mehrere Objekte
* Starte `Erweiterungen -> Ink/stitch -> Sticken -> Befehle`
* Aktiviere die gewünschten Befehle und wenden sie an
* Bei Befehlen wo die Positionierung wichtig ist: Der Endpunkt des Zeigers, der dem Objekt am nächsten ist, ist der Punkt, an dem der Befehl ausgeführt wird.

Unter `Erweiterungen -> Ink/stitch -> Sticken -> Befehle` gibt es drei Optionen: `Befehle hinzufügen...`, `Ebenenbefehle hinzufügen...` und `Befehle mit gewählten Objekten verknüpfen...`.

### Befehle hinzufügen ...

Diese Befehle wirken sich auf das gesamte Motiv aus.

### ![stop position](/assets/images/docs/visual-commands-stop-position.jpg) Stopp-Position

Die Stickmaschine springt nach jedem Stopp-Befehl zu diesem Punkt. Das erleichtert die Applikationsarbeit, da man so den Rahmen zum Nutzer nach vorne bringen kann.

### ![origin](/assets/images/docs/visual-commands-origin.jpg) Nullpunkt

Dieser Befehlt definiert den Ursprung (0,0) für das Dokument. Nullpunkte sind besonders für diejenigen sinnvoll, die unabhängig vom Rahmen vollen Zugang zur gesamten Arbeitsfläche der Maschine haben.

## Ebenenbefehle hinzufügen …

Diese Befehle wirken sich auf die aktive Ebene aus.

### ![ignore layer symbol](/assets/images/docs/visual-commands-ignore-layer.jpg) Ebene ignorieren

Alle Objete in dieser Ebene werden nicht in die Stickdatei exportiert. Eine typische Anwendung wäre z.B. Beschreibungstext für ein Tutorial, der nicht von Ink/Stitch gerendert werden soll.

## Befehle mit gewählten Objekten verknüpfen …

Diese Befehle hängen sich an ausgewählte Objekte.

### ![starting point symbol](/assets/images/docs/visual-commands-start.jpg) ![ending point symbol](/assets/images/docs/visual-commands-end.jpg) Füllstich Anfangs- und Endposition

Definiert (1) die Start- und (2) die Endposition bei Objekten mit Füllstich.

#### ![ripple stitch target symbol](/assets/images/docs/visual-commands-ripple-target.png) Ripplestich Zielposition

Definiert den Zielpunkt für einen Ripplestich-Bereich.

### ![trim symbol](/assets/images/docs/visual-commands-trim.jpg) Faden trennen

“Faden trennen” tells the embroidery machine to cut the thread after the assigned object has been stitched. Not all home machines support the trim function within a color block. Mainly used to prevent long jump stitched between embroidery objects and to avoid post embroidery trimming by the operator.

### ![stop symbol](/assets/images/docs/visual-commands-stop.jpg) Stopp

Kommerzielle Stickmaschinen mit mehreren Nadeln laufen normalerweise von einer Farbe zur nächsten, ohne dazwischen zu pausieren. Manchmal möchte man eine Pause (z.B. zum Beschneiden von Applikationsstoff), so fügt “danach stoppen” einen zusätzlichen Farbwechsel hinzu, die einem speziellen Stoppbefehl unter Verwendung der Benutzerschnittstelle des Geräts (z. B. C00 auf Barudan-Maschinen) zugewiesen werden kann. Üblicher Anwendung hierfür ist, dass auflegen von Puffschaum. Benutzen von Applikationsstoff und / oder sogar verlangsamen der Maschine an einer bestimmten Stelle für verschieden Arten einer Stickerei, ohne die Maschine beaufsichtigen zu müssen.

### ![ignore symbol](/assets/images/docs/visual-commands-ignore.jpg) Objekt ignorieren

Objekte mit diesem Befehl werden nicht exportiert.

### ![satin cut point symbol](/assets/images/docs/visual-commands-satin-cut-point.jpg) Satin-Schnittstelle

Dieser Befehlt definiert an welchem Punkt die Satinsäule geschnitten werden soll. Benutze anschließend die Funktion “[Satinsäule schneiden](/de/docs/satin-tools/#satin-schnittstelle)”.

####  ![auto route starting position symbol](/assets/images/docs/visual-commands-auto-route-satin-stitch-start.jpg) ![auto route  ending position symbol](/assets/images/docs/visual-commands-auto-route-satin-stitch-end.jpg) Start- und Endposition für automatisch geführten Laufstich

Definiert (1) die Start- und (2) die Enposition für automatisch geführte Geradstiche. Benutze anschließend Die Funktion "[Werkzeuge: Linie > Automatisch geführter Geradstich ...]"(https://inkstitch.org/docs/stroke-tools/).

Nutze immer nur einen Anfangs- und einen Endpunkt für jede Operation.

###  ![auto route satin starting position symbol](/assets/images/docs/visual-commands-auto-route-satin-stitch-start.jpg) ![auto route satin ending position symbol](/assets/images/docs/visual-commands-auto-route-satin-stitch-end.jpg) Anfangs- und Endposition für automatische Satinsäulenführung

Definiert (1) die Start- und (2) die Endposition für automatish geführte Satinsäulen. Benutze anschließend die Funktion “[Automatische Satinsäulenführung](/de/docs/satin-tools/#automatische-satinsäulenführung)”.

Nutze immer nur einen Anfangs- und einen Endpunkt für jede Auto-Route Operation.

## Objektbefehle anzeigen/verbergen

Schalte die Sichtbarkeit von Objekt-Befehlen an und aus. Befehle funktionieren auch, wenn sie nicht angezeigt werden.

`Erweiterungen > Ink/Stitch > Befehle > Ansicht > Objektbefehle anzeigen|vergergen`

## Befehlsymbole skalieren

Anpassen der Größe der Befehlsymbole im gesamten Dokument: `Erweiterungen > Ink/Stitch > Befehle > Ansicht > Befehlsymbole skalieren...`

Use live preview to see the effect while scaling.
