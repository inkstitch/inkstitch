---
title: "Mimosa"
permalink: /fonts/mimosa/
last_modified_at: 2025-01-30
toc: false
preview_image:
  - url: /assets/images/fonts/mimosa_medium.png
    height: 32
  - url: /assets/images/fonts/mimosa_large.png
    height: 64
data_title:
  - mimosa_large
  - mimosa_small
---
{%- assign font1 = site.data.fonts.mimosa_medium.font -%}
{%- assign font2 = site.data.fonts.mimosa_large.font -%}

{% include upcoming_release.html %}

<img 
     src="/assets/images/fonts/mimosa_medium.png"
     alt="Mimosa Medium" height="32">
     
<img 
     src="/assets/images/fonts/mimosa_large.png"
     alt="Mimosa Large" height="64">
## Glyphs

These fonts contain  {{ font1.glyphs.size }} glyphs:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }


## Dimensions
### Mimosa Medium
At a scale of 100% this font has an approximate height of   {{ font1.size }} mm. 

It can be scaled from  {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
à {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Mimosa Large
At a scale of 100% this font has an approximate height of  {{ font2.size }} mm. 

It can be scaled from  {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
up to {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).


## In real life


{%include folder-galleries path="fonts/mimosa/" %}

## License

[Download Mimosa Medium license](https://github.com/inkstitch/inkstitch/tree/main/fonts/mimosa_medium/LICENSE)

[Download Mimosa Large license](https://github.com/inkstitch/inkstitch/tree/main/fonts/mimosa_large/LICENSE)
