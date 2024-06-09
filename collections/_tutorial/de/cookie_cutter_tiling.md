---
permalink: /de/tutorials/cookie_cutter_tiling/
title: "Kacheln"
language: de
last_modified_at: 2023-05-11
excerpt: "Gemusterte Füllungen mit dem Kachel-Pfadeffekt"
image: "/assets/images/tutorials/tutorial-preview-images/cookie_cutter_tiling.jpg"
tutorial-typ:
  - Text
  - Beispieldatei
stichart:
  - "Geradstich"
  - "Mehrfachgeradstich"
  - "Spiralfüllung"
techniques:
field-of-use:
werkzeug:
  - Linie
  - Füllung
  
user-level:
toc:
  true
---
![Gestickt](/assets/images/tutorials/tutorial-preview-images/cookie_cutter_tiling.jpg)

Dieses Tutorial erklärt, wie man eine Füllung mit einem sich wiederholendem Muster mit Hilfe des Pfadeffekts "Kacheln" erzeugt.

##  Der Pfadeffekt "Kacheln"

Dieser Pfadeffekt wiederholt einen Pfad (oder eine Gruppe von Pfaden) in Zeilen und Reihen. Es gibt viele Optionen für Abstände, Versatz, Rotationen und alle möglichen Arten von Spiegelungen.

Kacheln sind wirklich interessant für die Stickerei, sei es um gemusterte Füllungen zu erstellen oder um luftige Füllungen mit wiederholten Mustern zu kreieren.

Hier sind einige Muster-Beispiele:

![tiles](/assets/images/tutorials/cookie_cutter_tiling/all_png.png) 
[Datei herunterladen](/assets/images/tutorials/cookie_cutter_tiling/tiles_idea.svg){: download="tiles_idea.svg" }

Vielleicht erkennst du sie wieder, wie sie an dieser Wäscheleine hängen:
 
* T-shirt : erste Reihe, mittlere Kachel
* Kleid open: letzte Reihe, letzte Kachel
* Kleid unten: letzte Reihe, zweitletzte Kachel
* Badeanzug: mittlere Reihe, letzte Kachel

Der Gürtel wurde mit einer Spiralfüllung mit einem Mehrfachgeradstichmuster (0 2) gestaltet.

Für alle Designs in dieser Datei wurde der Pfadeffekt `Kacheln` auf eine Gruppe angewendet. Das ist viel einfacher als ihn auf die einzelnen Pfade zu kacheln.
Und auch leichter anzupassen: Pfade in der Gruppe können weiterhin angepasst werden oder sogar Pfade hinzugefügt oder entfernt werden. Das Resultat wird direkt auf der Arbeitsfläche sichtbar.
Im Pfadeffekt-Dialog kann die Anzahl der Reihen und Zeilen angepasst werden.

Spiele einfach mal mit den Mustern herum. Vielleicht kommst du ja auf ganz neue Muster. Es ist wirklich einfach und macht Spaß.

Hier nun eine Beschreibung, wie die Wäscheleine erstellt wurde.

## Kleidung vorbereiten

Warum die Kleidung zeichnen, wenn wir sie einfach herunterladen können?

