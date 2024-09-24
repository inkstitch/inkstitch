---
title: "Ondulamarif"
permalink: /fonts/ondulamarif/
last_modified_at: 2024-05-21
preview_image:
  - url: /assets/images/fonts/ondulamarif_xl.png
    height: 110
  - url: /assets/images/fonts/ondulamarif_medium.png
    height: 82
  - url: /assets/images/fonts/ondulamarif_small.png
    height: 44
data_title:
  - ondulamarif_S
  - ondulamarif_Medium
  - ondulamarif_XL
---
{%- assign font3 = site.data.fonts.ondulamarif_S.font -%}
{%- assign font2 = site.data.fonts.ondulamarif_Medium.font -%}
{%- assign font1 = site.data.fonts.ondulamarif_XL.font -%}

## Ondulamarif XL

<img 
     src="/assets/images/fonts/ondulamarif_xl.png"
     alt="Ondulamarif XL " height="55">

**At 100% each letter of Ondulamarif XL has 6 ripples. When the font is upscale, the number of ripples increases**

### Glyphs

This font contains  {{ font1.glyphs.size }} glyphs:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Dimensions

At a scale of 100% this font has an approximate height of {{ font1.size }} mm. 

It can be scaled up to {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm) but should not be  reduced.

## Ondulamarif Medium

<img 
     src="/assets/images/fonts/ondulamarif_medium.png"
     alt="Ondulamarif XL " height="41">

**Each letter of Ondulamarif Medium has 6 ripples**

### Glyphs

This font contains  {{ font2.glyphs.size }} glyphs:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Dimensions

This variation allow for a smaller scale

It can be used from {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
up to {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).

## Ondulamarif Small

<img 
     src="/assets/images/fonts/ondulamarif_small.png"
     alt="Ondulamarif XL " height="22">

**Each letter of Ondulamarif Smalll has 4 ripples**

### Glyphs
     
This font contains  {{ font3.glyphs.size }} glyphs:

```
{{ font3.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Dimensions

This variation allow for a smaller scale

It can be used  from {{ font3.min_scale | times: 100 | floor }}% ({{ font3.size | times: font3.min_scale }} mm)
up to {{ font3.max_scale | times: 100 | floor }}% ({{ font3.size | times: fon3.max_scale }} mm).

## Color sorting

When using bicolor  letters, you may wish to color sort. It is possible, providing the sorting respects the relative order inside each letter. [This is a way to do it](https://inkstitch.org/en/docs/lettering/#color-sorting)

## Making the font monochromatic ... or not

You may also embroider ondulamarif with a single thread. In that case, do not color sort but give the  same stroke color to all the font objects. This will save you many stops. 

And it you use a varigated thread, then your font willl  have plenty of colors.

## In real life

{% include folder-galleries path="fonts/ondulamarif/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_XL/LICENSE)

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_Medium/LICENSE)

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_S/LICENSE)

