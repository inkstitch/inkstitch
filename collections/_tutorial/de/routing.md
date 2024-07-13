---
title: Stichpad-Optimisierung
permalink: /de/tutorials/routing/
last_modified_at: 2024-06-12
language: de
excerpt: "Optimising the stitch path is one of the most important subjects in embroidery. Learn how Ink/Stitch can assist you with the task."
image: /assets/images/tutorials/routing/routing.png

tutorial-typ:
  - Text
stichart:
  - Füllung
  - Kurvenfüllung
  - Spiralfüllung
  - Mäanderfüllung
  - Satinsäule
  - E-Stich
  - S-Stich
  - Geradstich
  - Mehrfachgeradstich
techniques:
field-of-use:
user-level: 

toc: true
---
Den Stickpfad zu optimisieren ist eine der wichtigsten Aufgaben beim Erstellen einer Stickdatei. Lerne hier, wie Ink/Stitch dir bei dieser Aufgabe helfen kann.

Beim Drucken spielt die Reihenfolge und die Verbindung der Elemente untereinander keine Rolle. Beim Sticken aber sollte man unbedingt darauf achten dass:

* **die Elemente in logischer Reihenfolge aufgebaut sind**

  * Vermeide Farbwechsel so gut wie möglich

    Es kann aber manchmal nötig sein, zusätzliche Farbwechsel zu nutzen, nämlich dann, wenn die Farben mal unterhalb, mal oberhalb anderer Elemente gestickt werden müssen oder
    wenn der Verzug am Stoff andernfalls für die folgenden Elemente zu groß werden würde.
  * Registrierungsprobleme verhinden
  * Knittern im Stoff verhindern

* **Sprungstiche vermieden werde**

  In der gesamten Stickdatei sollten keine unnätigen Sprungstiche vorhanden sein. Versuche nicht, sie durch Fadenschnittbefehle zu verstecken,
  sondern versuche lieber duch geschickte Unterpfade eine bessere Lösung zu finden. Fadenschnitte verursachen Chaos auf der Rückseite der Stickerei und
  verlangsamt die Maschine beim Stickvorgang stark.

Jede Datei ist individuell und du bist der Designer der entscheiden kann wie die Stickpfade aufgebaut sind. Aber Ink/Stitch hält ein paar Werkzeuge bereit, die dich unterstützen können.

## Generelle Pfadoptimisierung

### Objekte in Auswahlreihenfolge sortieren

Elemente im Ebenen und Objekte Dialog hoch und runter zu bewegen kann ermüdend sein. Dafür gibt es einen schnelleren Weg: wähle die Elemente in der gewünschten Stickreihenfolge aus und nutze die Ink/Stitch Erweiterung [Objekte in Auswahlreiehenfolge sortieren](/de/docs/edit/#objekte-in-auswahlreihenfolge-sortieren).

### Sprungstich zu Geradstich

Wenn alle Stickelemente gut vorbereitet sind. Alle in die richtige Reihenfolge gebracht worden sind und die Start- und Endpunkte festliegen, kann die Funktion [Sprungstich zu Geradstich](/de/docs/stroke-tools/#sprungstich-zu-geradstich) die letzten Sprungstiche beseitigen. Sie fügt Geradstiche an den Stellen ein, an denen ein Sprungstich gesetzt werden würde. Ändere den Pfad der neuen Geradstich-Pfade, um die Sprungstiche unter nachfolgenden Stickobjekten zu verstecken.

Gibt es einen kurzen Abstand ohne die Möglichkeit den Geradstich zu verdecken, nutze die Verbindung um kleine Zwischenstiche zu setzen, die beim Sticken in den Stoff einsinken werden.

![Jump to stroke process](/assets/images/docs/jump_to_stroke.png)

*1: Original 2: Sprungstich zu Geradstich 3: Der manuell angepasste Geradstich-Pfad verläuft unter der nachfolgenden Füllung*

## Pfadoptimisierung für linienartige Sticharten

Strokes elements start at the beginning of the path and run til the end.

### Make path directions visible

![Stroke with visible path direction](/assets/images/tutorials/routing/path_direction.png)

In our [customize](/docs/customize/#enabling-path-outlines--direction) article we described, how you can setup Inkscape so that you can see the path direction right away and know where your stroke type stitches will begin and end.

### Adapt stroke direction

You now already made sure, that you can see the path direction. When you select a path and run `Path > Reverse`, Inkscape will reverse the path and the stitching goes the other way around. You may need this function a lot. We recommend to set a shortcut key on it. In the [customize section](/docs/customize/#shortcut-keys) we describe, how that works.

### Params: adapt repeats

When you need to start and end at the same spot of a stroke. You have several options to achieve it. In the [params dialog](/docs/params/), set the number for repeats to an odd number. If you don't want to do that (maybe because you have a bean stitch applied), duplicate the stroke and the direction of the copy.

### Auto-route running stitch / Redwork

When you have a bunch of strokes, it can be a tidious job to route them correctly.
Ink/Stitch now has two tools for it. [Redwork](/docs/stroke-tools/#redwork) is definitely the one to prefer in most cases, since it will take care, that you'll receive exactly two passes for each line. You can set a start position. Redwork will always start and end at the same. If you do not wish that and want to define a start- and end position, then maybe [auto-route running stitch](/docs/stroke-tools/#autoroute-running-stitch) may be the better option for you.


## Satin Routing Options

Satin columns also run from the beginning of the rails to the end, just like a stroke path. Make sure they are no closed paths. Ink/Stitch can handle loops (closed paths), but it may end up in funny results and you cannot control the starting and enting point if there isn't a definite start and end position.

### Auto-route satin

Same as with the stroke type elements, Ink/Stitch has a [routing extension for satins](/docs/satin-tools/#auto-route-satin-columns). It may need some care though as it has one option (preserve oder of running stitches). If you enable it, it will do it's best to route your satins, but doesn't generate running stitches which could connect the satins underneath unrenedered columns. If you enable it, you do not have control of which parts of the satins are on top and which ones are underneath.

Best option so far would be to prepare the order carefully (use the above mentioned extension to order elements) and run auto-route satin with the preserve order option checked. Then with all routed elements selected, run the above mentioned jump to stroke extension to remove all left over jumps. Push the running stitches into a good shape, so that they are hidden when possible.

### Cut Satin

When you cut a satin column for better routing, you may lose the param settings. So it's better to use the Ink/Stitch [extension to cut the satin](/docs/satin-tools/#cut-satin-column) and keep the previous setup.

### Params: swap rails

In the [params dialog](/docs/params/) it is possible to swap the rail on which the stitches will start and on which stitches will end. Be aware that all sided properties with be swapped, so you may need to adjust a few of them if you only want to swap the start position. A default satin column doesn't have any other sided property except for the start and end position.

### Params: reverse rails

In the [params dialog](/docs/params/) you can also switch the stitch direction of the whole satin.

### Params: adapt centerline underlay repeats

When you adapt the repeat value for the centerline underlay in the [params dialog](/docs/params/) to an odd value, the satin column will start and end at the same side. This can be an easy option to avoid manual running stitches for routing.

## Fill Routing Options

### Start- and Stop commands

The start and end position of fill elements can be defined with [visual commands](/docs/commands/) (Fill stitch starting / ending position). If you set a lot of these commands the canvas can become a bit crowded. So it might be good to know, that commands will still work, even when invisible.
