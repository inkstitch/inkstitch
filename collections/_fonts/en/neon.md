---
title: "Neon"
permalink: /fonts/neon/
last_modified_at: 2025-09-07
toc: false
preview_image:
 - url: /assets/images/fonts/neon.png
   height: 70
 - url: /assets/images/fonts/neon_blinking.png
   height: 40
data_title:
  - neon
  - neon_blinking
---
{%- assign font1 = site.data.fonts.neon.font -%}
{%- assign font2 = site.data.fonts.neon_blinking.font -%}

{% include upcoming_release.html %}

![Neon](/assets/images/fonts/neon.png)

![Neon Blinking](/assets/images/fonts/neon_blinking.png)

## Glyphs

### Neon

This font contains  {{ font1.glyphs.size }} glyphs:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Neon Blinking

This font contains  {{ font2.glyphs.size }} glyphs:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

### Neon

At a scale of 100% this font has an approximate height of {{ font1.size }} mm. 

It can be scaled from {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
up to {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Neon Blinking

At a scale of 100% this font has an approximate height of {{ font2.size }} mm. 

It can be scaled from {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
up to {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).

## In real life 

{%include folder-galleries path="fonts/neon/" %}

## License

[Download Neon Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/neon/LICENSE)

[Download Neon Blinking Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/neon_blinking/LICENSE)
