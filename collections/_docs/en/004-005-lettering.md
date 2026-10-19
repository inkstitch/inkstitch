---
title: "Lettering"
permalink: /docs/lettering/
last_modified_at: 2026-10-18
toc: true
---
## Lettering Tool

The text module creates multi-line text. Choose the right font for your project from a wide variety of pre-digitized fonts.

![Lettering Extensions](/assets/images/docs/en/lettering.png)

### Usage

* Run `Extensions > Ink/Stitch  > Lettering > Lettering`
* Enter your text (multi-line is possible)
* Adjust font family and scaling.<br>
  **⚠ Warning**: For best results please note the limits for scaling in the font description.
* Click on `Apply and Quit`.
* Position your text within the svg document.

### Font filters

* **Font size filter**

  Fonts are designed for a special range of sizes. The font size filter helps you to reduce the font list to only the fonts fitting to your target size.
  A active font filter (not 0) will set the correct scale value when you select a font.

* **Glyphs**

  If checked only the fonts that contain all the glyphs of your text are listed

* **Font categories**

  Filter the fonts by categories, for example get only the applique fonts or only the script fonts

### Options

* **Scale**

  Defines the output size of the font compared to the original font size (%).
  It is recommended to use the scale option, rather than resizing the font on canvas.
  This way you can make sure, that you stay within the parameters the font has been designed for.

* **Align Text**

  Align multiline text: left, center, right, block (default), block (letterspacing)

* **Letter spacing**

  Add that width (mm) between letters

* **Word spacing**

  Add that width (mm) between words

* **Line height**

  Add that height (mm) between lines

* **Color sort**

  Sort colors of multicolor fonts to avoid a huge amount of color changes.

* **Stitch lines of text back and forth**

  With this option enabled the first line will be stitched from left to right and the second from right to left, etc.
  This will give your machine shorter ways to travel.

* **Add trims**

  Adds TRIM commands according to the chosen option (Never, after each line, after each word, after each letter).

* **Use command symbols**

  When adding trims, use command symbols. Uses the trim param setting otherwise.

### Presets

You can save and load your favourite font settings.

## Fonts

An overview of available fonts can be found it the [font library](/fonts/font-library/).

### Create your own fonts

Read the [font creation tutorial](/tutorials/font-creation/).

