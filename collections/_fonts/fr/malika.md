---
title: "Malika"
permalink: /fr/fonts/malika/
last_modified_at: 2025-02-17
toc: false
preview_image:
  - url: /assets/images/fonts/malika.png
    height: 23
data_title:
  - malika
---
{%- assign font = site.data.fonts.malika.font -%}

![ambigue](/assets/images/fonts/malika.png)

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

Chaque glyphe contient la forme de la lettre originelle, sous forme d'un chemin caché avec un remplissage rouge. Ces chemins ne sont pas prévus pour être brodés tels quels, mais pour aider qui voudrait modifier cette fonte, par exemple pour créer un embossage. Ils peuvent être ignorés sans souci.

## Dans la vraie vie 

{% include folder-galleries path="fonts/malika/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/malika/LICENSE)
