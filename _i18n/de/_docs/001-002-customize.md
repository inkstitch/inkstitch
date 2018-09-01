---
title: "Anpassung von Ink/Stitch"
permalink: /de/docs/customize/
excerpt: ""
last_modified_at: 2018-08-26
toc: true
---

## Tastenkürzel

Die Arbeit mit Ink/Stitch und Inkscape kann erheblich beschleunigt werden, wenn Tastenkombinationen zugewiesen werden. Unter: `Bearbeiten > Einstellungen > Benutzeroberfläche > Tastenkürzel` können die gewünschten Tastenkombinationen eingetragen werden. [Inkscape anpassen (en)](http://wiki.inkscape.org/wiki/index.php/Customizing_Inkscape)

Die folgende Liste wurde von @lexelby vorgeschlagen:

Tastenkürzel      | Effekt
----------------- | ------
<key>Strg</key>+<key>Umschalt</key>+<key>O</key> | Objektübersicht (Objekt -> Objekte...)
<key>Strg</key>+<key>Umschalt</key>+<key>P</key> | Erweiterungen -> Parameter (ohne Einstellungen)
<key>Strg</key>+<key>Umschalt</key>+<key>L</key> | Erweiterungen -> Simulierung (Live Simulation)
<key>Strg</key>+<key>Umschalt</key>+<key>E</key> | Erweiterungen -> Sticken (ohne Einstellungen)
<nobr><key>Strg</key>+<key>Umschalt</key>+<key>Bild↑</key></nobr>  | Auswahl -> Objekt anheben (ab Inkscape Version 0.92.2)
<key>Strg</key>+<key>Umschalt</key>+<key>Bild↓</key> | Auswahl -> Objekt absenken (ab Inkscape Version 0.92.2) Objekt anheben und Objekt absenken ist seit Inkscape 0.92.2 in einer verbesserten Art möglich. Damit kann ein Objekt in der Reihenfolge nach oben oder unten verschoben werden. Dadurch hat man eine bessere Kontrolle als mit den alten Befehlen, die Objekte nur neu anordnen konnten, wenn sie sich überlappten. Objekt anheben und Objekt absenken ermöglicht eine präzisere Kontrolle über die Objektreihenfolge. Sehr nützlich in Kombination mit dem Objektfenster.
<key>Strg</key>+<key>R</key> | Auswahl -> Richtung umkehren. Umkehr der Pfadrichtung. Bei Plattstich (Satinstich) und Laufstich kann die Stichrichtung geändert werden. Ich verwende dies mit der Einstellung "Inkscape" in den Einstellungen des Knoten-Tools "Pfadrichtung auf Konturen anzeigen". Wenn Sie mit dem Knoteneditor nur einen Stützpunkt auswählen und Strg+R drücken, kehrt Inkscape nur einen Pfad in einem Objekt um. Dadurch kann ich sicherstellen, dass beide Schienen in einem Satin in die gleiche Richtung zeigen.

### Tastenkürzel der Simulation
Die Ink/Stitch-Simulation enthält bereits folgende Tastenkombinationen:

Tastenkürzel | Effekt
-------- | --------
**↑** | Schneller
**↓** | Langsamer
**r** | Neustart der Animation
**p** | Pause der Animation
**q** | Beenden

## Gitter

Um Vektoren richtig auszurichten, sollte die Rasterfunktion von Inkscape verwendet werden. Gehe zu `Ansicht` und aktiviere das `Seiten Gitter`. Stelle in `Einrasten-Kontrollleiste` sicher, dass `Am Gitter einrasten` aktiviert ist. Es ist auch möglich, den Abstand und den Ursprung der Gitter unter `Datei -> Dokumenteinstellungen -> Gitter` anzupassen.

![Grids](https://user-images.githubusercontent.com/11083514/40359052-414d3554-5db9-11e8-8b49-3be75c5e9732.png)

## Konfiguration des Urprungs mit Gittern

Die Einrichtung vom Ursprung (0,0) ist besonders nützlich für Personen, die vollen Zugriff auf den gesamten Stickbereich haben, zu dem die Maschine fähig ist, unabhängig davon, welcher Rahmen verwendet wird.

Einrichtung:
  * Erstelle zwei Hilfslinien, indem man auf den Linealen den Zeiger auf die Arbeitsfläche zieht (eine horizontale, eine vertikale).
  * Doppelklick auf die Hilfslinien und beschrifte diese mit: `embroidery origin`. Es kann mehr Text hinzugefügt werden, aber er muss mit `embroidery origin` beginnen.
  * Die Position des kleinen Kreises auf der Hilfslinie sowie der Winkel sind nicht wichtig. Es kommt nur darauf an, wo sie sich kreuzen. Dieser Schnittpunkt ist der Stickursprung.

Wenn keine Hilfslinien gefunden werden, ist der Ursprung in der SVG-Datei im Mittelpunkt.
  
**Tip:** Es kann auch eine [Vorlage]((/docs/customize/#working-with-templates)) mit Hilfslinien und einem passenden Arbeitsbereich für die Stickmaschine erstellt werden.
{: .notice--info }

[Videoanleitung]({{ '/tutorials/custom-origins/' | relative_url }})

## Aktivierung von Pfadkonturen & Pfadrichtungen

Die Kenntnis über die Pfadrichtungen sind wichtig, um mit Ink/Stich arbeiten zu können. Wir empfehlen daher, die Kontrollkästchen **Umriss zeigen** und **Zeige temporär Umrandung für ausgewählte Pfade** unter `Bearbeiten -> Einstellungen -> Werkzeuge -> Knoten` zu aktivieren.

Stelle sicher, dass auch **Zeige Entwurfspfad** in der Werkzeugleiste wie in der folgenden Abbildung zu sehen ist, aktiviert ist.
[![Path outlines & directions](https://user-images.githubusercontent.com/11083514/40360721-f294ef0a-5dbe-11e8-9d4d-98f469ff1fba.png)](https://user-images.githubusercontent.com/11083514/40360721-f294ef0a-5dbe-11e8-9d4d-98f469ff1fba.png)

## Arbeiten mit Vorlagen

Wenn man Ink/Stitch häufiger verwendet, möchte man nicht die gleichen arbeiten immer und immer wiederholen. In diesem Fall kann eine Vorlage für die grundlegende Stickkonfiguration erstellt werden. Nachdem alles nach Wunsch organisiert wurde, speichere die Datei einfach in dem Vorlagenverzeichnis. Nun kann mit `Datei -> Neu aus Vorlage` darauf zugegriffen werden.

Betriebssystem|Vorlagenverzeichnis
---|---
Linux   | `~/.config/inkscape/templates`
Windows | `C:\Users\%USERNAME%\AppData\Roaming\inkscape\templates`

Es sollte das Benutzerverzeichnis für Erweiterungen in den Inkscape Einstellungen überprüft werden. [Mehr dazu](/docs/faq/#i-have-downloaded-and-unzipped-the-latest-release-where-do-i-put-it).

**Tip:** Hier gibt es [Fertige Vorlagen](/tutorials/resources/templates/).
{: .notice--info }

