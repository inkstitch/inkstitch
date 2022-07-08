---
title: "Kurvenfüllung"
permalink: /de/docs/stitches/guided-fill/
excerpt: ""
last_modified_at: 2022-05-19
toc: true
---
## Beschreibung

Kurvige Füllflächen  mit Hilfe von Führungslinien.

![Fill stitch detail](/assets/images/docs/guided-fill-detail.jpg)

## Funktionsweise

* Erstelle einen geschlossenen Pfad mit einer Füllung.
* Erstelle eine Führungslinie um die Stickrichtung zu definieren:
    * zeichne eine Linie mit einer Kontur und ohne Füllung
    * wähle die Linie aus
    * Öffne `Erweiterungen > Ink/Stitch > Bearbeiten > Auswal zu Fürhungslinie`
* Wähle beide Elemente aus und gruppiere sie (`Strg + G`)
  Jede Gruppe kann mehrere Füllobjekte enthalten, aber nur eine Führungslinie.
  Weitere Führungslinien werden ignoriert.
* Öffne den Parameter-Dialog (`Erweiterungen > Ink/Stitch > Parameter`) und wähle `Kurvenfüllung` als Methode aus.

## Anfangs- und Endpunkt festlegen

Ink/Stitch erlaubt es über visuelle Befehle den [Anfangs- und Endpunkt eines Füllobjekts](/de/docs/commands) zu kennzeichnen.

## Parameter

Run `Extensions > Ink/Stitch  > Params` to tweak the settings to your needs.

Read detailed information in the [Guided Fill Params](/de/docs/params/#kurvvenfüllung-parameter) section.

## Underlay

Underlay in Guided Fill doesn't follow the guide line, but uses the fill angle which can be defined in the underlay [params](/docs/params/#fill-underlay).

## Samples Files Including Guided Fill Stitches
{% include tutorials/tutorial_list key="stichart" value="Kurvenfüllung" %}
