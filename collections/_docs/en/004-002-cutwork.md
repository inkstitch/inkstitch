---
title: "Cutwork"
permalink: /docs/cutwork/
last_modified_at: 2022-12-30
toc: true
---
Cutwork in machine embroidery describes a technique, where specific needles are used to cut holes into the fabric. These needles come mostly in a set of four. Each needle is capable to cut in a specific angle range. Therefore it is necessary to split an element into the angle sections of your needles.

## Usage

Ink/Stitch comes with a tool that will help you to split your elements according to the needle angles.

* Select one or more stroke objects
* Open `Extensions > Ink/Stitch > Cutwork segmentation`
  ![Cutwork segmentation window](/assets/images/docs/en/cutwork-segmentation.png)
* Set the angles and colors as you need them for your specific needle kit
* Apply

![A circle cut into pieces by cutwork segmentation](/assets/images/docs/cutwork-segmentation.png)

Sometimes it will be necessary to leave gaps in the border of the hole, so that the cutout fabric stays connected to the main piece. This will prevent that the machine pulls in small cutout pieces of fabric.

**Attention:** Do not rotate your design after applying this feature.
{: .notice--warning }

## Common needle setups

Needle|Angle|Start|End
--|--|--
<span class="cwd">&#124;</span>   | 90°  | 67  | 113
<span class="cwd">/</span>        | 45°  | 112 | 157
<span class="cwd">&#8213;</span>  | 0°   | 158 | 23
<span class="cwd">&#x5c;</span>   | 135° | 22  | 68


Brand | #1  | #2 | #3 | #4
--|--|--|--
Bernina                  | <span class="cwd">&#124;</span>                                | <span class="cwd">/</span>                                        | <span class="cwd">&#8213;</span>                                   | <span class="cwd">&#x5c;</span>
Pfaff, Husqvarna Viking, Inspira | Red <span class="cwd" style="background:red;">/</span> | Yellow <span class="cwd" style="background: yellow">&#8213;</span>| Green <span class="cwd" style="background: green;">&#x5c;</span>   | Blue <span class="cwd" style="background: blue">&#124;</span>
Brother, Babylock        | Blue <span class="cwd" style="background: blue;">/</span>      | Purple <span class="cwd" style="background: purple;">&#8213;</span>| Green <span class="cwd" style="background: green;">&#x5c;</span>  | Orange <span class="cwd" style="background: #ff6000;">&#124;</span>
Janome                   | Red <span class="cwd" style="background: #ff3f7e;">&#8213;</span>  | Blue <span class="cwd" style="background: #00abff;">/</span>          | Black <span class="cwd" style="background: #413f57; color: white;">&#124;</span>| Green <span class="cwd" style="background: green;">&#x5c;</span>

## Cutwork with Bernina/Bernette

Save the .inf file along with your .exp file (name it equally) and the machine will recognize the cutwork lines and displays the correct needle numbers (as you defined in the cutwork segmentation tool).

Use the following settings (these are the typical colors, but they do not matter for cutwork recognition):

Needle|Color                                      |Start|End
------|-------------------------------------------|-----|---
1     |<span style="color: #ffff00">#ffff00</span>|67   |113
2     |<span style="color: #00ff00">#00ff00</span>|112  |157
3     |<span style="color: #ff0000">#ff0000</span>|158  |23
4     |<span style="color: #ff00ff">#ff00ff</span>|22   |68
