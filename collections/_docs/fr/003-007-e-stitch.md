---
title: "Point en E"
permalink: /fr/docs/stitches/e-stitch/
excerpt: ""
last_modified_at: 2023-01-20
toc: true
---
## Qu'est-ce que c'est

[![Dauphin au point E](/assets/images/docs/e-stitch-example.jpg){: width="200x"}](/assets/images/docs/e-stitch.svg){: title="Download SVG File" .align-left download="e-stitch.svg" }
Le point "E" est un point de recouvrement simple mais solide pour les éléments appliqués. Principalement pour les vêtements de bébé car leur peau a tendance à être plus sensible. Point en E Détail

![Point E Détail](/assets/images/docs/e-stitch-detail.jpg)

## Comment le créer

Préparez votre chemin exactement comme vous le feriez pour une [Colonne Satin](/fr/docs/stitches/satin-column). Mais dans les paramètres activez `"E" stitch`. N'oubliez pas d'élargir l'espacement du zig-zag pour ce type de point.

![Paramètres Satin Colonne.jpg](/assets/images/docs/en/params-e-stitch.jpg)

**Astuce** Si vos points ne sont pas tournés du bon côté utilisez ["Intervertir les rails satin"](/fr/docs/satin-tools/#intrevertir-les-rails-des-colonnes-satin) .
{: .notice--info }

## Paramétres

|Paramètres||Description|
|---|---|--|
|Colonne satin personnalisée   | ☑ |Doit être activé pour que ces paramètres prennent effet|
|Méthode                       | | Choisir `Point en E`|
|Longueur maximale du point    | ![Maximum stitch length](/assets/images/docs/params-satin-maximum_stitch_length.png) | Les points plus longs seront découpés en plusieus points.
|Décalage des points courts    | |Les points dans les zones à forte densité seront raccourcis de ce pourcentage.|
|Distance des points courts    | |Faire des points courts si la distance entre les crêtes est inférieure à cette valeur.|
|Espacement de Zig-zag         |![exemple d'espacement de zig-zag](/assets/images/docs/params-satin-zig-zag-spacing.png)|la distance de crête à crête entre les zig-zag|
|Pourcentage de compensation d'étirement |![Pull compensation example](/assets/images/docs/params-satin-pull_compensation.png)|Compensation d'étirement proportionelle à la largeur du point satin. Deux valeurs séparées par un espace peuvent être utilisées pour un effet asymétrique.|
|Compensation d'étirement      |![exemple de compensation d'étirement](/assets/images/docs/params-satin-pull_compensation.png)|Les points Satin [resserrent le tissu](/fr/tutorials/push-pull-compensation/),   il en résulte une colonne plus étroite que votre dessin dans Inkscape. Ce paramètre étend chaque paire de pénétrations d’aiguilles vers l’extérieur de la colonne satin. Vous devrez expérimentalement déterminer le montant de la compensation en tenant compte de votre tissu, de votre fil et de votre stabilisateur. Deux valeurs séparées par un espace peuvent être utilisées pour un effet asymétrique.|
Inverser un rail               |![Inverser un rail](/assets/images/docs/satin-reverse-rung.png) | Enabling this may help if your satin renders very strangely.
|Échanger les rails            |☑ |Échange les deux rails de la colonne satin, ce qui affecte le côté de fin de broderie ainsi que tous les paramètres asymétriques|
|Autoriser les points d'arrêts | ☑|Ajoute un point d'arrêt à la ou les positions choisies.|
|Forcer les points d'arrêts    | ☑ | Force un point d'arrêt après l'objet indépendament de la valeur de "Saut de fil" dans les Préférences d'Ink/Stitch|
|Point d'ancrage               | |Choisir le type de point d'ancrage.|
|Point d'arrêt                 | |Choisir le type de point d'arrêt.|
|Couper après                  |☑ | Coupe le fil après avoir brodé cet objet|
|Arrêter après                 |☑ |Fait faire une pause à la machine après avoir brodé cet objet. Si une position d'arrêt a été définie, elle est rejointe par un saut avant la pause. |
|Pourcentage maximum d'augmentation aléatoire de la largeur du satin |![Random width increase](/assets/images/docs/params-satin-random-width-increase.png)| Élargir le satin d'au plus ce pourcentage. Deux valeurs séparées par un espace peuvent être utilisées pour un effet asymétrique.|
|Pourcentage maximum  de diminution aléatoire de la largeur du satin |![Random width decrease](/assets/images/docs/params-satin-random-width-decrease.png)| Réduire la largeur du satin d'au plus ce pourcentage. Deux valeurs séparées par un espace peuvent être utilisées pour un effet asymétrique.|
|Pourcentage aléatoire pour l'espacement zigzag               |![Random zigzag spacing](/assets/images/docs/params-satin-random-zigzag-spacing.png)|Pourcentage maximum d'augmentation à appliquer à  l'espacement zigzag.|
|Déplacement aléatoire pour le découpage des points           |![Random split stitch jitter](/assets/images/docs/params-satin-random-split-stitch-jitter.png)| Si le découpage totalement aléatoire des points est activé, ce paramètre rend la longueur du point aléatoire, sinon, le déplacement aléatoire du découpage se fait autour de sa position normale (sans appliquer d'aléatoire)|
|Découpage totalement aléatoire des points                     | ☑ |Si activé, le découpage des points est totalement  aléatoire (ce qui risque de modifier le nombre de points), sinon, le nombre de points est conservé, mais leur position peut varier du déplacement aléatoire paramétré.|
|Longueur minimum du point si découpage totalement aléatoire   |  | Par défaut, prend la valeur de la longueur maximum du point. Une valeur inférieure permet une meilleure transition entre les points découpés et les points non découpés.|
|Graine Aléatoire              | | Utiliser cette graine aléatoire pour le calcul des attributs. Si vide, utilise l'identificateur de l'élément. Relancer si vous n'êtes pas satisfait du résultat.|
{: .params-table }

For the underlay params have a look at the [satin stitch params](/fr/docs/stitches/satin-column/).

## Fichiers exemples contenant du point en E
{% include tutorials/tutorial_list key="stitch-type" value="E-Stitch" %}

