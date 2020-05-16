---
title: "Visualize"
permalink: /docs/visualize/
excerpt: ""
last_modified_at: 2020-05-16
toc: true
---
## Simulator

Select the objects you wish to see in a simulated preview. If you want to watch your whole design being simulated, select everything (`Ctrl+A`) or nothing.

Then  run `Extensions > Ink/Stitch  > Visualize and Export > Simulator / Realistic Preview` and enjoy.

### Simulation Shortcut Keys

Shortcut Keys | Effect
-------- | --------
<key>→</key> | play forward
<key>←</key> | play backward
<key>↑</key> | speed up
<key>↓</key> | slow down
<key>+</key> | one frame forward
<key>-</key> | one frame backward
<key>space</key> | pause/start animation

It is also possible to **zoom** and **pan** the simulation with the mouse.

### Run Simulator Independently

Run the simulator by itself on any supported embroidery file:

```
PYTHONPATH=/usr/share/inkscape/extensions python -m lib.simulator path/to/myfile.ext
```

## Stitch Plan Preview

Run `Extensions > Ink/Stitch > Visualize and Export > Stitch Plan Preview`. This will insert the stitch plan directly into your document to the right side of your canvas.
You can inspect it from there and delete it afterwards.


