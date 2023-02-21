---
title: Patterned Running Stitch
permalink: /ru/tutorials/patterned-unning-stitch/
last_modified_at: 2023-02-20
language: ru
excerpt: "How to create a patterned running stitch with Inkscapes live path effects"
image: "/assets/images/tutorials/pattern-along-path/copy-paste.png"

tutorial-type:
  - Sample File
stitch-type: 
  - Running Stitch
techniques:
field-of-use:
user-level: 
---
Ink/Stitch is an Inkscape plugin. Inkscape has so called `Live Path Effects` (LPE). They can directly be used by Ink/Stitch.

So if we want to create a patterned running stitch we can make use of the LPE `Pattern Along Path`.

1. Create the target path and select it. The target path is a normal [running stitch path](/docs/stitches/running-stitch/).

   ![Target path](/assets/images/tutorials/pattern-along-path/target-path.png)
2. Press `Ctrl+&` to open the LPE-dialog. Alternatively go to `Pah > Path effects...`.
3. Click on the `+` sign in the LPE-dialog and select `Pattern Along Path`

   ![pattern along path](/assets/images/tutorials/pattern-along-path/pattern-along-path.png)
4. In the LPE-dialog chose "Repeated" or "Repeated stretched" for `Pattern copies`

   ![repeat pattern](/assets/images/tutorials/pattern-along-path/repeat.png)
5. There are various methods to apply a pattern to the path. If you want to create your path from scratch, here is how you do it. At the `Pattern source` line, click on the `Edit on canvas` symbol.

    ![edit on canvas](/assets/images/tutorials/pattern-along-path/edit.png)

    In the top left corner you'll see a small path. Zoom in and click on the node on the right side. For the x value enter the length, that you wish to have for your pattern.

    ![set pattern size](/assets/images/tutorials/pattern-along-path/set-size.png)
    
    Now you can edit the path. Double click on the path to add nodes at specific spots and drag the line or nodes to create your pattern. Keep the first and last nodes in place.

    ![final path](/assets/images/tutorials/pattern-along-path/final-path.png)
    
    The patterned path can be copied and altered as any other path. If you need to switch the direction to create a better stitch routing, click on the `Edit on canvas` button again and flip your pattern too.

    ![copy paste](/assets/images/tutorials/pattern-along-path/copy-paste.png)

    [Download SVG](/assets/images/tutorials/pattern-along-path/pattern_along_path.svg){: title="Download SVG File" .align-left download="pattern_along_path.svg" }