Für die gezeigte Wäscheleine wurden drei SVG-Dateien von Bernd Lakenbrink vom [Noun Project](https://thenounproject.com/browse/collection-icon/clothes-icon-set-158916/?p=1) genutzt.

Die Dateien müssen trotzdem zunächst noch für unseren Anwendungsfall vorbereitet werden.

Lasst uns das [T Shirt](https://thenounproject.com/browse/icons/term/womans-shirt/) anpassen ...

Die SVG-Datei ist perfekt für den Bildschirm. Für die Stickerei aber, müssen wir feststellen, dass die Linie tatsächlich eine Füllung ist.
Mit der Ink/Stitch Erweiterung `Erweiterungen > Ink/Stitch > Werkzeuge > Füllung zu Linie` können wir das Problem aber schnell lösen.

Die vier Bilder unten sind von links nach rechts:
* Originales Bild
* So sieht es aus, wenn wir die Füllung entfernen und eine Konturfarbe setzen
* Das Ergebnis von `Füllung zu Linie`
* Was wir brauchen: eine geschlossene Form (orangene Füllung) und zwei zusätzliche Details (rot)

![T-Shirt](/assets/images/tutorials/cookie_cutter_tiling/Tshirt.png) 

Nachdem wir nun also das [T-Shirt](https://thenounproject.com/browse/icons/term/womans-shirt/) heruntergeladen haben
* Wähle alle Pfade des T-Shirts aus
* `Erweiterungen > Ink/Stitch > Werkzeuge: Füllung > Füllung zu Linie`
* Dies erzeugt die Mittellinien-Gruppe. Wähle darin die Pfade aus, die die äußere Form des T-Shirts abbilden (Pfade kobinieren oder teilen wenn nötig). Zusätzliche Details können nach Wunsch behalten werden.

Die cloth_line.svg Datei enthält alle vorbereiteten Teile in der  "Cloth Preparation"-Ebene und die Kacheln in der "Tilings"-Ebene.

Sie enthält auch die Ergebnisse aller einzelnen Schritte, bis hin zum fertigen Stickdesign.

Jeder Schritt in diesem Tutorial wird in einer anderen Ebenen der Datei dargestellt (von unten nach oben). Denke daran, die Ebenen zu entsperren und sichtbar zu machen, wenn du sie nutzen willst.
Nicht genutzte Ebenen können verriegelt und versteckt werden.

![cloth_line](/assets/images/tutorials/cookie_cutter_tiling/cloth_line.svg) 

[Download cloth_line.svg](/assets/images/tutorials/cookie_cutter_tiling/cloth_line.svg){: download="cloth_line.svg" }


## Überdecke jedes Kleidungsstück mit Kacheln

Im nächsten Schritt werden Muster ausgewählt um die Kleidungsstücke zu füllen.

Auf der Arbeitsfläche können die Kacheln rotiert und skaliert werden. Im Pfadeffekt-Dialog kann die Reihen- und Zeilenanzahl angepasst werden.

Versuche die Formen bestmöglich abzudecken, ohne zu viele Wiederholungen des Musters zu kreieren.

In der Ebene "Clothline preparing pattern fill" in der Datei `cloth_line.svg` kannst du ein Beispiel für eine mögliche Musterverteilung finden.

![cloth_line](/assets/images/tutorials/cookie_cutter_tiling/tiled_cloths.png) 

## Musterfüllung

Dies ist unser Ziel

![final](/assets/images/tutorials/cookie_cutter_tiling/final_embroidery.png) 

Und es ist einfach zu erreichen: folge einfach den folgenden Schritten in der richtigen Reihenfolge.

Für jedes Kleidungsstück haben wir eine Gruppe die folgendes enthält:
* Form: eine geschlossene Form die die Außenkontur des Kleidungsstücks bildet
* Details: Eine Gruppe mit zusätzlichen Linien, die am Ende über die gemusterte Füllung gestickt werden sollen
* Kacheln: die gekachelte Gruppe, die alle Kacheln enthält. Der Pfadeffekt befindet sich direkt auf der Gruppe

### Pfadeffekt Kacheln - ein Überblick

Schauen wir uns den Pfadeffekt "Kacheln" auf dem T-Shirt einmal genauer an

![starting_point](/assets/images/tutorials/cookie_cutter_tiling/T-shirt-1.jpg)

Das rot umrandete Auge aktiviert/deaktiviert den Pfadeffekt.

Später im Prozess wollen wir den Pfadeffekt in einen Pfad umwandeln. Die Funktion hierfür befindet sich im Menü rechts von dem Auge.

Über Symbole, wie beispielsweise dieses ![symbole](/assets/images/tutorials/cookie_cutter_tiling/tiling_moulin.jpg), können die Spiegelungen des Pfadeffekts definiert werden.

Um dies besser zu verstehen, vereinfachen wir den Pfadeffekt und setzen ihn auf nur zwei Wiederholungen in jede Richtung:

![starting_point](/assets/images/tutorials/cookie_cutter_tiling/tiling_moulin2x2.jpg)

Die rosa eingefärbte Spitze ist die Originalform. Die drei weiteren Formen zeigen die Spiegelung die auf die Reihen und Zeilen angewendet wird.

Klicke auf die verschiedenen Symbole und das Muster der Kacheln ändern sich. Probiere es aus und finde deinen Favoriten.

![mirroring](/assets/images/tutorials/cookie_cutter_tiling/mirroring.jpg)

Wenn du zufrieden bist mit den Modifikationen, wende den Pfadeffekt über das Menü in der rechten oberen Ecke des Pfadeffekts an (In Pfad umwandeln).

Nun ist path8 kein Dreieck mehr, sondern ein Pfad mit mehreren Unterpfaden mit vielen Kopien der Ursprungsform und der Pfadeffekt-Dialog ist verschwunden.

Wählst du den Pfad mit dem Knotenwerkzeug aus, sieht das Ergebnis so aus:

![flattened](/assets/images/tutorials/cookie_cutter_tiling/flattened.jpg)

Versuche nicht, den Pfad zu trennen, es gäbe viele Dreicke...

Manchmal ist ein weiterer Schritt nötig, der vor der Umwandlung in einen Pfad geschehen sollte:

### Pfade in gekachelten Gruppen kombinieren und Pfadeffekt anwenden

Kombiniere alle Pfade in der Kachel-Gruppe und wende den Pfadeffekt an:

Für jede Kachel-Gruppe:
* enthält die Gruppe mehr als nur einen Pfad, wähle alle Pfade an und kombiniere sie.
* wähle die Gruppe aus und wähle im Pfadeffekt-Dialog die Option `In Pfad umwandeln` (neben Auge und Papierkorb)

Auf der Arbeitsfläche sollte nach diesem Schritt alles genauso aussehen wie zuvor.

### Ausschneidepfad setzen

Für jede Kachel-Gruppe:
* Dupliziere die Außenkontur
* Wähle den gekachelten Pfad in der Kachelgruppe und die duplizierte Form (die über den Kacheln liegen muss)
* `Objekt > Ausschneidepfad > Ausschneidemaske setzen`

So sollte das Ergebnis aussehen:
![clipepd](/assets/images/tutorials/cookie_cutter_tiling/after_clip.png)

### Farben abstimmen

Für jede Kachel-Gruppe:
* Entferne die Füllfarbe von der nun übriggebliebene Außenkontur und nutze lediglich eine Konturfarbe
* Stelle sicher, dass die Farbe des Kachel-Musters und die der Außenkontur gleich sind
* Wenn die Details ebenfalls die gleiche Farbe haben sollen (wie im Beispiel), dann wende auch auf diese die gleiche Farbgebung an

### Parameter vorbereiten

* Wähle die Außenkontur, Kacheln und Details aus
* Öffne den Parameter-Dialog (`Erweiterungen > Ink/Stitch > Parameter`)

Für schöne Dreifachgeradstiche:
* Wähle `Geradstich / Mehrfachgeradstich` als Methode
* Setzte die Stichlänge auf 2 mm
* Setze Mehrfachgerade Wiederholungen auf 1

Ein Kleidungsstück nach dem Anderen:
* Wähle die ganze Gruppe
* Öffne `Erweiterungen > Ink/Stitch > Visualisieren und Exportieren > Stichplanvorschau ...`

So sollte das Ergebnis aussehen:

![Before_Autoroute](/assets/images/tutorials/cookie_cutter_tiling/before_autorouting.jpg)

Ist die Option "Sprungsstiche anzeigen" aktiv (Frosch), dann kann man gut erkennen, dass die Pfade noch geordnet werden müssen.

### Automatisch geführte Geradstiche

Für jede Kachel Gruppe:
* Wähle den Kachelpfad und die Außenkontur
* Öffne `Erweiterungen > Ink/Stitch > Werkzeuge: Linie > Automatisch geführter Geradstich`. Aktiviere nur die Option `Knoten an Überschneidungen hinzufügen`

Für jede Kachel Gruppe:
* Wähle die gesamt Gruppe
* `Erweiterungen > Ink/Stitch > Visualisieren und Exportieren > Stichplanvorschau...`

und du kannst sehen, dass die Sprungstiche nun weg sind.

In der Gruppe der automatisch geführten Pfade können nicht benötigte, sehr kleine Pfade zu finden sein. Sie könnten entfernt werden (Dokument bereinigen).
Über die Parameter oder als globale Einstellung kann die minimale Stichlänge auf 0.5 mm gesetzt werden.

### Abschließende Schritte

* Entferne alle leeren Gruppen
* Passe die Positionen der Kleidungsstücke an die Wäscheleine an

Haben die Details eine andere Farbe, sind die einzigen übriggebliebenen Sprungstiche hier zu finden und ein Sprung des letzten Stiches der Autoführung auf das erste Detail.

Hierfür hast du folgende Optionen:
* Sprungstiche belassen
* Schnittbefehle einfügen
* Sprungstiche in Pfade umwandeln

  Diese Option kann mit `Erweiterungen > Ink/Stitch > Werkzeuge: Linie > Sprungstich zu Linie` umgesetzt werden.
