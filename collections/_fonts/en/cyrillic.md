---
title: "Кирилиця"
permalink: /fonts/cyrillic/
last_modified_at: 2025-09-07
toc: false
preview_image:
 - url: /assets/images/fonts/cyrillic.png
   height: 25
data_title:
  - cyrillic
---
{%- assign font1 = site.data.fonts.cyrillic.font -%}

{% include upcoming_release.html %}

![Cyrillic](/assets/images/fonts/cyrillic.png)

## Glyphs

This font contains {{ font1.glyphs.size }} glyphs:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

At a scale of 100% this font has an approximate height of {{ font1.size }} mm. 

It can be scaled from {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
up to {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

## In real life 

{%include folder-galleries path="fonts/cyrillic/" %}

## License

[Download Cyrillic Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/cyrillic/LICENSE)
