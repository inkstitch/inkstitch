---
title: "Neue Funktionen, Aktualisierungen und Fehlerbehebungen für die nächste Ink/Stitch Version"
permalink: /de/upcoming/
last_modified_at: 2025-05-02
sidebar:
  nav: pages
toc: true
---
Ink/Stitch befindet sich in ständiger Entwicklung. Hier kannst du alle Änderungen sehen, die nach Herausgabe der letzten offiziellen Version gemacht wurden.

## [Schriften](/de/fonts/font-library)

### Neue Schriften

* [Ambigüe](/de/fonts/ambigue/)

  ![Ambigüe](/assets/images/fonts/ambigue.png)
* [Barstitch bold](/de/fonts/barstitch_bold/)

  ![Barstitch bold](/assets/images/fonts/barstitch_bold.png)
* [Barstitch cloudy](/de/fonts/barstitch_bold/)

  ![Barstitch cloudy](/assets/images/fonts/barstitch_cloudy.png)
* [Barstitch mandala](/de/fonts/barstitch/bold/)

  ![Barstitch mandala](/assets/images/fonts/barstitch_mandala.png)
* [Barstitch regular](/de/fonts/barstitch_bold)

  ![Barstitch regular](/assets/images/fonts/barstitch_regular.png)
* [Barstitch textured](/de/fonts/barstitch_bold/)

  ![Barstitch textured](/assets/images/fonts/barstitch_textured.png)
  * [Blunesia 72](/fr/fonts/blunesia/)

  ![Blunesia_72](/assets/images/fonts/blunesia_72.png)

* [Califragilistic](/de/fonts/califragilistic/)

  ![Califragilistic](/assets/images/fonts/califragilistic.png)
* [Cogs_KOR](/de/fonts/cogs_KOR)

  ![Cogs_KOR](/assets/images/fonts/cogs_KOR.png)
* [Computer](/de/fonts/computer/)

  ![Copmuter](/assets/images/fonts/computer.png)
* [Decadent Flower Monogram](/de/fonts/decadent_flowers_monogram/)

  ![Decadent flower monogram](/assets/images/fonts/decadent_flowers_monogram.png)
* [גופן בינוני](/de/fonts/hebrew_font/)

  ![גופן בינוני](/assets/images/fonts/hebrew_font_medium.png)
  ![גופן בינוני](/assets/images/fonts/hebrew_font_large.png)
* [פשוט מעוגל](/de/fonts/hebrew_font/)

  ![פשוט מעוגל](/assets/images/fonts/hebrew_simple_rounded.png)
* [Ink/Stitch Masego](/de/fonts/inkstitch-masego/)

  ![Ink/Stitch Masego](/assets/images/fonts/inkstitch_masego.png)
* [Magnolia tamed](/de/fonts/magnolia-script/)

  ![Magnolia tamed preview](/assets/images/fonts/magnolia_tamed.png)
* [Malika](/de/fonts/malika/)

  ![Malika](/assets/images/fonts/malika.png)
* [Mimosa](/de/fonts/mimosa/)

  ![Mimosa medium](/assets/images/fonts/mimosa_medium.png)

  ![Mimosa large](/assets/images/fonts/mimosa_large.png)
* [Pixel 10](/de/fonts/pixel10/)

  ![Pixel 10](/assets/images/fonts/pixel_10.png)
* [Sunset](/de/fonts/sunset/)

  ![Sunset](/assets/images/fonts/sunset.png)
* [Western light](/de/fonts/western_light/)

  ![Western light](/assets/images/fonts/western_light.png)

### Schrift-Aktualisierungen

Wieder einmal haben alle Schriften unzählige Aktualisierungen erhalten. Ein großes Dankeschön, an alle Beteiligten!

## Neue Erweiterungen

### JSON bearbeiten

