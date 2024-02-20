---
title: "Text"
permalink: /de/docs/lettering/
last_modified_at: 2023-02-12
toc: true
---
## Text-Werkzeug

Das Text-Modul erzeugt mehrzeiligen Text. Die hinterlegten Schriftarten wurden von Community-Mitgliedern zur direkten Verwendung digitalisiert. Es gibt bereits Schriftarten die auf Satinsäulen beruhen, Applikations-, Füllstichschriften und Geradstichschriften. 

![Lettrage Extensions](/assets/images/docs/de/lettering.png)

## Anwendung

* Öffne `Erweiterungen > Ink/Stitch > Text`.
* Gib deinen Text ein (mehrzeilig möglich).
* Lege die Schriftart und die Skalierung fest.
* **⚠ Warnung**: Beachte die angegebenen Limitierungen auch bei späteren manuellen Skalierungen.
* Klicke auf `Anwenden und schließen`.
* Der eingegebene Text erscheint über der Seite.
* Freie Positionierung ist nun möglich.

  
### Font filters

* **Schriftgrößenfilter**<br>
  Schriften sind für eine bestimmte Skalierung digitalisiert. Der Schriftgrößenfilter hilft dir eine Schrift mit der richtigen Größe zu finden, indem er die
  Liste der Schriftarten nach der angegebenen Größe filtert.
  Ein aktivierter Filter (nicht 0) setzt bei der Auswahl einer Schriftart automatisch die Skalierung passend zur Suchgröße.
  
{% include upcoming_release.html %}
* **Glyphs**<br>
 If checked only the fonts that contain all the glyphs of your text are listed

* **Font family**<br>
Filter the fonts by families, by example get only the applique fonts or only the script fonts


### Optionen

* **Sticke Textzeilen vor und zurück**<br>
  Wenn diese Option aktiviert ist, wird die erste Zeile von links nach rechts gestickt und die zweite von rechts nach links usw.
  Dadurch muss die Stickmaschine weniger hin und herspringen, und die Laufzeit der Datei verkürzt sich.

* **Schnittmarker hinzufügen**<br>
   Wenn diese Option aktiviert ist, fügt Ink/Stitch für jeden Buchstaben Schnittbefehle hinzu.

### Voreinstellungen

Hier kann eine Liste mit den beliebtesten Schriftarten gespeichert und wieder geöffnet werden.

## Schrift entlang Pfad

Ink/Stitch Schriften sind liebevoll designed. Wenn sie mit Inkscape tools verformt werden (z.B. um sie in eine Kurve zu bringen) verliert das Ergebnis womöglich an Qualität. Auf der anderen Seite ist es ein langwieriger Prozess, die Buchstaben einzelnd an eine Linie anzupassen. Dieses Werkzeug hilft die, eine Schrift auf einen Pfad zu legen - ohne die Buchstaben zu verzerren.

### Anwendung

* Wähle eine Pfad und eine Ink/Stitch-Text-Gruppierung
* Öffne `Erweiterungen > Ink/Stitch > Schrift entlang Pfad ...`
* Ist `Strecken` aktiviert, wird Ink/Stitch die Buchstaben-Zwischenräume der Pfadlänge anpassen, so dass sich der Schriftzug über den gesamten Pfad erstreckt.
  Ist diese Option deaktiviert, bleiben die Buchstaben-Abstände unverändert.
* Klicke auf `Anwenden`

## Schrift-Bibliothek

Eine Übersicht über alle verfügbaren Schriftarten findet sich hier [Schrift-Bibliothek](/de/fonts/font-library/)

## Farben sortieren

Werden mehrere mehrfarbige Buchstaben gestickt, kann es sinnvoll sein zu viele Farbwechsel zu vermeiden.
Hier eine kurze Anleitung wie die Farben mehrfarbiger Ink/Stitch-Schriften schnell und einfach sortiert werden können:

* Wähle einen Buchstaben über den Ebenen und Objekte-Dialog
* Wähle den zuerst zu stickenden Pfad (der letzte Pfad dieser Gruppe)
* `Bearbeiten > Das Gleiche auswählen > Konturstil`
* Gruppiere die so entstandene Auswahl (Strg + G)
* Verschiebe diese Gruppe nach oben

Wiederhole diesen Prozess bis alle Farben gruppiert sind, wobei immer der zuerst zu stickende Pfad eines Buchstaben auszuwählen ist.

## Neue Schriftarten für Ink/Stitch erstellen

Weitere Infos zu diesem Thema findest du in einem eigenen [Schrifterstellungs Tutorial](/de/tutorials/font-creation/).

Kontaktiere uns wenn du deine Schriftart für die nächste Ink/Stitch Version zur Verfügung stellen willst: [GitHub](https://github.com/inkstitch/inkstitch/issues).
