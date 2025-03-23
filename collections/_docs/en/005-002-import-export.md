---
title: "Import and Export Files"
permalink: /docs/import-export/
last_modified_at: 2024-07-13
toc: true
---
## Import Embroidery Files

Open an embroidery file as you would open any SVG file in Inkscape: `File > Open...` > choose your file and click `Open`.

It will open your file in [Manual Stitch Mode](/docs/stitches/manual-stitch/). You can edit individual points and finetune your design. Once your are satisfied, save the file as described below.

## Export Embroidery Files

Export files directly through Inkscapes `File > Save a copy...` (`Ctrl + Shift + Alt + S`) dialog.

Select a file format that your embroidery machine can read and `Save` the file in your desired output directory.

![File Format Field](/assets/images/docs/en/export-selection-field.jpg)

For later changes make sure that you keep an SVG version of your design as well.

## Batch Export

Go to `File > Save a copy...` and click on the little arrow on the file format selection field to open a list of available file formats.

Navigate to your desired output folder and choose the Ink/Stitch ZIP file format. Click `Save`. You then will be asked which file formats you wish to be included.

![Batch export](/assets/images/docs/en/export-batch.jpg)

If you wish for the files within the zip-archive to have an other name than the previously saved original svg(!) file, insert the file name into the `custom file name` field.

![Batch export options](/assets/images/docs/en/zip-export1.png)

The zip-export also offers panelization options. If repeat values are higher than one Ink/Stitch will create copies of the stitchplan and place them in defined distances.
The distances are measured from the top left position of the original design. Colorblocks will be ordered to reduce color changes.

## Batch Lettering

{% include upcoming_release.html %}

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
* **Color sort:** Wether multicolor fonts should be color sorted or not
* **Add trims:** Wether trims should be added or not (never, after each line, word or letter)
* **Use command symbols:** Wether the trims should be added as command symbols or as a param option (only relevant for svg output)
* **Align Multiline Text:** Define how multiline text should be aligned
* **Lettering along path: text position:** The text position on the `batch lettering` path
* **File formats:** Enter a comma separated list of [file formats](/docs/file-formats/#writing)

### Command line usage

Here is a minimal example for command line usage of the batch lettering extension

```
./inkstitch --extension=batch_lettering --text="Hello\nworld" --font="Abecedaire" --file-formats="svg,dst" input_file.svg > output_file.zip
```

#### Options

Option           |Input Type|Values
-----------------|----------|------
--text           |string    |cannot be empty
--separator      |string    |default: '\n'
--font           |string    |must be a valid font name
--scale          |integer   |default: 100
--color-sort     |string    |off, all, line, word<br>default: off
--trim           |string    |off, line, word, glyph<br>default: off 
--command_symbols|bool      |default: False
--text-align     |string    |left, center, right, block, letterspacing<br>default: left
--file-formats   |string    |must be at least one valid output format