Contact us if you are willing to publish your font in the Ink/Stitch lettering tool on [GitHub](https://github.com/inkstitch/inkstitch/issues).

## Lettering along path

Ink/Stitch letters are carefully designed. If you try to transform them with common tools, they may not work as expected. This means placing letters along a path will be a lot of work. Therefore we've created a tool to assist you with that.

![curvy text](/assets/images/docs/text_along_path.jpg)

### Usage

* Select a path and a lettering group

  The length of the path should be appropriate for the length of the text. It is important to scale the text using the text tool rather than by manual transformation.
  The text tool also provides an option to increase or decrease the spacing between characters—this is particularly useful when the text is being curved inward.
  {: .notice--info}
* Run `Extensions > Ink/Stitch > Lettering > Lettering along path ...`
* Adjust the options according to your preferences (see below).
* Click on apply

Need to modify the path or adjust your options? You can refine them at any time—even after the text has been transformed—simply by reapplying the function.
{: .notice--info}

### Options

#### Text Position

Ink/Stitch offers several text positioning options to align your lettering along a path:
* **Left:** Places the text at the absolute beginning of the path.
* **Center:** Centers the text at the center of the path.
* **Right:** Aligns the text to the very end of the path.
* **Stretch:** Exands the spacing between characters to span the entire length of the path.

The exact alignment relies on two critical factors: the **starting point** of the path and the **direction** of the path.

![Text aligned along a path using various options](/assets/images/docs/text_along_path_alignment.png)

**Example: Lettering on a Circle**

A common use case is placing text along a circle or an oval. By default in Inkscape, a closed circular object starts at the top and runs counter-clockwise.
Running the simulator reveals that the embroidery path follows this exact behavior. Usually this is not the correct setting for your text positioning.

To adjust the circle, you must first convert the object into a path:
* Go to **Path > Object to Path** (or press `Ctrl + Shift + C`). 
* This action changes both the path direction and the starting point. 
* Verify this in the simulator; the embroidery path will now begin on the middle-right and run clockwise.

To position your text at the top of the circle, you need to **adjust the starting point**:
* Select the Node tool (`N`) and click on the **bottom node**.
* Break the path at this location by pressing `Shift + B`.
* To verify the break, click and drag the node slightly (without releasing the mouse button). You will see a second node hidden underneath.
  Press `Esc` to cancel the move and snap the node back into place. 

Your new starting point is now set at the bottom and the text can be centered at the top.

To change the starting position of a path that has already been broken apart, simply select both of the separated nodes, join them back together (`Shift + J`), and break the path at your new desired location.
{: .notice--info}

Now we need to determine the **path direction**. It is helpful to [display the path direction](/docs/customize/#enabling-path-outlines--direction) for this. Alternatively, you can also check the path direction using the simulator.

When the path direction is going the wrong way, adapt it with `Path > Reverse`.

Here is an example: same settings, but opposite path directions. The text position is set to `Center`.

![Two texts, each aligned to a path. In one case, the path goes from left to right and the text sits on top. The other path goes from right to left, and the text hangs from the bottom of the path, also running from right to left.](/assets/images/docs/text_along_path_path_direction.jpg)

#### Vertical Alignment

With vertical alignment, you determine whether the text should be displayed entirely above the path (`top`), whether the path serves as the `baseline`, or whether the text is shown completely below the path (`bottom`). Here is an example where text has been placed on a path using the options in exactly this order.

![A text aligned using the three alignment options. The difference between Top and Baseline is particularly clear here with the letter p. The top option places the text completely above the path, while the baseline option rests the text on the path, causing the descender of the p to cross the line](/assets/images/docs/text_along_path_vertical_alignment.jpg)

**Example: Patch**

1. To align text at the top, the path must be split at the bottom. The path direction is clockwise. The text position is set to `Center`, and the vertical alignment is `Top`.
2. To align text at the bottom, the path must be split at the top. The path direction is counter-clockwise. The text position is set to `Center`, and the vertical alignment is `Bottom`.
3. Assembled as a patch.

![Text on a circle, positioned at the top and bottom, and assembled as a patch.](/assets/images/docs/text_along_path_patch.jpg)

## Batch Lettering

Batch lettering allows to easily create multiple text files.

![A patch with four different names](/assets/images/docs/batch-lettering.png)

* Prepare a design file.
  If the file contains a path with the label `batch lettering` it will be used for the text position.
  It will work the same say as [Lettering Along Path](/docs/lettering/#lettering-along-path).
* Go to `File > Save a copy...` and click on the little arrow on the file format selection field to open a list of available file formats.
* Choose `Ink/Stitch: batch lettering (.zip)`
* Navigate to your desired output folder and click on Save

### Options

* **Text:** Enter the text, by default each new line will be placed in it's own file
* **Custom Separator:** Defaults to new lines. Specify an other separator if you wish that your text file has multiline text.
  The text will be split and placed into a new file with every occurence of the custom separator.

* **Font name:** The name of the font you wish to use. Have a look at the [font library](/fonts/font-library/) to find a list of available fonts
* **Scale (%):** Scale value to resize a font. The value will be clamped to the available scale range of the specific font.
* **Color sort:** Whether multicolor fonts should be color sorted or not
* **Add trims:** Whether trims should be added or not (never, after each line, word or letter)
* **Use command symbols:** Whether the trims should be added as command symbols or as a param option (only relevant for svg output)
* **Align Multiline Text:** Define how multiline text should be aligned
* **Lettering along path**
  * **horizontal text position:** The horizontal text position along the `batch lettering` path
  * **vertical text position:** The vertical position in relation to the `batch lettering` path
* **File formats:** Enter a comma separated list of [file formats](/docs/file-formats/#writing)

[Download sample file](/assets/images/docs/batch_lettering_template_example.svg){: title="Download SVG File" download="batch_lettering_template_example.svg" }

### Command line usage

Here is a minimal example for command line usage of the batch lettering extension

```
./inkstitch --extension=batch_lettering --text="Hello\nworld" --font="Abecedaire" --file-formats="svg,dst" input_file.svg > output_file.zip
```

#### Options

Option             |Input Type|Values
---------- --------|----------|------
`--text`           |string    |cannot be empty
`--separator`      |string    |default: '\n'
`--font`           |string    |must be a valid font name
`--scale`          |integer   |default: 100
`--color-sort`     |string    |off, all, line, word<br>default: off
`--trim`           |string    |off, line, word, glyph<br>default: off 
`--command_symbols`|bool      |default: False
`--text-align`     |string    |left, center, right, block, letterspacing<br>default: left
`--file-formats`   |string    |must be at least one valid output format

## Sample Files Including Lettering

{% include tutorials/tutorial_list key="techniques" value="Lettering" %}
