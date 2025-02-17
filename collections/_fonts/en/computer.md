---
title: "Computer"
permalink: /fonts/computer/
last_modified_at: 2025-02-17
toc: false
preview_image:
  - url: /assets/images/fonts/computer.png
    height: 23
  - url: /assets/images/fonts/computer.png
    height: 6

data_title:
  - computer
  - computer_small
---
{%- assign font1 = site.data.fonts.computer.font -%}

{%- assign font2 = site.data.fonts.computer_small.font -%}

{% include upcoming_release.html %}

<img 
     src="/assets/images/fonts/computer.png"
     alt="Emilio20" height="23">
     
<img 
     src="/assets/images/fonts/computer.png"
     alt="Emilio20" height="6">

## Glyphs

These fonts contain  {{ font1.glyphs.size }} glyphs:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

### Computer
It can be scaled from {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
up to {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Computer Small
It can be scaled from {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
up to {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).

## Special features
Each glyph contains the  original letter, in the form of a hidden black fill. These fills are not intended to be embroidered as is, but to help anyone who wants to modify this font. They can be ignored safely.

## In real life

{% include folder-galleries path="fonts/computer/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/computer/LICENSE)
