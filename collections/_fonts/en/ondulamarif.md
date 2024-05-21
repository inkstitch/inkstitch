---
title: "Ondulamarif"
permalink: /fonts/ondulamarif/
last_modified_at: 2024-05-21
preview_image:
  - url: /assets/images/fonts/ondulamarif_XL.png
    height: 110
  - url: /assets/images/fonts/ondulamarif_Medium.png
    height: 82
  - url: /assets/images/fonts/ondulamarif_small.png
    height: 44
---
{%- assign font3 = site.data.fonts.ondulamarif_S.font -%}
{%- assign font2 = site.data.fonts.ondulamarif_Medium.font -%}
{%- assign font1 = site.data.fonts.ondulamarif_XL.font -%}



## Ondulamarif XL

<img 
     src="/assets/images/fonts/ondulamarif_XL.png"
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

It can be scaled 
up to {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm) but should not be  reduced.

## Ondulamarif Medium

<img 
     src="/assets/images/fonts/ondulamarif_Medium.png"
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

It can be used  from {{ font2.min_scale | times: 100 | floor }}% ({{ font1.size | times: font2.min_scale }} mm)
up to {{ font2.max_scale | times: 100 | floor }}% ({{ font1.size | times: font2.max_scale }} mm).

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

It can be used  from {{ font3.min_scale | times: 100 | floor }}% ({{ font1.size | times: font3.min_scale }} mm)
up to {{ font3.max_scale | times: 100 | floor }}% ({{ font1.size | times: fon3.max_scale }} mm).

## Add some color to  Ondulamarif.

A very easy and very effective way to add color to Ondulamarif is to use a variagated  thread.

But it is also a  beautiful bicolor font, when the contours are stitched with a  different  color.

To select  all contours you may either do

*  Ink/Stitch  > Edit > Select embroidery element and then  look for running stitches with bean repeat set to one. Unfortunatly this extension is not currently working for mac user.
 
  or
  
* Inkscape >  Edit > Search and Replace and search for the string "contour" (without the quotes).The search must be extended to properties,  and attribute value must be checked. After clicking Search, all Contours are selected, and a new stroke color may be chosen.


* If you  wish to color sort the letters , [see](https://inkstitch.org//docs/lettering/#color-sorting)

## In real life

{% include folder-galleries path="fonts/ondulamarif/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_XL/LICENSE)

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_Medium/LICENSE)

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_S/LICENSE)

