---
permalink: /de/tutorials/font-creation/
title: "Schriftarten für Ink/Stitch erstellen"
language: de
last_modified_at: 2025-09-06
excerpt: "Erstelle neue Schriftarten für Ink/Stitch"
image: "/assets/images/tutorials/font_creation_complement/multifont3.jpg"
tutorial-type: 
stitch-type:
tool:
techniques:
field-of-use:
user-level: 
toc: true

---
**Warnung** :
Manche dieser Werkzeuge die hier genutzt werden, sind noch nicht in Ink/Stitch 3.2.2.
Dieser Text ist sehr lang, aber wir empfehlen ihn einmal komplett zu lesen, bevor mit der Schrifterstellung begonnen wird.
{: .notice--warning }

Das Ziel dieses Tutorials ist es, aus einer ttf oder otf Schriftdatei eine Schrift zu erstellen, die mit dem Ink/Stitch Textwerkzeug genutzt werden kann.

Der Text enthält nicht nur eine Liste aller benötigten Schritte, sondern versucht auch ein tieferes Verständnis über das Warum zu vermitteln.

## Ink/Stitch Schriften - Grundlagen

### Ordnerstruktur

Die Dateien die eine Schriftart ausmachen sind in einem speziellen Ordner gespeichert.
Der Ordner wiederrum befindet sich entweder im offiziellen Ordner für Ink/Stitch Schriften (Achtung bei Updates!) oder
in einem [benutzerdefinierten Schriftenorder](/de/docs/font-tools/#benutzerdefinierter-ordner-für-schriften) für persönliche Schriftarten.

Jeder Schriftartenordner muss mindestens zwei Dateien enthalten:

* `font.json`: die Datei enthält Schriftinformationen
* mindestens eine SVG-Datei, die die digitalisierten Glyphen enthält

Außerdem enthalten die Schriftarten-Ordner:

* `preview.png`: ein Vorschaubild mit dem Schriftnamen das im Textwerkzeug angezeigt wird (das Format ist 15:1, normalerweise 300x20px)
* `LICENSE` mit der Schriftarten-Lizenz. Damit eine Schrift auch offiziell in das Ink/Stitch Schriftmodul aufgenommen werden kann, muss die Originallizenz der Schrift die Weiterverarbeitung und Nuzung auch erlauben. Nutze bitte keine sogenannten kommerziellen Lizenzen, da sie in der Regel die integration in Ink/Stitch untersagen.

### Namenskonventionen für die SVG-Datei

Die meisten Ink/Stitch-Schriften nutzen eine einzige SVG-Datei mit dem Namen `ltr.svg`.
In diesem Fall wurden die Buchstaben von links nach rechts digitalisiert.

Die Zeichen für arabische oder hebräische Schriften befinden sich in einer Datei mit dem Namen `rtl.svg`.

Manche Schriften, so wie beispielsweise Déja vu, enthalten beide Dateien `ltr.svg` und `rtl.svg`.
Dies ist praktisch für mehrzeiligen Text, so kann dieser vor und zurück gestickt werden:
in der Datei `ltr.svg` sind die Buchstaben von lins nach rechts digitalisiert, in der Datei `rtl.svg` von rechts nach links.
Das Textwerkzeug wird beide Dateien abwechselnd für jede Textzeile nutzen und so die Sprungstiche zwischen den Zeilen minimieren.

Schriften mit einer sehr großen Anzahl an Schriftzeichen können aus Performanzgründen in mehrere Dateien aufgespalten werden.
Die einzelnen Dateien müssen in diesem Fall nicht nach einem bestimmten Muster benannt werden. Stattdessen werden sie in einem Unterordner abgespeichert, der nach der Stickrichtung benannt ist.
Für Schriftzeichen, die von links nach rechts digitalisiert wurden, trägt der Ordner den Namen `ltr`.

## Eine Schriftart auswählen

Die Wahl der Schrift und der Schriftgröße hängt maßgeblich von dem Stickstil ab, der angewendet werden soll: Satin, Geradstich, Füllung, Applikation...

Eine Satinsäule darf nicht zu schmal (mindestens 1,5mm wären gut), aber auch nicht zu breit sein (bei mehr als 7mm wird das Gestickte zu locker und mehr als 12mm können viele Maschinen nicht sticken).
Daher können Schriftarten mit einer sehr variablen Linienbreite nur schwer als reine Satinsäulen verarbeitet werden.
Serifen-Schriften sind generell schwieriger zu digitalisieren als serifenlose Schriten. Für eine Applikations-Schrift sollte eine sehr breite Schriftart gewählt werden. Der Hauptfaktor für die Wahl der Schriftart, liegt aber natürlich in der persönlichen Vorliebe.

Egal wie die Wahl ausfällt, die Ausgestaltung der Buchstaben muss beim Festlegen der Stickparameter unbedingt beachtet werden.

## Die Schriftdatei erstellen

Zusätzlich zur Einhaltung der Namenskonventionen muss jede Glyphendatei:

* eine Ebene pro Schriftzeichen enthalten und die Ebene mit dem Zeichen `A` muss das Label `GlyphLayer-A` haben.
* Eine Hilfslinie mit dem Namen `baseline` ist die Grundlinie auf der die Buchstaben stehen. Ink/Stitch braucht diese Hilfslinie um die Buchtaben vertikal auszurichten.
* Die Datei kann andere Elemente enthalten.

### Manuell

Es ist möglich eine Schriftdatei manuell zu erstellen. Dieser Vorgang ist aber nicht empfehlenswert.
Andere Methoden sind einfacher:
* beginnt man mit einer .ttf oder .otf Datei, profitiert man vom vordefinierten Kerning (den festgelegten Buchstabenabständen) der Originalschrift
* beginnt man mit fertigen Stickdateien fällt die Digitalisierungsarbeit weg und die Zeichen müssen nur noch positioniert werden

### Aus Stickdateien

Wenn du bereits fertige Buchstaben-Stickdateien hast (eine Datei pro Schriftzeichen, als Stickdatei oder im SVG-Format), kannst du die Erweiterung [Buchstaben zu Schrift](/de/docs/font-tools/#buchstaben-zu-schrift) verwenden, um eine eizige Schriftdatei zu erstellen.

Die einzelnen Buchstaben müssen nun nur noch zum linken Arbeitsflächenrand und zur Grundlinie positioniert werden.

### Aus einer TTF oder OTF Datei

Wir empfehlen die Verwendung von [FontForge](https://fontforge.org/) zur Erstellung der grundlegenden SVG-Schriftdatei.
Eine SVG-Schrift kann mit Inkscape geöffnet und die enthaltenen Zeichen mit einer Ink/Stitch-Erweiterung in Glyphen-Ebenen umgewandelt werden.

#### Eine SVG-Schrift mit FontForge erstellen

TTF oder OTF Schriften enthalten in de Regel eine sehr große Anzahl an Zeichen. Wahrscheinlich wills du nicht alle Zeichen in die Stickdatei integrieren.

Daher müssen zunächst bestimmte Glyphen zur Löschung ausgewählt werden.

##### Glyphen auswählen

Zunächst müssen alle Zeichen die nicht in eine Stickerei umgewandelt werden sollen, gelöscht werden.

Öffne die Schriftdatei in FontForge:

![FontForge](/assets/images/tutorials/font_creation/open_fontforge_de.png)

Erste Option: Wähle alle Glyphen aus, die behalten werden sollen, dann `Bearbeiten > Auswählen > Auswahl invertieren`, gefolgt von `Bearbeiten > Löschen`.

Wenn du nicht sicher bist, welche Glyphen du behalten solltest, kann folgender Prozess sinnvoll sein:

Wähle `Element > Schriftinformationen... > Unicode-Bereiche` um diese Informationen zu erhalten:

![UnicodeIntervals](/assets/images/tutorials/font_creation/unicode_intervals_de.png)

Klickt man auf einen Unicode-Bereich in der Liste, werden alle zugehörigen Zeichen ausgewählt.
Es ist nicht unüblich alle Zeichen eines Bereiches zu löschen oder zu behalten.

Sind alle unerwünschten Glyphen gelöscht, muss die Schrift nun nur noch als SVG-Schrift abgespeichert werden:
`Datei > Schriften erstellen...`. Wähle `SVG Schrift` als Schrifttyp aus und klicke auf `Erstellen`.

![Generate Fonts](/assets/images/tutorials/font_creation/generate_font_de.png)

##### Eine SVG-Schrift in eine Glyphen-Ebenen umwandeln

Öffne die SVG-Schriftdatei in Inkscape. Sie sieht komplett leer aus, keine Sorge, das ist normal.

Öffne `Erweiterungen > Ink/Stitch > Schriftverwaltung > SVG-Schriftart in Glyphenebenen konvertieren`.

![Convert to glyph layers](/assets/images/tutorials/font_creation/convert_to_glyph_layers_de.png)

Nun ist es Zeit zu entscheiden, wie groß die Schrift sein soll.

Um dies zu tun, nutze einen Referenzbuchstaben von dem du weißt, dass er sich in der SVG-Datei befindet (üblicherweise das M) und lege die Höhe dieses Buchstabens fest.
Dann klicke auf `Anwenden`.

Dieser Wert wird später auch in der JSON-Datei als Höhenangabe genutzt.

Die Datei ist nun in Glyphen-Ebenen konvertiert und enthält sehr viele dieser Ebenen.

Zusätzlich zur `baseline` (Grundlinie), wurden weitere Hilfslinien hinzugefügt. Es ist immer eine gute Idee diese für die Bearbeitung zu blockieren, so werden sie später nicht ausversehen bewegt.
Dies kann über die Dokumenteinstellungen geschehen oder mit einem Klick auf das kleine Schloss-Symbol in der oberen, linken Ecke der Arbeitsfläche.

Die Pfade in der Datei haben undefinierte Kontur- und Füllfarben.
Wähle alle Pfade in allen Ebenen aus. Wenn deine Inkscape Einstellungen nicht die Auswahl von versteckten Elementen erlaubt, müssen zunächst alle Objekte eingeblendet werden.
Gib allen Pfaden eine Füllfarbe und keine Konturfarbe (oder andersherum) und blende die Ebenen erneut aus.

Wenn du eine Schrift von links nach rechts digitalisieren willst, speichere die Datei nun als `ltr.svg` in einem neuen Unterordner innerhalb des Ordners für benutzerdefinierte Schriften ab.

## Die Datei font.json erstellen

Haben wir einmal die `ltr.svg` Datei erstellt, können wir nun die `font.json`-Schriftinformationsdatei generieren. Wir empfehlen dies bereits jetzt zu tun.

Öffne `Erweiterungen > Ink/Stitch > Schriftverwaltung > JSON erstellen ...`.

Der Erweiterungsdialog erlaubt es uns Informationen zur Schrift festzulegen. Die Dokumentation dazu befindet sich [hier](/de/docs/font-tools/#json-datei-erstellen).

Diese Informationen können jederzeit über `Erweiterungen > Ink/Stitch > Schriftverwaltung > JSON bearbeiten ...` bearbeitet werden.
Die Dokumentation dazu befindet sich [hier](/de/docs/font-tools/#json-bearbeiten).

### Buchstabenabstände: das Kerning

Dieser Abschnitt ist für die Neugierigen unter euch und kann vorerst auch übersprungen werden.

Kerning beschreibt die horizontalen Abstände innerhalb der Schrift. Der im deutschsprachigen Raum gebräuchliche Begriff ist "Unterschneidung". Wir bleiben hier aber bei der englischen Terminologie.

#### Wo ist diese Information gespeichert

Die `font.json`-Datei enthält die Kerning-Information. Sie wird bei der Erstellung der json-Datei aus der `ltr.svg`-Schriftdatei extrahiert.

Hierdurch wird die relative Positionierung der einzelnen Zeichen zueinander festgelegt.

Um die Zeichenpositionierung in einem Text festzulegen, nutzt Ink/Stitch drei Informtaionsquellen:

* Wird ein Zeichen auf der Arbeitsfläche horizontal oder vertikal bewegt, hat dies Einfluss auf die Positionierung in der Textausgabe. Nur der erste Charakter in einer Zeile ist für links ausgerichteten Text immer an der oberen, linken Seite der Arbeitsfläche positioniert.
* `horiz_adv_x` ist die Information über den Vorschub. Es gibt einen Standardwert, aber jeder Buchstabe kann diesen Wert durch einen eigenen Wert überschreiben. Eine durch fontforge erstellte Schriftdatei enthält diesen Wert für jedes Zeichen, das vor dem Export nicht gelöscht worden ist.
* `hkern` ist die Information über den Abstand von zwei Glyphen zueinander. Auch diese Information wird durch fontforge in die SVG-Datei übertragen. Bei diesem Attribut geht die Information auch für gelöschte Buchstaben nicht verloren. Die Abstandswerte für die Glyphenpaare werden ebenfalls bei der Erstellung der `font.json`-Datei dort abgespeichert.

#### Wie funktioniert das Kerning?

Ink/Stitch zerlegt einen Text in Zeilen, eine Zeile in Wörter und Wörter in Glyphen.

Lasst uns einmal annehmen, wir wollen das Wort `Test` sticken.

Lasst uns ebenfalls annehmen, dass wir den Text links ausrichten wollen. Dabei sprechen wir über die horizontale Position. Der linke Rand der Arbeitsfläche ist bei `x = 0`.

* Am Anfang der Zeile ist der Cursor bei 0. Das erste Zeichen `T` beginnt demnach bei `x = 0`
* Bevor das nächste Zeichen eingefügt wird, muss die Position des Cursors neu festgelegt werden und definiert sich aus der Summe folgender Werte:
  * der Vorschub `horiz_adv_x` des Buchstabens T (der Wert der dem Zeichen T zugeordnet ist, ansonsten der Standardwert für den Vorschub) (z.B. `horiz_adv_x = 20`)
  * der Abstand des linken Randes der Arbeitsfläche in der Schriftdatei zum Zeichen `e` (z.B. `2`)
  * wenn es einen `hkern`-Wert für das Buchstabenpaar `Te` gibt, so wird der Cursor entsprechend verschoben (ein positiver Wert verringert den Abstand, ein negativer Wert erhöht ihn) (z.B. `12`)
* Der Cursor ist in unserem Beispiel nun bei `x=10` und das `e` kann an dieser Position eingefgt werden

Nun fängt die Berechnung für die Position des nächsten Buchstabens an ... und so weiter und so fort ... bis alle Buchstaben ausgegeben sind.

If you did not start from an ttf file and want some basic kerning, set the value for horiz_adv_x_default to 0 in the json file. This will make Ink/Stitch use the width of the individual glyphs.


#### Kerning-Probleme beheben

Bemerkst du ein Kerning-Problem in einer Schrift:

* überprüfe ob der Buchstabe richtig in seiner Ebene positioniert ist oder versehentlich verschoben wurde
* wenn das Problem in Kobination mit den meisten anderen Schriftzeichen ebenfalls auftaucht, passe für diesen Buchstaben den Wert für den horizontalen Vorschub an (`horiz_adv_x`)
* wenn das Problem nur in Kombination mit ein paar anderen Schriftzeichen auftritt, passe den `hkern`-Wert für die betroffenen Buchstabenpaare an (oder füge ihn hinzu).

Die beiden letzten Operationen können mit der Erweiterung `Extensions > Ink/Stitch > Schriftverwaltung > JSON bearbeiten...` durchgeführt werden.

## Schriftdatei testen

Wenn beide Dateien erstellt sind und sie sich in ihrem eigenen Unterordner innerhalb des Ordners für benutzerdefinierte Schriften befinden, taucht die Schrift nun im Schriftmodul auf.

Der Stickpfad für jeden Buchstaben ist zunächst als automatische Füllung konfiguriert (wenn du eine Füllfarbe für alle Schriftzeichen gesetzt hast) oder als Geradstich (wenn du eine Konturfarbe für die Schriftzeichen verwendet hast). Es ist keine qualitativ gute Stickschrift, aber die Schrift ist nun funktionsfähig.

Die Erweiterung [Zeichentabelle](/de/docs/font-tools/#zeichentabelle) unter `Erweiterungen > Ink/Stitch > Schriftverwaltung > Zeichentabelle` gibt alle freigeschalteten Schriftzeichen einer Schrift aus.
Und erlaubt eine genaue Überprüfung des Stickergebnisses. Es empfiehlt sich während des Digitalisierungsvorgangs immer wieder das Ergebnis zu überprüfen.

## Eine stickbare Schrift erstellen

Nun müssen die Buchstaben, die ursprünglich für den Druck erstellt wurden, in stickbare Pfade umgewandelt werden.

Jeder Buchstabe ist selbst eine kleine Stickerei und alle Regeln für das digitalisieren von Stickdateien müssen hier angewandt werden.

Wir empfehlen, zunächst ein paar Buchstaben, z.B. `A`, `H`, `M`, `G`, `o`, `a` und `p` zu digitalisieren.
So kann man auf recht verschiedene Formen zurückgreifen und austesten, ob alles vernünftig gestickt wird.

Dies ist ein guter Zeitpunkt für die Entscheidung, wie bei Satinschriften die [Ecken ausgestaltet](/de/tutorials/satin-edges/) werden sollen.
Durch die frühe Klärung dieser Frage, wird ein einheitliches Aussehen der Schrift sichergestellt.

Außerdem macht es Sinn grundsätzliche Fragen der Stickparameter zu klären. Beispielsweise welche Stickdichte, welche Zugkompensation, etc.
Aber diese Parameter können auch zu einem späteren Zeitpunkt noch für die gesamte Schrift angepasst werden.

Neben den üblichen Aspekten gibt es bei der Arbeit mit einer Schriftart aber noch weitere Besonderheiten zu beachten.

### Sprung- und Vernähstiche

#### So wenig wie möglich

Normalerweise werden mehrere Buchstaben hintereinander gestickt und wir wollen so wenig Sprungstiche dabei produzieren wie möglich.

Eine gute Stickpfadführung erlaubt es einen Buchstaben ohne Sprungstiche zu sticken. Natürlich geht dies nicht bei unverbundenen Buchstaben, wie z.B. Buchstaben mit einem Akzent.
Manchmal ist auch ein Sprungstich zwischen zwei Buchstaben nötig. Aber es lohnt sich, sich über die Vermeidung von Sprungstichen Gedanken zu machen.

Vor und nach jedem Sprungstich, wird der Faden vernäht. Auch dies verlangsamt die Maschine und verursacht evtl. einen Verzug des Stickbildes. Deshalb sollten auch dies so gut wie möglich vermieden werden.

Ist die Schrift dazu gedacht, mit Ink/Stitch veröffentlicht zu werden, beachte, dass nicht jede Maschine den Faden schneiden kann. Es sollten also auch große Sprünge zwischen den Buchstaben vermieden werden. Besonders dann, wenn über diese Stellen noch weiter gestickt wird.

Um dies zu vermeiden, macht es Sinn einen Buchstaben unten links zu beginnen und unten rechts zu beenden.

Wenn dir das Konzept der Vernäh- und Sprungstiche noch nicht bekannt ist, kann es in der [Dokumentation](/de/docs/stitches/lock-stitches/) nachgelesen werden.

Benutzt deine Schrift Satinsäulen, versuche Vernähstiche an den Enden der Säule zu vermeiden. Dort sind sie am besten sichtbar. Hierfür kann ein Endpositionsbefehl festgelegt werden, der dann auch die Position der Vernähstiche bestimmt.

#### Soviel wie nötig

Es sollte aber auch beachtet werden, dass viele Nutzer die Sprungstiche zwischen den Buchstaben oder zwischen den Akzenten und i-Punkten gerne Schneiden.
Damit die Fäden auch sicher geschnitten werden können, sollte der Sprungstich auch ein wirklicher Sprungstich sein, d.h. er muss entweder lang genug sein oder direkt nach Vernähstichen erfolgen.
Dies gilt besonders dann, wenn der Sprungstich Teil eines Buchstabends ist.

`Erweiterungen > Ink/Stitch > Schriftverwaltung > Sprungstiche erzwingen ...` erleichtert diesen Prozess.
Zum Beispiel ist es hiermit möglich, für eine Satinsäulenschrift die aus alleinstehenden Buchstaben besteht, Vernähstiche für das jeweils letzte Element eines jeden Buchstabens zu erzwingen.

Vernähstiche für Akzente können darüber erzielt werden, dass alle Pfade für einen Akzent in einer Gruppe angeordnet werden. Nun kann über die Sprungstiche erzwingen Erweiterung jedem letzten Element in einer Gruppe das Attribut für erzwungene Vernähstiche zugewiesen werden.

Die Dokumentation für die Erweiterung findest du [hier](/de/docs/font-tools/#vernähstiche-erzwingen)

Alternativ kann auch der Parameter für die minimale Sprungstichlänge für einzelne Elemente gesetzt werden. Auch dies beeinflusst das Setzen der Vernähstiche.

### Fadenschnittbefehle

Das Ink/Stitch Textmodul erlaubt es Benutzern Fadenschnittbefehle nach jedem Buchstaben, Wort oder Zeile zu setzen.
Daher ist die einzige Anwendung im Buchstaben selbst nur dann sinnvoll, wenn es sich um unverbundene, aus mehreren Teilenen bestehende Buchstaben handelt.

### Buchstaben mit diakritischen Zeichen und Arbeitsorganisation

Ink/Stitch Nutzer kommen aus vielen verschiedenen Ländern und sprechen verschiedene Sprachen. Daher versuchen wir mit den Ink/Stitch Schriften so viele Personen wie möglich zu bedienen.
Obwohl hier keine Universalität angestrebt wird, ermöglicht das Hinzufügen von Buchstaben mit diakritischen Zeichen eine größere Anzahl von Benutzern.

`Erweiterungen > Ink/Stitch > Schriftverwaltung > Glyphen organisieren` hilft dir deine Arbeit zu strukturieren und reduziert das Ausführen von den immer wieder gleichen Arbeitsschritten.

Diese Erweiterung erlaubt auch ein paar weitere Optimierungen:

Das Ziel der Erweiterung ist es, die Arbeitsschritte Schritt für Schritt zu strukturieren.

Bei jedem Schritt wird eine Gruppen von Zeichen in der Objektreihenfolge nach oben geschoben und der Schriftautor muss zunächst diese Glyphen digitalisieren, bevor der nächste Schritt ausgeführt werden kann.

So wird der Digitalisierungsprozess in kleinere Teilbereiche aufgeteilt und die Wiederverwendung einzelner Buchstaben ermöglicht.

Zwischen den Schritten sollten ausführliche Tests der digitalisierten Buchstaben erfolgen, da Fehler sonst weiter kopiert werden und später an vielen Stellen korrigiert werden müssen:

* Nutze die [Zeichentabelle](#zeichentabelle) um alle freigeschalteten Buchstaben zu generieren
* Nutze die Erweiterung [Fehlerbehebung an Objekten](/de/docs/troubleshoot/) und korrigiere alle gefundenen Fehler
* Nutze die [Simulation](/de/docs/visualize/#simulator) um ungewünschte Sprungstiche ausfindig zu machen. Am Besten zoomt man hierfür weit in die Buchstaben rein.
* Nutze die [realistische Vorschau](/de/docs/visualize/#stich-plan-vorschau) um weitere Fehler zu entdecken
* Sticke die Buchstaben, das ist der beste Test überhaupt

[Lies die Beschreibung für alle einzelnen Schritte der Glyphen organisieren-Erweiterung](/de/docs/font-tools/#glyphen-organisieren)

### Ink/Stitch Nutzer

Ink/Stitch-Nutzer machen manchmal komische Dinge. Daher sollten folgende Dinge beachtet werden.

#### Probleme durch ungewöhnliche Einstellungen verhindern

Um sicher zu gehen, dass die Sprungstiche und Stichlängen den getesten Ergebnissen entsprechen, setze die Werte für die minimale Sprungstichlänge und die minimale Stichlänge für jeden Pfad. 

#### Ungewollte Skalierung

Nutzer sollen die Schriften über das Textmodul skalieren.
Aber die Realität sieht anders aus.
Eine sinnvolle Vorsichtsmaßnahme für Satinsäulen ist es, den Wert für die maximale Stichlänge bei der Digitalisierung festzulegen.

### Skalierungsoptionen festlegen

Der Schriftautor muss die Skalierungsgrenzen in der JSON-Datei festlegen. Daher muss die Schrift in verschiedenen Größen getestet werden um zu sehen, welche Größen funktionieren.

Für eine Satinschrift ist der wichtigste Wert die Breite der Säule.

`Erweiterungen > Ink/Stitch > Fehlerbehebung > Element Info` erlaubt es, die maximalen und minimalen Stichlängen für alle ausgewählten Elemente einzusehen.

Über den Hilfereiter können die Ergebnisse auch in den Zwischenspeicher kopiert und von dort aus in eine Tabelle kopiert werden.
So kann man schnell die schmalsten und breitesten Säulen ausmachen.
Diese Werte können dir bei der Entscheidung helfen, wie weit eine Schrift skaliert werden darf.
Manchmal gibt es nur ein paar sehr breite Satinsäulen in einer Schrift. In manchen dieser Fälle, kann das Hinzufügen oder Anpassen von Richtungsvektoren zu einem besseren Ergebnis führen und die Stichlängen verkleinern.

### Glyphen hinzufügen oder entfernen

Werden Glyphen zum Dokument hinzugefügt oder gelöscht, muss die JSON-Datei ebenfalls angepasst werden. Dies geschieht automatisch über die Erweiterung `JSON bearbeiten`.

War das Zeichen zuvor nicht in der Datei als die font.json-Datei generiert wurde, muss der Wert für den horizontalen Vorschub (`horiz_adv_x`) gesetzt werden, falls er nicht dem Standardwert entspricht.

Daher macht es Sinn, zu Bginn lieber einen Buchstaben zu viel als einen zu wenig aufzunehmen.

### Mehrfarbige Schriften

Soll die Schriftausgabe mehrfarbig sein, gibt es zwei Dinge, die hierfür getan werden müssen:
* in der font.json-Datei muss die Schrift als `sortable` (sortierbar) definiert werden
* lege einen [Farbsortierindex](/de/docs/font-tools/#farbsortierindex-festlegen) für jeden Pfad fest. In den meisten Fällen (alle Buchstaben haben die gleichen Farben in der gleichen Reihenfolge und alle Pfade mit der gleichen Farbe sind aufeinanderfolgend) kannst du einfach alle Ebenen anzeigen, einen Buchstaben auswählen, das zuerst gestickte Element anwählen und über das Rechtsklick-Menü alle Elemente mit der gleichen Farbe auswählen. Den ausgewählten Elementen kann nun ein Farbsortierindex zugewisen werden. Dann wähle das Element mit der nächsten Farbe und führe den Prozess fort.

  In komplizierteren Fällen kann es ein bisschen schwieriger sein, die richtigen Elemente auszuwählen.

  Wenn sich Befehle oder Führungslinien oder Texturen in der Datei befinden, müssen auch sie den gleichen Farbsortindex erhalten wie das Element auf das sie angewendet werden.

### Limitierungen des Textmoduls

Es können (noch) nicht alle Ink/Stitch Features in der SVG-Datei angewendet werden. Beispielsweise sind Klone, Pfadeffekte, Farbverläufe nicht durch das Textmodul unterstützt.

Es kann (noch) nicht für jede Sprache der Welt eine Schrift erstellt werden, aber seit Ink/Stitch 3.2.0 werden kontextbezogene Varianten des arabischen Alphabets erkannt.

### Ein nettes, kleines Extra

Es ist möglich Layer für mehrere Buchstaben zu erstellen, nicht nur Ligaturen.

Zumm Beispiel gibt es in der Schrift `Allegria 55` eine Ebene mit dem Namen `GlyphLayer-Inkscape_logo`. Hierüber kann das Inkscape Logo über die Eingabe von `Inkscape_logo` in das Textmodul schnell in das Dokument eingefügt werden.
