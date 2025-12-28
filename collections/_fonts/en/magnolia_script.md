---
title: "Magnolia KOR"
permalink: /fonts/magnolia-script/
last_modified_at: 2024-05-29
toc: false
preview_image:
  - url: /assets/images/fonts/magnolia_small.jpg
    height: 15
  - url: /assets/images/fonts/magnolia_KOR.jpg
    height: 31
  - url: /assets/images/fonts/magnolia_bicolor.png
    height: 47
  - url: /assets/images/fonts/magnolia_tamed.png
    height: 47
data_title:
  - magnolia_KOR
  - magnolia_small
  - magnolia_bicolor
  - magnolia_tamed
---
{%- assign font = site.data.fonts.magnolia_KOR.font -%}
{%- assign font2 = site.data.fonts.magnolia_small.font -%}
{%- assign font3 = site.data.fonts.magnolia_bicolor.font -%}
{%- assign font3 = site.data.fonts.magnolia_tamed.font -%}

<img 
     src="/assets/images/fonts/magnolia_small.jpg"
     alt="Magnolia small" height="50">

<img 
     src="/assets/images/fonts/magnolia_KOR.jpg"
     alt="Magnolia KOR" height="100">

<img 
     src="/assets/images/fonts/magnolia_bicolor.png"
     alt="Magnolia bicolor" height="150">

<img 
     src="/assets/images/fonts/magnolia_tamed.png"
     alt="Magnolia tamed" height="150">

## Glyphs

This font contains  {{ font.glyphs.size }} glyphs:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

### Magnolia KOR

At a scale of 100% this font has an approximate height of {{ font.size }} mm. 

It can be scaled from {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
up to {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).


### Magnolia Small

Magnolia Small is a variation of this font with different embroidery settings. Pull compensation, density and underlays are different to allow to scale down between {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)  and {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).

That's why in the lettering dialog window, if using Magnolia Small, you will have to pick up a scale between 25 and 50%. 

Contrarly to Magnolia KOR, Magnolia  Small  **MUST** be embroidered with thread and needle smaller than usual.
A USA 8 (EUR 60) size needle, and 60WT thread **MUST** be used.


### Magnolia Bicolor 

Magnolia Bicolor has an approximate height of {{ font3.size }} mm. 

It can be scaled from {{ font3.min_scale | times: 100 | floor }}% ({{ font3.size | times: font3.min_scale }} mm)
up to {{ font3.max_scale | times: 100 | floor }}% ({{ font3.size | times: font3.max_scale }} mm).

### Magnolia tamed

Mangnolia tamed has an approximate height of {{ font4.size }} mm. 

It can be scaled from {{ font4.min_scale | times: 100 | floor }}% ({{ font4.size | times: font4.min_scale }} mm)
up to {{ font4.max_scale | times: 100 | floor }}% ({{ font4.size | times: font4.max_scale }} mm).


## Color sorting

If you use Magnolia bicolor or Magnolia tamed, you may wish to color sort. It is possible, providing the sorting respects the relative order inside each letter. [This is a way to do it](https://inkstitch.org/en/docs/lettering/#color-sorting)

## In real life

{% include folder-galleries path="fonts/magnolia_KOR/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/magnolia_%20KOR/LICENSE)
