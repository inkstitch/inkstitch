---
title: "Simulate"
permalink: /docs/simulate/
excerpt: ""
last_modified_at: 2018-09-16
toc: true
---

Select the objects you wish to see in a simulated preview. If you want to watch your whole design being simulated, select everything (`Ctrl+A`) or nothing.

Then  run `Extensions > Ink/Stitch > English > Simulate` and enjoy.

## Simulation Shortcut Keys

Shortcut Keys | Effect
-------- | --------
**→** | play forward
**←** | play backward
**↑** | speed up
**↓** | slow down
**+** | one frame forward
**-** | one frame backward
**p** | pause animation
**r** | restart animation
**q** | close

It is also possible to zoom and pan the simulation with the mouse.

## Run Simulator Independently

Run the simulator by itself on any supported embroidery file:

```
PYTHONPATH=/usr/share/inkscape/extensions python -m lib.simulator path/to/myfile.ext
```
