---
permalink: /de/tutorials/circular-monogram/
title: "Monogramm mit Spiralfüllung"
language: de
last_modified_at: 2023-05-04
excerpt: "Monogramm mit Spiralfüllung"
image: "/assets/images/tutorials/tutorial-preview-images/circular_monogram.jpg"
tutorial-type:
stichart:
  - Spiralfüllung
werkzeug:
  - Füllung
  - Linie
---

{% include upcoming_release.html %}

![Stickerei](/assets/images/tutorials/tutorial-preview-images/circular_monogram.jpg)

Dieses Tutorial bezieht sich nicht auf das Text-Werkzeug von Ink/Stitch
{: .notice--info }

Diese Methode kann nicht auf sehr kleine Buchstaben angewandt werden (bis zu 5 cm Höhe ist ok)
{: .notice--warning }

Für einen schnellen Start können entweder bereits im PC installierte Monogramm-Schriftarten genutzt werden ([z.B. Round Monogram](https://www.dafont.com/round-monogram.font)),
oder es kann ein Monogramm mit Hilfe von beispielsweise der Webseite [Makemonogram](https://www.makemonogram.com/monogram-maker) erstellt werden.

In diesem Tutorial starten wir mit diesem Monogramm:

![starting-points](/assets/images/tutorials/circular_monogram/starting-point.jpg)

## Die Buchstaben mit einer Spirale füllen
 
Bei der Verwendung einer im System installierten Schrift, muss das Textobject zunächst in einen Pfad umgewandelt werden (`Umschalttaste + Strg +C)`

Dann führe der Reihe nach folgende Schritte durch:

* Wähle die 3 Pfade für die Buchstaben (sie sollten eine Füllung und keine Kontur haben)
* `Erweiterungen > Ink/Stitch > Params`
* Wähle als Füllmethode `Spiralfüllung`
  * Entferne das Häkchen von `Verbindungsstiche innerhalb des Objekts`
  * Entferne die Unterlage
  * Setze deine bevorzugten Parametereinstellungen

![parametres](/assets/images/tutorials/circular_monogram/parameters.jpg)

Jeder Buchstabe wird nun mit Kreisen rund um den eigenen Mittelpunkt gefüllt.

Um nun allen Kreisen den gleichen Mittelpunkt zu geben, muss eine Zielposition festgelegt werden:

* Wähle alle 3 Buchstaben aus
* `Erweiterungen > Ink/Stitch > Befehle > Befehle mit gewählten Objekten verknüpfen...`
* Aus der Liste wähle den Befehl `Zielposition` und klicke auf Anwenden
* Bewege die 3 Symbole nun alle auf die selbe Position
* Überprüfe das Ergebnis mit der Simulation

## Die Satinstich-Umrandung erstellen

Der 4. Pfad ist ebenfalls eine Füllung, die wir wie folgt in eine Satinsäule umwandeln:

* `Erweiterungen > Ink/Stitch > Werkzeuge: Linie > Füllung zu Linie` 
* Deaktiviere die möglichen Optionen und klicke auf Anwenden
 
 ![after_fill_to_stroke](/assets/images/tutorials/circular_monogram/fill_to_stroke.jpg)
 
  Wähle den neu erstellten Pfad aus
 
 * `Pfad > Vereinfachen`
 
 * `Erweiterungen > Ink/Stitch > Werkzeuge: Satin > Linie zu Pfadeffekt-Satin...`

 ![satin_path_effet_before](/assets/images/tutorials/circular_monogram/satin_path_effect_before.jpg)
 
 * Anwenden
 
  ![satin_path_effet_after](/assets/images/tutorials/circular_monogram/satin_path_effect_after.jpg)
  
  * Schließe das Dialog-Fenster

Nun kann das Satinmuster geändert werden:

* Wähle die Satinsäule aus
* `Pfad > Pfadeffekte...`
* Klicke auf `Auf der Arbeitsfläche bearbeiten` unter `Quelle des Musters`

 ![satin_path_effet_after](/assets/images/tutorials/circular_monogram/pattern_before.jpg)

* Modifiziere das Muster: hier wurde eine Außenlinie begradigt und die Breite etwas erhöht

  ![satin_path_effet_after](/assets/images/tutorials/circular_monogram/pattern_after.jpg)

  Die Änderungen können direkt auf der Arbeitsfläche mitverfolgt werden.

Die Datei ist fertig zum sticken. Der Pfadeffekt kann für spätere Anpassungen beibehalten werden.
