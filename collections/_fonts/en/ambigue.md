---
title: "Ambigüe"
permalink: /fonts/ambigue/
last_modified_at: 2025-01-30
toc: false
preview_image:
  - url: /assets/images/fonts/ambigue.png
    height: 26
data_title:
  - ambigue
---
{%- assign font = site.data.fonts.ambigue.font -%}

{% include upcoming_release.html %}

![ambigue](/assets/images/fonts/ambigue.png)

## Glyphs

This font contains  {{ font.glyphs.size }} glyphs:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

At a scale of 100% this font has an approximate height of {{ font.size }} mm. 

It can be scaled from {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
up to {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).

## Special features
Each glyph contains the outline of the original letter, in the form of a hidden black path. These paths are not intended to be embroidered as is, but to help anyone who wants to modify this font, for example to create embossing. They can be ignored without worry.

## In real life

{% include folder-galleries path="fonts/ambigue/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ambigue/LICENSE)
