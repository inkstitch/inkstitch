---
title: "Mimosa"
permalink: /de/fonts/mimosa/
last_modified_at: 2025-01-30
toc: false
preview_image:
  - url: /assets/images/fonts/mimosa_medium.png
    height: 32
  - url: /assets/images/fonts/mimosa_large.png
    height: 64
data_title:
  - mimosa_large
  - mimosa_medium
---
{%- assign font1 = site.data.fonts.mimosa_medium.font -%}
{%- assign font2 = site.data.fonts.mimosa_large.font -%}

<img 
     src="/assets/images/fonts/mimosa_medium.png"
     alt="Mimosa Medium" height="32">
     
<img 
     src="/assets/images/fonts/mimosa_large.png"
     alt="Mimosa Large" height="64">
## Schriftzeichen

Diese Schrift enthält  {{ font1.glyphs.size }} Schriftzeichen:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße

### Mimosa Medium
Bei einer Skalierung von 100 % ist diese Schrift {{ font1.size }} mm groß.

Sie kann bis auf {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
herunterskaliert und bis zu {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm hochskaliert  werden.

### Mimosa Large
Bei einer Skalierung von 100 % ist diese Schrift {{ font2.size }} mm groß.

Sie kann bis auf {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
herunterskaliert und bis zu {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm) hochskaliert  werden.


## Impressionen


{%include folder-galleries path="fonts/mimosa/" %}

## Lizenz

[Download Mimosa Medium license](https://github.com/inkstitch/inkstitch/tree/main/fonts/mimosa_medium/LICENSE)

[Download Mimosa Large license](https://github.com/inkstitch/inkstitch/tree/main/fonts/mimosa_large/LICENSE)
