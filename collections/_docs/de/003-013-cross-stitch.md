---
title: "Kreuzstich"
permalink: /de/docs/stitches/cross-stitch/
last_modified_at: 2026-04-03
toc: true

feature_row:
  - image_path: /assets/images/docs/cross_stitch_coverage.jpg
    alt: "Cross stitch grid with a fill. Fields covered by the fill for more than 50% show a cross on top"
  - image_path: /assets/images/docs/cross_stitch_coverage02.jpg
    alt: "Same image as before, but the fill element has moved. More crosses are build"
---

{% include upcoming_release.html %}

## Beschreibung

Kreuzstich ahmt traditionelle Handsticktechniken nach.
Kreuzstich zeichnet sich durch kleine, gleichmäßige Kreuze aus, die dem gestickten Bild ein flaches, blockartiges Aussehen verleihen.

{% include folder-galleries path="butterfly-fill-project/cross/" captions="1:Kreuzstich mit einem schwarzen Rand mit Mehrfachgeradstichen" %}

## Funktionsweise

* Zeichne eine geschlossene Form mit einer Füllfarbe
* Öffne den Parameter-Dialog
* Wähle `Kreuzstich` als Füllmethode

### Gitter und der Füllabdeckung-Parameter

Es ist wichtig den Parameter `Füllabdeckung` zu verstehen.

Er bestimmt wieviel Prozent jedes Kreuz die Füllfläche überdecken muss. Das bedeutet, er hat einen Einfluss darauf, ob ein Kreuz an einer bestimmten Stelle gebildet wird oder nicht.

Kreuzstiche richten sich nach einem Gitter aus. Das Gitter selbst (in der Standarddefinition) richtet sich an der oberen, linken Ecke der Arbeitsfläche aus.

Ink/Stitch prüft nun für jedes Gitterfeld die prozentuale Abdeckung des Füllelements. Ist die Abdeckung höher als die im Parameter definierte Prozentzahl, wird ein Kreuz gebildet.

Im folgenden Beispiel sind nur die grünen Felder mit mehr als 50% von der schwarzen Füllung überdeckt und werden gestickt.
Wird das Element auf der Arbeitsfläche verschoben, werden mehr Kreuze gestickt.

{% include feature_row %}

Wird die Option `Gitter an Arbeitsfläche ausrichten` deaktiviert, kann das Element frei auf der Arbeitsfläche bewegt werden, ohne dass sich das Stickergebnis ändert.
Aber angrenzende Kreuzstichflächen können falsch ausgerichtet sein.
{: .notice--info }

### Kreuzstich-Methoden

Ink/Stitch kennt verschiedene Kreuzstich-Methoden.

* **Kreuzstich und Kreuzstich (gedreht)**

  Dies ist die gewöhnliche Kreuzstich-Methode. Zwei diagonale Stiche bilden ein Kreuz.
  Sind zwei Kreuze nur über die Diagonale verbunden, ist es sinnvoll einen kleinen Wert für die Option `Erweitern` festzulegen, um einen zusammenhängenden Stichablauf zu gewährleisten.

  ![Cross stitch method: cross stitch](/assets/images/docs/cross_stitch_method_cross_stitch.jpg)
* **Halbstich und Halbstich (gedreht)**

  Halbstich bildet ein halbes Kreuz (nur eine Diagonale). Verbundungsstiche verlaufen entlang der Außenlinie.

  ![Cross stitch method: half cross](/assets/images/docs/cross_stitch_method_half_cross.jpg)
* **Aufrechter Kreuzstich und aufrechter Kreuzstich (gedreht)**

  Ein gedrehter Kreuzstich, bildet ein aufrechtes Kreuz.
  Diese Stichart kann Sprungstiche beinhalten, wenn Flächen nur diagonal verbunden sind.

  ![Cross stitch method: upright cross](/assets/images/docs/cross_stitch_method_upright.jpg)

* **Kompakter aufrechter Kreuzstich und kompakter aufrechter Kreuzstich (gedreht)**

  Ein weiterer aufrechter Kreuzstich, der ein dichteres Stickbild erzeugt.

  Der Wert für die Füllabdeckung ist in diesem Beispiel 50%.

  ![Cross stitch method:  dense upright cross](/assets/images/docs/cross_stitch_method_dense_upright.jpg)

* **Doppeltes Kreuz und doppeltes Kreuz (gedreht)**

  Eine Kombination von Kreuzstichen und aufrechten Kreuzstichen. Das aufrechte Kreuz liegt unten.

  ![Cross stitch method: double cross](/assets/images/docs/cross_stitch_method_double_cross.jpg)

* **Smyrna Kreuz und Smyrna Kreuz (gedreht)**

  Eine Kombination von Kreuzstichen und aufrechten Kreuzstichen. Das aufrechte Kreuz liegt oben.

  ![Cross stitch method:Smyrna cross](/assets/images/docs/cross_stitch_method_smyrna.jpg)

### Kreuzstich-Assistent

Ink/Stitch kommt mit einer Erweiterung, die Kreuzstich-spezifische Aufgaben in einem Arbeitsablauf erledigen kann.

* Erstellen eines Seitengitters für die Stichpositionierung (als visuelle Unterstützung bei der Erstellung des Kreuzstichmusters)
* Kreuzstichparameter auf gewählte Füllstich-Elemente anwenden
* Füllstichelemente kombinieren und verpixeln (weniger Sprungstiche, bessere visuelle Repräsentation des Ergebnisses)
* Umwandeln von Rastergrafiken in Kreuzstich-Füllungen

Außerdem wird die aus den Gitter-Dimensionen erechnete Stichlänge der diagonalen Stiche angezeigt. Große Kreuze können durch die Eingabe eines Wertes für die maximale Stichlänge unterteilt werden.

[Mehr lesen](/de/docs/fill-tools/#kreuzstich-assistent)

### Anfangs- und Endpunkt festlegen

In der Standardeinstellung starten Füllelemente so nah wie möglich am zuvor gestickten Element und enden so nah wie möglich am nächsten Element.

Dieses Verhalten kann durch das Setzen von manuellen [Anfangs- bzw. Endpunken](/de/docs/commands/) überschrieben werden.

## Parameter

Öffne das Parameter-Dialogfenster (`Erweiterungen > Ink/Stitch  > Parameter`, um die Einstellungen zu verfeinern.

{% include params.html stitch_type='cross_stitch'%}

## Beispieldateien mit Kreuzstichen

{% include tutorials/tutorial_list key="stichart" value="Kreuzstich" %}
