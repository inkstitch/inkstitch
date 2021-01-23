---
title: "Create New Fonts for Ink/Stitch"
permalink: /fonts/create/
last_modified_at: 2020-01-02
toc: true
---
@Augusa wrote an excellent article about the creation of new fonts for Ink/Stitch in her blog: [Inkstitch : Créer une police de caractères brodés](https://lyogau.over-blog.com/2020/12/inkstitch-creer-une-police-de-caracteres-brodes.html)

<bold><u>Here you will find a shortened and slightly altered version of her text in english translation.</u></bold><br>

This article wil not explain how to digitize single letters, but how to create a font to be used in the lettering tool of Ink/Stitch.

It would be possible to create a completely new font with the svg font editor tool offered by Inkscape. I will prefer to use an existent font. Using [Fontforge](https://fontforge.org) will make it easy for us to define the kerning (distances between letters) later. 

![Augusa Deja Vu](/assets/images/fonts/augusa_tutorial/augusa_dejavu.png)

A SVG font contains a layer for each glyph. Each layer has to follow a precise pattern. Especially the baseline will be important in order to use the font with Ink/Stitch.

![Augusa Glyph Layers](/assets/images/fonts/augusa_tutorial/augusa_glyph_layer.jpg)

**Warning**<br>Fonts are copyrighted, as are images or embroidery files. It is therefore important to carefully review the required permissions. "Free" does not mean that you can do anything with it. In particular, if the file is to be published for use with Ink/Stitch. The license terms must be strictly adhered to. For example, choose fonts under public domain or Open Font License. In any case, it is advisable to read the license carefully before starting the laborious digitization work.
{: .notice--warning }

After checking the font license carefully, start to determine the size of the font. We have to know the maximum height of the letters above and below the baseline. These values can be determined by writing all uppercase and lowercase letters of the alphabet. In some fonts lower case letters are taller than capitals (e.g. b or l). In the image you can see, that the l is higher than the M.

![Augusa Font Size](/assets/images/fonts/augusa_tutorial/augusa_font_size.jpg)

## Step one: Create a file with glyph layers

  1. Use FontForge and open a ttf-file or any other font-fileformat.

  2. Select those glyphs which you are wanting to digitize. Count the approximate number of glyphs, you will need it later. Make sure to really select every sign you want to digitize, also scroll to the very bottom of the list. The selection shown in the image is not a guide which glyphs to choose.
  
     After you've done your selection go to `Edit > Select > Invert Selection`.

     ![Glyphen-Auswahl](/assets/images/fonts/augusa_tutorial/en_select_glyphs.png)

     Delete the now inverted selection through the menu popup on right click.

     ![Glyphen entfernen](/assets/images/fonts/augusa_tutorial/en_remove_glyphs.png)

  3. Open the General Font Information: `Element > Font Info... > General`

     ![Font Info](/assets/images/fonts/augusa_tutorial/en_font_info.png)

      Define Ascent (maximum height above the baseline), Descent (maxmimum height below the baseline) and Em Size (the sum of ascent ad descent).

  4. Run `File > Generate Fonts > SVG font > Generate` and ignore errors.

     ![Create SVG Font](/assets/images/fonts/augusa_tutorial/en_generate_font.png)

     Fontforge will now generate the svg font file.
 
  5. Open the generated file in Inkscape. It is empty!

     Run `Extensions > Typhographie > Convert SVG font to Glyph layers...`

     ![Convert](/assets/images/fonts/augusa_tutorial/en_convert.png)

      Enter the approximate number of glyphs to convert (higher values will cause no error) and apply

     ![Convert Dialog](/assets/images/fonts/augusa_tutorial/en_convert_dialog.png)

  6. The basic file is done. Now it will be necessary to open `File > Document properties`. In Scale click on `+` and `-` once. This will create a `viewbox` tag in the document which is missing otherwise and the baseline will not be properly regognized by Ink/Stitch.
  
  7. Define font lines. Place the lines while unhiding suitable letters.
     * Descender will be at the lowest point of your glyphs. In most cases the **p** can be used to define it.
     * The baseline (writing line) will be the online one by now which is used by Ink/Stitch to position the glyphs and must be set properly (use e.g. **M**).
     * Caps will define the height of the upper case letters (e.g. **M**).
     * xheight the height of lower case letters (e.g. the top of **x**)
     * Ascender defines the highest point of your glyphs in most fonts it can be set with help of the **l**)

     Now your file will look similar to this:
 
     ![Augusa Schriftlinien](/assets/images/fonts/augusa_tutorial/augusa_schriftlinien.jpg)

Keep the original file. Just in case there will be problems with the font at a later time.
{: .notice--warning}

## Step two: Digitize the Glyphs

We will now beginn to prepare a glyph to be embroiderable.

Satin columns are best for letters. Create them without having the order in mind.

Before you order them correctly save a copy of the file named  `→.svg`. In this copy define the glyph order if it will be stitched from left to right. Each glyph should have its starting point in the lower left corner and end in the lower right corner.

Ink/Stitch comes with a tool "Auto-Route Satin". Use it to order your satin columns. If it runs on all letters without any issue, you don't have to do anythin more. Use your basefile and allow Ink/Stitch to automatically run the Auto-Route Satin tool when inserting the letters into the document.

Otherwise inspect every letter carefully and create separate files for each stitch direction with manual routing.

## Step three: the JSON file

Each font in Ink/Stitch has its own font.json file. The file can be edited with a text editor (e.g. Notepad).

It defines the name of the font and can also contain a short description. Additionally the font spacing will be found here.

![Augusa Schriftlinien](/assets/images/fonts/augusa_tutorial/augusa_json.jpg)

Defining the name will be sufficient for the font to be shown in the Ink/Stitch lettering tool. The result will most propably look unevenly. If font or letters will not show up, inspect your glyphs carefully again, searching for rendering errors.

Additionally to the font files and the json file, also a license file has to be placed into the font folder.

When everything works out, test embroider your font.

![Augusa Schrift](/assets/images/fonts/augusa_tutorial/augusa_roboto.jpg)

## Step four: Kerning

For the font to look even and harmonious the kerning has to be right. Here a little example for better understanding:

![Augusa Avantage 1](/assets/images/fonts/augusa_tutorial/augusa_avantage1.jpg)

*Line 1* was created with the Inkscape text tool. We read "AVANTAGE" without hesitation.

In *line 2* all letters are equally spaced. The reading is more difficult and we hesitate a little between the words "AVANT" and "AGE". We now select all the letters and compare the two lines.

![Augusa Avantage 2](/assets/images/fonts/augusa_tutorial/augusa_avantage2.jpg)

In *line 1* the letters are not evenly arranged, while in *line 2* they are evenly spaced.

For better quality it is therefore necessary to adjust the position of the letters relative to one another and to achieve the best possible kerning. We must therefore examine the position of the letters relative to one another. For example, A and V are close to each other, while G and E are far apart. A font has 2 by 26 letters plus accented characters plus special characters plus punctuation. We quickly come to more than 80 glyphs or 6400 pairs.

---

It's impossible to do that by hand. Now we can benefit from the method that we used to digitize the fonts (FontForge). This means that we have already integrated the correct kerning into the font file and only need to extract it from here.

Ink/Stitch cannot do it automatically yet. But it is planned for a future version.

Please contact the Ink/Stitch team and we will be happy to help.
