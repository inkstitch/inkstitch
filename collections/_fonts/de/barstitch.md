---
title: "Barstitch"
permalink: /de/fonts/barstitch_bold/
last_modified_at: 2025-01-05
toc: false
preview_image:
  - url: /assets/images/fonts/barstitch_bold.png
    height: 12
  - url: /assets/images/fonts/barstitch_textured.png
    height: 20
data_title:
  - barstitch_bold
  - barstitch_textured
---
{%- assign font1 = site.data.fonts.barstitch_bold.font -%}
{%- assign font2 = site.data.fonts.barstitch_textured.font -%}
{% include upcoming_release.html %}

<img 
     src="/assets/images/fonts/barstitch_bold.png"
     alt="Barstitch Bold" height="23">

<img 
     src="/assets/images/fonts/barstitch_textured.png"
     alt="Barstitch textured" height="40">

## Schriftzeichen

Diese Schriften enthalten {{ font1.glyphs.size }} Schriftzeichen:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße
### Barstitch bold

Bei einer Skalierung von 100 % ist diese Schrift {{ font1.size }} mm groß.

Sie kann bis auf {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm) herunterskaliert und bis zu {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm) hochskaliert  werden.

### Barstitch textured

Bei einer Skalierung von 100 % ist diese Schrift {{ font2.size }} mm groß.

Sie kann bis auf {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm) herunterskaliert und bis zu {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm) hochskaliert  werden.

## Impressionen
{% include folder-galleries path="fonts/barstitch/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/barstitch_bold/LICENSE)

