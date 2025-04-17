---
title: "Utilliser Ink/Stitch en ligne de commande"
permalink: /fr/docs/command-line/
last_modified_at: 2024-09-10
---

Les extensions Ink/Stitch peuvent être lancées en ligne de commande

## Example  de code de ligne de commandes

### Export en zip

Par exemple si vous souhaitez exporter votre fichier dans une archive zip (avec  un .dst, un .pes  et un fichier de liste de fils vous pouvez lancer la commande suivante

```
./inkstitch --extension=zip --format-dst=True --format-pes=True --format-threadlist=True input-file.svg > output-file.zip
```

### Plan de broderie

Voici un exemple dont la sortie est un fichier de points de broderie svg, pour deux éléments spécifiés, qui cachera les calques de dessin, montrera les points d'aiguilles et sera positionné exactement au dessus du dessin originel.

```
./inkstitch --extension=stitch_plan_preview --id=path1 --id=path2 --move-to-side=False --layer-visibility=hidden --needle-points=True input.svg > output.svg
```

## Options des lignes de commandes pour Inkscape 

Pour un manuel complet des options des lignes de commandes d'inkscape, vous pouvez consulter [leur page de manuel ](https://inkscape.org/doc/inkscape-man.html)

Notez que vous pouvez aussi  combiner les actions d'Ink/Stitch à celles d'Inkscape. Pour voir la liste compléte des actions disponibles :

```
inkscape --action-list
```
