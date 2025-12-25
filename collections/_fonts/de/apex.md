---
title: "Apex Lake"
permalink: /de/fonts/apex/
last_modified_at: 2023-04-24
toc: false
preview_image:
 - url: /assets/images/fonts/apex_lake.jpg
   height: 60
 - url: /assets/images/fonts/apex_simple_AGS.jpg
   height: 35
data_title:
  - apex_lake
  - apex_simple_AGS
  - apex_simple_small_AGS
---
{%- assign font1 = site.data.fonts.apex_lake.font -%}
{%- assign font2 = site.data.fonts.apex_simple_AGS.font -%}
{%- assign font3 = site.data.fonts.apex_simple_small_AGS.font -%}

![Apex Lake](/assets/images/fonts/apex_lake.jpg)

![Apex Simple](/assets/images/fonts/apex_simple_AGS.jpg)

<hr>

{% include upcoming_release.html %}

![Apex Simple AGS](/assets/images/fonts/apex_simple_small_AGS.jpg)

## Schriftzeichen

Glyphen sind identisch (bis auf die Dekoration)

### Apex Lake

Diese Schrift enthält  {{ font1.glyphs.size }} Schriftzeichen:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Apex Simple AGS

Diese Schrift enthält  {{ font2.glyphs.size }} Schriftzeichen:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Apex Simple small AGS

Diese Schrift enthält  {{ font3.glyphs.size }} Schriftzeichen:

```
{{ font3.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Besonderheiten

Apex Lake ist eine Schriftart für Einzelbuchstaben. 

Wer den Rahmen nicht sticken möchten, überspringt die letzten beiden Schritte.  

Wer einen Stoff mit in die Umrandung applizieren möchte, verwendt eine Kopie des vorletzten Pfades, als Platzierungsstich für den Applikationsstoff.

Um eine zu dicke Stickerei zu vermeiden, ist das Hintergrundmotiv bei den meisten Schriftzeichen unvollständig. Wer es alleine als Dekoration verwenden möchte, findet es vollständig in dem Zeichen J.

Die beiden Versionen passen gut zusammen. Es bietet sich an für den ersten Buchstaben Apex Lake zu nutzen und anschließend Apex Simple AGS.

![Both_Apex](/assets/images/fonts/both_apex.png)

## Maße

### Apex Lake

Apex Lake ist eine große Schrift, sie ist dafür gedacht, einen Buchstaben oder sehr wenige Buchstaben gleichzeitig zu verwenden. 

Mit einer Skalierung von 100% ist sie ca. 60 mm hoch. Sie kann bis zu 80% verkleinert (50mm) und bis zu 130% vergrößert (110mm) werden.

### Apex Simple AGS

Mit einer Skalierung von 100% ist sie ca. 35 mm hoch. Sie kann bis zu 75% verkleinert (25mm) und bis zu 300% vergrößert (100mm) werden.

### Apex Simple Small AGS

Bei einer Skalierung von 100% hat die Schrift eine ungefähre Höhe von {{ font3.size }} mm. 

Sie kann von {{ font3.min_scale | times: 100 | floor }}% ({{ font3.size | times: font3.min_scale }} mm)
bis zu {{ font3.max_scale | times: 100 | floor }}% ({{ font1.size | times: font3.max_scale }} mm) skaliert werdens.

## Farben sortieren

Wenn man mehrere Buchstaben sticken möchte, kann man die Farben sortieren. Das ist möglich, man muss aber die relative Reihenfolge innerhalb der einzelnen Buchstaben beachten. [So geht's](https://inkstitch.org/de/docs/lettering/#sortierung-von-farben)

## Impressionen

Wie wäre es auf einem schicken T-Shirt? Oder auf einem Stoffkorb?

{%include folder-galleries path="fonts/apex-lake/" %}

## Lizenz

[Lizenz herunterladen (Apex Lake)](https://github.com/inkstitch/inkstitch/tree/main/fonts/apex_lake/LICENSE)

[Lizenz herunterladen (Apex simple)](https://github.com/inkstitch/inkstitch/tree/main/fonts/apex_simple_AGS/LICENSE)
