---
title: "Cutwork"
permalink: /docs/cutwork/
excerpt: ""
last_modified_at: 2022-02-18
toc: true
---
This feature will be part of an upcoming Ink/Stitch release. It is not yet integrated in Ink/Stitch v2.1.2
{: .notice--info }

Cutwork in machine embroidery describes an technique, where you use specific needles to cut holes into the fabric. These needles come mostly in a set of four, while each needle is only capable to cut a specific angle range. Therefore it is necessary to split the element that you want to cut into the angle sections of your needles.

Ink/Stitch comes with a tool that will help you to split your elements according to the needle angles.

* Open `Extensions > Ink/Stitch > Cutwork segmentation`
  ![Cutwork segmentation window](/assets/images/docs/en/cutwork-segmentation.png)
* Set the angles and colors as you need them for your specific needle kit

Here is a small list of common needle setups.

Needle|Angle|Start|End
--|--|--
<span class="cwd">&#124;</span>   | 90°  | 67  | 113
<span class="cwd">/</span>        | 45°  | 22  | 68
<span class="cwd">&#8213;</span>  | 0°   | 158 | 23
<span class="cwd">&#x5c;</span>   | 135° | 112 | 157


Brand | #1  | #2 | #3 | #4
--|--|--|--
Bernina                  | <span class="cwd">&#124;</span>                                | <span class="cwd">/</span>                                        | <span class="cwd">&#8213;</span>                                   | <span class="cwd">&#x5c;</span>
Pfaff, Husqvarna Viking, Inspira | Red <span class="cwd" style="background:red;">/</span> | Yellow <span class="cwd" style="background: yellow">&#8213;</span>| Green <span class="cwd" style="background: green;">&#x5c;</span>   | Blue <span class="cwd" style="background: blue">&#124;</span>
Brother, Babylock        | Blue <span class="cwd" style="background: blue;">/</span>      | Purple <span class="cwd" style="background: purple;">&#8213;</span>| Green <span class="cwd" style="background: green;">&#x5c;</span>  | Orange <span class="cwd" style="background: #ff6000;">&#124;</span>
Janome                   | Red <span class="cwd" style="background: #ff3f7e;">&#8213;</span>  | Blue <span class="cwd" style="background: #00abff;">/</span>          | Black <span class="cwd" style="background: #413f57; color: white;">&#124;</span>| Green <span class="cwd" style="background: green;">&#x5c;</span>


Note, that sometimes it would make sense to not fully cut the hole to prevent that the machine will pull in small pieces of fabric.

![A circle cut into pieces by cutwork segmentation](/assets/images/docs/cutwork-segmentation.png)
