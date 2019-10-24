---
title: "Hidden Features"
permalink: /fr/docs/features/
excerpt: ""
last_modified_at: 2019-10-24
toc: true
---
## Mélange de couleurs

La version 1.4.0 introduit une fonctionnalité masquée pour le dégradé. Cela ne fonctionne pas avec une fiabilité à 100%, c'est pourquoi elle est gardée cachée.
Si vous utilisez l'éditeur XML pour ajouter le paramètre masqué `embroider_end_row_spacing_mm`, vous obtiendrez un effet similaire à celui décrit dans[#78](https://github.com/inkstitch/inkstitch/issues/78), Exponent Modifier for Fill and Satin (juste la partie remplissage).

Notamment, certaines formes avec des trous compliqués semblent provoquer l'algorithme de remplissage automatique sans fin, et vous devez arrêter le processus manuellement. Mais pour la plupart des formes, cela semble faire l'affaire. Combinez deux de ces remplissages dans des directions opposées et vous obtiendrez un remplissage en dégradé.

![image](https://user-images.githubusercontent.com/11083514/38469632-dc97b73c-3b4f-11e8-9044-c03d1f5d17ab.png)


Voici un fichier de tutoriel

[Tutorial-embroider_end_row_spacing_mm.zip](https://github.com/inkstitch/inkstitch/files/1887652/Tutorial-embroider_end_row_spacing_mm.zip)
