---
title: "Multiversion Install"
permalink: /de/developers/inkstitch/multiversion/
last_modified_at: 2025-04-13
toc: true
---
Die Möglichkeit mehrere Versionen von Ink/Stitch zu installieren, kann bei der Entwicklung des Programms hilfreich seind.

Es erleichtert das Testen und den Vergleich verschiedener Versionen.

## Ink/Stitch Menü-Dateien einrichten

Um die Installation mehrerer Ink/Stitch Versionen zu ermöglichen, brauchen die Menü-Dateien eine eigene ID.

Hier ist ein Beispiel wie dies erreicht werdeb kann:

* Installiere Ink/Stitch in zwei unterschiedlichen Orten (z.B. _inkstitch_ und _inkstitch-k_)
* Führe `make inx` für beide Installationen durch (dies generiert die `inx/locale/` Dateien)
* In der zweiten Installation generiere nun die inx-Dateien mit `generate-inx-files -a k` 
* Verlinke wie gewohnt die Ordner mit den Ink/Stitch Installationen in den Erweiterungsordner von Inkscape
  * symlink `.config/inkscape/extensions/inkstitch   -> inkstitch`
  * symlink `.config/inkscape/extensions/inkstitch-k -> inkstitch-k`
* Modifiziere `.config/inkscape/keys/default.xml` falls nötig
* Inkscape hat nun zwei Ink/Stitch Versionen im Erweiterungsmenü
  * erste Version: `Erweiterungen > Ink/Stitch`
  * zweite Version: `Erweiterungen > Ink/stitch-k`
