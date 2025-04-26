---
title: "コリンの書き方"
permalink: /fonts/honoka/
last_modified_at: 2024-05-22
toc: false
preview_image:
  - url: /assets/images/fonts/honoka.jpg
    height: 20
data_title:
  - honoka
---
{%- assign font = site.data.fonts.honoka.font -%}

![Honoka](/assets/images/fonts/honoka.jpg)

## Glyphs

This font contains  {{ font.glyphs.size }} glyphs:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }
This font contains all hiragana, katakana and punctuation symbols plus a few hundred kanjis.

## Dimensions

At a scale of 100% this font has an approximate height of {{ font.size }} mm. 

It can be scaled from {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
up to {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).


## In real life



{% include folder-galleries path="fonts/honoka/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/honoka/LICENSE)
