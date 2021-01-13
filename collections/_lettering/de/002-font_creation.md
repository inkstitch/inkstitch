---
title: "Neue Schriftarten für Ink/Stitch erstellen"
permalink: /de/fonts/create/
last_modified_at: 2020-01-02
toc: true
---
@Augusa hat einen tollen Artikel in ihrem Blog zur Erstellung neuer Schriftarten veröffentlicht.

[Inkstitch : Créer une police de caractères brodés](https://lyogau.over-blog.com/2020/12/inkstitch-creer-une-police-de-caracteres-brodes.html)

<bold><u>Den Text findet ihr hier in einer nicht ganz wortgereuen und gekürzten deutschen Übersetzung</u></bold><br>

Hier erkläre ich nicht, wie man einzelne Buchstaben digitalisiert, sondern wie man eine Datei mit einem bestimmten Schrifttyp erstellen kann, um sie anschließend mit dem Lettering-Tool von Ink/Stitch zu verwenden.

Wir können eine komplett neue Schriftart mit dem SVG-Schriftarten-Editor von Inkscape erstellen. Ich ziehe es hier jedoch vor, mit einer bereits vorhandenen Schrift zu arbeiten. Mit Hilfe von [Fontforge](https://fontforge.org) erleichtern wir uns so das Festlegen von Buchstabenabständen.

Ich fing blind an, eine erste Schriftart zu digitalisieren, und sagte mir, dass ich diese Schriftart möglicherweise in Ink/Stitch einfügen könnte. Also nahm ich die Buchstaben von einer Schriftart (DejaVu-Serif) und skalierte sie auf die Größe, die ich haben wollte bevor ich dich Zeichen nacheinander digitalisierte. Dann kontaktierte ich das Ink/Stitch-Team. Mit ihrer Hilfe konnte ich die erforderliche Datei erstellen, damit sie für alle in Ink/Stitch verfügbar ist.

![Augusa Deja Vu](/assets/images/fonts/augusa_tutorial/augusa_dejavu.png)

Ich wollte eine zweite Schrift digitalisieren (Lobster 2 fett kursiv). Laure hat mir geholfen die Schriftart von [Dafont](https://www.dafont.com/) herunterzuladen und direkt in eine Datei umzuwandeln, in der wir die Buchstaben und alles, was dazu gehört (Interpunktion, Sonderzeichen) digitalisieren können ...

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

## Schritt eins: Die Glyphenebenendatei

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

     Über `Erweiterungen > Typhografie > Konvertiere SVG-Schrift zu Glyph-Ebenen...` lassen sich die gewünschten Glyphenebenen erstellen

     ![Convert](/assets/images/fonts/augusa_tutorial/de_convert.png)

     Stelle die Anzahl der Zeichen auf die am Anfang ausgewählte Anzahl von Glyphen ein (ein höherer Wert ist in Ordnung). Anwenden.

     ![Convert Dialog](/assets/images/fonts/augusa_tutorial/de_convert_dialog.png)

  6. Die Basisdatei ist fertig. Es ist nun notwendig, die Abmessungen der Seite in den `Datei > Dokumenteinstellungen` zu ändern. Klicken Sie unter Skalieren x einmal auf + und dann auf -. Ansonsten fehlt die viewbox im Dokument. Das kann zu Problemen mit der baseline führen.
  7. Schriftlinien definieren

     Majuskelhöhe (descender) ist die niedrigste Linie, die Ihre Glyphen erreichen können (oft die unterste Linie des **p**

     Die Grundlinie (baseline) entspricht der Schreibzeile und ist momentan die einzige Hilfslinie, die von Ink/Stitch genutzt wird

     Caps ist die Höhe der Großbuchstaben

     xheight ist die Höhe der Kleinbuchstaben (die Oberseite des **x**)

     Ascender ist die höchste Linie, die die Glyphen erreichen können (oft durch das **l** bestimmt)

     Schließlich werden wir alle Schriftlinien sorgfältig platzieren, indem wir die für diese Arbeit geeigneten Buchstabenschichten sichtbar machen. Dies sind diejenigen, die zu Beginn zu sehen sind: M für Grundlinie und Caps, l für Oberlänge, x für Höhe, p für Unterlänge.

     Jetzt sieht das Ganze so aus:
 
     ![Augusa Schriftlinien](/assets/images/fonts/augusa_tutorial/augusa_schriftlinien.jpg)

Es macht Sinn die Ursprungsdatei zu behalten. Nur für den Fall, dass es später Probleme mit der Schrift geben sollte.

## Zweiter Schritt: Digitalisierung der Glyphen

Wir beginnen mit einem Buchstaben der jetzt zum Sticken vorbereitet werden muss.

Für Buchstaben eignen sich besonders Satinkolumnen. Diese erstellen wir zunächst ohne an die Stickriehenfolge zu denken.

Für die Stickreihenfolge erstellen wir eine Kopie der Datei mit dem Namen `→.svg`. Dort legen wir die Reihenfolge für von links nach rechts zu stickenden Schriftzügen fest. In dieser Datei sollte jede Glyphe unten links beginnen und unten rechts enden.

Für die Stickreihenfolge können wir die Erweiterung "Automatisch geführte Satinkolumne" nutzen. Sollte sie bei allen Buchstaben problemlos funktionieren, können wir die digitalisierten Buchstaben so für jede Richtung nutzen, da das Lettering-Tool von Ink/Stitch diese Funktion auch automatisch durchführen kann.

Ansonsten sollten alle Buchstaben ordentlich geprüft werden und bei Bedarf eine separate Datei für jede Stickrichtung mit manueller Führung entstehen.

## Dritter Schritt: die JSON-Datei

Zu jeder Schrift in Ink/Stitch gibt es die Datei font.json. Die Datei kann mit einem Texteditor (z.B. Notepad) geöffnet werden.

Dort kann der Name der Schrift, sowie eine kleine Beschreibung eingegeben werden. Außerdem werden hier bestimmte Abstände definiert.

![Augusa Schriftlinien](/assets/images/fonts/augusa_tutorial/augusa_json.jpg)

Die Angabe des Namens kann zunächst ausreichen, um Ihre Buchstaben anzuzeigen. Das Ergebnis wird wahrscheinlich ungleichmäßig aussehen, aber man kann die Schriftart bereits nutzen, was ein wichtiger Schritt ist. Sollte die Schrift nicht erscheinen, sollten alle Buchstaben noch einmal auf Fehler untersucht werden.

In den Ordner gehört auch auf jeden Fall die Lizenz der Schrift, die Sie mit der Schriftdatei erhalten haben. Der Dateiname für die Schrift selbst lautet `→.svg`.

Wenn alles funktioniert, können wir einen ersten Entwurf sticken.

![Augusa Schrift](/assets/images/fonts/augusa_tutorial/augusa_roboto.jpg)

## Vierter Schritt: Kerning.

Mit Kerning können die Buchstaben harmonische aufeinander abgestimmt werden. Ein kleines Beispiel zum besseren Verständnis:

![Augusa Avantage 1](/assets/images/fonts/augusa_tutorial/augusa_avantage1.jpg)

*Zeile 1* wurde mit dem Text-Werkzeug von Inkscape erstellt. Wir lesen ohne zu zögern "AVANTAGE"

In *Zeile 2* haben alle Buchstaben den gleichen Abstand zueinander. Das Lesen ist schwieriger, wir zögern ein wenig zwischen den Wörtern "AVANT" und "AGE". Wir wählen jetzt alle Buchstaben aus und vergleichen die beiden Zeilen.

![Augusa Avantage 2](/assets/images/fonts/augusa_tutorial/augusa_avantage2.jpg)

In *Zeile 1* sind die Auswahlrechtecke nicht gleichmäßig angeordnet, während sie in *Zeile 2* alle gleich weit voneinander entfernt sind.

Für eine bessere Qualität ist es daher erforderlich, die Position der Buchstaben relativ zueinander anzupassen und das bestmögliche Kerning zu erzielen. Wir müssen daher die Position der Buchstaben zueinander untersuchen. A und V liegen beispielsweise nahe beieinander, während G und E weit voneinander entfernt sind! In einer Schriftart gibt es 2 mal 26 Buchstaben plus Zeichen mit Akzent plus Sonderzeichen plus Interpunktion. Wir kommen schnell zu mehr als 80 Glyphen oder 6400 Paaren!!!

---

Das kann man unmöglich von Hand machen. Jetzt kommt uns die Methode zu Gute, die wir zur digitalisierung der Schriften genutzt haben (FontForge). Dadurch haben wir das richtige Kerning bereits in die Schriftdatei integriert und müssen sie nur noch auslesen.

Noch kann Ink/Stitch dies nicht automatisch tun. Es ist aber für zukünftige Versionen geplant.

Wendet euch in Fragen des Kernings gerne an das Ink/Stitch-Team. Wir helfen gerne weiter!
