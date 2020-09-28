---
title: "Import und Export von Dateien"
permalink: /de/docs/import-export/
excerpt: ""
last_modified_at: 2020-08-28
toc: true
---

Ink/Stitch unterstützt viele Stickformate. Es kann Dateien in die unten aufgeführten Formate importieren und exportieren.

## Unterstützte Formate (A - Z):

### Schreiben
CSV, **DST**, **EXP**, **JEF**, PEC, **PES**, SVG, TXT (G-CODE), U01, **VP3**

### Lesen
100, 10o, BRO, DAT, DSB, **DST**, DSZ, EMD, **EXP**, EXY, FXY, GT, INB, **JEF**, JPX, KSM, MAX, MIT, NEW, PCD, PCM, PCQ, PCS, PEC, **PES**, PHB, PHC, SEW, SHV, STC, STX, TAP, TBF, TXT (G-CODE), U01, **VP3**, XXX, ZXY

**Info:** Detaillierte Informationen zu Stickdateiformaten gibt es hier [EduTechWiki](http://edutechwiki.unige.ch/en/Embroidery_format).
{: .notice--info }

## Import von Stickdateien

Öffne eine fertige Stickdatei, so wie eine beliebige SVG-Datei in Inkscape geöffnet wird: `Datei -> Öffnen ...`, wähle die Datei aus und wähle `Öffnen`.

Es öffnet die Datei im Modus [Manueller Stich Modus](/docs/stitches/stroke/#manual-stitch-mode). Es können einzelne Punkte bearbeitet und das Design optimiert werden. Sobald alles erledigt ist, speichere die Datei wie unten beschrieben ab.

## Stickdateien exportieren

### Methode 1

Die Version 1.10.0 von Ink/Stitch hat die Möglichkeit, Dateien direkt über den Dialog von Inkscape `Datei -> Speichern als ...` (`Strg + Umschalt + S`) zu exportieren.

Wähle ein Dateiformat, das die Stickmaschine lesen kann, und speichere die Datei im gewünschten Ausgabeverzeichnis.

![Ausgabeformat](/assets/images/docs/en/export-selection-field.jpg)

Für zukünftige Änderungen stelle sicher, dass auch eine SVG-Version des Designs behalten wird.

### Methode 2 (Stichplan anzeigen)
Um Designs zu exportieren, starte `Erweiterungen -> Ink/Stitch -> Sticken ...`.

![Sticken ...](/assets/images/docs/en/embroider.jpg){: width="450" }

Einstellungen|Beschreibung
---|---
Mindestlänge (mm)        | 0.0 - 10.0
Andere Ebenen ausblenden | Verberge die ursprünglichen Design-Ebenen, während der Neuerstellung des Stichplans
Ausgabeformat            | Wähle ein Dateiformat, dass die Stickmaschine lesen kann
Verzeichnis              | Gib Verzeichnis an, in dem die Datei gespeichert werden soll. Das verwendete Verzeichnis ist standardmäßig der Ort, an dem die Erweiterung installiert ist.

**Info:** Für die Dateiformatkonvertierung verwendet Ink/Stitch [*pyembroidery*](https://github.com/inkstitch/pyembroidery).
{: .notice--info }

Ink/Stich erstellt eine Datei mit dem Namen `irgendwas.ext`, wobei `irgendwas` der Name der SVG-Datei ist (z. B.`irgendwas.svg`). `ext` ist die Erweiterung für das ausgewählte Ausgabeformat. Wenn `irgendwas.ext` bereits existiert, wird diese in `irgendwas.ext.1` unbenannt. Es werden bis zu 5 Backup-Kopien unterstützt.

   <span style="color: #3f51b5;">↳ irgendaws.ext</span><br/>
   <span style="color: #ff9800;">↳ irgendwas.ext</span>, <span style="color: #3f51b5;">irgendwas.ext.1</span><br/>
   <span style="color: #f44336;">↳ irgendwasg.ext</span>, <span style="color: #ff9800;">irgendwas.ext.1</span>, <span style="color: #3f51b5;">irgendwas.ext.2</span>

**Info:** In zukünftigen Versionen wird diese Methode in *`Stichplan anzeigen`* umbenannt werden und keine Speicherfunktion mehr erfüllen.
{: .notice--info}

## Batch-Export

**Info:** Seit Ink/Stitch Version 1.10.0 ist es möglich, mehrere Dateiformate gleichzeitig zu exportieren.
{: .notice--info }

Unter `Datei -> Speichern unter ...` wähle den kleinen Pfeil im Dateiformat-Auswahlfeld, um eine Liste der verfügbaren Dateiformate zu öffnen.

Navigiere zum gewünschten Ausgabeverzeichnis und wähle dort das `Ink/Stitch: Export von mehreren Formaten (.zip)` aus. Klicke auf "Speichern". Dort wird  gefragt, welche Dateiformate hinein sollen.

![Batch Export](/assets/images/docs/en/export-batch.jpg)




## Die Druckvorschau

Starte `Erweiterungen -> Ink/Stitch -> Drucken` um das Design zu exportieren. Dort hat man die Möglichkeit, einige Einstellungen vorzunehmen, aus verschiedenen Vorlagen zu wählen und diese nach Fertigstellung an einen (PDF-) Drucker zu senden.

## Anpassung

### Editierbare Felder und benutzerdefiniertes Logo
In der Druckvorschau sind viele bearbeitbare Felder. Wähle mit der Maus die Felder aus und gib den gewünschten Text ein. Kopfzeilenanpassungen werden automatisch auf jeder Seite ausgefüllt.

Über einen Klick auf das Ink/Stitch-Logo, kann ein eigenes Logo in den Kopfbereich gesetzt werden. In der Dateiauswahl, wähle dein Logo und klicke auf `Öffnen`.

**Tipp:** Wenn nach dem Ausfüllen der Bedienungshinweise die Objektreihenfolge sich ändern, verwende Ausschneiden (`Strg + X`) und Einfügen (`Strg + V`), um sie an die richtigen Stellen zu plazieren.
{: .notice--warning }

### Designvorschau

Die Designvorschau hat auch verschiedene Optionen. Dort können die Größe entweder durch Klicken auf `Fit`, `100%` oder durch `Strg + Scrollen` angepasst werden, um nahtlos zu skalieren. Nimm das Design mit der Maus und verschiebe es im Arbeitsbereich an einen anderen Ort. Es ist auch möglich, die Transformationen auf alle Seiten anzuwenden, indem "Auf alle anwenden" gewählt wird.

Standardmäßig verwendet die Druckvorschau den Linienzeichnungsmodus. Aktiviere `Realistisch`, wenn eine realistische Vorschau gewünscht wird. Es wird eine Weile dauern um diese Ansicht darzustellen, aber es lohnt sich zu warten. Diese Einstellung muss für jede einzelne Seite aktiviert werden, die verwendet werden soll.

![Linienzeichnung und realistische Vorschau](/assets/images/docs/en/print-realistic-rendering.jpg){: width="450x" }

### Einstellungen

Wähle `Einstellungen` um auf die folgenden Optionen zuzugreifen.

#### Page Setup

Einstellung|Beschreibung
---|---
Papierformat | Es kann zwischen `Letter` und `A4` gewählt werden.
Drucklayouts | Es gibt zwei verschiedene Layout-Typen:<br />⚬ **Stickmaschinen Bedienungs Layout** mit Farbblöcken, Garnnamen, Stichanzahl und benutzerdefinierten Notizen<br />⚬ **Endkunden Layout**, dass dem Kunden gesendet werden kann<br />⚬ **Benutzerdefinierte Seite** bietet viel Platz für freien Text, z.B. Anleitungen für in-the-hoop-Dateien
Als Standard speichern | *Seiteneinstellungen* können als Standardeinstellungen gespeichert werden. Beim nächsten Öffnen einer Druckvorschau werden diese Einstellungen verwendet. Linux z.B. würde die Standard-Druckeinstellungen in die Datei `~/.config/inkstich/print_settings.json` speichern.

#### Design

Einstellung|Beschreibung
---|---
Garnpalette | Ändern der Garnhersteller Farbpalette. Ink/Stitch wählt übereinstimmende Farbnamen entsprechend der Wahl. Es löscht alle Änderungen, die möglicherweise zuvor vorgenommen wurden.


## Drucken / Als PDF exportieren

Wähle oben auf der Seite `Drucken`, um das Dokument im PDF-Betrachter zu öffnen. Dies öffnet das Dokument im PDF-Betrachter, von wo aus es an den Drucker geschickt werden kann. Stelle sicher, dass die Druckgröße den Einstellungen aus der Druckvorschau entspricht. Um direkt eine PDF-Datei zu speichern, wähle die Option `PDF speichern`.

## Zurück zu Inkscape

Wenn alles erledigt ist, ist es Zeit, zu Inkscape zurückzukehren. Schließe das Fenster mit der Druckvorschau.

