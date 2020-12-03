---
title: "Import und Export von Dateien"
permalink: /de/docs/import-export/
excerpt: ""
last_modified_at: 2020-10-01
toc: true
---

## Import von Stickdateien

Öffne eine fertige Stickdatei, so wie eine beliebige SVG-Datei in Inkscape geöffnet wird: `Datei -> Öffnen ...`, wähle die Datei aus und wähle `Öffnen`.

Es öffnet die Datei im [Manuellen Stich Modus](/de/docs/stitches/manual-stitch). Es können einzelne Punkte bearbeitet und das Design optimiert werden. Sobald alles erledigt ist, speichere die Datei wie unten beschrieben ab.

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

