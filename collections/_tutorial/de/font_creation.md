---
title: "Schriftarten für Ink/Stitch erstellen"
permalink: /de/tutorials/font-creation/
last_modified_at: 2020-01-02
language: de
toc: true

excerpt: Erstelle neue Schriftarten für Ink/Stitch
image: /assets/images/fonts/augusa_tutorial/augusa_dejavu.png

tutorial-typ:
  - Text
stichart: 
techniken:
field-of-use: Text
schwierigkeitsgrad: fortgeschritten
---
@Augusa hat einen tollen Artikel in ihrem Blog zur Erstellung neuer Schriftarten veröffentlicht: [Inkstitch : Créer une police de caractères brodés](https://lyogau.over-blog.com/2020/12/inkstitch-creer-une-police-de-caracteres-brodes.html)


Den Text findet ihr hier in einer **nicht ganz wortgereuen, gekürzten und ergänzten** deutschen Übersetzung.
{: .notice--info }

<hr>

In diesem Artikel geht es nicht darum, wie man einzelne Buchstaben digitalisiert, sondern wie man eine Datei mit einem bestimmten Schrifttyp erstellen kann, um sie anschließend mit dem Lettering-Tool von Ink/Stitch zu verwenden.

Mit dem SVG-Schriftarten-Editor von Inkscape ist es möglich komplett neue Schriftarten zu erstellen. Ich ziehe es hier jedoch vor, mit einer bereits vorhandenen Schrift zu arbeiten. Mit Hilfe von [Fontforge](https://fontforge.org) erleichtern wir uns so das Festlegen von Buchstabenabständen.

![Augusa Deja Vu](/assets/images/fonts/augusa_tutorial/augusa_dejavu.png)

**Vokabular**<br>Eine Schrift besteht aus mehreren Schriftarten. Die DejaVu-Schriftart besteht beispielsweise aus Kursivschrift, Fettdruck, serifenloser Fettschrift, ...<br>Jede Schriftart besteht aus einer Reihe von Grundelementen, die Buchstaben, Zahlen, Satzzeichen ... etc. Wir werden hier über Glyphen sprechen.
{: .notice--info }

Eine SVG-Schrift enthält für jede Glyphe eine Ebene.

![Augusa Glyph Layers](/assets/images/fonts/augusa_tutorial/augusa_glyph_layer.jpg)

Jede dieser Ebenen muss einem sehr präzisen Muster folgen, insbesondere die Einhaltung der Grundlinie ist für die Nutzung mit Ink/Stitch unbedingt erforderlich.

**Warnung**<br>Bei den Schriftarten handelt es sich um urheberrechtlich geschützte Werke wie bei den Bildern und anderen Stickdateien auch. Es ist daher wichtig, die erforderlichen Berechtigungen sorgfältig zu überprüfen. "Frei" bedeutet nicht, dass man alles damit machen kann. Insbesondere wenn die Datei für die Verwendung mit Ink/Stitch veröffentlicht werden soll, müssen die Lizenbestimmungen unbedingt eingehalten werden. Wähle beispielsweise eine Public Domain oder eine Open Font License-Schriftart. Es empfiehlt sich in jedem Fall die Lizenz sorgfältig durchzulesen, bevor man sich an die mühevolle Digitalisierungsarbeit begibt.
{: .notice--warning }

Nachdem die Schriftartlizenz auf Eignung genau überprüft wurde, sollte die Schriftgröße bestimmt werden. Wir müssen die maximale Höhe der Buchstaben über und unter der Schriftlinie (Grundlinie) genau kennen. Diese Werte können einfach durch Schreiben der Buchstaben des Alphabets in Groß- und Kleinschreibung ermittelt werden. In einigen Fällen sind Kleinbuchstaben, z. B. b und l, höher als Großbuchstaben. Die Buchstaben M, 1, B, P, G, X sind für diese Identifizierung von großem Nutzen. Die Grundlinie, die im Rest dieses Dokuments als baseline bezeichnet wird, ist notwenig, um die Ink/Stitch-Anforderungen zu erfüllen. Im Bild unten können wir die Höhe der Schrift ablesen und stellen fest, dass in diesem Fall das l höher ist als das M.

![Augusa Font Size](/assets/images/fonts/augusa_tutorial/augusa_font_size.jpg)

Es ist gut - und äußerst interessant -, sich mit der Dokumentation von Schriftarten zu befassen. Es ist überraschend, was für ein Universum von unglaublichem Reichtum es zu entdecken gilt.

## 1. Die Glyphenebenendatei

Die Glyphenebenendatei aus der heruntergeladenen Schriftartdatei erstellen

  1. Öffnen Sie Fontforge um eine ttf-Datei oder ein anderes Schriftformat zu öffnen. Hier habe ich an der Roboto-Schriftart gearbeitet

     ![Open Roboto in FontForge](/assets/images/fonts/augusa_tutorial/de_open_roboto.png)

  2. Wähle die gewünschten Zeichen aus und zähle ungefähr deren Anzahl (wir benötigen die Anzahl später). Stelle sicher, dass alle gewünschten Zeichen ausgewählt sind (bis ganz nach unten scrollen). Die unten gezeigte Auswahl ist nur ein Beispiel und keine Anleitung, nach der die Glyphenauswahl getroffen werden soll.
  
     Anschließend invertieren wir die Auswahl mit `Bearbeiten > Auswählen > Auswahl Invertieren`.

     ![Glyphen-Auswahl](/assets/images/fonts/augusa_tutorial/de_select_glyphs.png)

     Die nun invertierte Auswahl wird über das Menü der rechten Maustaste gelöscht.

     ![Glyphen entfernen](/assets/images/fonts/augusa_tutorial/de_remove_glyphs.png)

  3. Öffne die allgemeinen Schriftinformationen: Element > Schriftinformationen > Allgemein

     ![Font Info](/assets/images/fonts/augusa_tutorial/de_font_info.png)

     Definiere die Oberlänge (die maximale Höhe über der baseline), Unterlänge (die maximale Höhe unter der baseline) und Geviertgröße (die Summe der beiden und somit die gesamte Schrifthöhe)
  4. `Datei > Schriften erstellen > SVG-Schrift > Erstellen`

     Möglicherweise werden Fehler erkannt. Einfach ignorieren ...

     ![Create SVG Font](/assets/images/fonts/augusa_tutorial/de_create_svg_font.png)

     Fontforge erstellt nun die gewünschte SVG-Datei.
  5. Öffne die SVG-Datei mit Inkscape. Sie ist leer!

  6. Erstelle die Canvas-Oberfläche entsprechend deiner Schrift über `Erweiterungen > Typographie > Arbeitsfläche für Typographie einrichten ...`

    ![Typographie Canvas](/assets/images/fonts/augusa_tutorial/de_typography_canvas.png)

    Setze mindestens den Em-Wert auf die richtige Größe

  7. Über `Erweiterungen > Typografie > Konvertiere SVG-Schrift zu Glyph-Ebenen...` lassen sich die gewünschten Glyphenebenen erstellen

     ![Convert](/assets/images/fonts/augusa_tutorial/de_convert.png)

     Stelle die Anzahl der Zeichen auf die am Anfang ausgewählte Anzahl von Glyphen ein (ein höherer Wert ist in Ordnung). Anwenden.

     ![Convert Dialog](/assets/images/fonts/augusa_tutorial/de_convert_dialog.png)

  8. Die Basisdatei ist fertig. Es ist nun notwendig, die Abmessungen der Seite in den `Datei > Dokumenteinstellungen` zu ändern. Klicken Sie unter Skalieren x einmal auf + und dann auf -. Ansonsten fehlt die viewbox im Dokument. Das kann zu Problemen mit der baseline führen.
  9. Schriftlinien definieren

     Majuskelhöhe (descender) ist die niedrigste Linie, die Ihre Glyphen erreichen können (oft die unterste Linie des **p**

     Die Grundlinie (baseline) entspricht der Schreibzeile und ist momentan die einzige Hilfslinie, die von Ink/Stitch genutzt wird

     Caps ist die Höhe der Großbuchstaben

     xheight ist die Höhe der Kleinbuchstaben (die Oberseite des **x**)

     Ascender ist die höchste Linie, die die Glyphen erreichen können (oft durch das **l** bestimmt)

     Schließlich werden wir alle Schriftlinien sorgfältig platzieren, indem wir die für diese Arbeit geeigneten Buchstabenschichten sichtbar machen. Dies sind diejenigen, die zu Beginn zu sehen sind: M für Grundlinie und Caps, l für Oberlänge, x für Höhe, p für Unterlänge.

     Jetzt sieht das Ganze so aus:
 
     ![Augusa Schriftlinien](/assets/images/fonts/augusa_tutorial/augusa_schriftlinien.jpg)

Es macht Sinn die Ursprungsdatei zu behalten. Nur für den Fall, dass es später Probleme mit der Schrift geben sollte.

## 2. Digitalisierung der Glyphen

Wir beginnen mit einem Buchstaben der jetzt zum Sticken vorbereitet werden muss.

Für Buchstaben eignen sich besonders [Satinkolumnen](/de/docs/stitches/satin-column/). Diese erstellen wir zunächst ohne die Stickriehenfolge zu beachten.

Für die Stickreihenfolge erstellen wir eine Kopie der Schriftdatei mit dem Namen `→.svg`. Dort legen wir die Reihenfolge für von links nach rechts zu stickenden Schriftzügen fest. In dieser Datei sollte jede Glyphe unten links beginnen und unten rechts enden.

Für die Stickreihenfolge können wir die Erweiterung "[Automatisch geführte Satinkolumne](/de/docs/satin-tools/#automatische-satinkolumnenführung)" nutzen. Sollte sie bei allen Buchstaben problemlos funktionieren, können wir die digitalisierten Buchstaben so für jede Richtung nutzen, da das Lettering-Tool von Ink/Stitch diese Funktion auch automatisch durchführen kann.

Ansonsten sollten alle Buchstaben ordentlich geprüft werden und bei Bedarf eine separate Datei für jede Stickrichtung mit manueller Führung entstehen.

## 3. Die JSON-Datei und Kerning

Zu jeder Schrift in Ink/Stitch gibt es die Datei font.json. Dort wird der Name der Schrift, sowie eine kleine Beschreibung definiert. Außerdem werden hier die Buchstabenabstände festgelegt.

![Augusa Schriftlinien](/assets/images/fonts/augusa_tutorial/augusa_json.jpg)

In den Ordner gehört auch auf jeden Fall die **Lizenz** der Schrift, die du mit der Schriftdatei erhalten hast. Der Dateiname für die Schrift lautet `→.svg`.

Mit Kerning können die Buchstaben harmonische aufeinander abgestimmt werden. Ein kleines Beispiel zum besseren Verständnis:

![Augusa Avantage 1](/assets/images/fonts/augusa_tutorial/augusa_avantage1.jpg)

**Zeile 1** wurde mit dem Text-Werkzeug von Inkscape erstellt. Wir lesen ohne zu zögern "AVANTAGE"

In **Zeile 2** haben alle Buchstaben den gleichen Abstand zueinander. Das Lesen ist schwieriger, wir zögern ein wenig zwischen den Wörtern "AVANT" und "AGE". Wir wählen jetzt alle Buchstaben aus und vergleichen die beiden Zeilen.

![Augusa Avantage 2](/assets/images/fonts/augusa_tutorial/augusa_avantage2.jpg)

In **Zeile 1** sind die Auswahlrechtecke nicht gleichmäßig angeordnet, während sie in **Zeile 2** alle gleich weit voneinander entfernt sind.

Für eine bessere Qualität ist es daher erforderlich, die Position der Buchstaben relativ zueinander anzupassen und das bestmögliche Kerning zu erzielen. Wir müssen daher die Position der Buchstaben zueinander untersuchen. A und V liegen beispielsweise nahe beieinander, während G und E weit voneinander entfernt sind! In einer Schriftart gibt es 2 mal 26 Buchstaben plus Zeichen mit Akzent plus Sonderzeichen plus Interpunktion. Wir kommen schnell zu mehr als 80 Glyphen oder 6400 Paaren.

Das kann man unmöglich von Hand machen. Jetzt kommt uns die Methode zu Gute, die wir zur digitalisierung der Schriften genutzt haben (FontForge). Dadurch haben wir das richtige Kerning bereits in die Schriftdatei integriert und wir müssen sie nur noch auslesen.

Ink/Stitch bietet ein Werkzeug an, mit dem die JSON-Datei mit der richtigen Kerning-Information befüllt werdeb kann.

1. `Erweiterungen > Ink/Stitch > Schriftverwaltung > JSON erstellen ...`
   ![Generate JSON](/assets/images/fonts/augusa_tutorial/en_generate_JSON.png)

2. Fülle die gewünschten Felder aus:
   * **Name** Pflichfeld. Der Name der Schrift.
   * **Beschreibung** eine kurze Beschreibung deiner Schrift (wie z.B. Informationen zur Größe der Schrift, etc.)
   * **Schriftdatei** Pflichtfeld. Wenn du deine Schrift mit Hilfe von FontForge erstellt hast, wird Ink/Stitch die Kerning Informationen aus dieser Datei lesen und in die JSON-Datei einfügen.
     Außerdem legt der Dateipfad den Speicherort für die neue JSON-Datei fest.
   * **Automatisch geführte Satinkolumne**:
     * aktiviert: Ink/Stitch generiert automatisch geführte Satinkolumnen, wenn die Schrift mit dem Text Werkzeug von Ink/Stitch benutzt wird. [Mehr Informationen über automatisch geführte Satinkolumnen](/de/docs/satin-tools/#auto-route-satin-columns)
     * deaktiviert: Ink/Stitch benutzt die Buchstaben so wie du sie digitalisiert hast. Wennn du selbst schon für einen optimalen Stichpfad gesorgt hast, kannst du diese Funktion deaktivieren.
   * **Umkehrbar**: definiere, ob deine Schrift vorwärts und rückwärts gestickt werden kann.
  * **Klein-/Großbuchstaben erzwingen**:
      * Nein: Wähle diese Option, wenn deine Schrift sowohl Klein- als auch Großbuchstaben enthält (Standard)
      * Großbuchstaben: Wähle diese Option, wenn deine Schrift nur Großbuchstaben enthält.
      * Kleinbuchstaben: Wähle diese Option, wenn deine Schrift nur Kleinbuchstaben enthält.
   * **Standard-Glyphe**: das Zeichen/der Buchstabe der ausgegeben werden soll, wenn der eingegebene Buchstabe nicht in der Schriftdatei vorhanden ist
   * **Minimale Skalierung / Maximale Skalierung**: definiert, wie weit die Schrift maximal skaliert werden darf ohne beim Sticken an Qualität zu verlieren 

   Die folgenden Felder sind nur notwendig, wenn die SVG-Schriftdatei keine Kerning Information enthält.
   Wenn keine Kerning Information vorhanden ist, werden die unten stehenden Werte automatisch genutzt.

   * **Wert erzwingen**: Benutze nicht die Kerning Information aus der Schriftdatei, sondern die nebenstehenden Werte.

   * **Zeilenhöhe (px)**: Abstand zur nächsten Zeile
   * **Wortabstand (px)**: Die Breite des Leerzeichens

3. Klicke auf `Anwenden` um die JSON-Datei zu erstellen. Sie wird im selben Ordner gespeichert in dem sich die Schriftdatei befindet.
   Sie kann mit einem Text-Editor (z.B. Notepad) nachbearbeitet werden.

## 4. Ink/Stitch Speicherorte für Schriftdateien

Ink/Stitch kann Schriften aus verschiedenen Speicherorten lesen, aber der beste Weg ist einen eigenen Ordner für deine Schriftarten zu bestimmen.

1. Öffne `Erweiterungen > Schriftverwaltung > Benutzerdefinierter Ordner für Schriften ...`
2. Wähle den Ordner aus, in dem du deine Schriften speichern willst
3. Klicke auf `Anwenden`

Jetzt kannst du in dem soeben festgelegten Ordner für jede neue Schriftart einen weiteren Ordner erstellen und die Schriftdateien (svgs, json und license) darin speichern.

Wenn alles funktioniert, können wir einen ersten Entwurf sticken. Das dazu benötigte Text-Werkzeug findest du unter `Erweiterungen > Ink/Stitch > Text`.

![Augusa Schrift](/assets/images/fonts/augusa_tutorial/augusa_roboto.jpg)

Sollte die Schrift nicht angezeigt werden, untersuche deine digitalisierten Buchstaben noch einmal genau und verbessere die Pfade, wenn du Fehler findest.

## 5. SVG-Schriftdatei aufräumen (Optional)

**⚠ Warnung**: Änderungen die von diesem Werkzeug durchgeführt werden, können nicht rückgängig gemacht werden. Speichere auf jeden Fall eine **Kopie** deiner Datei ab, bevor du die hier beschriebenen Schritte durchführst.
{: .notice--warning }

Deine Schrift ist bereits einsatzbereit. Aber wenn du sie mit FontForge erstellt hast, beinhaltet sie noch jede Menge Informationen, die wir jetzt nicht mehr brauchen. Sie können sogar die Benutzung der Schrift ein wenig verlangsamen. Ink/Stitch stellt deshalb ein Werkzeug bereit, um die Datei von überflüssigen Informationen zu bereinigen.

1. Stelle sicher, dass du eine **Kopie** deiner Schriftdatei erstellt hast. Die zusätzlichen Informationen werden zwar nicht für den Gebrauch der Schrift benötigt,
   könnten aber nützlich werden, wenn du z.B. weitere Buchstaben zu der Schrift hinzufügen willst.
2. Öffne `Erweiterungen > Ink/Stitch > Schriftverwaltung > Kerning entfernen `
3. Die die zu bereinigende(n) Datei(en)
4. Klicke auf `Anwenden`
