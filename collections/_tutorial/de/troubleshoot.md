---
title: Fehlerbehebung in Ink/Stitch
permalink: /tutorials/troubleshoot/
last_modified_at: 2024-06-13
language: de
excerpt: "Fehlermeldungen gekonnt meistern"
image: /assets/images/posts/de/troubleshoot.png

tutorial-typ:
  - Text
stichart: 
techniques:
field-of-use:
user-level: 

toc: true
---

Keine Scheu einen Fehler oder nerviges Programm-Verhalten zu melden.
Entwickler sind auf eure Berichte angewiesen und freuen sich über jede Rückmeldung.
{: .info--notice}

## Element identifizieren

Tritt ein Fehler auf, ist es zunächst wichtig, das problematische Element ausfindig zu machen.
Dafür kann gut die Stickplan-Vorschau genutzt werden. Mit einem Tastenkürzel versehen, können
kleinere Gruppen oder einzelne Elemente schnell gerendert werden, bis das defekte Element genau
bestimmt worden ist.

## Problem lösen

Für das weitere Vorgehen ist die Art des aufgetretenen Fehlers entscheidend.

* Teilt Ink/Stitch euch mit, dass es sich um ein Fehler im Programm handelt, habt ihr die
  einmalige Gelegenheit dazu beizutragen Ink/Stitch zu verbessern und mit den freundlichen
  Entwicklern in Kontakt zu treten. Leider tragen hier die Ink/Stitch Standard-Tools meist
  wenig zur Problemlösung bei.
* Alle anderen Fehler können mit Bordmitteln einfach bearbeitet werden.

### Fehler im Programm (Traceback)

* Datei abspeichern
* Ist das problematische Element schon identifiziert, kann gerne schon nach Lösungen gesucht werden
  * Parameter löschen / ändern
  * Start-/Endpunkt ändern
  * Formveränderungen (z.B. schmale Stellen bei Füllstichen vermeiden)
  * was euch sonst noch so in den Kopf kommt - einfach ausprobieren
* Die letzte Zeile der Fehlermeldung kopieren und auf GitHub danach suchen:
  <https://github.com/inkstitch/inkstitch>
