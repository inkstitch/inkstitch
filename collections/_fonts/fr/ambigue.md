---
title: "Ambigüe"
permalink: /fr/fonts/ambigue/
last_modified_at: 2025-01-30
toc: false
preview_image:
  - url: /assets/images/fonts/ambigue.png
    height: 26
data_title:
  - ambigue
---
{%- assign font = site.data.fonts.ambigue.font -%}

![Ambigue](/assets/images/fonts/ambigue.png)

## Glyphes

Cette fonte comporte  {{ font.glyphs.size }} glyphes:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

A une échelle de  100% cette fonte a une hauteur approximative de  {{ font.size }} mm. 

Elle peut être redimensionnée  de {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
à {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).

## Particularités

Chaque glyphe contient le contour de la lettre originelle, sous forme d'un chemin noir caché. Ces chemins ne sont pas prévus pour être brodés tels quels, mais pour aider qui voudrait modifier cette fonte, par exemple pour créer un embossage. Ils peuvent être ignorés sans souci.

## Dans la vraie vie 

{% include folder-galleries path="fonts/ambigue/" %}

## License

[Télécharger la license de la police](https://github.com/inkstitch/inkstitch/tree/main/fonts/ambigue/LICENSE)
