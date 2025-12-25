---
title: "Ink/Stitch personalisieren"
permalink: /de/docs/customize/
last_modified_at: 2025-04-13
toc: true
---

## Tastenkürzel

Deine Arbeit mit Ink/Stitch kann sich erheblich beschleunigen, wenn du Tastenkürzel benutzt.

Die folgende Liste zeigt Tastenkürzel, die über die unten zur Verfügung gestellte Datei schnell eingerichtet werden könne.

Einige dieser Tastenkürzel werden andere Tastenkürzel, die bereits durch Inkscape verwendet werden, ersetzen. In der Tabelle kannst du sehen, welche das sind und wie diese Funktionen weiterhin erreichbar sind.
{: .notice--warning }

Tastenkürzel | Effekt | Ersetzt
-------- | --------
<key>Bild↑</key>                        | Anheben* | Objekt > Anheben (siehe Werkzeugleisten)
<key>Bild↑</key>                        | Absenken* | Objekt > Absenken (siehe Werkzeugleisten)
<key>Strg</key><key>R</key>             | Pfad > Richtung umkehren**
<key>Strg</key><key>⇧</key><key>P</key> | Parameter | Bearbeiten > Einstellungen
<key>Strg</key><key>⇧</key><key>L</key> | Simulator (Live Simulation)
<key>Strg</key><key>⇧</key><key>/</key> | Stichplan Vorschau (neben der Leinwand) | Pfad > Division (nutze stattdessen Strg+/)
<key>Strg</key><key>⇧</key><key>O</key> | Aufteilen von Füllobjekten... (O für Object) | Objekt > Objekteigenschaften
<key>Strg</key><key>⇧</key><key>I</key> | PDF-Export
<key>Strg</key><key>⇧</key><key>Q</key> | Text (Q für QWERTY) | Objekt > Selectoren und CSS
<span style="white-space: nowrap;"><key>Strg</key><key>⇧</key><key>Entf</key></span> | Fehlerbehebung an Objekten (Fehler entfernen)
<key>Strg</key><key>⇧</key><key>+</key> | Befehle mit gewählten Objekten verknüpfen
<key>Strg</key><key>⇧</key><key>U</key> | Linie zu Satin (U sieht wie zwei Schienen aus) | Objekt > Gruppieren (benutze stattdessen Strg+G)
<key>Strg</key><key>⇧</key><key>J</key> | Konturen der Satinsäule umkehren (J sieht wie ein Pfeil aus)
<key>Strg</key><key>⇧</key><key>B</key> | Satinsäule schneiden (B ist in der Hälfte geschnitten) | Pfad > Vereinigen (nutze stattdessen Strg++)
<key>Strg</key><key>⇧</key><key>*</key> | Automatisch geführte Satinsäulen (\* bringt Ordnung)

