---
permalink: /de/tutorials/image_to_cross_stitch/
title: "Vom Bild zum Kreuzstich"
language: de
last_modified_at: 2026-05-17
excerpt: "Mit dem Kreuzsich-Helfer ein Bild in Kreuzstichfüllungen umwandeln"
image: "/assets/images/tutorials/tutorial-preview-images/cross_stitch_cat.jpg"
tutorial-type:
stichart:
 - Kreuzstich
werkzeug:
 - Füllung
techniques:
field-of-use:
user-level: 
---
{% include upcoming_release.html %}
Der Kreuzstich-Helfer ist eine große Hilfe, wenn es darum geht, Bilder in Kreuzstich-Füllungen umzuwandeln.

Da Ergebnis der in diesem Tutorial beschriebenen Schritte, befindet sich in dieser Datei:

![SVG](/assets/images/tutorials/image_to_cross_stitch/pawpedia.svg)

[Herunterladen](/assets/images/tutorials/image_to_cross_stitch/pawpedia.svg){: download="pawpedia.svg" }


## Ursprungsbild

Der Prozess wird einfache und effizienter sein, wenn das Bild einfach ist, d.h. wenige Farben enthält und klar abgegrenzte Farbbereiche aufweist.

Je einfacher da Ursprunsbild, desto weniger Nacharbeit ist am Ende erforderlich.

In diesem Tutorial verwenden wir als Ursprungsbild ein Bild von Pawpedia auf [Pixabay](https://pixabay.com/de/illustrations/image-10216974).
Es ist lizensiert von Pixabay und erlaubt Modifikationen. 

Zunächst müssen folgende Parameter festgelegt werden:

- Skaliere da Bild auf die gewünschte Größe der gesamten Stickerei (180 mm x 270 mm in diesem Beispiel)
- Überlege schon jetzt, wie groß die Kreuze werden sollen (2 mm in diesem Beispiel)

## Mit dem Kreuzstich-Helfer die Kreuzstich-Füllungen ersellen

Wähle das Bild aus und öffne den Kreuzsich-Helfer (`Erweiterungen > Ink/Stitch > Werkzeuge: Füllung > Kreuzsich-Helfer`)

- Im Einstellungs-Tab:
  - Setze die Werte auf die Standarteinstellungen zurück (unten links)
  - Setze den horizontalen Gitterabstand (hier: 2 mm)
- Experimentiere im Bitmap-Einstellungs-Tab mit den verschiedenen Parametern, bis du mit dem Ergebnis zufrieden bist.

  ![cat](/assets/images/tutorials/image_to_cross_stitch/de/cat_settings.jpg)

  Um die Farbregionen einfacher erkennbar zu machen, habe ich hier die Sättigung hoch eingestellt, was die Ursprungsfarben abändert.

  Wenn dein Computer nicht zu langsam ist, ist es hilfreich die SVG-Vorschau zu aktivieren.
  Aber auch die Vorschau des einfachen Bildes hilft bereits die richtigen Farbeinstellungen zu finden.

  In diesem Beispiel war es nicht möglich, den mehrfarbigen Hintergrund komplett zu entfernen.

  Beachte, dass die Anzahl der Farben, die Farben der Hintergrundfarbe miteinschließt, egal ob, ob sie entfernt wird oder nicht.
  Die Zahl ist außerdem nur eine Maximalangabe. Abhängig vom Urprungsbild wird Ink/Stitch wird nicht immer genau diese Anzahl an Farben einfügen.

Das Ergebnis ("first_result" Ebene) ist ein Anfangspunkt für weitere Verbesserungen.

## Formen und Stickerei verbessern

- Entferne die unerwünschten Bereiche des Hintergundes.

- Füge Schnurrhaare und andere Haare hinzu. Die weißen Haar im Originalbild sind nicht breit genug und werden vom Kreuzstich-Helfer nicht berücksichtigt.

  Zeichne die Haare dabei mit dem Bézier-Werkzeg (Zeichenwerkzeug) **über** die Kreuzsich-Füllungen. Kümmere dich dabei noch nicht um die Pixel.
  Ich nutze dabei ein Konturbreite von 3 mm. Anschließend konvertiere ich die Pfade in Füllungen (`Pfad > Kontur in Pfad umwandeln`).

  Nun wähle ich sowohl die gezeichneten Haare, als auch die Gruppe mit den Kreuzsich-Füllungen des restlichen Bildes aus und öffne den Kreuzstich-Helfe erneut.

  Mit Hilfe des Kreuzstich-Helfers wollen wir nun die Haare mit dem reslichen Bild vereinen.
  Hierzu aktiviere unter den Augabe-Optionen `Verpixeln` und `Überlappungn entfernen`.
  Mit diesem Einstellungen werden die gesamtn Formen neu berechnet und ohne Übershneidungen ausgegeben.

Während des Verbesserungsprozesses, wirst den den Kreuzstich-Helfer imme wieder nutzen.

Mit diesem Ursprungsbild is es unvermeidbar, dass sehr kleine Farbregionen entstehen (mit nur einem ode zwei Pixeln).
Da bedeutet, es entstehen unvebundene Formen, die wiederrum viele Sprungsiche oder Fadenshnitte hervorrufen.

- Für sehr kleine Farbregionen setze ich gerne eine Fabe die bereits in den anrenzenden Feldern vorhanden ist:
  wähle die kleine Fabregion aus, dann aktivire die Fabpipette (`D`) und klicke auf ein angrenzendes Feld.

- Ich versuche Felde gleicher Fabe zu vebinden, wenn sie fast angrenzend sind.
  Für die meisten Kreuzsicharten ist es ausreichend, wenn sich die Felder an nur einr Ecke berühren.

  Dies kann erreicht werden, indem bereits exisierende Formen angepasst werden oder indem ein verbindendes Element oberhalb der Kreuzsich-Füllungen hinzugefügt wird.

Nachdem ein visuell zufriedenstellendes Ergbnis erzielt wurde, denke daran, alles auszuwählen und die Formen mit dem Kreuzstich-Helfer neu zu berechnen.
Somit werden Regionen gleiche Fabe zu eine Form zusammengefügt.

Es muss dabei eine gute ein Balance zwischen dem visuellen Eindruck im Vergleich zum Originalbild und de Vereinfachung für die Stickerei gefunden werden.

Das Ergebnis dieses Schrittes befindet sich in der Ebene mit dem Name `tweaking the shapes`.

## Die endgültigen Farben festlegen

Wenn du magst, kannst du ketzt noch die Farben so festlegen, dass sie mehr dem Originalbild entspechen.
Dabei macht es Sinn, sich auf die Farben zu beschränken, die deiner vorhandnen Garnfarbenpalette entsprechen.

Das Endergebnis ist in der Ebene `changing_colors` ersichtlich.
