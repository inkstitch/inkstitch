---
title: Stichpfad-Optimisierung
permalink: /de/tutorials/routing/
last_modified_at: 2024-09-09
language: de
excerpt: "Optimising the stitch path is one of the most important subjects in embroidery. Learn how Ink/Stitch can assist you with the task."
image: /assets/images/tutorials/routing/routing.png

tutorial-typ:
  - Text
stichart:
techniques:
field-of-use:
user-level: 

toc: true
---
Den Stickpfad zu optimisieren ist eine der wichtigsten Aufgaben beim Erstellen einer Stickdatei. Lerne hier, wie Ink/Stitch dir bei dieser Aufgabe helfen kann.

Beim Drucken spielt die Reihenfolge und die Verbindung der Elemente untereinander keine Rolle. Beim Sticken aber sollte man unbedingt darauf achten dass:

* **die Elemente in logischer Reihenfolge aufgebaut sind**

  * Vermeide Farbwechsel so gut wie möglich

    Es kann aber manchmal nötig sein, zusätzliche Farbwechsel zu nutzen, nämlich dann, wenn die Farben mal unterhalb, mal oberhalb anderer Elemente gestickt werden müssen oder
    wenn der Verzug am Stoff andernfalls für die folgenden Elemente zu groß werden würde.
  * Registrierungsprobleme verhinden
  * Knittern im Stoff verhindern

* **Sprungstiche vermieden werden**

  In der gesamten Stickdatei sollten keine unnätigen Sprungstiche vorhanden sein. Versuche nicht, sie durch Fadenschnittbefehle zu verstecken,
  sondern versuche lieber duch geschickte Unterpfade eine bessere Lösung zu finden. Fadenschnitte verursachen Chaos auf der Rückseite der Stickerei und
  verlangsamt die Maschine beim Stickvorgang stark.

Jede Datei ist individuell und du bist der Designer der entscheiden kann wie die Stickpfade aufgebaut sind. Aber Ink/Stitch hält ein paar Werkzeuge bereit, die dich unterstützen können.

## Generelle Pfadoptimisierung

### Objekte in Auswahlreihenfolge sortieren

