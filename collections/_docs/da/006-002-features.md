---
title: "Hidden Features"
permalink: /da/docs/features/
excerpt: ""
last_modified_at: 2018-05-04
toc: true
---
## Color Blending

Version 1.4.0 introduced a hidden feature for gradient blending. It doesn't work with a 100% reliability, that's why it's kept hidden.
If you use the XML editor to add the hidden setting `embroider_end_row_spacing_mm`, you'll get an effect like the one described in [#78](https://github.com/inkstitch/inkstitch/issues/78), Exponent Modifier for Fill and Satin (just the fill part).

Notably, certain shapes with complicated holes seem to cause the autofill algorithm to run forever and never finish, and you have to kill the process manually. But for most shapes, it seems to do the job. Combine two such fills going in opposing directions and you'd get a gradient fill.

![image](https://user-images.githubusercontent.com/11083514/38469632-dc97b73c-3b4f-11e8-9044-c03d1f5d17ab.png)


Here's a Tutorial file

[Tutorial-embroider_end_row_spacing_mm.zip](https://github.com/inkstitch/inkstitch/files/1887652/Tutorial-embroider_end_row_spacing_mm.zip)
