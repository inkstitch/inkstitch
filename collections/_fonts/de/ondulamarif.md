---
title: "Ondulamarif"
permalink: /de/fonts/ondulamarif/
last_modified_at: 2024-05-25
preview_image:
  - url: /assets/images/fonts/ondulamarif_xl.png
    height: 55
  - url: /assets/images/fonts/ondulamarif_medium.png
    height: 41
  - url: /assets/images/fonts/ondulamarif_small.png
    height: 22
data_title:
  - ondulamarif_S
  - ondulamarif_Medium
  - ondulamarif_XL
---
{%- assign font3 = site.data.fonts.ondulamarif_S.font -%}
{%- assign font2 = site.data.fonts.ondulamarif_Medium.font -%}
{%- assign font1 = site.data.fonts.ondulamarif_XL.font -%}

## Ondulamarif XL

<img 
     src="/assets/images/fonts/ondulamarif_xl.png"
     alt="Ondulamarif XL " height="55">

**At 100% each letter of Ondulamarif XL has 6 ripples. When the font is upscale, the number of ripples increases**
     
### Schriftzeichen

Diese Schrift umfasst  {{ font1.glyphs.size }} Zeichen:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Maße

Bei einer Skalierung von 100% hat diese Schrift eine ungefähre Höhe von {{ font1.size }} mm. 

Sie kann bis zu {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm) hochskaliert, aber nicht verkleinert werden.

## Ondulamarif Medium

<img 
     src="/assets/images/fonts/ondulamarif_medium.png"
     alt="Ondulamarif XL " height="41">

**Each letter of Ondulamarif Medium has 6 ripples**

### Schriftzeichen

Diese Schrift umfasst {{ font2.glyphs.size }} Zeichen:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Maße

Diese Variante kann von {{ font2.min_scale | times: 100 | floor }}% ({{ font1.size | times: font2.min_scale }} mm)
bis zu {{ font2.max_scale | times: 100 | floor }}% ({{ font1.size | times: font2.max_scale }} mm) skaliert werdens.

## Ondulamarif Small

<img 
     src="/assets/images/fonts/ondulamarif_small.png"
     alt="Ondulamarif XL " height="22">

**Each letter of Ondulamarif Smalll has 4 ripples**

### Schriftzeichen
     
Diese Schrift umfasst {{ font3.glyphs.size }} Zeichen:

```
{{ font3.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Maße 

Diese Variante kann von {{ font3.min_scale | times: 100 | floor }}% ({{ font1.size | times: font3.min_scale }} mm)
bis zu {{ font3.max_scale | times: 100 | floor }}% ({{ font1.size | times: fon3.max_scale }} mm) skaliert werden.

## Farben sortieren

In der zweifarbigen Variante ist es sinnvoll die Farben zu sortieren. Dabei sollte die Objekt-Reihenfolge innerhalb einer Farbe eines Zeichens unbedingt beibehalten werden. Eine genauere Beschreibung gibt es beim Text-Modul im Abschnitt [Farben sortieren](/de/docs/lettering/#farben-sortieren).


## Einfarbig ... oder nicht

Ondulamarif kann auch einfarbig gestickt werden. In diesem Fall sollten die Farben niht sortiert werden, sondern eine Farbe auf alle Linien angewendet werden. Dies erspart viele Stickpausen.

Mit mehrfarbigem Garn kann diese Schrift trotzdem farbenfroh sein.


## Impressionen

{% include folder-galleries path="fonts/ondulamarif/" %}

## Lizenz

[Lizenz herunterladen (Ondulamarif XL)](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_XL/LICENSE)

[Lizenz herunterladen (Ondulamarif Medium)](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_Medium/LICENSE)

[Lizenz herunterladen (Ondulamarif Small)](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_S/LICENSE)
