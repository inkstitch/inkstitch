---
title: QR-Code
permalink: /de/tutorials/qr-code/
last_modified_at: 2026-05-14
language: de
excerpt: "Erstelle einen Kreuzstich-QR-Code"
image: "/assets/images/tutorials/qr-code/qr-code.jpg"
tutorial-typ:
  - Beispieldatei
stichart: 
  - Kreuzstich
  - Füllstich
field-of-use:
schwierigkeitsgrad: Leicht
---

{% include upcoming_release.html %}

Mit der Inkscape-Erweiterung `Erweiterungen > Rendern > Strichcode / QR-Code > QR-Code` und dem Ink/Stitch-Kreuzstich ist es sehr leicht einen funktionierenden QR-Code zu sticken:

![Cross Stitch QR Code](/assets/images/tutorials/qr-code/qr-code.jpg)

## Die QR-Code Erweiterung nutzen

![Extension Menu](/assets/images/tutorials/qr-code/QR_extension.jpg)

### Textfeld

In das Feld `Text` ist der Text einzugeben, der decodiert werden soll. In diesem Tutorial verwenden wir die URL der englischen Seite für dieses Tutorial:

`https://inkstitch.org/tutorials/qr-code/`

Vergesse dabei nicht das `https://` am Anfang.

Es ist z.B. auch möglich, WiFi-Informationen über QR-Code zu teilen. Hierfür muss das Textfeld nach diesem Schema befüllt werden:

```
WIFI:S:<SSID>;T:<WPA|WEP|>;P:<password>;; 
```

Das sieht dann für ein WiFI mit der SSID "My_Wifi" und dem Passwort "Hello" und dem WAP-Sicherheitsprotokoll dann so aus:

```
WIFI:S:My_Wifi;T:WPA;P:Hello;;
```

### Fehlerkorrektur-Level

Nutze hier ein hohes Level, das wird später für die Erstellung des Stickpfades hilfreich sein.

### Größe

Quadratgröße (px) definiert die Größe der Quadrate in Pixeln. Diese Größe brauchen wir später in der Kreuzstich-Erweiterung in mm.

Ich wähle hier im Beispiel eine Größe von 8 px für meine Quadrate, das entspricht dann 2.12 mm für Ink/Stitch.

### Anwenden

Nachdem der QR-Code in die Arbeitsfläche eingefügt wurde, erhälst du zwei verschiedene Objekte. Eine ist ein Rechteck, lösche es.
Der QR-Code selbst, ist ein einzelner Pfad, den behalten wir.

![Extension result](/assets/images/tutorials/qr-code/generated_QR_code.jpg)

## QR-Code für Ink/Stitch vorbereiten

- Wähle den Pfad des QR-Codes aus und positioniere ihn in der linken oberen Ecke der Arbeitsfläche, indem du in der Inkscape Werkzeugeinstellungsleiste x und y auf 0 setzt.
- **Dieser Schritt ist wichtig**: Nachdem unter `Bearbeiten > Einstellungen > Verhalten > Schritte > Schrumpfen/Erweitern um:` auf 0.5 px eingestellt wurde, erweitere den QR-Pfad um diesen Wert über `Pfad > Erweitern`

## Kreuzstiche in Ink/Stitch nutzen

Wähle den nun vorbereiteten QR-Code-Pfad aus und wende die Kreuzstichparameter an.
Setze die Mustergröße auf die Größe, die du für die Quadrate verwendet hast.
In unserem Beispiel auf 2.12.

Wir im Screenshot ersichtlich, hast du bereits jetzt einen stickbaren QR-Code erstellt.

![Extension Menu](/assets/images/tutorials/qr-code/First_trial.jpg)

Allerdings gibt es noch eine erhebliche Menge an Sprunstichen, die wir vermeiden wollen.

Aufgrund des hohen Levels für die Fehlerrate, können wir es uns erlauben, kleine Bereiche aus dem QR-Code herauszulöschen und erhalten noch immer einen funktionierenden QR-Code.

- Nutze zunächst den Kreuzstich-Helfer unter `Erweiterungen > Ink/Stitch > Werkzeuge: Füllung > Kreuzstich-Helfer`.

  Setze die Mustergröße auf 2.12 und aktiviere die Checkbox `Verpixeln` in den Ausgabe-Einstellungen. Dies wird die einzelnen Teilbereiche der Form auseinanderbrechen.
- Nutze nun `Erweiterungen > Ink/Stitch > Fehlerbehebung > Dokument bereinigen` und setze die minimale Größe für Fülstichobjekte auf 65 (8x8+1).
  So werden alle alleinstehenden Quadrate entfernt.
- In diesem Beispiel werden 5 Quadrate entfernt.
- Teste, ob dein QR-Code noch funktionsfähig ist. Ist er das, versuchen wir ihn noch weiter zu vereinfachen.
- Wiederhole den Prozess und entferne nun Bereiche die kleiner als 129 (2x64+1) sind.
- In meinem Beispiel werden weitere 4 Formen entfernt.
- Überprüfe, ob der QR-Code noch funktioniert.

Nun habe ich noch 9 Formen, die ich für das Sticken sinnvoll anordnen kann:

![Extension Menu](/assets/images/tutorials/qr-code/Second_trial.jpg)
