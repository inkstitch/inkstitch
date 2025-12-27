---
title: "Konturfüllung"
permalink: /de/docs/stitches/contour-fill/
last_modified_at: 2025-04-12
toc: true
---
## Beschreibung

![Konturfüllung Detail](/assets/images/docs/contour-fill-detail.jpg)

Konturfüllung füllt eine Fläche der Kontur folgend.

### Funktionsweise

Erstelle einen geschlossenen Pfad mit einer Füllfarbe.

### Anfangs- und Endpunkt festlegen

Ink/Stitch erlaubt es über visuelle Befehle den [Anfangs- und Endpunkt eines Füllobjekts](/de/docs/commands) zu kennzeichnen.

### Parameter

Öffne `Erweiterungen > Ink/Stitch > Parameter`. Setze die Füllmethode auf `Konturfüllung` und passe die restlichen Einstellungen den jeweiligen Bedürfnissen an.

Einstellung                     ||Beschreibung
---|---|---
Automatisch geführte Füllstiche | ☑ |Muss aktiviert sein, damit diese Einstellungen wirksam werden.
Füllmethode                     | Konturfüllung | Hier bitte Konturfüllung auswählen
Methode                         | ![Von Innen nach Außen](/assets/images/docs/contour-fill-innertoouter-bottlenecks.jpg)<br>![Konturspiralen](/assets/images/docs/contour-fill-spirals.jpg)|**Von Innen nach Außen** (Standard) kann auch Formen mit Engpässen füllen<br>**Einfach Spirale** füllt eine Fläche mit einer einfachen Spirale von außen nach innen<br>**Doppelte Spirale** füllt eine Fläche mit einer doppelten Spirale, die Außen beginnt und endet.
Stil der Verbindungen           | rund, spitz, abgeschrägt|Legt fest, wie Ecken beim Herunterskalieren der Kontur für die inneren Spiralen behandelt werden sollen
Selbstüberschneidungen vermeiden| ![Avoid self crossing effect](/assets/images/docs/contour-fill-self-crossing.jpg)|Legt fest, ob die Pfade sich bei der Methode `Von Innen nach Außen` überkreuzen dürfen oder nicht
Uhrzeigersinn                   || Bestimmt die Richtung in der die Kontur gestickt wird
Glätten                         ||Glättet den Stichpfad. Diese Einstellung definiert, wie weit der geglättete Stichpfad vom ursprünglichen Pfad abweichen darf. Versuche niedrige Zahlen wie z.B. 0.2. Hinweis: Eventuell ist auch eine geringere Geradstich-Toleranz erforderlich.
Erweitern                       ||Erweitert die Ursprungsform. Diese Option kann genutzt werden, um Lücken zwischen angrenzenden Objekten zu verringern. Negative Werte verkleinern die Form.
Maximale Füllstichlänge         || Die Stichlänge in einer Reihe. Ein kürzerer Stich kann am Anfang oder am Ende einer Reihe verwendet werden.
Reihenabstand                   || Abstand zwischen den Stichreihen.
Geradstich-Toleranz             || Alle Stiche müssen innerhalb dieses Abstandes zum Pfad befinden. Ein niedrigerer Toleranzwert führt zu kürzeren Stichen. Ein höherer Wert könnte Ecken abrunden.
Zufällige Stiche                |☑| Anstatt einer gleichmäßigen Verteilung, erfolgt die Stichlänge und -phase nach dem Zufallsprinzip. Dies wird besonders für eng beieinander liegende Kurvenfüllungen empfohlen, um Moiré-Artefakte zu vermeiden.
Zufallsabweichung von der Stichlänge|| Maximale randomisierte Abweichung der Stichabstände in Prozent.
Zuffalszahl                     || Zufallswert für randomisierte Attribute. Verwendet die Element-ID, falls leer.
Minimale Stichlänge             || Überschreibt die globale Einstellung für die minimale Stichlänge. Stiche, die kleiner sind als dieser Wert werden entfernt.
Minimale Länge für Sprungstiche || Überschreibt die globale Einstellung für die minimale Länge für Sprungstiche. Kleinere Entfernungen zum nächsten Objekt haben keine Vernähstiche.
Vernähen erlauben               || Vernäht bei Bedarf an den ausgewählten Positionen
Vernähen erzwingen              || Vernäht den Faden nach diesem Element, auch dann, wenn der Abstand zum Folgeobjekt geringer ist als in den [Ink/Stitch Einstellungen](/de/docs/preferences/) definiert.
Anstecher                       || Wähle die [Anstecher](/de/docs/stitches/lock-stitches) Variante (Anfang).
Verstecher                      || Wähle die [Verstecher](/de/docs/stitches/lock-stitches) Variante (Ende).
Fadenschnitt                    || Schneidet den Faden nachdem dieses Objekt genäht wurde
Stopp                           || Stoppt die Maschine nachdem dieses Objekt genäht wurde und springt zur Stopp-Position (sofern vorhanden)
Zufällige Stiche |☑  |Anstatt einer gleichmäßigen Verteilung, erfolgt die Stichlänge und -phase nach dem Zufallsprinzip. Dies wird besonders für eng beieinander liegende Kurvenfüllungen empfohlen, um Moiré-Artefakte zu vermeiden.
Zufallsabweichung von der Stichlänge| |Maximale randomisierte Abweichung der Stichabstände in Prozent.
Zuffalszahl| |Zufallswert für randomisierte Attribute. Verwendet die Element-ID, falls leer.

{: .params-table }

### Unterlage

Die Unterlage einer Konturfüllung folgt nicht der Kontur, aber nutzt den Stickwinkel, der in den [Parametern der Unterlage](/de/docs/params/#füllung-unterlage) eingestellt werden kann.

### Beispieldateien für Konturfüllung

{% include tutorials/tutorial_list key="stichart" value="Konturfüllung" %}