Elemente im Ebenen und Objekte Dialog hoch und runter zu bewegen kann ermüdend sein. Dafür gibt es einen schnelleren Weg: wähle die Elemente in der gewünschten Stickreihenfolge aus und nutze die Ink/Stitch Erweiterung [Objekte in Auswahlreiehenfolge sortieren](/de/docs/edit/#objekte-in-auswahlreihenfolge-sortieren).

### Sprungstich zu Geradstich

Wenn alle Stickelemente gut vorbereitet sind. Alle in die richtige Reihenfolge gebracht worden sind und die Start- und Endpunkte festliegen, kann die Funktion [Sprungstich zu Geradstich](/de/docs/stroke-tools/#sprungstich-zu-geradstich) die letzten Sprungstiche beseitigen. Sie fügt Geradstiche an den Stellen ein, an denen ein Sprungstich gesetzt werden würde. Ändere den Pfad der neuen Geradstich-Pfade, um die Sprungstiche unter nachfolgenden Stickobjekten zu verstecken.

Gibt es einen kurzen Abstand ohne die Möglichkeit den Geradstich zu verdecken, nutze die Verbindung um kleine Zwischenstiche zu setzen, die beim Sticken in den Stoff einsinken werden.

![Jump to stroke process](/assets/images/docs/jump_to_stroke.png)

*1: Original 2: Sprungstich zu Geradstich 3: Der manuell angepasste Geradstich-Pfad verläuft unter der nachfolgenden Füllung*

## Pfadoptimisierung für linienartige Sticharten

Linienartige Sticharten starten am Anfang des Pfades und laufen am Pfad entlang. 
Geschlossene Pfade sollten geöffnet werden um Anfang und Ende klar zu definieren.

### Pfadrichtung sichtbar machen

![Stroke with visible path direction](/assets/images/tutorials/routing/path_direction.png)

Im [Personaliserungs-Artikel](/de/docs/customize/#pfadkonturen--pfadrichtungen) wird beschrieben, wie in Inkscape die Pfadrichtungen sichtbar gemacht werden können. So kannst du direkt überprüfen wo der Pfad anfängt und wo er endet.

### Stickrichtung anpassen

Nun hast du bereits sichergestellt, dass die Pfadrichtungen sichtbar sind. Zeigt der Pfad in die falsche Richtung, kann er markiert werden und mit `Pfad > Richtung umkehren` umgedreht werden. Dies ist bei der Erstellung von Stickdateien eine häufig genutzte Funktion. Daher empfehlen wir hierfür ein Tastenkürzel zu setzen. Im [Personalisierungs-Artikel](/de/docs/customize/#tastenkürzel) erklkären wir, wie das geht.

### Parameter: Wiederholungen anpassen

Soll die Stickerei am gleichen Punkt der Linie enden wo sie gestartet ist, gibt es mehrere Optionen dies zu erreichen. Im [Parameterdialog](/de/docs/params/) kann die Anzahl der Wiederholungen auf eine gerade Zahl gesetzt werden. Dies empfiehlt sich jedoch nicht, wenn beispielsweise ein Mehrfachgeradstich genutzt wurde. In diesem Fall sollte der Pfad dupliziert und in umgekehrter Richtung als einfacher Geradstich ausgestickt werden.

### Automatisch geführter Geradstich / Redwork

Nutzt das Design eine große Anzahl an Linien, kann es sehr aarbeitsaufwändig sein, diese manuell in einen optimalen möglichst zusammenhängenden Pfad umzuwandeln.

Ink/Stith stellt für diesen Zweck zwei Werkzeuge zur Verfügung. [Redwork](/de/docs/stroke-tools/#redwork) ist in den meisten Fällen zu bevorzugen, da es einen gleichmäßigen Pfad erzeugt, bei dem jede Linie genau zwei mal durchlaufen wird. Es ist möglich ein Startposition festzulegen. Redwork wird immer an der gleichen Stelle starten und enden. Ist das nicht gewünscht, ist vielleicht das Werkzeug [Automatisch geführter Geradstich](/de/docs/stroke-tools/#automatisch-geführter-geradstich) die richtige Wahl.

## Optionen für Satin Routing

Auch Satinsäulen verlaufen vom Anfang des Pfades der Konturlinien Richtung Ende des Pfades. Am Besten sind sie keine durchgehenden Pfade, sondern an einer Stelle geöffnet. Andernfalls kann das Ergebnis anders als erwartet ausfallen oder zumindest an einer unerwünschten Stelle beginnen.

### Automatisch geführte Satinsäulen

Genauso wie für die einfachen Linien, gibt es auch für Satinsäulen ein Werkzeug zur automatischen Pfadoptimisierung: [Automatisch geführte Satinsäulen](/de/docs/satin-tools/#automatisch-geführte-satinsäulen).

Ist die Option `Behalte Reihenfolge der Satinsäulen bei` aktiviert, wird Ink/Stitch versuchen die Satinsäulen so gut es geht zu optimieren, allerdings werden hier keine Geradstiche erzeugt, die die Säulen verdeckt verbinden. Ist die Option deaktiviert, kann die Reihenfolge nicht kontrolliert werden.

Die beste Option ist derzeit die Reihenfolge der Säulen sorgfältig vorzubereiten. Dabei kann die oben genannte Erweiterung zum Sortieren der Element hilfreich sein. Anschließend kann die Erweiterung "Automatisch geführte Satinsäulen" ausgeführt werden. Wähle alle Säulen an und führe die Funktion [Sprungstich zu Geradstich](/de/docs/stroke-tools/#sprungstich-zu-geradstich) aus. Passe die so eingefügten Geradstiche so an, dass sie unter den oben gestickten Satinsäulen liegen.

### Satinsäulen schneiden

Wenn ein Satinsäule manuell geteilt wird, beispielsweise für einen optimierten Stichpfad, gehen alle Parametereinstellungen verloren. Daher empfehlen wir die Ink/Stitch Erweiterung [Satinsäule schneiden](/de/docs/satin-tools/#satinsäule-schneiden) zu verwenden. So können die Parametereinstellungen erhalten bleiben.

### Parameter: Seiten umkehren

Über den [Parameterdialog](/de/docs/params/) können die Seiten der Satinsäule vertauscht werden. Dies bedeutet, dass die Säule auf der anderen Seite als zuvor beginnen wird. Bitte beachte dabei, dass alle Einstellungen die sich auf eine Seite beziehen dabei ebenfalls gedreht werden und ggf. angepasst werden müssen.

### Parameter: Konturlinien umkehren

Im [Parameterdialog](/de/docs/params/) kann die gesammte Stickrichtung angepasst werden.

### Parameter: Wiederholungen für Mittellinien und Unterlagen anpassen

Wird im [Parameterdialog](/de/docs/params/) die Anzahl der Wiederholungen der Mittellinien-Unterlage auf einen ungerade Wert gesetzt, wird die Satinsäule an der gleichen Seite starten und enden. Dies kann hilfreich sein, um das manuelle digitalisieren von Geradtsichen unter der Stainsäule zu vermeiden.

## Routing Optionen für Füllstiche

Ink/Stitch erlaubt offene Pfade für Füllungen. Um Probleme zu vermeiden, empfiehlt es sich aber, die Pfade als geschlossene Pfade anzulegen.

### Start- und Endbefehle

Start- und Endpositionen für Füllstiche werden über [visuelle Befehle](/de/docs/commands/) gesteuert (Füllstich Anfangs- und Endposition). Werden viele dieser Befehle eingesetzt, kann es auf der Arbeitsfläche etwas unübersichtlich werden. So kann es hilfreich sein zu wissen, dass die Befehle auch dann weiterhin funktionieren, wenn sie unsichtbar sind.
