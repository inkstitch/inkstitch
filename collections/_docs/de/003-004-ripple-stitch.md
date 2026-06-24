---
title: "Ripplestich"
permalink: /de/docs/stitches/ripple-stitch/
last_modified_at: 2025-12-29
toc: true
---
## Beschreibung

Ripple stich ist zum Teil Geradstich und zum Teil Füllstich: es verhält sich wie ein Geradstich (es kann beispielsweise als Dreifach-Geradstich genutzt werden) und definiert sich über eine Linie, aber das Stickergebnis erstreckt sich über eine Oberfläche. Ripples werden für lose Stickereien verwendet und sehen ein bisschen wie Wellen aus, daher auch der Name.

Geschlossene Formen werden mit einer Spirale gefüllt (z.B. Kreis). Bei offenen Formen (Linie mit Anfang und Ende) wird hin und her gestickt. Schauen wir uns beide Formen genauer an.

{% include folder-galleries path="butterfly-fill-project/ripple/" captions="1:Einfacher Ripple mit geschlossener Form;2:Satingeführter Ripplestich" %}

## Funktionsweise

{% include video id="cyvby3KJM10" provider="youtube" %}

### Geschlossene Formen

* Erstelle einen einfachen geschlossenen Pfad mit einer Linienfarbe (keine kombinierten Pfade aus mehreren Teilen)
* (Optional) Erstelle eine [Zielposition oder Führungslinien](#ripple-stiche-führen)
* Öffne die Parametereinstellungen (`Erweiterungen > Ink/Stitch > Parameter`) und setze die `Methode` auf `Ripple`.
* Stelle die übrigen [Parameter](#parameter) nach deinen Wünschen ein und klicke auf Anwenden

![Circular ripple examples](/assets/images/docs/circular-ripple.svg)

[Beispieldatei herunterladen](/assets/images/docs/circular-ripple.svg){: download="circular-ripples.svg" }

### Offene Formen

Lineare Ripples können auf verschiedene Weise erstellt werden. Sie können aus einer einfachen Kurve bestehen oder sogar wie eine Satinsäule konstruiert werden.

* Erstelle eine offene Form (einfache Linie, kombinierte Linien oder Satinsäule)
* (Optional) Erstelle eine [Zielposition oder Führungslinien](#ripple-stiche-führen)
* Öffne die Parametereinstellungen (`Erweiterungen > Ink/Stitch > Parameter`) und setze die `Methode` auf `Ripple`.
* Stelle die übrigen [Parameter](#parameter) nach deinen Wünschen ein und klicke auf Anwenden

![Linear ripple examples](/assets/images/docs/linear-ripple.svg)

[Beispieldatei herunterladen](/assets/images/docs/linear-ripple.svg){: download="linear-ripple.svg" }

## Schleifen

Schleifen (also sich selbst kreuzende Pfade) sind bei Ripple-Stichen erlaubt und willkommen. Nutze Schleifen um besondere, interessante Effekte zu erzielen.

![Looping ripple stitches](/assets/images/docs/ripple-loops.svg)

[Beispieldatei herunterladen](/assets/images/docs/ripple-loops.svg){: download="ripple-loops.svg" }

##  Ripple-Stiche führen

Ripples mit nur **einem Unterpfad** (geschlossene Formen oder einfache Bézier-Kurven) können mit jeder der folgenden Methoden geführt werden.

### Zielposition

Definiere eine Zielposition mit einem [visuellen Befehl](/de/docs/commmands/):

* Öffne `Erweiterungen > Ink/Stitch > Befehle > Befehle mit gewählten Objekten verknüpfen...`
* Wähle `Zielposition` und clicke auf Anwenden
* `Strg + Klick` auf das Symbol des Befehls um es auszuwählen, dann bewege es zur gewünschten Position

Wenn keine Zielposition definiert wurde, läuft der Pfad auf die Mitte des Objektes zu.

### Führungslinie

* Erstelle mit dem Bézier-Werkzeug eine Linie die in der Nähe der Ripple-Form startet und von ihr wegführt. Die neue Linie muss sich genau in der gleichen Gruppen (auch keine Untergruppe) befinden, wie die Ripple-Form.
* Wähle die Linie aus und wandel sie mit `Erweiterungen > Ink/Stitch > Bearbeiten > Auswahl zu Führungslinie` in eine Führungslinie um.
* Wähle die Ripple-Form aus und öffne die Parametereinstellungen. Ändere die Parameter bis das Ergebnis den Wünschen entspricht.

### Satin-Führung

Die Satin-Führung eröffnet die Möglichkeit die Ripplestiche genauer zu führen. Sowohl die Satin-Querstreben, als auch die Breite der Satinkolumne selber wirken sich auf die Ripplestiche aus. Ausschlaggebend für die spätere Positionierung ist nicht die Ripple-Form selbst, sondern die Position der Führungslinie. Zur Vereinfachung der Steuerung der finalen Breite ist es ratsam (aber nicht notwendig) die Satin-Führung so anzulegen, dass sie zu Beginn ungefähr der Breite der Ripple-Form entspricht.

* Erstelle eine [Satinsäule](/de/docs/stitches/satin-column/) mit Richtungslinien. Die Satinsäule muss sich genau in der gleichen Gruppen (auch keine Untergruppe) befinden, wie die Ripple-Form.
* Wähle die Satinsäule aus und wandel sie mit `Erweiterungen > Ink/Stitch > Bearbeiten > Auswahl zu Führungslinie` in eine Führungslinie um.
* Wähle die Ripple-Form aus und öffne die Parametereinstellungen. Ändere die Parameter bis das Ergebnis den Wünschen entspricht.

Das Muster für Satinsäulen-geführte Ripples können mit Hilfe einer sogenannten Ankerlinie in ihrer Richtug angepasst werden.

* Zeichne eine Linie von oben nach unten über das Muster. Die Positionierung entspricht denen der Richtungsvektoren.
* Wähle die Linie aus und markiere sie als Ankerlinie über `Erweiterungen > Ink/Stitch > Bearbeiten > Auswahl zu Ankerlinie`

![satin guided ripple](/assets/images/docs/ripple_satin_guide.svg)

[Download](/assets/images/docs/ripple_satin_guide.svg){: download="satin_guided_ripples.svg" }

## Clipping

{% include upcoming_release.html %}

Ripple stitches can be clipped to form the outline.

* Create the ripple stitch
* Create the clip shape (must be on top of the ripple stitch)
* Select both and run `Objekt > Ausschneidepfad > Ausschneidemaske setzen`

## Parameter

{% include upcoming_release_params.html %}

{% include params.html stitch_type='ripple-stitch'%}

## Ripple-Übersicht

![Many ripples](/assets/images/docs/en/rippleways_en.svg)

[Download](/assets/images/docs/en/rippleways_en.svg){: download="rippleways.svg" }

## Beispieldateien mit Ripple Stitch

{% include tutorials/tutorial_list key="stichart" value="Ripplestich" %}
