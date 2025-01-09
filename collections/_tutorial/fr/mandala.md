---
permalink: /fr/tutorials/mandala/
title: Mandala
language: fr
last_modified_at: 2022-06-12
excerpt: "Mandala et Broderie"
read_time: false
image: "/assets/images/tutorials/mandala/whaletail.png"
tutorial-type:
  - 
stitch-type:
  - Running Stitch
tool:
  - Stroke
techniques:
field-of-use:
user-level: 
---

<table>
        <tr>
            <td> <img src="/assets/images/tutorials/mandala/Fullmandala.png" alt="Full Mandala" height="200"/>    </td>
            <td> <img src="/assets/images/tutorials/mandala/whaletail.png" alt="Whale tail" height="200" /></td>
        </tr>
</table>

 



Inkscape permet de construire rapidement et simplement des mandalas. Si l'on prend soin de construire des mandalas avec très peu d'objets isolés,  mais plutôt des 
objets connectés,alors l'outil redwork d'Ink/Stitch permet de les transformer en  une broderie qui se brode avec pas (ou peu) de sauts de fils. 

On peut soit broder un mandala entier, soit l'utiliser pour créer un remplissage original.

Les outils d'Inkscape qui vont nous permettre de construire facilement des mandalas sont les deux effets de chemin  "Reflet miroir"  et "Tourner les copies".

## Construction d'un mandala

### Premières étapes, version simple
Commençons par construire un mandala assez simple. Comme tout mandala, il est plein de symétries


<table>
        <tr>
            <td> <img  src="/assets/images/tutorials/mandala/nopatheffect.png"
     alt="Mirror path  effect" height="200"/> </td>
    <td><img src="/assets/images/tutorials/mandala/jusmirror.png"
     alt="Mirror path  effect" height="200"/> </td>
    <td>   <img 
     src="/assets/images/tutorials/mandala/2patheffect.png"
     alt="Mirror and Rotate" height="200"/></td>
        </tr>
</table>

Ce mandala est composé de:
* en rouge : deux cercles et un genre d'étoile qui sont dessinés une fois et qui n'ont besoin d'aucun  effet de chemin
* en violet : un groupe de chemins  sur lesquels sont appliqués d'une part un effet de chemin Reflet miroir et d'autre part un effet Tourner les copies avec 6 copies.

Voyons en un peu plus de détails comment s'y prendre, rien de tout cela n'est obligatoire, mais cela simplifie le processus:

* Créer un nouveau document inkscape, dans les propriétés du document lui donner une dimension carrée.
* Créer au moins 3 guides. Je les fais tous passer par le point (0,0), et  je leur donne les angles 0°, 90° pour avoir des repères horizontaux et  verticaux et 30° parce que je vais dessiner mes chemins violets entre le guide horizontal et le guide  à 30° (6 copies et le miroir font qu'ils seront reproduits 12 fois et 30=360/12). Un 4-ième guide  à -30° sans être indispensable permet de mieux visualiser. Verrouiller les guides.
* Activer le  magnétisme, uniquement avec les guides et les noeuds.

* Créer d'abord les objets qui ne nécessitent pas d'effet de chemin, et utiliser "Aligner et Distribuer" pour les centrer horizontalement et verticalement par rapport à la page. Verrouiller ces chemins. Ajouter plusieurs cercles concentriques que l'on est pas obligé de garder ensuite peut aider à dessiner.
* Dessiner un chemin dans le triangle entre l'horizontale et le guide des 30°.
* Créer un groupe autour de ce chemin.
* Sélectionner le groupe et ajouter les  deux effets  de chemins sur le  groupe. De cette manière les effets de chemins agiront sur tous les chemins que vous ajouterez  dans le  groupe.

#### Effet de chemin  Reflet miroir

Choisir le mode centre horizontal de la page , le reste des paramètres est sans importance

#### Effet de chemin Tourner les copies
* Choisir le mode normal
* 6 copies
* angle de départ 0°
* angle de rotation 60°
* laisser les autres paramètres tels quels
* cocher distribuer régulièrement
* Avec l'effet de chemin sélectionné, sélectionner l'outil noeud pour afficher les poignées de la rotation et aller placer le centre de la rotation exactement au centre de la page

#### Construire le mandala

Ajoutez des chemins dans ce groupe pour construire votre mandala. Je commence par des objets dont les extrémités sont sur les guides à 0° et 60°, si tout est bien réglé vous devez  voir les copies bien jointives.
Faites en sorte que chaque objet en touche au moins un autre (une petite approximation de moins de 0.5 mm est possible)


![Mandala simple](/assets/images/tutorials/mandala/simplemandala.svg) 

[Télécharger le fichier exemple mandala simple ](/assets/images/tutorials/mandala/simplemandala.svg){: download="simplemandala.svg" }


### Complexifier le mandala
![Mandala moins simple](/assets/images/tutorials/mandala/lesssimplemandala.svg) 

[Télécharger le fichier exemple mandala moins simple ](/assets/images/tutorials/mandala/simplemandala.svg){: download="lessimplemandala.svg" }


Pour un mandala plus complexe, ajoutez des chemins. Attention si vous voulez ajoutez des chemins qui comme les chemins verts de l'exemple ci-dessus sont soit sur un des guides (traits verts) ou traversent les guides (rond verts), il ne faut pas leur appliquer d'effet miroir, seulement la rotation. Le nouvel exemple comporte donc un groupe supplémentaire avec le seul effet de chemin tourner les copies.

### Complexifier encore

Rien n'oblige a utiliser toujours le même nombre de copies. La nouvelle partie du mandala utilise 9 copies et non plus 6 copies.

![Mandala complexe](/assets/images/tutorials/mandala/complexmandala.svg) 

[Télécharger le fichier exemple mandala complexe ](/assets/images/tutorials/mandala/complexmandala.svg){: download="compleximplemandala.svg" }

## Transformer le mandala en redwork

Il suffit de 
* tout  sélectionner 
* Inkscape > Chemins > Objets en chemin
* Extensions > Ink/Stich > Outils: Trait > Redwork
* Allez faire un tour ou boire un café ou passer un coup de fil
* Et admirez le résultat. Si vous obtenez plusieurs groupes connectés c'est que certains objets n'en touchent aucun autre, rectifiez si vous le souhaitez...

## Utilisez le mandala pour un remplissage

Il ne faut pas partir du mandala transformé en redwork mais des groupes avec effets de chemins

* Groupez tout le monde ensemble, appelons ce groupe mandala
* Ici j'ai utilisé un texte écrit avec la police ojuju. Il faut d'abord transformer ce texte en chemin en le selectionant puis Inkscape > Chemins > Objets en chemin
* Faire une  copie du texte.
* Une des copies du texte doit être au dessus du groupe mandala, selectionnez  le groupe mandala et  cette copie,  puis Inkscape > Objet > Decoupe > Définir une découpe
* Placez la deuxième copie du texte au dessus du groupe mandala, selectionnez les deux et Extensions > Ink/Stich > Outils: Trait > Redwork
* Allez vous promenez, mais moins loin, ça devrait aller plus vite.
* Cettte fois-ci vous obtenez trois groupes connectés un par lettre

![Texte mandala](/assets/images/tutorials/mandala/lettremandala.svg) 

[Télécharger le fichier exemple texte mandala ](/assets/images/tutorials/mandala/lettremandala.svg){: download="lettremandala.svg" }







  
  
