---
title: "Simulation"
permalink: /fr/docs/simulate/
excerpt: ""
last_modified_at: 2019-10-24
toc: true
---

Sélectionnez les objets que vous souhaitez voir dans un aperçu simulé. Si vous souhaitez regarder toute votre conception simulée, sélectionnez tout (`Ctrl+A`) ou rien.

Puis faites `Extensions > Ink/Stitch  > Simulate` et appréciez.

## Raccourcis pour la Simulation 

Raccourci | Effet
-------- | --------
<key>→</key> | Avancer
<key>←</key> | Reculer
<key>↑</key> | Accélérer
<key>↓</key> | Ralentir
<key>+</key> | Une image en avant
<key>-</key> | Une image en arrière
<key>p</key> | Pause animation
<key>r</key> | Redémarrer animation
<key>o</key> | Afficher les points de pénétration de l'aiguille
<key>q</key> | Fermer

C'est aussi possible de **zoomer** et de **déplacer** la simulation avec la souris.

## Exécuter le simulateur indépendamment

Exécutez le simulateur sur n'importe quel fichier de broderie pris en charge:

```
PYTHONPATH=/usr/share/inkscape/extensions python -m lib.simulator path/to/myfile.ext
```