`Schriftverwaltung > JSON bearbeiten` [#3371](https://github.com/inkstitch/inkstitch/pull/3371)

"JSON bearbeiten" ist Teil der Schriftverwaltung und hilft Schriftautoren schnell und einfach Daten in der JSON-Schriftdatei zu bearbeiten.
Es ist besonders nützlich um das Kerning zu korrigieren, da es Zeichenpaare mit zusätzlichem optionalen Text anzeigen kann, während die Buchstabenabstände angepasst werden.

![Edit Kerning (distance between letters](/assets/images/upcoming/3.2.0/edit_json.png)

[Mehr Informationen](/de/docs/font-tools/#json-bearbeiten)

### Füllung zu Satin

`Werkzeuge: Satin > Füllung zu Satin...` [#3406](https://github.com/inkstitch/inkstitch/pull/3406)

Konvertiert ein Füllemente in Satinsäulen. Ein manuelles setzen von Richtungsvektoren ist hierfür erforderlich.

![Fill to satin](/assets/images/docs/fill_to_satin_bridge.png)

[Mehr Informationen](/de/docs/satin-tools/#füllung-zu-satin)

### Addons für Inkscape installieren

` Addons für Inkscape installieren` [#3606](https://github.com/inkstitch/inkstitch/pull/3606)

Installiert Farbpaletten oder eine Symbolbibliothek mit Motifstichen. Inkscape nach der Installation bitte neu starten.

![Motif stitches](/assets/images/upcoming/3.2.0/motif-stitches.png)

Ersetzt `Farbpaletten für Inkscape installieren`.

[Mehr Informationen](/de/docs/install-addons/)

### Doppelte Knoten entfernen

`Bearbeiten > Doppelte Knoten entfernen` [#3117](https://github.com/inkstitch/inkstitch/pull/3117)

Diese Erweiterung kann (unter Anderem) dazu genutzt werden, aus einem Beanstich-Pfad Stichplan einfache Linien zu generieren.

![Remove duplicated points](/assets/images/upcoming/3.2.0/remove_duplicated_points.png)

[Mehr Informationen](/de/docs/edit/#doppelte-knoten-entfernen)

### Knockdown Füllung

`Werkzeuge: Füllung > Knockdown Füllung` [#3526](https://github.com/inkstitch/inkstitch/pull/3526)

Eine Hilfsmethode um ausgewählte Elemente mit einer Füllfläche zu unterlegen, optional mit Versatz.
Dies kann sehr nützlich für das Besticken von hochflorigen Stoffen sein.

![A figure with a surrounding knockdown stitch](/assets/images/docs/knockdown.png)

[Mehr Informationen](/de/docs/fill-tools/#knockdown-füllung)

### Farbsortierindex festlegen

`Schriftverwaltung > Farbsortierindex festlegen` [#3242](https://github.com/inkstitch/inkstitch/pull/3242)

Ein Werkzeug für Schriftersteller.
Es legt einen bestimmten Farbsortierindex für ausgewählte Elemente fest, um die Gruppierung der Elemente zu steuern, wenn die Option für die Farbsortierung im Textwerkzeug aktiviert ist.

![Color sort index](/assets/images/upcoming/3.2.0/color_sort_index.png)

[Mehr Informationen](/de/docs/font-tools/#farbsortierindex-festlegen)

### Transformation

`Bearbeiten > Transformation...` [#3657](https://github.com/inkstitch/inkstitch/pull/3657)

Wendet Transformationen (Rotation / Spiegelung) an und passt zeitgleich ebenfalls den Füllwinkel an.

![Fill element transformed by 45 degrees, fill angle adapted](/assets/images/docs/transform.png)

## Aktualisierungen für Erweiterungen

### Allgemein

* Ink/Stitch fragt nach, ob alte SVG-Dateien aktualisiert werden sollen, wenn die Ink/Stitch-SVG-Version in einer Datei nicht angegeben ist [#3228](https://github.com/inkstitch/inkstitch/pull/3228)

  Dies verhindert, dass ein ungewolltes Update von Stickelementen stattfindet, die in eine neue Datei kopiert wurden.
* Ink/Stitch Erweiterungen werden nun mit Icons und einer kurzen Erklärung in der Erweiterungs-Galerie angezeigt [#3287](https://github.com/inkstitch/inkstitch/pull/3287)

  ![Extension gallery](/assets/images/upcoming/3.2.0/extension_gallery.png)

### Automatisch geführte Satinsäulen

`Werkzeuge: Satin > Automatisch geführte Satinsäulen`

* Option um die Originalpfade zu behalten [#3332](https://github.com/inkstitch/inkstitch/pull/3332)
* Der Wert für die objekbasierte minimale Sprungstichlänge (falls vorhanden) wird von der Satinsäule auf neu generierte Mittellinien übertragen [#3154](https://github.com/inkstitch/inkstitch/pull/3154)

[Mehr Informationen](/de/docs/satin-tools/#automatisch-geführte-satinsäulen)

### Objektbefehle hinzufügen

* Es gab viele Beschwerden, dass es schwierig sei, Objektbefehle zu positionieren. Deshalb richtet sich jetzt der Zielpunkt nicht mehr auf den Berührungspunkt der Verbindungslinie mit dem Element, sondern auf das Symbol selbst. [#3542](https://github.com/inkstitch/inkstitch/pull/3542).

  Das bedeutet, wenn du ein Startsymbol positionieren willst, dann muss die Symbolmitte auf dem gewünschten Startpunkt liegen. Vorhandene Datei aktualisieren sich automatisch entsprechend.

  ![Hidden connector command](/assets/images/upcoming/3.2.0/hidden_connector_commands.png)
* Verschiedene Sticharten hatten bisher unterschiedliche Befehlssymbole für dieselbe Logik (z.B. automatisch geführte Geradstiche hatten ein anderes Startsymbol als automatisch geführte Satinsäulen).
  Diese Symbole sind jetzt reduziert und verschiedene Sticharten, nutzen das gleiche Symbol für die gleichen logischen Operationen.

[Mehr Informationen](/de/docs/commands/)

### Farbverlauf in Blöcke aufteilen

* Die Farbblöcke werden nun in einer Gruppe eingefügt. Elemente die durch den Farbverlauf entstehen, aber zu klein sind, werden ausgelassen [#3584](https://github.com/inkstitch/inkstitch/pull/3584)

[Mehr Informationen](/de/docs/fill-tools/#farbverlauf-in-blöcke-aufteilen)

### Befehlsymbole skalieren

`Befehle > Ansicht > Befehlsymbole skalieren`

* Setze alle Symbole auf eine einheitliche Größe (vorherige Transformationen werden zurückgesetzt) [#3329](https://github.com/inkstitch/inkstitch/pull/3329)

  Manuelle Transformationen von Gruppen, die Befehlssymbole enthalten können die tatsächliche Größe des jeweiligen Symbols beeinflussen.

[Mehr Informationen](/de/docs/commands/#befehlsymbole-skalieren)

### Zeichentabelle

`Schriftverwaltung > Zeichentabelle`

* Farbsortier-Option für mehrfarbige Schriften hinzugefügt [#3242](https://github.com/inkstitch/inkstitch/pull/3242).
  Die jeweilige Schrift muss hierfür diese Funktion unterstützen.

[Mehr Informationen](/de/docs/font-tools/#zeichentabelle)

### Vernähstiche erzwingen

`Schriftverwaltung > Vernähstiche erzwingen`

* Vernähstiche nach Abstand zu erzwingen ist nun optional (wenn man beispielsweise die Vernähstiche nur für jedes letzte Element eines jeden Zeichens erzwingen will)
  [#3559](https://github.com/inkstitch/inkstitch/pull/3559)

[Mehr Informationen](/de/docs/font-tools/#vernähstiche-erzwingen)

### Lettering

`Text > Text`

* Lädt direkt mit der zuletzt gewählten Schrift und erinnert sich an einige Einstellungen [#3498](https://github.com/inkstitch/inkstitch/pull/3498) [#3504](https://github.com/inkstitch/inkstitch/pull/3504)
* Unterstützung für mehr Sprachen (rechts nach links) [#3432](https://github.com/inkstitch/inkstitch/pull/3358) [#3466](https://github.com/inkstitch/inkstitch/pull/3466)
* Schrift-Simulator: zeige die richtigen Start- und Endpunkte [#3358](https://github.com/inkstitch/inkstitch/pull/3358)
* Einheitliche Informationsdarstellung der Schriftgröße (% und mm) [#3346](https://github.com/inkstitch/inkstitch/pull/3346)
* Farbsortierfunktion für mehrfarbige Schriften [#3242](https://github.com/inkstitch/inkstitch/pull/3242), [#3381](https://github.com/inkstitch/inkstitch/pull/3381).
  Die jeweilige Schrift muss die Farbsortierung unterstützen.
* Optionen für die Ausrichtung mehrzeiliger Texte [#3382](https://github.com/inkstitch/inkstitch/pull/3382)

![Text: mehr Optionen](/assets/images/upcoming/3.2.0/lettering.png)

[Mehr Informationen](/de/docs/lettering/)

### Schrift entlang Pfad

`Text > Schrift entlang Pfad`

Neue Option für die Textausrichtung am Pfad (links, mitte, rechts, gestreckt)

![A text aligned along a path while using the various options](/assets/images/docs/text_along_path_alignment.png)

[Mehr Informationen](/de/docs/lettering/#schrift-entlang-pfad)

### Mehrfarbige Satinsäule

Neue Option zur Anpassung der Unterlage [#3152](https://github.com/inkstitch/inkstitch/pull/3152)

[Mehr Informationen](/de/docs/satin-tools/#mehrfarbige-satinsäule)

### Redwork

* Option zum zusammenfügen von Pfaden [#3407](https://github.com/inkstitch/inkstitch/pull/3407)
* Option um Originalpfade zu behalten [#3407](https://github.com/inkstitch/inkstitch/pull/3407)

[Mehr Informationen](/de/docs/stroke-tools/#redwork)

### Simulator

* Knopf um Fadenkreuz ein- und ausschalten [#3616](https://github.com/inkstitch/inkstitch/pull/3616)
* Speichert optional die Simulationsgeschwindigkeit [#3420](https://github.com/inkstitch/inkstitch/pull/3420)
* Simulator-Einstellungen werden gespeichert und beim erneuten Öffnen geladen (Anzeigen von: Sprungstichen, Fadenschnitten, Farbwechseln, Stopp-Befehlen, Nadeleinstichstellen, Seitenrahmen)
  [#3323](https://github.com/inkstitch/inkstitch/pull/3323)
* Darstellung der Seitengröße im Simulator [#3120](https://github.com/inkstitch/inkstitch/pull/3120)

[Mehr Informationen](/docs/visualize/#simulator)

### Stichplan-Vorschau

* Verbesserte realistische Ansicht [#3222](https://github.com/inkstitch/inkstitch/pull/3222)

[Mehr Informationen](/docs/visualize/#stitch-plan-preview)

### Linie zu Pfadeffekt-Satin

* Transformationen werden bei der Erstellung mit einberechnet (nur pfadspezifische LPE-Satins) [#3500](https://github.com/inkstitch/inkstitch/pull/3500)

[Mehr Informationen](/de/docs/satin-tools/#linie-zu-pfadeffekt-satin)

### Fehlerbehebung an Objekten

* Die Zeiger werden nur gruppiert. So können bestimmte Warnungstypen/Fehlermeldungstypen einfach angezeigt oder versteckt werden [#3486](https://github.com/inkstitch/inkstitch/pull/3486)
* Texte zur Hilfe bei der Fehlerbehebung erhalten eine Hintergrundfarbe [#3357](https://github.com/inkstitch/inkstitch/pull/3357)

[Mehr Informationen](/de/docs/troubleshoot/)

### Klonverbindung auftrennen

* Option um aufgetrennte Symbol-Elemente zu gruppieren / nicht zu gruppieren [#3624](https://github.com/inkstitch/inkstitch/pull/3624)

[Mehr Informationen](/de/docs/edit/#klonverbindung-auftrennen)

## Entfernte Erweiterungen

### Zeichenliste aktualisieren

Diese Erweiterung war teil der Schriftverwaltung und wurde durch die deutlich mächtigere Erweiterung
[JSON bearbeiten](/de/docs/font-tools/#json-bearbeiten) ersetzt [#3380](https://github.com/inkstitch/inkstitch/pull/3380)

### Garn-Farbpaletten für Inkscape installieren

Wurde in die neue Erweiterung `Addons für Inkscape installieren` integriert.

[Mehr Informationen](/de/docs/install-addons/)

## Sticharten und damit verwandte Aktualisierungen

### Automatische Start- und Endpunkte

Füllelemente und Satinsäulen beginnen nun automatisch am nächsten Punkt zum vorangegangenen Element und enden am nächsten Punkt zum folgenden Element
[#3370](https://github.com/inkstitch/inkstitch/pull/3370).

Dieses Verhalten ist anpassbar und natürlich können auch weiterhin Start- und Endbefehle eingesetzt werden.

![Two satins joining at one point, rendered without a jump stitch](/assets/images/upcoming/3.2.0/start_at_nearest_point.png)

### Ausschneidemasken

Ausschneidemasken sind jetzt in allen Varianten direkt mit Ink/Stitch nutzbar. Dies ist insbesondere in der Kombination mit Redwork sehr nützlich.

* **Gruppen:** Ink/Stitch kann nun auch Ausschneidemasken verarbeiten, die auf Gruppen angewandt wurden [#3261](https://github.com/inkstitch/inkstitch/pull/3261).

  ![cliped groups](/assets/images/tutorials/mandala/lettremandala.svg)
* **Pfadeffekt Ausschneidemasken** erlauben eine invertierte Maske ([#3364](https://github.com/inkstitch/inkstitch/pull/3364)).

  ![interved clips](/assets/images/galleries/fonts/decadent_flowers_monogram/IMG_5211.jpg)

### Klone

* Verbessertes Handling von Befehlen [#3086](https://github.com/inkstitch/inkstitch/pull/3086)

[Mehr Informationen](/de/docs/stitches/clone/)

### Konturfüllung

* Neue Option: Erweitern [#3462](https://github.com/inkstitch/inkstitch/pull/3462)

[Mehr Informationen](/de/docs/stitches/contour-fill/)

### Lineare Verlaufsfüllung

* Randomisierungsoptionen hinzugefügt [#3311](https://github.com/inkstitch/inkstitch/pull/3311)

[Mehr Informationen](/de/docs/stitches/linear-gradient-fill/)

### Manuelle Stichpositionierung

* Option für Mehrfachgeradstich hinzugefügt [#3312](https://github.com/inkstitch/inkstitch/pull/3312)

[Mehr Informationen](/de/docs/stitches/manual-stitch/)

### Ripplestich

* Option für manuelle Stichpositionierung hinzugefügt [#3256](https://github.com/inkstitch/inkstitch/pull/3256)
* Option um das Gitter zuerst zu sticken [#3436](https://github.com/inkstitch/inkstitch/pull/3436)
* Satingeführte Ripplestiche

  ![satin guided ripple](/assets/images/docs/ripple_satin_guide.svg)

  * Option um festzulegen ob das Muster bei jeder zweiten Iteration in die entgegengesetzte Richtung verlaufen soll oder nicht
  * Ankerlinie um die Ausrichtung des Musters festzulegen [#3436](https://github.com/inkstitch/inkstitch/pull/3436)

  [Mehr Informationen](/de/docs/stitches/ripple-stitch/#satin-guide)

### Satinsäulen

* Beginnen und enden standardmäßig am nächsten Punkt [#3423](https://github.com/inkstitch/inkstitch/pull/3423)

  ![Automated start and end point for satin column](/assets/images/upcoming/3.2.0/satin_start_end.png)
* Start- und Endbefehle können eingesetzt werden [#3315](https://github.com/inkstitch/inkstitch/pull/3315)

  ![Start/end command for satin columns](/assets/images/upcoming/3.2.0/satin_start_end_command.png)

[Mehr Informationen](/de/docs/stitches/satin-column/)

### Zick-Zack Stich

* Die Zugkompensation kann nun für jede Seite definiert werden (asymmetrisch, wie bei den Satinsäulen)

## Farbpaletten

* `InkStitch Madeira Rayon.gpl` aktualisiert [#3444](https://github.com/inkstitch/inkstitch/pull/3444)
* Isacord polyester: `0713 Lemon` hinzugefügt [#3225](https://github.com/inkstitch/inkstitch/pull/3225)

## Export / Import

Siehe hier eine komplette Liste aller [unterstützten Dateiformate](/de/docs/file-formats/)

### Neue Dateiformate zum Exportieren

TBF

Longarm Quilting: PLT, QCC

### Neue Dateiformate zum Importieren

Longarm Quilting: PLT, QCC, IQP

### GCODE

* Benutzerdefiniertes einfügen von RGB-Werten [#3530](https://github.com/inkstitch/inkstitch/pull/3530)
* Benutzerdefinierte Sprungstich-Befehle

### Batch Lettering

Ink/Stitch kann jetzt auch mehrere Textdateien mit unterschiedlichen Texten auf einmal exportieren.
Ein Pfad mit einem speziellen Label kann genutzt werden, um den Text wie bei `Text entlang Pfad` auszurichten.

![A patch with four different names](/assets/images/docs/batch-lettering.png)

[More information](/de/docs/lettering/#batch-lettering)

## Releases

* Unsere Windows Version ist jetzt kostenlos signiert mit [SignPath.io](https://about.signpath.io) und zertifiziert von [SignPath Foundation](https://signpath.org). Wir sind sehr dankbar für die Unterstützung.
* Die Windows 32bit Version wird nicht mehr unterstützt und wurde entfernt
* Linux Versionen gibt es für 64bit und 32bit

## Developer and Build Stuff

* Sew Stack (first steps) [#3133](https://github.com/inkstitch/inkstitch/pull/3133)

  The Sew Stack will ultimately replace Params and contain its functionality. For now, it is invisible in our releases.
  The params dialog as it is now suffers from all the options, we've added over the years. It is now hard to find a specific setting in there
  and even harder if you are not yet familiar with the program. Sew Stack will help to organize parameter settings.

  It is only visible in manual installs and will not render, unless `enable_sew_stack` is enabled in the debug config file.
  Please note, that this will alter the start and end points of the elements and should only be used for development purposes.

* Update update build process [#3652](https://github.com/inkstitch/inkstitch/pull/3652)
  * removed win32 build
  * use geos source build only for linux32
  * set python version to 3.11 for all builds
  * sign only releases for windows
  * sign windows release with release certificate [#3613](https://github.com/inkstitch/inkstitch/pull/3613)
* Mypy type correctness [#3199](https://github.com/inkstitch/inkstitch/pull/3199)
* use get_user_dir [#3549](https://github.com/inkstitch/inkstitch/pull/3549)
* Migrate from appdirs to platformdirs [#3450](https://github.com/inkstitch/inkstitch/pull/3450)
* remove scipy dependency [#3483](https://github.com/inkstitch/inkstitch/pull/3483) [#3481](https://github.com/inkstitch/inkstitch/pull/3481)
* Update translations workflow [#3435](https://github.com/inkstitch/inkstitch/pull/3435)
* Add lmde6 32bit build [#3298](https://github.com/inkstitch/inkstitch/pull/3298)
* Update macos cloud build [#3291](https://github.com/inkstitch/inkstitch/pull/3291)
* Use colormath2 instead of colormath [#3266](https://github.com/inkstitch/inkstitch/pull/3266)
* make hook actually cancel the commit [#3235](https://github.com/inkstitch/inkstitch/pull/3235)
* linux package fix [#3210](https://github.com/inkstitch/inkstitch/pull/3210)
* arm64 python update [#3201](https://github.com/inkstitch/inkstitch/pull/3201)
* only style-check staged changes [#3186](https://github.com/inkstitch/inkstitch/pull/3186)
* Additional CI Improvements [#3174](https://github.com/inkstitch/inkstitch/pull/3174)
* CI: Added pytest, some speed improvements [#3135](https://github.com/inkstitch/inkstitch/pull/3135)

## Bug Fixes

* Fix zerodivision error in zigzag to satin [#3696](https://github.com/inkstitch/inkstitch/pull/3696)
* Circular fill: use first boundary linestring if outline is multilinestring [#3694](https://github.com/inkstitch/inkstitch/pull/3694)
* Auto route satin: do not try to add a trim to a deleted element [#3683](https://github.com/inkstitch/inkstitch/pull/3683)
* Prevent possbile RecursionError for relative lock stitches [#3695](https://github.com/inkstitch/inkstitch/pull/3695)
* Ensure command symbols in font sampling [#3684](https://github.com/inkstitch/inkstitch/pull/3684)
* Duplicate-consistant autoroute element selection [#3638](https://github.com/inkstitch/inkstitch/pull/3638)
* Do not solely rely on random ids for commands in lettering [#3681](https://github.com/inkstitch/inkstitch/pull/3681)
* Fix NoneType error in auto_fill travel [#3659](https://github.com/inkstitch/inkstitch/pull/3659)
* Fix an issue when auto_satin produces NoneType satins [#3680](https://github.com/inkstitch/inkstitch/pull/3680)
* Multicolor satin (windows): apply settings in spinctrldouble when they hit enter [#3677](https://github.com/inkstitch/inkstitch/pull/3677)
* fix ensure even center walk underlay repeats in auto_satin when value is empty [#3651](https://github.com/inkstitch/inkstitch/pull/3651)
* Prevent unwanted simulator scale transforms [#3637](https://github.com/inkstitch/inkstitch/pull/3637)
* Always update satin param to avoid actual param/rendering mismatch [#3647](https://github.com/inkstitch/inkstitch/pull/3647)
* Lettering, custom directories: do not try to read hidden directories [#3632](https://github.com/inkstitch/inkstitch/pull/3632)
* Simulator on macOS Ventura: update background color correctly [#3621](https://github.com/inkstitch/inkstitch/pull/3621)
* ignore palette files with wrong encoding [#3620](https://github.com/inkstitch/inkstitch/pull/3620)
* fix updater [#3583](https://github.com/inkstitch/inkstitch/pull/3583)
* Element info: take pattern into account [#3581](https://github.com/inkstitch/inkstitch/pull/3581)
* Autosatin: more efforts to keep the stroke width consistant [#3563](https://github.com/inkstitch/inkstitch/pull/3563)
* display stop commands in simulator and print preview [#3545](https://github.com/inkstitch/inkstitch/pull/3545)
* auto-route: apply transforms to ensure stroke width being unchanged [#3538](https://github.com/inkstitch/inkstitch/pull/3538)
* lettering: do not add commands on top of command connectors [#3528](https://github.com/inkstitch/inkstitch/pull/3528)
* Fix jump to trim: NoneType element error [#3525](https://github.com/inkstitch/inkstitch/pull/3525)
* stroke: as_multi_line_string ignore single point paths [#3491](https://github.com/inkstitch/inkstitch/pull/3491)
* Adapt simulator slider symbols to dark theme [#3475](https://github.com/inkstitch/inkstitch/pull/3475)
* Auto-run: try harder to avoid networkx issues [#3457](https://github.com/inkstitch/inkstitch/pull/3457)
* Improve handling of symbols [#3440](https://github.com/inkstitch/inkstitch/pull/3440)
* Lettering: ignore auto-satin setting in the json file when there is no satin [#3434](https://github.com/inkstitch/inkstitch/pull/3434)
* Fix issue in preferences when value is 0.0 [#3430](https://github.com/inkstitch/inkstitch/pull/3430)
* Exclude invisible from node_to_elements directly [#3424](https://github.com/inkstitch/inkstitch/pull/3424)
* Cache: reset on operational error [#3421](https://github.com/inkstitch/inkstitch/pull/3421)
* Update README [#3405](https://github.com/inkstitch/inkstitch/pull/3405)
* Fix an other FloatingPointError [#3404](https://github.com/inkstitch/inkstitch/pull/3404)
* Minimize multi shape tartan jumps [#3386](https://github.com/inkstitch/inkstitch/pull/3386)
* Lettering: prevent duplicated output [#3365](https://github.com/inkstitch/inkstitch/pull/3365)
* Cut satin column: add more rungs when rails are intersecting [#3344](https://github.com/inkstitch/inkstitch/pull/3344)
* Fix jump to stroke transform glitch [#3306](https://github.com/inkstitch/inkstitch/pull/3306)
* Make remove commands more robust for broken commands with active selection [#3288](https://github.com/inkstitch/inkstitch/pull/3288)
* Avoid code repetition in paths detection [#3282](https://github.com/inkstitch/inkstitch/pull/3282)
* Thread catalog: fix broken path [#3281](https://github.com/inkstitch/inkstitch/pull/3281)
* Clone: do not fixup href [#3277](https://github.com/inkstitch/inkstitch/pull/3277)
* Prevent zerodivision error for zero length segments [#3268](https://github.com/inkstitch/inkstitch/pull/3268)
* Set svg version when importing an embroidery file [#3276](https://github.com/inkstitch/inkstitch/pull/3276)
* Redwork/Auto-Run: keep stroke width [#3264](https://github.com/inkstitch/inkstitch/pull/3264)
* Fix 'None'-string confusions in style [#3243](https://github.com/inkstitch/inkstitch/pull/3243)
* Print pdf: prevent rendering original paths [#3262](https://github.com/inkstitch/inkstitch/pull/3262)
* Avoid error message on info panel update [#3246](https://github.com/inkstitch/inkstitch/pull/3246)
* Satin column: ignore single point paths [#3244](https://github.com/inkstitch/inkstitch/pull/3244)
* Fix select redwork top layer [#3230](https://github.com/inkstitch/inkstitch/pull/3230)
* Fix gradient style [#3200](https://github.com/inkstitch/inkstitch/pull/3200)
* Fix clones with NoneType hrefs [#3196](https://github.com/inkstitch/inkstitch/pull/3196)
* Fixed hidden objects being stitched out when cloned (Fix #3167) [#3171](https://github.com/inkstitch/inkstitch/pull/3171)
* Fixed transforms on cloned commands [#3160](https://github.com/inkstitch/inkstitch/pull/3160)
* fill: ensure polygon in pull comp adjusted shape [#3143](https://github.com/inkstitch/inkstitch/pull/3143)
* add wxpython abort message (as alternative to stderr output) [#3145](https://github.com/inkstitch/inkstitch/pull/3145)
* fix fills without underpath and bad start-end positions [#3141](https://github.com/inkstitch/inkstitch/pull/3141)
* satin troubleshoot: do not fail on satins without rails [#3148](https://github.com/inkstitch/inkstitch/pull/3148)
* auto satin: filter zero length strokes as well [#3139](https://github.com/inkstitch/inkstitch/pull/3139)
* Disable darkmode symbols for windows (darkmode in windows doesn't work as excepted) [#3144](https://github.com/inkstitch/inkstitch/pull/3144)
* Fix simulator slider dark theme issue [#3147](https://github.com/inkstitch/inkstitch/pull/3147)
* skip empty gradient blocks [#3142](https://github.com/inkstitch/inkstitch/pull/3142)
* Simulator: toggle info and preferences dialog [#3115](https://github.com/inkstitch/inkstitch/pull/3115)
