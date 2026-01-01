---
title: "Kreuzstich"
permalink: /de/docs/stitches/cross-stitch/
last_modified_at: 2025-12-2
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

![Cross stitched froq in double cross style](/assets/images/upcoming/3.3.0/cross_stitch.jpg)

# Funktionsweise

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
* **Doppeltes Kreuz**

  Eine Kombination von Kreuzstichen und aufrechten Kreuzstichen. Da auch hier aufrechte Kreuzstiche enthalten sind, sind auch hier Sprungstiche bei nur diagonal verbundenen Flächen möglich.

  ![Cross stitch method: double cross](/assets/images/docs/cross_stitch_method_double_cross.jpg)

### Kreuzstich-Helfer

Ink/Stitch kommt mit einer Erweiterung, die Kreuzstich-spezifische Aufgaben in einem arbeitsablauf erledigen kann.

* Erstellen eines Seitengitter für die Stichpositionierung (als visuelle Unterstützung bei der Erstellung des Kreuzstichmusters)
* Kreuzstichparameter auf gewählte Füllstich-Elemente anwenden
* Füllstichelemente verpixeln, so dass sie die Stichpositionen besser abbilden

Außerdem wird die aus den Gitter-Dimensionen erechnete Stichlänge der diagonalen Stiche angezeigt. Große Kreuze können durch die Eingabe eines Wertes für die maximale Stichlänge unterteilt werden.

[Mehr lesen](/de/docs/fill-tools/#kreuzstich-helfer)

### Anfangs- und Endpunkt festlegen

In der Standardeinstellung starten Füllelemente so nah wie möglich am zuvor gestickten Element und enden so nah wie möglich am nächsten Element.

Dieses Verhalten kann durch das Setzen von manuellen [Anfangs- bzw. Endpunken](/de/docs/commands/) überschrieben werden.

## Parameter

Öffne das Parameter-Dialogfenster (`Erweiterungen > Ink/Stitch  > Parameter`, um die Einstellungen zu verfeinern.

Einstellung                        ||Beschreibung
---|---|---
Automatisch geführte Füllstiche    | ☑ |Muss aktiviert sein, damit diese Einstellungen wirksam werden.
Füllmethode                        |Kreuzstich| `Kreuzstich` auswählen
Kreuzstich-Methode                 ||Wähle eine Methode. Für detailierte Informationen siehe oben.
Mustergröße                        ||Definiert die Größe des Kreuzstichgitters
Gitter an Arbeitsfläche ausrichten ||Dies gewährleistet eine gute Ausrichtung benachbarter Kreuzstichbereiche, bedeutet jedoch auch, dass sich das Ergebnis ändern kann, wenn das Element verschoben wird.<br>Ist die Option deaktiviert, wird das Element unabhängig von seiner Position auf der Leinwand immer gleich gestickt wird.
Gitter-Versatz                     ||Verschiebt das Gitter um die angebenen Werte. X und Y Werte werden durch ein Leerzeichen getrennt angegeben. Ist nur ein Wert definiert, wird er für beide Richtungen verwendet.
Erweitern                          |![Expand example](/assets/images/docs/params-fill-expand.png) |Erweitern der Form vor dem Füllstich, um Lücken zwischen den Formen auszugleichen.<br>Für den Kreuzstich wird ein kleiner Wert (z.B. 0.1) empfohlen.
Maximale Füllstichlänge            |![Stitch length example](/assets/images/docs/params-fill-stitch_length.png)|Normalerweise mindestens die Länge der Kreuzstichdiagonalen. Große Kreuze können mit einem kleineren Wert unterteilt werden.
Mehrfachgeradstich Anzahl der Wiederholungen || ◦ Jeden Stich vervielfachen.<br/>◦ Ein Wert von 1 würde jeden Stich verdreifachen (vorwärts, rückwärts, vorwärts).<br/>◦ Ein Wert von 2 würde jeden Stich fünffach ausführen, usw.<br/>◦ Gilt nur für den Geradstich.
Minimale Stichlänge             || Überschreibt die globale Einstellung für die minimale Stichlänge. Stiche, die kleiner sind als dieser Wert werden entfernt.
Minimale Länge für Sprungstiche || Überschreibt die globale Einstellung für die minimale Länge für Sprungstiche. Kleinere Entfernungen zum nächsten Objekt haben keine Vernähstiche.
Vernähen erlauben               || Vernäht bei Bedarf an den ausgewählten Positionen
Vernähen erzwingen              || Vernäht den Faden nach diesem Element, auch dann, wenn der Abstand zum Folgeobjekt geringer ist als in den [Ink/Stitch Einstellungen](/de/docs/preferences/) definiert.
Anstecher                       || Wähle die [Anstecher](/de/docs/stitches/lock-stitches) Variante (Anfang).
Verstecher                      || Wähle die [Verstecher](/de/docs/stitches/lock-stitches) Variante (Ende).
Stopp                           || Stoppt die Maschine nachdem dieses Objekt genäht wurde und springt zur Stopp-Position (sofern vorhanden)
Fadenschnitt                    || Schneidet den Faden nachdem dieses Objekt genäht wurde
{: .params-table }

### Beispieldateien mit Kreuzstichen

{% include tutorials/tutorial_list key="stichart" value="Kreuzstich" %}
