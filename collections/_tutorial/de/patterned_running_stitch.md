---
title: Gemusterter Geradstich
permalink: /de/tutorials/patterned-unning-stitch/
last_modified_at: 2023-02-21
language: de
excerpt: "Wie man mit dem Inkscape Pfadeffekten einen gemusterten Geradstich erstellt"
image: "/assets/images/tutorials/pattern-along-path/copy-paste.png"

tutorial-typ:
  - Beispieldatei
stichart: 
  - Geradstich
techniken:
schwierigkeitsgrad: 
---
Ink/Stitch ist ein Inksape Plugin. Inkscape hat die Option sogenannte Live Pfadeffekte einzusetzen (LPE). Diese Effekte können direkt mit Ink/Stitch genutzt werden.

Wenn wir also einen gemusterten Geradstich erstellen wollen, können wir ganz einfach den LPE `Muster entlang Pfad` einsetzen.

1. Erstelle den Zielpfad und wähle in aus. Der Zielpfad ist ein ganz normaler [Geradstich](/de/docs/stitches/running-stitch/).


   ![Target path](/assets/images/tutorials/pattern-along-path/target-path.png)
2. Drücke `Ctrl+&` um den Pfadeffekt-Dialog zu öffnen. Alternativ geht das z.B. auch über `Pfad > Pfadeffekte...`.
3. Click on the `+` sign in the LPE-dialog and select `Pattern Along Path`

   ![pattern along path](/assets/images/tutorials/pattern-along-path/pattern-along-path.png)
4. In dem LPE-Dialog wähle Bei `Musterkopien` "Wiederholt" oder "Wiederholt, gestreckt" aus.

   ![repeat pattern](/assets/images/tutorials/pattern-along-path/repeat.png)
5. Es gibt nun verschiedene Methoden dem Pfad ein Muster zuzuordnen. Willst du nun ein eigenes Muster erstellen, beschreiben wir hier wie das geht.

    Neben `Quelle des Musters` klicke auf das Symbol für `Auf der Arbeitsfläche bearbeiten`.

    ![edit on canvas](/assets/images/tutorials/pattern-along-path/edit.png)

    In der linken oberen Ecke erscheint jetzt ein kleiner Pfad. Zoome ihn herein und wähle den rechten Knoten an. Setze den x-Wert auf die Länge die du für dein fertiges Muster haben willst.

    ![set pattern size](/assets/images/tutorials/pattern-along-path/set-size.png)
    
    Jetzt kann der Pfad bearbeitet werden. Mit einem Doppelklick auf die Linie können weitere Knoten punktgenau hinzugefügt werden. Die Linien und Knoten können beliebig gezogen und verschoben werden. Achte dabei darauf den Anfangs- und Endknoten nicht zu bewegen, damit nachher die Übergänge auch gut passen (auf der x-Achse).

    ![final path](/assets/images/tutorials/pattern-along-path/final-path.png)
    
    Der fertige gemusterte Pfad kann auch im Nachhinein kopiert und verändert werden. Wenn jedoch ein Richtungswechsel für eine bessere Stickreihenfolge nötig ist, muss auch das Muster gedreht werden. Dies geschieht wie oben beschrieben über den Knopf `Auf der Arbeitsfläche bearbeiten`.

    Wenn Teile des Musters weiter rechts liegen als der Endknoten, kann das Muster mit dem Wert `Abstand` im LPE-Dialog wieder zurech gerückt werden.

    ![copy paste](/assets/images/tutorials/pattern-along-path/copy-paste.png)

    [SVG-Datei herunterladen](/assets/images/tutorials/pattern-along-path/pattern_along_path.svg){: title="Download SVG File" .align-left download="pattern_along_path.svg" }
