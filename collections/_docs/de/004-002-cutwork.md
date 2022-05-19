---
title: "Cutwork"
permalink: /de/docs/cutwork/
excerpt: ""
last_modified_at: 2022-05-19
toc: true
---
{% include upcoming_release.html %}

Cutwork beschreibt eine Technick im Maschinensticken bei der mit speziellen Nadeln Löcher in den Stoff geschnitten werden. Meistens sind diese Nadeln in einem Vierer-Set erhältich, wobei jede Nadel nur in eine bestimmte Richtung schneiden kann. Daher ist es nötig, Elemente in Winkel-Segmente zu unterteilen.

## Anwendung

Ink/Stitch hält ein Werkzeug bereit, um die Elemente entsprechend der Nadelwinkel zu zerteilen.

* Wähle ein oder mehrere Pfade mit einer Kontur aus.
* Öffne `Erweiterungen > Ink/Stitch > Cutwork Segmentierung ...`
  ![Cutwork segmentation window](/assets/images/docs/en/cutwork-segmentation.png)
* Passe die Winkel und Farben dem vorhandenen Nadelset entsprechend an
* Anwenden

![A circle cut into pieces by cutwork segmentation](/assets/images/docs/cutwork-segmentation.png)

Bei kleinen Elementen kann es nötig sein, Lücken am Rand des Loches zu lassen, so dass der herausgeschnittene Stoff mit dem Reststoff verbunden bleibt. Andernfalls könnte es passieren, dass die Maschine kleine Stoffstücke nach unten zieht.

**Achtung:** Das Design sollte nach Anwendung dieser Funktion nicht mehr rotiert werden.
{: .notice--warning }

## Beispiele für Nadeleinstellungen

Nadel|Winkel|Anfang|Ende
--|--|--
<span class="cwd">&#124;</span>   | 90°  | 67  | 113
<span class="cwd">/</span>        | 45°  | 22  | 68
<span class="cwd">&#8213;</span>  | 0°   | 158 | 23
<span class="cwd">&#x5c;</span>   | 135° | 112 | 157


Firma | #1  | #2 | #3 | #4
--|--|--|--
Bernina                  | <span class="cwd">&#124;</span>                                | <span class="cwd">/</span>                                        | <span class="cwd">&#8213;</span>                                   | <span class="cwd">&#x5c;</span>
Pfaff, Husqvarna Viking, Inspira | Rot <span class="cwd" style="background:red;">/</span> | Gelb <span class="cwd" style="background: yellow">&#8213;</span>| Grün <span class="cwd" style="background: green;">&#x5c;</span>   | Blau <span class="cwd" style="background: blue">&#124;</span>
Brother, Babylock        | Blau <span class="cwd" style="background: blue;">/</span>      | Lila <span class="cwd" style="background: purple;">&#8213;</span>| Grün <span class="cwd" style="background: green;">&#x5c;</span>  | Orange <span class="cwd" style="background: #ff6000;">&#124;</span>
Janome                   | Rot <span class="cwd" style="background: #ff3f7e;">&#8213;</span>  | Blau <span class="cwd" style="background: #00abff;">/</span>          | Schwarz <span class="cwd" style="background: #413f57; color: white;">&#124;</span>| Grün <span class="cwd" style="background: green;">&#x5c;</span>