Wenn man den Ink/Stitch Simulator öffnet, hat man weitere Tastenkürzel zur Verfügung. [Hier](/docs/visualize/#simulation-shortcut-keys) ist verlinkt wie man diese verwendet.

\* Anheben und Absenken gibt genaue Kontrolle darüber, in welcher Reihenfolge Objekte gestickt werden (von unten nach oben). Das ist sehr nützlich in Verbindung mit dem Objekt-Dialog (`Objekt > Ebenen und Objekte ...`).<br><br>** Für Satin- und Geradstiche ändert dies die Stickrichtung. Nutze dies mit der Einstellung `Zeige Pfadrichtung an Außenlinien` unter `Bearbeiten > Einstellungen > Werkzeuge > Knoten`. Wenn du nur einen Knoten mit dem Knotenwerkzeug auswählst und `Strg+R` drückst, kehrt sich nur der ausgewählte Unterpfad um. Auf diesem Wege kannst du sicherstellen, dass beide Schienen der Satinsäule in die gleiche Richtung zeigen.
{: .notice--info }
{: style="font-size: 70%" }

### Download und Import von benutzerdefinierten Tastenkürzeln

* [Ink/Stitch Tastenkürzel herunterladen](/assets/files/inkstitch.xml)
* Gehe zu `Bearbeiten > Einstellungen > Benutzeroberfläche > Tastenkürzel`
* Klicke auf `Importieren...`
* Wähle die Tastenkürzel-Datei (inkstitch.xml)
* Klicke auf `öffnen`

Jetzt kannst du die oben genannten Tastenkürzel verwenden.

Wenn du deine eigenen Tastenkürzel verwenden willst, füge sie in den Tastenkürzel-Dialog ein.
Benutze die Suchfunktion um die Erweiterungen schneller zu finden. [Mehr informationen](http://wiki.inkscape.org/wiki/index.php/Customizing_Inkscape)
{: .notice--info }

## Zoomkorrektur

Beim Sticken ist es wichtig, ein Gefühl für die tatsächliche Größe des Entwurfs zu bekommen. Inkscape verfügt über eine Einstellung, mit der man die Zoomstufen an die Bildschirmgröße anpassen kann.

* Navigiere zu `Bearbeiten > Einstellungen > Benutzeroberfläche`
* Nun hält man ein Lineal auf das Display und passt den Schieberegler an, bis die Länge übereinstimmt.
 
![Zoom correction](/assets/images/docs/de/customize-zoom-correction_ruler.jpg)

## Gitter

Um Vektoren richtig auszurichten, kann die Rasterfunktion von Inkscape verwendet werden. Gehe zu `Ansicht` und aktiviere das `Seitengitter`. Stelle in der `Einrasten-Kontrollleiste` sicher, dass `Am Gitter einrasten` aktiviert ist. Es ist auch möglich, den Abstand und den Ursprung der Gitter unter `Datei > Dokumenteinstellungen > Gitter` anzupassen.

![Gitter](https://user-images.githubusercontent.com/11083514/40359052-414d3554-5db9-11e8-8b49-3be75c5e9732.png)

## Pfadkonturen & Pfadrichtungen

Bei der Arbeit mit Ink/Stitch ist es wichtig, erkennen zu können, in welche Richtung ein Pfad verläuft. Wir empfehlen daher, die Kontrollkästchen `Umriss zeigen` und `Zeige temporär Umrandung für ausgewählte Pfade` unter `Bearbeiten > Einstellungen > Werkzeuge > Knoten` zu aktivieren.

Damit die Pfadrichtungen auch wirklich angezeigt werden, aktiviere außerdem die Option `Zeige die Pfadrichtung an Außenlinie` in der Werkzeugleiste. In der Abbildung kannst du sehen, wo du die Option findest.

[![Path outlines & directions](/assets/images/docs/de/customize-path-outlines.png)](/assets/images/docs/de/customize-path-outlines.png)

## Vorlagen

Wenn man Ink/Stitch häufiger verwendet, bietet es sich an eine Vorlage für die grundlegende Stickkonfiguration zu erstellen. So kann man die Dokumenteinstellungen wiederverwenden und muss nicht wiederholt die gleichen Einstellungen vornehmen.

Nach der vollständigen Einrichtung des Dokumentes wird die Datei über `Datei > Als Vorlage speichern` abgspeichert und kann nun über `Datei > Neu aus Vorlage > Benutzerdefiniert` aufgerufen werden.

Wer Inkscape hautpsächlich für Ink/Stitch nutzt, kann beim Abspeichern der Vorlage auch die Option `Als Standartvorlage festlegen` anwählen.

**Tip:** Hier gibt es [Vorlagen](/de/tutorials/resources/templates/) die du nutzen kannst.
{: .notice--info }

## Farbpaletten für Inscape installieren

Ink/Stitch enthält viele Farbpaletten der üblichen Garnhersteller. Diese können installiert werden, damit sie in Inkscape nutzbar sind.
Das erlaubt dir dein Design mit den richtigen Farben zu planen. Die Farben werden in die PDF-Ausgabe übernommen und auch in der Stickdatei abgespeichert, sofern dein Stickformat dies unterstützt.

[Mehr Informationen](/de/docs/thread-color/#farbpaletten-installieren)
