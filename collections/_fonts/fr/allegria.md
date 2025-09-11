---
title: "Allegria"
permalink: /fr/fonts/allegria/
last_modified_at: 2025-09-07
toc: false
preview_image:
 - url: /assets/images/fonts/allegria20.png
   height: 55
 - url: /assets/images/fonts/allegria55.png
   height: 55
data_title:
  - allegria20
  - allegria55
---
{%- assign font1 = site.data.fonts.allegria20.font -%}
{%- assign font2 = site.data.fonts.allegria55.font -%}

{% include upcoming_release.html %}

![Allegria20](/assets/images/fonts/allegria20.png)

![Allegria 55](/assets/images/fonts/allegria55.png)

## Glyphes

### Allegria 20

Cette fonte comporte {{ font1.glyphs.size }} glyphes:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Allegria 55

Cette fonte comporte {{ font2.glyphs.size }} glyphes:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

### Allegria 20

A une échelle de 100% cette fonte a une hauteur approximative de {{ font1.size }} mm. 

Elle peut être redimensionnée de {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
à {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Allegria 55

A une échelle de 100% cette fonte a une hauteur approximative de {{ font2.size }} mm. 

Elle peut être redimensionnée de {{ font2.min_scale | times: 100 | floor }}% ({{ font1.size | times: font2.min_scale }} mm)
à {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).

## Dans la vraie vie

{%include folder-galleries path="fonts/allegria/" %}

## License

[Télécharger la license d'Allegria 20](https://github.com/inkstitch/inkstitch/tree/main/fonts/allegria20/LICENSE)

[Télécharger la license d'Allegria 55](https://github.com/inkstitch/inkstitch/tree/main/fonts/allegria55/LICENSE)
