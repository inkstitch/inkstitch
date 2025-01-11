---
permalink: /de/tutorials/mandala/
title: Mandala
language: de
last_modified_at: 2025-01-11
excerpt: "Mandala-Stickerei"
read_time: false
image: "/assets/images/tutorials/mandala/whaletail.png"
tutorial-type:
  - 
stichart:
  - Geradstich
werkzeug:
  - Linie
toc: True
---

<table>
        <tr>
            <td> <img src="/assets/images/tutorials/mandala/Fullmandala.png" alt="Full Mandala" height="200"/>    </td>
            <td> <img src="/assets/images/tutorials/mandala/whaletail.png" alt="Whale tail" height="200" /></td>
        </tr>
</table>

Mit Inkscape können schnell und einfach Mandalas konstruiert werden. Mandalas mit ein paar wenigen, sich berührenden Objekten können mit dem Ink/Stitch-Redwork-Werkzeug in ein Stickmuster ohne Sprungstiche oder Fadenschnitte umgewandelt werden.

Du kannst entweder ein komplettes Mandala aussticken oder es als interessantes Füllmuster verwenden.

Die Inkscape-Werkzeuge für eine schnelle Erstellung von Mandalas sind die beiden Pfadeffekte `Spiegelsymmetrie` und `Gedrehte Kopien`.

Solltest du Video-Tutorials bevorzugen, gibt es hier ein Video von [Gus Visser](https://youtu.be/LS6lgspQkbM) (englisch).

## Mandala erstellen

### Erster Schritt, einfaches Mandala

Erstelle zunächst ein einfaches Mandala. In jedem Mandala gibt es sehr viele Symmetrien.

<table>
        <tr>
            <td> <img  src="/assets/images/tutorials/mandala/nopatheffect.png"
     alt="Mirror path  effect" height="200"/> </td>
    <td><img src="/assets/images/tutorials/mandala/jusmirror.png"
     alt="Mirror path  effect" height="200"/> </td>
    <td>   <img 
     src="/assets/images/tutorials/mandala/2patheffect.png"
     alt="Mirror and Rotate" height="200"/></td>
        </tr>
</table>

In diesem Mandala haben wir:

* rot: zwei Kreise und einen Stern die bereits das gesamte Mandala umfassen und keinen Pfadeffekt benötigen.
* violett: eine Gruppe mit Pfaden. Auf die Gruppe wurden die Pfadeffekte "Spiegelsymmetrie" und "Gedrehte Kopien" (mit 6 Kopien) angewendet

So geht es:

* Öffne ein neues Inkscape Dokument. In den Dokumenteinstellungen (`Strg + Umschalt + D`) eine quadratische Größe setzen, hier 200mm x 200mm)
* Erstelle mindesten 3 Hilfslinien. Alle sollten durch die Mitte der Seite verlaufen (in unserem Beispiel 100mm x 100mm).
  Die vertikale Hilfslinie hat einen Winkel von 0°. Die Horizontale Hilfslinie 90°.
  Die dritte Hilfslinie hat einen 30° Winkel (das Spiegeln und Rotieren wird 12 Kopien von jedem Pfad erzeugen: 360/12 = 30)
* Aktiviere die Einrastfunktion in Inkscape, aber nur für Hilfslinien und Knoten

* Zuerst erstelle ich ein Objekt, das keinen Pfadeffekt benötigt und nutze `Ausrichten und verteilen` um das Objekt in der Mitte der Seite auszurichten.

* Nun erstelle ich einen ersten Pfad in dem Dreieck zwischen der horizontalen und der 30° Hilfslinie
* Gruppiere diesen Pfad
* Wir werden die Pfadeffekte auf diese Gruppe anwenden.
  Alle Pfade, die wir später zu der Gruppe hinzufügen, werden automatisch in 12 Kopien erscheinen.

#### Den Pfadeffekt "Spiegelsymmetrie" anwenden

Wähle den Modus "horizontale Seitenmitte" und nutze ansonsten die Standardeinstellungen

#### Den Pfadeffekt "Gedrehte Kopien" anwenden

Nutze des Pfadeffekt "Gedrehte Kopien"

