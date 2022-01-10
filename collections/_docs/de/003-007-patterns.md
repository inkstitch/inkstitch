---
title: "Stichmuster"
permalink: /de/docs/stitches/patterns/
excerpt: ""
last_modified_at: 2021-10-23
toc: true
---
Muster werden durch besondere Stichpositionierung erzeugt.

![Pattern](/assets/images/docs/stitch-type-pattern.png)

[Beispieldatei herunterladen](/assets/images/docs/pattern.svg)

## Muster erstellen

Muster können in Ink/Stitch durch hinzufügen oder entfernen von Stichen aus einem bestehenden Stickobjekt erstellt werden.

* Zuerst benötigst du ein **Stickobject**. Das kann sowohl eine Satinkolumne, als auch eine Füllfläche sein. Muster können auch auf Linien angewendet werden, wobei sich hier über die Sinnhaftigkeit streiten lässt.

* Nun muss der **Pfad für das Muster** erstellt werden. Ein Muster besteht entweder aus Linien oder gefüllten Flächen (oder beides gleichzeitig). Durch Linien werden Stiche hinzugefügt, während Füllflächen Stiche vom Stickobjekt entfernen.

* Markiere sowohl das Stickobjekt, als auch das Muster und **gruppiere beide** mit `Strg+G`.

* **In Muster umwandeln**: Führe mit angewähltem Muster die Funktion `Erweiterungen > Ink/Stitch > Bearbeiten > Auswahl zu Muster` aus. Hierdurch wird eine Knotenmarkierung zum Muster hinzugefügt, die bewirkt, dass dieses Objekt nicht direkt gestickt wird, sondern sich als Muster auf andere Elemente in derselben Gruppe auswirkt. Elemente in Untergruppen bleiben unberührt.

   ![Pattern groups](/assets/images/docs/en/pattern.png)

## Muster-Knotenmarkierung entfernen

Die Muster-Knotenmarkierung kann im Dialog "Füllung und Kontur" (`Strg+Umstelltaste+F`) entfernt werden. Öffne den Reiter "Muster der Kontur" und wähle in der ersten Auswahlliste unter Knotenmarkierungen den ersten (leeren) Eintrag.

![Remove pattern](/assets/images/docs/de/stitch-type-remove-pattern.png)
