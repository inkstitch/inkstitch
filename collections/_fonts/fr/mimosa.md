---
title: "Mimosa"
permalink: /fr/fonts/mimosa/
last_modified_at: 2025-01-30
toc: false
preview_image:
  - url: /assets/images/fonts/mimosa_medium.png
    height: 32
  - url: /assets/images/fonts/mimosa_large.png
    height: 64
data_title:
  - mimosa_large
  - mimosa_small
---
{%- assign font1 = site.data.fonts.mimosa_medium.font -%}
{%- assign font2 = site.data.fonts.mimosa_large.font -%}

<img 
     src="/assets/images/fonts/mimosa_medium.png"
     alt="Mimosa Medium" height="32">
     
<img 
     src="/assets/images/fonts/mimosa_large.png"
     alt="Mimosa Large" height="64">

## Glyphes
Ces fontes comportent  {{ font1.glyphs.size }} glyphes:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }


## Dimensions
### Mimosa Medium
A une échelle de  100% cette fonte a une hauteur approximative de  {{ font1.size }} mm. 

Elle peut être redimensionnée  de {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
à {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Mimosa Large
A une échelle de  100% cette fonte a une hauteur approximative de  {{ font2.size }} mm. 

Elle peut être redimensionnée  de {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
à {{ font2.max_scale | times: 100 | floor }}% ({{ fon2t.size | times: font2.max_scale }} mm).


## Dans la vraie vie


{%include folder-galleries path="fonts/mimosa/" %}

[Télécharger la license de Mimosa Medium](https://github.com/inkstitch/inkstitch/tree/main/fonts/mimosa_medium/LICENSE)

[Télécharger la license de Mimosa Large](https://github.com/inkstitch/inkstitch/tree/main/fonts/mimosa_large/LICENSE)
