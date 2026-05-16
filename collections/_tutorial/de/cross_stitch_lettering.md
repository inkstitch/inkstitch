---
permalink: /de/tutorials/cross_stitch_lettering/
title: "Kreuzstich Lettering"
language: de
last_modified_at: 2026-05-14
excerpt: "Kreuzstich-Schriftzüge erstellen"
image: "/assets/images/tutorials/tutorial-preview-images/hello.png"
tutorial-type: 
stitch-typ: 
 - Kreuzstich
tool:
techniques:
field-of-use:
user-level: 
toc: true
---

{% include upcoming_release.html %}

## Das Textwerkzeug nutzen

Die einfachste Methode ist eine wiederverwendbare, stickfertige Schrift aus dem Textwerkzeug zu nutzen. Ink/Stitch bietet mittlerweile über 20 Schriftarten.

Über den Kategorie-Filter (Dropdown-Menü in der oberen rechten Ecke) kann die Schriftartenliste schnell auf Kreuzstich-Schriftarten reduziert werden.

![cross stitch font selection](/assets/images/tutorials/cross_stitch_lettering/de/choix_point_de_croix.jpg)

Kreuzstichschriftarten funktionieren genauso, wie alle anderen Schriftarten auch.

## Eine Pixelschriftart für individuelle Beschriftungen nutzen

