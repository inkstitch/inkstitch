---
title: "New Features, Updates and Fixes for the upcoming Ink/Stitch version (3.1.0)"
permalink: /upcoming/
last_modified_at: 2024-05-12
sidebar:
  nav: pages
toc: true
---
## Fonts

### New fonts

* [Cats](/fonts/cats) ([#2860](https://github.com/inkstitch/inkstitch/pull/2860))

  ![Cats preview](/assets/images/fonts/cats.jpg)
* [Chicken Little KOR](/fonts/chicken_little/) ([#2839](https://github.com/inkstitch/inkstitch/pull/2839))

  ![Chicken little preview](/assets/images/fonts/chicken_little_KOR.jpg)
* [Chicken Scratch](/fonts/chicken_scratch/) ([#2703](https://github.com/inkstitch/inkstitch/pull/2703))

  ![Chicken Scratch preview](/assets/images/fonts/chicken_scratch.jpg)
* [Colorful](/fonts/colorful/) ([#2887](https://github.com/inkstitch/inkstitch/pull/2887))

  ![Colorfu preview](/assets/images/fonts/colorful.png)
* [Emilio 20 Tartan](/fonts/emilio-20/) ([#2869](https://github.com/inkstitch/inkstitch/pull/2869))

  ![Emilio 20 Tartan preview](/assets/images/fonts/emilio_tartan.png)
* [Invercelia](/fonts/invercelia/) ([#2888](https://github.com/inkstitch/inkstitch/pull/2888))

  ![Invercelia preview](/assets/images/fonts/invercelia.png)
* [Millimarif-bold20](/fonts/milli-marif-bold/) ([#2780](https://github.com/inkstitch/inkstitch/pull/2780))

  ![Millimarif-bold20 preview](/assets/images/fonts/milli_marif.jpg)
* [Roaring twenties KOR](/fonts/roaring_twenties_KOR/) ([#2856](https://github.com/inkstitch/inkstitch/issues/2856))

  ![Roaring twenties preview](/assets/images/fonts/roaring_twenties_KOR.jpg)
* [Violin Serif](/fonts/violin_serif/) ([#2703](https://github.com/inkstitch/inkstitch/pull/2703))

  ![Violin Serif preview](/assets/images/fonts/violin_serif.jpg)

### Font Updates

* Most fonts have now the following glyphs: éèêëÉÈÊËÜÄÖäöüß
  Only exceptions are April en Fleur, Apex Lake, Cherry fonts, Emilio fonts, Fold Inkstitch, Infinipicto, Namskout and Sortefax (they contain only non diacritic glyphs).
* Cherry for Kaalleen has been modified to include a light blue fill and random stitch length cherries.

  ![Cherry for  kaallen preview](/assets/images/fonts/cherry_for_kaalleen.png)
* All fonts have been reworked to be more stable when transformed.

 [#2898](https://github.com/inkstitch/inkstitch/pull/2898)
 [#2894](https://github.com/inkstitch/inkstitch/pull/2894)
 [#2890](https://github.com/inkstitch/inkstitch/pull/2890)
 [#2886](https://github.com/inkstitch/inkstitch/pull/2886)
 [#2871](https://github.com/inkstitch/inkstitch/pull/2871)
 [#2868](https://github.com/inkstitch/inkstitch/pull/2868)
 [#2857](https://github.com/inkstitch/inkstitch/pull/2857)
 [#2850](https://github.com/inkstitch/inkstitch/pull/2850)
 [#2833](https://github.com/inkstitch/inkstitch/pull/2833)
 [#2812](https://github.com/inkstitch/inkstitch/pull/2812)
 [#2807](https://github.com/inkstitch/inkstitch/pull/2807)
 [#2803](https://github.com/inkstitch/inkstitch/pull/2803)
 [#2802](https://github.com/inkstitch/inkstitch/pull/2802)
 [#2793](https://github.com/inkstitch/inkstitch/pull/2793)
 [#2784](https://github.com/inkstitch/inkstitch/pull/2784)
 [#2769](https://github.com/inkstitch/inkstitch/pull/2769)
 [#2762](https://github.com/inkstitch/inkstitch/pull/2762)
 [#2749](https://github.com/inkstitch/inkstitch/pull/2749)
 [#2744](https://github.com/inkstitch/inkstitch/pull/2744)
 [#2742](https://github.com/inkstitch/inkstitch/pull/2742)
 [#2714](https://github.com/inkstitch/inkstitch/pull/2714)
 [#2607](https://github.com/inkstitch/inkstitch/pull/2607)
 [#2579](https://github.com/inkstitch/inkstitch/pull/2579)
 [#2476](https://github.com/inkstitch/inkstitch/pull/2476)
 [#2682](https://github.com/inkstitch/inkstitch/pull/2682)

## New Extensions

### [Apply Palette](/docs/thread-color/#apply-palette)

`Thread Color Management > Apply Palette` ([#2738](https://github.com/inkstitch/inkstitch/pull/2738))

This extension applies nearest colors from a specified thread palette on a design. This will also be recognized by the Ink/Stitch embroidery file and pdf output.

### [Display Stacking order](/docs/visualize/#display-stacking-order)

`Visualize and Export > Display Stacking order` ([#2656](https://github.com/inkstitch/inkstitch/issues/2656))

This extension inserts numbered labels for selected elements into the document to visualize the stitch order.

![Display stacking order](/assets/images/docs/stacking_order.png)

### [Element info](/docs/troubleshoot/#element-info)

`Troubleshoot > Element info` ([#2544](https://github.com/inkstitch/inkstitch/issues/2544))

This extension informs about various parameters of selected stitch elements.

![Element info](/assets/images/docs/en/element_info.png)

### [Font Sampling](/docs/font-tools/#font-sampling)

`Font Management > Font Sampling` ([#2858](https://github.com/inkstitch/inkstitch/issues/2858))

This extension creates a list of all letters in a font. It helps font creators to test the outcome of a new font.

### [Generate Test Swatches from Selection](/docs/edit/#generate-test-swatches-from-selection)

`Edit > Generate Test Swatches from Selection` ([#2528](https://github.com/inkstitch/inkstitch/issues/2528))

This extension allows to easily test different values for embroidery parameters by creating test swatches.

![Example test swatches](/assets/images/docs/test_swatches.png)

### [Jump Stitch to Trim Command](/docs/commands/#jump-to-trim)

`Commands > Jump Stitch to Trim Command` ([#2864](https://github.com/inkstitch/inkstitch/issues/2864))

Inserts trim commands to avoid jump stitches

### [Multicolor Satin](/docs/satin-tools/#multicolor-satin)

`Tools: Satin: Multicolor Satin` ([#2863](https://github.com/inkstitch/inkstitch/issues/2863))

This extension creates copies of selected satins to mimic a multicolor satin

![Multicolor Satin](/assets/images/tutorials/multicolor_satin/solution.png)

### [Outline](/docs/stroke-tools/#outline)

`Stroke tools > Outline` ([#2529](https://github.com/inkstitch/inkstitch/issues/2529), [#2881](https://github.com/inkstitch/inkstitch/issues/2881))

This extension helps reconstruct an original object from a stitch file.

![Fill to outline](/assets/images/docs/outline.png)

### [Tartan](/docs/fill-tools/#tartan)

`Tools: Fill > Tartan` ([#2782](https://github.com/inkstitch/inkstitch/issues/2782))

This extension generates the tartan stripes and applies them to the document either as svg elements or as tartan fill params

### [Unlink Clone](/docs/edit/#unlink-clone)

`Edit > Unlink Clone ...`

This extension unlinks clones (optionally recursive) and applies fill angle transformations

## Extension Updates

### [Cleanup document](/docs/troubleshoot/#cleanup-document)

`Troubleshoot > Cleanup document`

* add option to delete empty groups and layers ([#2552](https://github.com/inkstitch/inkstitch/issues/2552))
* add test run option to display names of the elements that will be removed with the current settings ([#2552](https://github.com/inkstitch/inkstitch/issues/2552))

### [Convert line to Satin](/docs/satin-tools/#convert-line-to-satin)

`Tools: Satin > Conert to Satin`

Do not split into several parts ([#2418](https://github.com/inkstitch/inkstitch/issues/2418))

![Converted square](/assets/images/docs/convert-to-satin-update.png)

### [Density map](/docs/visualize/#density-map)

`Visualize and Export > Density Map`

* add indicator size option ([#2544](https://github.com/inkstitch/inkstitch/issues/2544))
* add ignore layer command ([#2522](https://github.com/inkstitch/inkstitch/issues/2522))

### [Fill to Stroke](/docs/stroke-tools/#fill-to-stroke)

`Tools: Stroke > Fill to Stroke`

* add one centerline group for each selected fill or replace existing fill if it results in only one path ([#2675](https://github.com/inkstitch/inkstitch/issues/2675#issuecomment-1882919122))

### [Force lock stitches](/docs/font-tools/#force-lock-stitches)

`Font Management > Force lock stitches`

* Add "Restrict to Satin" option ([#2773](https://github.com/inkstitch/inkstitch/pull/2773))

### [Jump to Stroke](/docs/stroke-tools/#jump-to-stroke)

`Tools: Stroke > Jump to Stroke`

* Add options ([#2733](https://github.com/inkstitch/inkstitch/pull/2733))
    * Min width
    * Max width
    * Connect only within groups or layers
    * Do not connect after trim, stop or forced lock stitches
    * Merge new strokes with previous/next stroke
    * Merge subpaths ([#2750](https://github.com/inkstitch/inkstitch/pull/2750))

### [Lettering](/docs/lettering/)

`Lettering`

* Add glyph filter ([#2400](https://github.com/inkstitch/inkstitch/issues/2400))

### [Params](/docs/params/)

`Params`

* Improved error reporting ([#2437](https://github.com/inkstitch/inkstitch/issues/2437))
* Add object based min stitch length und min jump stitch length ([#2792](https://github.com/inkstitch/inkstitch/issues/2792))

### [Preferences](/docs/preferences/)

`Preferences`

* electron -> wxpython ([#2479](https://github.com/inkstitch/inkstitch/issues/2479))

### [Print PDF](/docs/print-pdf/)

* Move print pdf back to webbrowser ([#2849](https://github.com/inkstitch/inkstitch/issues/2849))

### [Remove embroidery settings](/docs/troubleshoot/#remove-embroidery-settings)

`Troubleshoot > Remove embroidery settings`

* add option to remove only specific commands ([#2494](https://github.com/inkstitch/inkstitch/issues/2494))

### [Select embroidery elements](/docs/edit/#select-embroidery-elements)

`Edit > Select embroidery elements`

* Option to select satins with no rungs or two rails and two rungs (possible detection conflict) ([#2734](https://github.com/inkstitch/inkstitch/pull/2734))
* Option to select by bean stitch repeats ([#2875](https://github.com/inkstitch/inkstitch/pull/2875))
* Option to select auto-satin underpathing ([#2875](https://github.com/inkstitch/inkstitch/pull/2875))
* Options to select new stitch types

### [Simulator](/docs/visualize/#simulator)

`Visualize and Export > Simulator`

**Important announcement**<br>Realistic and simulator divorced. `Realistic preview` and `Stitch plan preview` started living together.<br><br><span style="font-style: italic;">The realistic preview has been moved to the stitch plan preview.</span>
{: .notice--warning }

The "standalone simulator" has been replaced with the reworked simulator from param and lettering extensions.

* Improved params simulator([#2481](https://github.com/inkstitch/inkstitch/issues/2481))
* Simulator is now attachable/detachable ([#2557](https://github.com/inkstitch/inkstitch/issues/2557))
* Simulator has a changable background color and can show/hide jumps ([#2844](https://github.com/inkstitch/inkstitch/issues/2844))

### [Stitch Plan Preview](/docs/visualize/#stitch-plan-preview)

`Visualize and Export > Stitch Plan Preview`

**Important announcement**<br>The realistic preview has been moved to the stitch plan preview.
{: .notice--warning }

* Add option to keep/overwrite previous stitch plan ([#2642](https://github.com/inkstitch/inkstitch/issues/#2642))
* Add realistic render methods (png, vector) [#2838](https://github.com/inkstitch/inkstitch/issues/2838)

### [Troubleshoot](/docs/troubleshoot/)

`Troubleshoot > Troubleshoot`

* Add warning for satins with two rails and two rungs (possible detection conflict) ([#2734](https://github.com/inkstitch/inkstitch/pull/2734))
* Add no rung warning ([#2791](https://github.com/inkstitch/inkstitch/pull/2791))
* Add warning for elements with stroke and fill color ([#2761](https://github.com/inkstitch/inkstitch/pull/2761))

## Palettes

### New Palettes

* Simthread glow in the dark / 15 colors ([#2752](https://github.com/inkstitch/inkstitch/pull/2752))
* Simthread 63 Brother Colours Polyester ([#2752](https://github.com/inkstitch/inkstitch/pull/2752))

## Stitch types

### Clones

* Improved angle detection for fill clones ([#2766](https://github.com/inkstitch/inkstitch/issues/2766), ([#2834](https://github.com/inkstitch/inkstitch/issues/2834))
* Add ability to render clones of groups ([#2766](https://github.com/inkstitch/inkstitch/issues/2766), ([#2834](https://github.com/inkstitch/inkstitch/issues/2834))
* Improved style detection (([#2834](https://github.com/inkstitch/inkstitch/issues/2834))

### Fill Stitch - family

* Randomize stitch length option ([#2830](https://github.com/inkstitch/inkstitch/issues/2830))
* Smooth underpath ([#2346](https://github.com/inkstitch/inkstitch/issues/2346))
* Prevent fill stitch from going outside the shape ([#2346](https://github.com/inkstitch/inkstitch/issues/2346))
* [Linear gradient fill](/docs/stitches/linear-gradient-fill/): a new stitch type to stitch gradients ([#2587](https://github.com/inkstitch/inkstitch/issues/2587))

  [![Linear gradient fill](/assets/images/docs/linear-gradient.jpg)](/assets/images/docs/linear-gradient.svg)
* Meander fill: add zig-zag option ([#2699](https://github.com/inkstitch/inkstitch/pull/2699))

  [![Zigzag-Meander Grumpy-Cat](/assets/images/docs/zigzagmeander_grumpycat.jpg)](/assets/images/docs/zigzagmeander_grumpycat.svg)

* [Tartan Fill](/docs/stitches/tartan-fill): a new stitch type to mimic tartan patterns ([#2782](https://github.com/inkstitch/inkstitch/issues/2782))

  [![Tartan pattern](/assets/images/docs/tartan-fill.jpg)](/assets/images/docs/tartan-fill.svg)

### Running stitch - family

* Randomize stitch length option ([#2830](https://github.com/inkstitch/inkstitch/issues/2830))

### Satin column - family

* Add stagger option for split stitches ([#2431](https://github.com/inkstitch/inkstitch/issues/2431))
  ![Staggered split stitch example](/assets/images/docs/split-satin-detail.png)
* Add stitch tolerance to satin underlays ([#2814](https://github.com/inkstitch/inkstitch/issues/2431))
* S-Stitch: a new stitch type for the satin stitch type family ([#2431](https://github.com/inkstitch/inkstitch/issues/2431))
  ![S-Stitch](/assets/images/docs/s-stitch-detail.png)
* Zig-Zag: a new stitch type for the satin stitch type family ([#2431](https://github.com/inkstitch/inkstitch/issues/2431))
  ![Zigzag Stitch](/assets/images/docs/en/compare-satin-zigzag.png)

### Polylines

Polylines have been registered as a special stitch type (in fact manual stitchting) in previous Ink/Stitch versions.
They will now be recognized as normal path objects and will render by default as either running stitches (when they have a stroke color)
or as auto fill (when they have a fill color). Existing files with any Ink/Stitch parameters applied will automatically convert polylines
to manual stitches and keep previous behavior. [#2866](https://github.com/inkstitch/inkstitch/issues/2866)

## Export

### Zip-Export

* Add input field for custom file names within the zip file ([#2426](https://github.com/inkstitch/inkstitch/issues/2426))
* Add option to export panel ([#2349](https://github.com/inkstitch/inkstitch/issues/2349))

### Inkscape export dialog

* Ink/Stitch file formats are also available from the Inkscape export dialog ([#2489](https://github.com/inkstitch/inkstitch/issues/2489))

## Install

* Windows is now available as 32 bit and 64 bit version ([#2413](https://github.com/inkstitch/inkstitch/issues/2413))

## Developer Features

* [#2715](https://github.com/inkstitch/inkstitch/issues/2715) Multiversion support
* [#2655](https://github.com/inkstitch/inkstitch/issues/2655) In Ink/Stitch preferences set cache size to 0 to disable caching
* [#2653](https://github.com/inkstitch/inkstitch/issues/2653) [#2720](https://github.com/inkstitch/inkstitch/issues/2720) Updated debug and profiling procedures

## Bug Fixes

* [#2836](https://github.com/inkstitch/inkstitch/issues/2836) Fixes None value param display when multiple elements are selected
* [#2853](https://github.com/inkstitch/inkstitch/issues/2853) Fix an issue with font kerning
* [#2819](https://github.com/inkstitch/inkstitch/issues/2819) Fix cleanup extension
* [#2818](https://github.com/inkstitch/inkstitch/issues/2818) Remove empty d error
* [#2777](https://github.com/inkstitch/inkstitch/issues/2777) Save thread names into embroidery files
* [#2754](https://github.com/inkstitch/inkstitch/issues/2754) Fix lettering along path when glyphs have subgroups or trims
* [#2683](https://github.com/inkstitch/inkstitch/issues/2683) Select embroidery elements: output error message when python path cannot be found
* [#2675](https://github.com/inkstitch/inkstitch/issues/2675) Fix error message on fill to stroke if small fill artifacts are present
* [#2674](https://github.com/inkstitch/inkstitch/issues/2674) Zip: fix error message when no file format is selected
* [#2644](https://github.com/inkstitch/inkstitch/issues/2644) Letters to font: escape labels to allow import of filenames with quotes
* [#2657](https://github.com/inkstitch/inkstitch/issues/2657) Troubleshoot satin: point on rail and not the center of the element
* [#2643](https://github.com/inkstitch/inkstitch/issues/2643) Fix some networkx errors for fill stitches
* [#2603](https://github.com/inkstitch/inkstitch/issues/2603) fix polyline shape 
* [#2637](https://github.com/inkstitch/inkstitch/issues/2637) Add shape property to clone
* [#2638](https://github.com/inkstitch/inkstitch/issues/2638) Troubleshoot: remove old layer before creating a new one to avoid transform (and other) issues
* [#2647](https://github.com/inkstitch/inkstitch/issues/2647) Ignore multipoints in intersect regions with gratings
* [#2635](https://github.com/inkstitch/inkstitch/issues/2635) [#2645](https://github.com/inkstitch/inkstitch/issues/2645) Fix some networkx no path errors
* [#2624](https://github.com/inkstitch/inkstitch/issues/2624) Replace jumps by running stitches in large satin columns
* [#2578](https://github.com/inkstitch/inkstitch/issues/2578) Auto-route Satin: handle sided properties correctly
* [#2566](https://github.com/inkstitch/inkstitch/issues/2566) Update depcrecated inx file descriptions, so they are translatable now
* [#2550](https://github.com/inkstitch/inkstitch/issues/2550) Lettering: error on empty layer in font file
* [#2527](https://github.com/inkstitch/inkstitch/issues/2527) Stitch plan: multiply sequence error
* [#2502](https://github.com/inkstitch/inkstitch/issues/2502) Gradient Blocks: Unit fix
* [#2499](https://github.com/inkstitch/inkstitch/issues/2499) LPE Satin: width of "normal" straight pattern wasn't correct
* [#2491](https://github.com/inkstitch/inkstitch/issues/2491) Toggle commands: fix if first command in invisible group/layer
* [#2468](https://github.com/inkstitch/inkstitch/issues/2468) Zigzag to satin: do not ignore elements in a group
* [#2467](https://github.com/inkstitch/inkstitch/issues/2467) Render context-stroke and context-fill as black
* [#2461](https://github.com/inkstitch/inkstitch/issues/2461) Letters to font: fix guide line insertion
* [#2460](https://github.com/inkstitch/inkstitch/issues/2460) Satin Column: obey reversed rails when synthesizing rungs
* [#2458](https://github.com/inkstitch/inkstitch/issues/2458) Density Map: add ignore layer command
* [#2434](https://github.com/inkstitch/inkstitch/issues/2434) Ignore commands with "empty-d-connectors"
* [#2404](https://github.com/inkstitch/inkstitch/issues/2404) Render satins with only one subpath as running stitch
* [#2403](https://github.com/inkstitch/inkstitch/issues/2403) ignore small contour fill with single or double spiral
