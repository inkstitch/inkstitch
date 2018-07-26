---
title: "Ink/Stitch XML Namespace"
permalink: /namespace/
excerpt: "Document of all metadata tags and embroidery attributes - in future"
---
This page contains a description of all metadata tags and embroidery attributes.

See the [namespace github discussion](https://github.com/inkstitch/inkstitch/issues/202).

## Namespace Declaration

`<svg>` attribute: `xmlns:inkstitch="http://inkstitch.org/namespace"`

## Embroider

|Attribute of `<path>`                              | Data Type| Description |
|---|---|
|embroider_angle                                    | float    |  |
|embroider_auto_fill                                | boolean  |  |
|embroider_center_walk_underlay                     | boolean  |  |
|embroider_center_walk_underlay_stitch_length_mm    | float    |  |
|embroider_contour_underlay                         | boolean  |  |
|embroider_contour_underlay_inset_mm                | float    |  |
|embroider_contour_underlay_stitch_length_mm        | float    |  |
|embroider_expand_mm                                | float    |  |
|embroider_fill_underlay_angle                      | float    |  |
|embroider_fill_underlay                            | boolean  |  |
|embroider_fill_underlay_inset_mm                   | float    |  |
|embroider_fill_underlay_max_stitch_length_mm       | float    |  |
|embroider_fill_underlay_row_spacing_mm             | float    |  |
|embroider_fill_underlay                            | boolean  |  |
|embroider_flip                                     | boolean  |  |
|embroider_manual_stitch                            | boolean  |  |
|embroider_max_stitch_length_mm                     | float    |  |
|embroider_pull_compensation_mm                     | float    |  |
|embroider_repeats                                  | float    |  |
|embroider_row_spacing_mm                           | float    |  |
|embroider_running_stitch_length_mm                 | float    |  |
|embroider_satin_column                             | boolean  |  |
|embroider_staggers                                 | float    |  |
|embroider_zigzag_spacing_mm                        | float    |  |
|embroider_zigzag_underlay                          | boolean  |  |
|embroider_zigzag_underlay_inset_mm                 | float    |  |
|embroider_zigzag_underlay_spacing_mm               | float    |  |


## Visual Commands

|Attribute of `<use>`| Description|
|---|---|
|xlink:href="#inkstitch_fill_start"   | Fill Start |
|xlink:href="#inkstitch_fill_end"     | Fill End   |
|xlink:href="#inkstitch_stop"         | Stop       |
|xlink:href="#inkstitch_trim"         | Trim       |
|xlink:href="#inkstitch_ignore"       | Ignore     |

## Print PDF

|Elements within `<metadata>`                     | Data Type           | Description                                       |
|---|---|---|
|inkstitch:paper-size                             | string [A4,Letter]  | Paper Format                                      |
|inkstitch:operator-overview                      | boolean             | Wether operator overview should be displayed      |
|inkstitch:operator-detailedview                  | boolean             | Wether operator detailedview should be displayed  |
|inkstitch:client-overview                        | boolean             | Wether client overview should be displayed        |
|inkstitch:client-detailedview                    | boolean             | Wether client detailedview should be displayed    |
|inkstitch:operator-detailedview-thumbnail-size   | integer             | Size of operator detailedview thumbnails in mm    |
|inkstitch:thread-palette                         | string              | Name of the thread palette                        |
|inkstitch:title                                  | string              | Job title                                         |
|inkstitch:client-name                            | string              | Client name                                       |
|inkstitch:purchase-order                         | string              | Purchase order                                    |
|inkstitch:client-overview-transform              | string [matrix(n,n,n,n,n,n)] | CSS 2D tranformation                     |
|inkstitch:color-000000                           | string              | Name of the color specified by RGB color value  (here: 000000) |
|inkstitch:thread-000000                          | string              | Name of the thread specified by RGB color value (here: 000000) |
|inkstitch:operator-notes-block1                  | string              | Color block note specified by block number (here: 1) |

