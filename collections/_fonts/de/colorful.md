---
title: "Colorful"
permalink: /fonts/colorful/
last_modified_at: 2024-05-11
toc: false
preview_image:
  - url: /assets/images/fonts/colorful.png
    height: 40
---
{%- assign font = site.data.fonts.colorful.font -%}

{% include upcoming_release.html %} 

![colorful](/assets/images/fonts/colorful.png)
## Schriftzeichen

Diese Schrift enthält  {{ font.glyphs.size }} Schriftzeichen:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße

Bei einer Skalierung auf 100 % ist diese Schrift ungefähr {{ font.size }} mm groß.

Sie kann bis auf {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm) hochskaliert 
und bis zu {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm) herunterskaliert werden.



## Impressionen



{% include folder-galleries path="fonts/colorful/" %}


## Lizenz
[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/colorful/LICENSE)