* Ist der Fehler noch nicht auf GitHub vermerkt, unbedingt einen Fehlerbericht an die
  Entwickler senden und die problematische SVG-Datei anhängen
  (<https://github.com/inkstitch/inkstitch/issues>).

Fällt es auf Englisch schwer, geht das auch auf Deutsch. Sogar über eine wortlose Meldung
mit dem kopierten Fehlerbericht und der SVG-Datei ist hilfreich. Alternativ kann auch eine
Mail an mich gesendet werden (kaalleen@inkstitch.org).

### Ink/Stitch-Werkzeuge zur Problemlösung

#### Fehlerbehebung an Objekten

`Erweiterungen > Ink/Stitch > Fehlerbehebung > Fehlerbehebung an Objekten`

![Fehlermeldungen mit Lösungsvorschlägen](/assets/images/docs/de/troubleshoot.jpg)
Fehlermeldungen mit Lösungsvorschlägen

[Fehlerbehebung an Objekten](/de/docs/troubleshoot/#fehlerbehebung) weist auf Fehler hin (rot) und
zeigt Warnungen für potenziellproblematische Pfade an (gelb).

Gleichzeitig werden Lösungsvorschläge gegeben deren Befolgung meist zu einer funktionierenden
Datei führen sollte.

Die im Bild gezeigten Fehler und Warnungen sind allerdings mittlerweile überholt, bzw.
überarbeitet. Sich kreuzende Außenlinien stellen zum Glück kein so großes Problem mehr dar.
Stattdessen wird hierfür eine Warnung ausgegeben, denn noch immer lassen sich die Stickpfade
besser optimieren, wenn das Element manuell zerlegt wurde (Ausnahmen bestätigen die Regel:
siehe Farbwechselreduktion für Tartanmuster bzw. Farbübergänge).

Es lohnt sich also, diese Funktion zu nutzen – auch wenn kein Fehler aufgetreten ist.

#### Dokument bereinigen

`Erweiterungen > Ink/Stitch > Fehlerbehebung > Dokument bereinigen`

Häufige Fehlerursachen sind zu kleine Elemente im Dokument, die entweder keine schönen
Ergebnisse liefern oder tatsächlich zu Fehlermeldungen führen.

Mit diesem Werkzeug lassen sie sich recht einfach entfernen. Auch leere Ebenen und Gruppen
können so mit einem Wisch beseitigt werden. Wer unsicher ist welche Werte hier eingetragen
werden sollen, kann auch einen Testlauf starten und sich die Namen und die Anzahl der zu
entfernenden Elemente vorher einmal anschauen oder sich eine Vorschau über die Live Preview
geben lassen (mit deaktiviertem Testlauf).

[Mehr Infos](/de/docs/troubleshoot/#dokument-bereinigen)

#### Element Info

`Erweiterungen > Ink/Stitch > Fehlerbehebung > Dokument bereinigen`

Ein Werkzeug für die Stickanalytiker unter euch. Hiermit können Maße und Stiche genauer
untersucht werden.

Noch ist dies eine recht einfache Liste. Fehlen euch bestimmte Angaben, könnt ihr mich gerne
kontaktieren oder auf GitHub eure Wünsche äußern.

[Mehr Infos](/de/docs/troubleshoot/#element-info)

#### Füllobjekte aufspalten

`Erweiterungen > Ink/Stitch > Fehlerbehebung > Dokument bereinigen`

Wer Ink/Stitch schon mehrere Jahre nutzt weiß, dass sich kreuzende Linien eine nervige
Angelegenheit waren. Aus dieser Situation heraus ist dieses Werkzeug entstanden, das
glücklicherweise an Bedeutung verloren hat. Trotz der verbesserten Lage verzweifelter Ink/Stitch-
Nutzer hat es dennoch nicht vollends seinen Sinn verloren und kann weiterhin zur Bereinigung und
Aufspaltung von Pfaden verwendet werden. Einzelne Elemente sind für die Stickpfadoptimierung
immer besser geeignet als kombinierte Pfade, die wenigen Ausnahmen kennt ihr ja bereits.

[Mehr Infos](/de/docs/fill-tools/#füllstich-objekte-zerlegen)

#### Parameter überprüfen

Manche [Ink/Stitch Parameter](/de/docs/params/) sind einfach zu verstehen. Andere sind ein wenig versteckter,
haben aber ggf. eine verwirrende Auswirkung auf das Stickergebnis. Dazu gehört beispielsweise die
minimale Stichlänge. Die Festlegung dieses Wertes kann in den Ink/Stitch Einstellungen
(Erweiterungen > Ink/Stitch > Einstellungen) dokumentweit vorgenommen werden. Ab der nun
kommenden Version (v 3.1.0) gibt es zusätzlich die Möglichkeit die minimale Stichlänge
objektbasiert zu festzulegen.

![E-Stich mit unterschiedlichem Wert für die minimale Stichlänge](/assets/images/tutorials/troubleshoot/min_stitch_len_effect.png)

Beide hier im Bild gezeigten E-Stiche haben die gleichen Parameter.
Links ist der Wert für die minimale Stichlänge kleiner als der Abstand zum nächsten Zacken.

Andere Parameter können dazu führen, dass ein Element nicht mehr gerendert werden kann. Hier
müssen Einstellungen auf Abstände und Größen hin überprüft werden. Ein gutes Beispiel hierfür ist
ein zu großes Mäandermuster für ein zu kleines Füllobjekt.

#### Stickparameter entfernen

`Erweiterungen > Ink/Stitch Fehlerbehebung > Stickeinstellungen entfernen`

Wenn nichts mehr hilft, kann es vielleicht sinnvoll sein auf Null zurück zu gehen und neu
anzufangen.

Mit diesem Werkzeug können von ausgewählten Elementen alle (oder bestimmte) Parameter und
Befehle entfernt werden. Zusätzlich können Einstellungen aus der PDF-Ausgabe zurückgesetzt
werden.

[Mehr Infos](/de/docs/troubleshoot/#stickeinstellungen-entfernen)

### Inkscape: XML-Editor

`Bearbeiten > XML Editor`

Wer ein bisschen tiefer in die Materie einsteigen möchte, hat mit dem XML-Editor die Möglichkeit
die Datei auf Code-Ebene zu betrachten und zu ändern. Alle Ink/Stitch-Parameter sind hierüber
direkt editierbar.

### Testen, testen, testen

Ink/Stitch bietet mittlerweile eine Vielzahl an Parametereinstellungen (Hinweis an die Entwickler:
es wird langsam wirklich etwas unübersichtlich).

Stickergebnisse verschiedener Parameter zu testen, gehört zum Lernprozess in der Digitalisierung
von Stickmustern einfach dazu. Dafür bietet die neue Ink/Stitch Version jetzt auch ein Werkzeug an:
[Testmuster aus Auswahl erstellen](/de/docs/edit/#testmuster-aus-auswahl-erstellen).
Zu finden ist es unter `Erweiterungen > Ink/Stitch > Bearbeiten > Testmuster aus Auswahl erstellen`.

Hiermit lässt sich schnell ein Raster mit Elementen anlegen, bei denen ein Stickparameter
kontinuierlich geändert wird.

### Sticken

Auch beim Sticken können Fehlerquellen liegen. Achtet beim Sticken auf

* Stabiliserung durch passende Vliese
* gutes Einspannen in den Stickrahmen
* Nadel regelmäßig tauschen, passende Nadel für Faden / Stoff einsetzen
* Fadenspannung
* Stickgeschwindigkeit: schnell ist nicht immer gut
* etc.
