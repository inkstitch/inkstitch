---
title: "Schriftwerkzeuge"
permalink: /de/docs/font-tools/
excerpt: ""
last_modified_at: 2021-03-07
toc: true
---
Eine Sammunlung von Werkzeugen für Schriftarten Entwickler oder Personen, die dem [Text-Werkzeug](/de/docs/lettering/) von Ink/Stitch zusätzliche Schriften hinzufügen wollen.

Ein Blick in das [Schriften für Ink/Stitch erstellen Tutorial](/de/tutorials/font-creation) lohnt sich auf jeden Fall, wenn du neue Schriften erstellen willst.

## Benutzerdefinierter Ordner für Schriften

Diese Erweiterung erlaubt dir, einen Ordner zu definieren, in dem du zusätzliche Schriften für das Text-Werkzeug speichern willst.

Jede Schriftart sollte in einem eigenen Unterordner gespeichert werden und sollte mindestens folgende Dateien enthalten: eine Schriftdatei (svg) und eine json-Datei.
Zusätzlich empfehlen wir eine Lizenz-Datei.

Die Schriftdatei muss nach der Stichrichtung für die sie erstellt wurde benannt werden (`→.svg`, `←.svg`, etc.).

Die JSON-Datei muss als minimale Bedingung den Namen der Schrift enthalten.

## JSON-Datei erstellen

Diese Erweiterung wurde entwickelt, um die Erstellung der JSON-Datei zu erleichtern.

Abhängig davon, wie du deine Schriftdatei erstellt hast, wird die Kerning Information ebenfalls in die JSON-Datei übertragen.
Lese nach [**wie man eine SVG-Schrift mit Kerning Information erstellt**](/de/tutorials/font-creation)

Wenn du deine Schrift ohne Kerning erstellt hast, kannst du mit diesem Werkzeug immer noch eine JSON-Datei mit den Grundinformationen erstellen.

* **Name** Pflichfeld. Der Name der Schrift.
* **Beschreibung** eine kurze Beschreibung deiner Schrift (wie z.B. Informationen zur Größe der Schrift, etc.)
* **Schriftdatei** Pflichtfeld. Wenn du deine Schrift mit Hilfe von FontForge erstellt hast, wird Ink/Stitch die Kerning informationen aus dieser Datei lesen und in die JSON-Datei einfügen.
 Außerdem legt der Dateipfad den Speicherort für die neue JSON-Datei fest.
* **Automatisch geführte Satinkolumne**:
    * aktiviert: Ink/Stitch generiert automatisch geführte Satinkolumnen, wenn die Schrift mit dem Text Werkzeug von Ink/Stitch benutzt wird. [Mehr Informationen über automatisch geführte Satinkolumnen](/de/docs/satin-tools/#auto-route-satin-columns)
    * deaktiviert: Ink/Stitch benutzt die Buchstaben so wie du sie digitalisiert hast. Wennn du selbst schon für einen optimalen Stichpfad gesorgt hast, kannst du diese Funktion deaktivieren.
* **Klein-/Großbuchstaben erzwingen**:
    * Nein: Wähle diese Option, wenn deine Schrift sowohl Klein- als auch Großbuchstaben enthält (Standard)
    * Großbuchstaben: Wähle diese Option, wenn deine Schrift nur Großbuchstaben enthält.
    * Kleinbuchstaben: Wähle diese Option, wenn deine Schrift nur Kleinbuchstaben enthält.
* **Umkehrbar**: definiere, ob deine Schrift vorwärts und rückwärts gestickt werden kann.
* **Standard-Glyphe**: das Zeichen/der Buchstabe der ausgegeben werden soll, wenn der eingegebene Buchstabe nicht in der Schriftdatei vorhanden ist
* **Minimale Skalierung / Maximale Skalierung**: definiert, wie weit die Schrift maximal skaliert werden darf ohne beim Sticken an Qualität zu verlieren 

Die folgenden Felder sind nur notwendig, wenn die SVG-Schriftdatei keine Kerning Information enthält.
Wenn keine Kerning Information vorhanden ist, werden die unten stehenden Werte automatisch genutzt.

* **Erzwinge nutzerdefinierte Werte**: Benutze nicht die Kerning Information aus der Schriftdatei, sondern die unten definierten Werte.

* **Zeilenhöhe (px)**: Abstand zur nächsten Zeile
* **Wortabstand (px)**: Die Breite des Leerzeichens

Die Datei `font.json` wird in demselben Ordner erstellt, in dem deine SVG-Schriftdatei liegt.

## Kerning entfernen

**⚠ Warnung**: Änderungen die von diesem Werkzeug durchgeführt werden, können nicht rückgängig gemacht werden. Speichere auf jeden Fall eine **Kopie** deiner Datei ab, bevor du die hier beschriebenen Schritte durchführst.
{: .notice--warning }

Deine Schrift ist bereits einsatzbereit. Aber wenn du sie mit FontForge erstellt hast, beinhaltet sie noch jede Menge Informationen, die wir jetzt nicht mehr brauchen. Sie können sogar die Benutzung der Schrift ein wenig verlangsamen. Ink/Stitch stellt deshalb ein Werkzeug bereit, um die Datei von überflüssigen Informationen zu bereinigen.

1. Stelle sicher, dass du eine **Kopie** deiner Schriftdatei erstellt hast. Die zusätzlichen Informationen werden zwar nicht für den Gebrauch der Schrift benötigt,
   könnten aber nützlich werden, wenn du z.B. weitere Buchstaben zu der Schrift hinzufügen willst.
2. Öffne `Erweiterungen > Ink/Stitch > Font Tools > Remove Kerning`
3. Die die zu bereinigende(n) Datei(en)
4. Klicke auf `Anwenden`