* Nutze den Modus "Normal"
* 6 Kopien
* Startwinkel 0°
* Drehwinkel 60°
* Setze den Ursprung (x, y) auf die Seitenmitte (hier: 100)
  Alternativ kann der Ursprung auch von Hand eingestellt werden:
  Mit ausgewähltem Pfadeffekt, wähle das Knotenbearbeitungswerkzeug an (`N`) und bewege den Knoten der Rotationsachse des Pfadeffekts in die Seitenmitte

#### Mandala konstruieren

Jetzt können weitere Pfade zu der Gruppe hinzugefügt werden.
Ich starte gerne mit Objekten, deren Endpunkte auf der 0° und 30° Hilfslinie liegen

Wenn alle Einstellungen richtig vorgenommen wurden, sollten die 12 Kopien jetzt wie ein zusammenhängender Pfad aussehen (Abstände von weniger als 0.5mm sind kein Problem)

![Simple Mandala](/assets/images/tutorials/mandala/simplemandala.svg) 

[Beispieldatei für ein einfaches Mandala herunterladen](/assets/images/tutorials/mandala/simplemandala.svg){: download="simplemandala.svg" }

### Komplexere Mandalas

![Less simple Mandala ](/assets/images/tutorials/mandala/lesssimplemandala.svg) 

[Weniger einfaches Mandala herunterladen](/assets/images/tutorials/mandala/lesssimplemandala.svg){: download="lessimplemandala.svg" }

Füge einfach weitere Pfade hinzu ...

Aber wenn du Pfade wie beispielsweise den grünen Pfad im oben gezeigten Beispiel nutzen möchtest (Pfade die genau auf den Hilfslinien liegen oder sie überschneiden),
dann sollten sie keine Spiegelsymmetrie verwenden. Erstelle eine neue Gruppe, auf die nur der Pfadeffekt für gedrehte Kopien angewendet wird.

### Noch komplexere Mandalas

Es ist nicht notwendig überall die gleiche Anzahl an gedrehten Kopien anzuwenden. Hier ist ein Beispiel in dem ich nur 9 Kopien für den außenliegenden Teil nutze.
Dafür habe ich 2 neue Gruppen erstellt.

![Complex Mandala ](/assets/images/tutorials/mandala/complexmandala.svg) 

[Komplexes Mandala herunterladen](/assets/images/tutorials/mandala/complexmandala.svg){: download="compleximplemandala.svg" }

## Mandala in Redwork umwandeln

Du musst lediglich

* alles auswählen
* `Erweiterungen > Ink/Stitch > Werkzeuge: Linie > Redwork`. Wähle 0.5 mm für "Verbinde Linien deren Abstand geringer ist als (mm)"
* Mache einen schönen Spaziergang, trinke Kaffee, rufe jemanden an für ein nettes Gespräch ... wenn du zurück kommst, kannst du
* Das Ergebnis bewundern. Solltest du mehrere verbundene Gruppen haben, sind manche Objekte zu weit auseinander liegend (weiter als 0.5 mm).
  Hier kann sich eine Korrektur lohnen

## Mandala als Füllmuster nutzen

Nutze hierfür nicht das Redwork-Mandala, sondern die Gruppen mit den Pfadeffekten

* Gruppiere alle Gruppen und nenne die Gruppe "Mandala"
* In diesem Beispiel nutze ich einen Text mit der Ojuju Schrift.
  Jeder Text muss zunächst in einen Pfad umgewandelt werden (`Pfad > Objekt in Pfad umwandeln`)
* Erstelle eine Kopie des Texts. Die Kopie erhält nur eine Konturfarbe und keine Füllung)
* Das Original mit einer Füllfarbe wird über die Mandala-Gruppe gelegt. Beide auswählen und `Objekt > Auschneidepfad > Ausschneidepfad setzen` ausführen
* Wähle die Pfadkopie des Buchstabens zusammen mit der Mandala-Gruppe aus und wende die Redwork Funktion an: `Erweiterungen > Ink/Stitch > Werkzeuge: Linie > Redwork`
* Wähle 0.5 mm für "Verbinde Linien deren Abstand geringer ist als (mm)" und "Minimal Pfadlänge (mm)"
* Mache einen kurzen Spaziergang
* Dieses Mal erhalte ich 3 verbundene Gruppen, für jeden Buchstaben eine.

![Mandala text](/assets/images/tutorials/mandala/lettremandala.svg) 

[Beispieldatei für Mandala-Text herunterladen](/assets/images/tutorials/mandala/lettremandala.svg){: download="lettremandala.svg" }

