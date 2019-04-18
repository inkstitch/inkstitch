---
title: "Simulate"
permalink: /docs/simulate/
excerpt: ""
last_modified_at: 2019-04-10
toc: true
---

Select the objects you wish to see in a simulated preview. If you want to watch your whole design being simulated, select everything (`Ctrl+A`) or nothing.

Then  run `Extensions > Ink/Stitch  > Simulate` and enjoy.

## Simulation Shortcut Keys

Shortcut Keys | Effect
-------- | --------
<key>→</key> | play forward
<key>←</key> | play backward
<key>↑</key> | speed up
<key>↓</key> | slow down
<key>+</key> | one frame forward
<key>-</key> | one frame backward
<key>p</key> | pause animation
<key>r</key> | restart animation
<key>o</key> | display needle penetration points
<key>q</key> | close

It is also possible to **zoom** and **pan** the simulation with the mouse.

## Run Simulator Independently

Run the simulator by itself on any supported embroidery file:

```
PYTHONPATH=/usr/share/inkscape/extensions python -m lib.simulator path/to/myfile.ext
```