Es gibt viele Pixelschriftarten. Auf [fonts.google.com](https://fonts.google.com) kann sogar mit einem Filter gezielt danach gesucht werden.
Aber auch anderswo kann man fündig werden.

Für dieses Tutorial nutzen wir die Doto-schriftart von fonts.google.com

![doto](/assets/images/tutorials/cross_stitch_lettering/doto.jpg)

Wir nehmen an, dass diese Schrift auf deinem Computer installiert ist.

Beachte: Wenn du eine neue Schrift installierst, kann es nötig sein **Inkscape** neu zu starten. Erst dann wird die Schrift im Programm erscheinen.

Unser Ziel ist es, jeden "Pixel" der Schrift in ein Kreuz zu verwandeln. Für eine Verwendung mit dem üblichen 40wt Garn, ist ine Schrifthöhe zwischen 1.8 mm und 4 mm sinnvoll.
Dünneres Garn erlaubt auch kleinere Buchstaben, mit dickerem Garn, darf die Schrift weiter vergrößert werden.

### Arbeitsablauf

Die Schritte sind folgende:

- Unter `Bearbeiten > Einstellungen > Benutzeroberfläche > Ursprung in der oberen linken Ecke, wobei die y-Achse nach unten zeigt` ist aktiviert
- Entscheide dich für die Größe der Kreuze: in diesem Beispiel nutzen wir eine Größe von 3 mm. Diese größe ist für alle verfügbaren Kreuzsticharten von Ink/Stitch brauchbar.
- Erstelle ein Seitengitter mit 3 mm Abstand auf beiden Achsen (x und y). Dies kann entweder über die Dokumenteinstellungen geschehen oder über den Kreuzstich-Helfer.
  Wähle alle Objekte ab (keine aktive Auswahl) und öffne `Erweiterungen > Ink/Stitch > Werkzeuge: Füllung > Kreuzstich-Helfer`. Setze den gewünschten Gitterabstand im Einstellungs-Tab und
  aktiviere das Seitengitter im Tab für die Ausgabe-Optionen.
- Aktiviere das Inkscape Textwerkzeug mit `T` oder über die Werkzeugleiste. Versichere dich, dass eine Füllfarbe, aber keine Konturfarbe aktiviert ist.
- Wähle die Doto-Schrift aus dem Dropdown-Menü aus.
- Klicke auf die Arbeitsfläche und gib einen Text ein.
- Wenn nötig, skaliere die Schrift, bis sich nur noch ein "Pixel" der Schrift in einer Gitterzelle befindet.

![hello1](/assets/images/tutorials/cross_stitch_lettering/hello1.jpg)

- Konvertiere den Text in einen Pfad (`Pfad > Objekt in Pfad umwandeln`)
- Wähle den Pfad aus und öffne den Kreuzstich-Helfer (`Erweiterungen > Ink/Stitch > Werkzeuge: Füllung > Kreuzstich-Helfer`).

![hello1](/assets/images/tutorials/cross_stitch_lettering/de/assistant1.jpg)

Im Einstellungs-Tab gibt es zwei wichtige Parameter, die sind:

- Horizontaler Gitterabstand
- Füllabdeckung (%): Da die "Pixel" kleiner sind als eine eigentliche Gitterzelle, sollte dieser Wert nicht zu groß sein.
- Die gewählte Kreuzstich-Methode kann ebenfalls schon hier gesetzt werden. Hierfür muss im Ausgabe-Tab die Option `Parameter` angewählt sein.
- Ebenfalls im Ausgabe-Tab sollte unbedingt die Option `Verpixeln` aktiviert sein.

Nach dem Anwenden des Kreuzstich-Helfers wird der Schriftpfad entsprechend verpixelt sein:

![pixelateandparams](/assets/images/tutorials/cross_stitch_lettering/en/pixelateandparams.jpg)

Jeder Buchstabe ist nun eine einzige Form; Sprungstiche entstehen nur zwischen den Buchstaben.

### Ein Überfluss an Informationen?

Du kannst diesen Part gerne überspringen, aber wenn du einen tieferen Einblick gewinnen möchtest, lies gerne weiter.

Als Erinnerung: der Kreuzstich-Helfer hat drei im wesentlichen **unabhängige** Funktionen die wir nutzen können:

- Seitengitter erstellen. Dies ist ein optionales, rein visuelles Werkzeug. Es hat keinen Einfluss auf die Funktionalität.
  Das Seitengitter hilft aber, die Positionierung der Stiche zu erkennen und die Füllabdeckung der Gitterzellen abzuschätzen.
  Das Gitter kann über den Kreuzstich-Helfer oder über die Dokumenteinstellungen eingerichtet werden.
- Stickparameter. Stichparameter können entweder über den Kreuzstich-Helfer oder über die Ink/Stitch Parameter angewendet werden.
  Der Kreuzstich-Helfer setzt dabei auf jedes Element einen kleinen Wert für den `Erweitern`-Parameter. So kann für die meisten Kreuzstich-Methoden
  das Auftrennen von Formen an Stellen verhindert werden, die sich nur an einer Ecke berühren.
- Verpixeln. Diese Option modifiziert die Formen: jedes Mal wenn der Wert für die Füllabdeckung für eine Gitterzelle überschritten wurde, wird die gesamte Zelle gefüllt.
  Berühren sich zwei Zellen, werden sie verbunden.
  Im vorangegangenen Beispiel wurden die einzelnen "Pixel" in der Schrift zu einer einzigen Form zusammengefügt.
  Die Verpixelung erfolgt für die angegebene Gittergröße; wird die Gittergröße nachträglich angepasst, gibt die Form nicht mehr die Form des gestickten Pfades wieder!

Was wäre passiert, wenn wir nur die Option `Parameter`, nicht aber `Verpixeln` angewählt hätten?

In diesem Fall, wären nur die Parameter angepasst worden. Die Form aber wäre gleich geblieben.

Rufen wir nun die Parameter-Erweiterung mit der angewählten Form auf, erhalten wir dieses Ergebnis:

![pixelateandparams](/assets/images/tutorials/cross_stitch_lettering/de/cross_stitch.jpg)

Jedes Kreuz füllt weiterhin die kompletten Gitterzellen aus und das obwohl die Form nicht erpixelt ist.

Die Parameter werden aber auf die ursprünglichen Formen angewandt. D.h. auf jeden einzelnen "Pixel". So wie mit jeder anderen Ink/Stitch Füllung,
sucht sich Ink/Stitch eine eigene Sortierung für kombinierte Pfade. Dies kann funktionieren, aber z.B. im `e` werden die Probleme offensichtlich.

Die Anordnung der Quadrate wird offensichtlicher, wenn die Standardfüllung angewendet wird:

![pixelateandparams](/assets/images/tutorials/cross_stitch_lettering/de/autofill.jpg)

Das Verpixeln hat daher gleich zwei Vorteile:

- eine bessere visuelle Repräsentation des finalen Ergebnisses: es wird ersichtlich, wie viel Raum die Stickerei einnehmen wird (vorausgesetzt, dass die Angaben der Gittergröße mit den Parametern übereinstimmt)
- ein besseres Stickergebnis: zusammenhängende Gitterzellen sind zu einer Form zusammengefügt und was zur Vermeidung von Sprungstichen beiträgt.

Kreuzstiche funktionieren aber auch ohne die Verpixelung der Form.

## Schriftvielfalt

Es ist tatsächliche möglich, fast jede Schrift auch als Kreuzstich zu nutzen. Das ist manchmal auch gar nicht so schwer.

### Beispiel mit einer Script-Schriftart (Handschrift)

Wir nutzen für dieses Beispiel die Great Vibes Schrift, die auch unter fonts.google.com zu finden ist.

![great vibes](/assets/images/tutorials/cross_stitch_lettering/great_vibes.jpg)

Grün: so sieht das Ergebnis mit dem Inkscape Textwerkzeug aus. Beachte die Überschneidungen im H und im e. Dort ist die Schrift nicht komplett schwarz.

Ein einfacher Weg eine schwarze Form zu erhalten ist dieser:

- Wähle den Text aus
- `Text > Text zerlegen`
- Wähle alle Elemente aus und kombiniere sie mit `Pfad > Vereinigen`

Für ein zufriedenstellendes Ergebnis ist es am Besten eine größere Anzahl an Kreuzen zu haben. Daher ist der Text im Beispiel 60 mm hoch und die
das Kreuzstichgitter umfasst 2 mm. Es ist offensichtlich, dass mehr Kreuze eine größere Flexibiliät mit der Form des Originaltextes ermöglichen.

Verpixeln ist nicht unbedingt notwendig, erlaubt es jedoch einen besseren visuellen Eindruck des Endergebnisses zu bekommen (drittes Bild von oben).

Unten ist die Sticksimulation dargestellt.

Mit einer Handschriftart wie dieser, erhalten wir keinerlei Sprungstiche.

### Unverbundene Schriftarten

Wir benutzen in diesem Beispiel die Audiowide-Schrift, die ebenfalls auf fonts.google.com zum Download zur Verfügung steht.

Es ist eine Schrift mit annähernd konstanter Breite und ist nicht zu detailreich, was sie zu einer idealen Schrift für diese Übung macht.

![audiowide](/assets/images/tutorials/cross_stitch_lettering/audiowide.jpg)

* In grün dargestellt ist das direkte Ergebnis aus dem Inkscape Textwerkzeug.

Für unverbundene Schriftarten ist es wichtig, die einzelnen Buchstaben gut auf dem Gitter zu platzieren.

Hier eine Schritt für Schritt Anleitung:

* Wähle den Text aus und wende die Funktion `Text > Text zerlegen` an.

  Nun kann jeder Buchstabe einzelnd bewegt werden; hier ist das Ergebnis:

  ![positioning](/assets/images/tutorials/cross_stitch_lettering/positioning.jpg)
* Konvertiere jeden Buchstaben in einen Pfad (`Pfad > Objekt in Pfad umwandeln`).
* Verpixele die Buchstaben und wende die Stickparameter mit dem Kreuzstich-Helfer an.

  Du kannst die SVG-Vorschua benutzen um verschiedene Werte für die Füllabdeckung zu testen.

  ![svg preview](/assets/images/tutorials/cross_stitch_lettering/de/svg_preview.jpg)

Das Ergebnis wird hier in braun dargestellt; es kann manuell bearbeitet werden, z.B. um die Symmetrie im `o` zu verbessern (rot).

Dieses Mal wird jeder einzelne Buchstabe ohne Sprungstiche gestickt. Sprungstiche zwischen den Buchstaben sind unvermeidbar,
bzw. können nur durch einen Zwischenstich überbrückt werden.
