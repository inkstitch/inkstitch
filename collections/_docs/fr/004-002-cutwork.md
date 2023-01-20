---
title: "Richelieu"
permalink: /fr/docs/cutwork/
excerpt: ""
last_modified_at: 2023-01-20
toc: true
---
En broderie machine, Richelieu (cutwork en anglais) décrit une  technique où des aiguilles spécifiques sont utilisées pour découper des trous dans le tissu. Ces aiguilles sont généralement vendues par quatre. Chaque aiguille peut couper selon un angle qui est dans un intervalle spécifique. Il est donc nécessaire de diviser un élément selon les sections d'angle de vos aiguilles.

## Exemple de segmentation

![Un cercle découpé en morceaux par la segmentation Cutwork](/assets/images/docs/cutwork-segmentation.png)

Il sera parfois nécessaire de laisser des espaces sur le périmètre du trou, afin que le tissu découpé reste connecté à la pièce principale. Cela empêchera la machine de  tirer sur des petits morceaux de tissu découpés, causant des problèmes à l'exécution.


## Usage

Ink/Stitch contient un outil qui va vous aider à découper vos éléments selon les angles des aiguilles.

* Selectionnez un ou plusieurs objets contour (sans remplissage). 
* Ouvrir `Extensions > Ink/Stitch > Segmentation Richelieu`
  ![Cutwork segmentation window](/assets/images/docs/fr/cutwork-segmentation.png)
* Définir les angles et les couleurs selon les caractéristiques de votre ensemble d'aiguilles.
* Appliquer.


**Attention:** Ne pas tourner votre dessin après la segmentation.
{: .notice--warning }

## Réglages classiques  des aiguilles


Aiguille|Angle                                    |Début|Fin
------|-------------------------------------------|-----|---
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


## Broderie Richelieu avec  Bernina/Bernette

{% include upcoming_release.html %}

Sauvegarder le fichier .inf avec votre fichier .exp (avec le même nom, seule l'extension différe) et la machine reconnaitra les lignes de coupe et montrera les bons numéros d'aiguilles (tels que défini dans l'outil de segmentation).

Utilisez ce paramètrage (ce sont les couleurs classiques, mais elles n'influencent pas la reconaissance du richelieu):



Aiguille|Couleur                                 |Début|Fin
------|-------------------------------------------|-----|---
1     |<span style="color: #ffff00">#ffff00</span>|67   |113
2     |<span style="color: #00ff00">#00ff00</span>|112  |157
3     |<span style="color: #ff0000">#ff0000</span>|158  |23
4     |<span style="color: #ff00ff">#ff00ff</span>|22   |68

