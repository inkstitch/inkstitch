---
title: "Point Satin en Zigzag"
permalink: /fr/docs/stitches/zigzag-satin-stitch/
last_modified_at: 2024-05-02
toc: true
---
## Qu'est-ce que c'est

Le satin en  "zigzag" est une colonne satin avec un air de zigzag

![Point Satin Zigzag](/assets/images/docs/en/compare-satin-zigzag.png)

## Comment le créer

Préparez votre chemin exactement comme vous le feriez pour une [Colonne Satin](/fr/docs/stitches/satin-column). 
Mais dans les paramètres choisissez la méthode `Zigzag`.

## Paramètres

### Couche supérieure du satin

|Paramètres||Description|
|---|---|--|
|Colonne  de satin personnalisée   | ☑ |Doit être activé pour que ces paramètres prennent effet|
|Méthode                       | | Choisir `Zigzag`|
|Décalage des points courts    | ![Short Stitch example](/assets/images/docs/params-satin-short_stitch_inset.png) |Les points dans les zones à forte densité seront raccourcis de ce pourcentage.|
|Distance des points courts    | ![Short Stitch example](/assets/images/docs/params-satin-short_stitch_distance.png) |Faire des points courts si la distance entre les crêtes est inférieure à cette valeur.|
|Espacement de Zig-zag         |![exemple d'espacement de zig-zag](/assets/images/docs/params-satin-zig-zag-spacing.png)|la distance de crête à crête entre les zig-zag|
|Pourcentage de compensation d'étirement |![Pull compensation example](/assets/images/docs/params-satin-pull_compensation.png)|Compensation d'étirement proportionnelle à la largeur du point satin. Deux valeurs séparées par un espace peuvent être utilisées pour un effet asymétrique.|
|Compensation d'étirement      |![exemple de compensation d'étirement](/assets/images/docs/params-satin-pull_compensation.png)|Les points Satin [resserrent le tissu](/fr/tutorials/push-pull-compensation/),   il en résulte une colonne plus étroite que votre dessin dans Inkscape. Ce paramètre étend chaque paire de pénétrations d’aiguilles vers l’extérieur de la colonne satin. Vous devrez expérimentalement déterminer le montant de la compensation en tenant compte de votre tissu, de votre fil et de votre stabilisateur.<br /> Deux valeurs séparées par un espace peuvent être utilisées pour un effet asymétrique.<br /> Une valeur négative contracte.|
Inverser la direction des rails    |![Reverse Rung](/assets/images/docs/satin-reverse-rung.png) |Ceci peut aider si le rendu de votre satin est étrange. <br />Options:<br /> ◦ Automatique, valeur par défaut, cherche à détecter et corriger le cas des rails ayant des directions opposées.  <br />◦ Ne pas inverser désactive la détection automatique <br />◦ Inverser la direction du premier rail <br />◦ Inverser la direction du second rail <br />◦ Inverser la direction des deux rails
|Échanger les rails            |☑ |Échange les deux rails de la colonne satin, ce qui affecte le côté de fin de broderie ainsi que tous les paramètres asymétriques|
|Longueur minimum de point||Est prioritaire par rapport à la valeur de la longueur minimum de point définie dans les préférences. Les points plus courts seront supprimés.|
|Longueur minimum de saut||Est prioritaire par rapport à la valeur de la longueur minimum de saut définie dans les préférences. Si la distance à l'objet suivant est inférieure, il n'y aura pas de points d'arrêt, sauf si les points d'arrêts sont forcés.|
|Autoriser les points d'arrêts | ☑|Ajoute un point d'arrêt à la ou les positions choisies.|
|Forcer les points d'arrêts    | ☑ | Force un point d'arrêt après l'objet indépendamment de la valeur de "Saut de fil" dans les Préférences d'Ink/Stitch|
|Point d'arrêt initial              | |Choisir le [style désiré](/fr/docs/stitches/lock-stitches/).|
|Point d'arrêt final                 | |Choisir le [style désiré](/fr/docs/stitches/lock-stitches/).|
|Arrêter après                 |☑ |Fait faire une pause à la machine après avoir brodé cet objet. Si une position d'arrêt a été définie, elle est rejointe par un saut avant la pause. |
|Couper après                  |☑ | Coupe le fil après avoir brodé cet objet|
|Augmentation aléatoire de la largeur du satin (%)|![Random width increase](/assets/images/docs/params-satin-random-width-increase.png)| Élargir le satin d'au plus ce pourcentage. Deux valeurs séparées par un espace peuvent être utilisées pour un effet asymétrique.|
|Diminution aléatoire de la largeur du satin (%) |![Random width decrease](/assets/images/docs/params-satin-random-width-decrease.png)| Réduire la largeur du satin d'au plus ce pourcentage. Deux valeurs séparées par un espace peuvent être utilisées pour un effet asymétrique.|
|Pourcentage aléatoire pour l'espacement zigzag               |![Random zigzag spacing](/assets/images/docs/params-satin-random-zigzag-spacing.png)|Pourcentage maximum d'augmentation à appliquer à  l'espacement zigzag.|
|Méthode de découpage  | ![default](/assets/images/docs/param_split_satin_default.png) ![simple](/assets/images/docs/param_split_satin_simple.png) ![stager](/assets/images/docs/param_split_satin_stagered.png) | Options:<br /> ◦ Par défaut  <br />◦ Simple <br />◦ Décalé
|Longueur maximale du point    | ![Maximum stitch length](/assets/images/docs/params-satin-maximum_stitch_length.png) | Les points plus longs seront découpés en plusieurs points.
|Déplacement aléatoire pour le découpage des points           |![Random split stitch jitter](/assets/images/docs/params-satin-random-split-stitch-jitter.png)| Si le découpage totalement aléatoire des points est activé, ce paramètre rend la longueur du point aléatoire, sinon, le déplacement aléatoire du découpage se fait autour de sa position normale|
|Découpage totalement aléatoire des points                     | ☑ |Si activé, le découpage des points est totalement  aléatoire (ce qui risque de modifier le nombre de points par zig (ou par zag)), sinon, le nombre de points par zig est conservé, mais leur position sur le zig peut varier du déplacement aléatoire paramétré.|
|Longueur minimum du point si découpage totalement aléatoire   |  | Par défaut, prend la valeur de la longueur maximum du point. Une valeur inférieure permet une meilleure transition entre les points découpés et les points non découpés.|
|Graine Aléatoire              | | Utiliser cette graine aléatoire pour le calcul du plan de broderie. Si vide, utilise l'identificateur de l'élément. Relancer le dé si vous n'êtes pas satisfait du résultat.|
{: .params-table }

Pour le paramétrage de la sous-couche, se référer [au paramétrage des colonnes satin](/fr/docs/stitches/satin-column/).

## Fichiers exemples contenant du satin en zigzag

{% include tutorials/tutorial_list key="stitch-type" value="zigzag-satin-stitch" %}
