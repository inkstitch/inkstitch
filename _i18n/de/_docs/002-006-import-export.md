---
title: "Import und Export von Dateien"
permalink: /de/docs/import-export/
excerpt: ""
last_modified_at: 2018-06-23
toc: true
---

Ink/Stitch unterstützt viele Stickformate. Es kann Dateien in die unten aufgeführten Formate importieren und exportieren.

## Unterstützte Formate (A - Z):

### Schreiben
DST, EXP, JEF, PEC, PES, VP3

### Lesen
100, 10o, BRO, DSB, DST, DSZ, EMD, EXP, INB, JEF, KSM, PEC, PES, SEW, SHV, STX, TAP, TBF, u01, VP3, XXX

**Info:** Detaillierte Informationen zu Stickdateiformaten gibt es hier [EduTechWiki](http://edutechwiki.unige.ch/en/Embroidery_format).
{: .notice--info }

## Import von Stickdateien

Öffne eine fertige Stickdatei, so wie eine beliebige SVG-Datei in Inkscape geöffnet wird: `Datei -> Öffnen ...`, wähle die Datei aus und wähle `Öffnen`.

Es öffnet die Datei im Modus [Manueller Stich Modus](/docs/stitches/stroke/#manual-stitch-mode). Es können einzelne Punkte bearbeitet und das Design optimiert werden. Sobald alles erledigt ist, speichere die Datei wie unten beschrieben ab.

## Stickdateien exportieren

### Methode 1

Die Version 1.10.0 von Ink/Stitch hat die Möglichkeit, Dateien direkt über den Dialog von Inkscape `Datei -> Speichern als ...` (`Strg + Umschalt + S`) zu exportieren.

Wähle ein Dateiformat, das die Stickmaschine lesen kann, und speichere die Datei im gewünschten Ausgabeverzeichnis.

![Ausgabeformat](/assets/images/docs/export-selection-field.jpg)

Für zukünftige Änderungen stelle sicher, dass auch eine SVG-Version des Designs behalten wird.

### Methode 2 (Stichplan anzeigen)
Um Designs zu exportieren, starte `Erweiterungen -> Ink/Stitch -> Sticken ...`.

![Sticken ...](/assets/images/docs/embroider.jpg){: width="450" }

Einstellungen|Beschreibung
---|---
Mindestlänge (mm)        | 0.0 - 10.0
Andere Ebenen ausblenden | Verberge die ursprünglichen Design-Ebenen, während der Neuerstellung des Stichplans
Ausgabeformat            | Wähle ein Dateiformat, dass die Stickmaschine lesen kann
Verzeichnis              | Gib Verzeichnis an, in dem die Datei gespeichert werden soll. Das verwendete Verzeichnis ist standardmäßig der Ort, an dem die Erweiterung installiert ist.

**Info:** Für die Dateiformatkonvertierung verwendet Ink/Stitch [*pyembroidery*](https://github.com/inkstitch/pyembroidery).
{: .notice--info }

## Batch-Export

**Info:** Seit Ink/Stitch Version 1.10.0 ist es möglich, mehrere Dateiformate gleichzeitig zu exportieren.
{: .notice--info }

Unter `Datei -> Speichern unter ...` wähle den kleinen Pfeil im Dateiformat-Auswahlfeld, um eine Liste der verfügbaren Dateiformate zu öffnen.

Navigiere zum gewünschten Ausgabeverzeichnis und wähle dort das `Ink/Stitch: Export von mehreren Formaten (.zip)` aus. Klicke auf "Speichern". Dort wird  gefragt, welche Dateiformate hinein sollen.

![Batch Export](/assets/images/docs/export-batch.jpg)


