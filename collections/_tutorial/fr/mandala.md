---
permalink: /fr/tutorials/mandala/
title: Mandala
language: fr
last_modified_at: 2022-06-12
excerpt: "Mandala et Broderie"
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

 



Inkscape permet de construire rapidement et simplement des mandalas. Si l'on prend soin de construire des mandalas avec très peu d'objets isolés,  mais plutot des 
objets connectés,alors l'outil redwork d'Ink/Stitch permet de les transformer en  une broderie qui se brode avec pas (ou peu) de sauts de fils. 

On peut soit broder un mandala entier, soit l'utiliser pour créer un remplissage original.

Les outils d'Inkscape qui vont nous permettre de construire facilement des mandalas sont les deux effets de chemin  "Reflet mirroir"  et "Tourner les copies".

## Construction d'un mandala

### Premières étapes, version simple
Commençons par construire un mandala assez simple. Comme tout mandala, il est plein de symmétries.


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
* en violet : un groupe de chemins  sur lesquels sont appliqués d'une part un effet de chemin Reflet Mirroir et d'autre part un effet Tourner les copies avec 6 copies.

Voyons en un peu plus de détails comment s'y prendre, rien de tout cela n'est obligatoire, mais cela simplifie le processus:

* Créer un nouveau document inkscape, dans les propriétés du document lui donner une dimension carrée
* Créer au moins 3 guides. Je les fais tous passer par le point (0,0), et  je leur donne les angles 0°, 90° pour avoir des repères horizontaux et  verticaux et 30° parce que je vais dessiner mes chemins violets entre l'horizonal et ce guide (6 copies et le mirroir font qu'ils seront reproduits 12 fois et 30=360/12). Un 4 ième guide  à -30° sans être indispensable permet de mieux visualiser. Vérouiller les guides
* Activer le magnetisme, uniquement pour les guides et les noeuds

* Créer d'abord les objets qui ne necessitent pas d'effet de chemin, et utiliser "Aligner et Distribuer" pour les centrer horizontalement et verticalement par rapport à la page. Vérouiller ces chemins
* Dessiner un chemin dans le triangle entre l'horizontale et le guide des 30 degrés
* Créer un groupe autour de ce chemin
* Sélectionner le groupe et ajouter les  deux effets  de chemins sur le  groupe. De cette manière les effets de chemins agiront sur tous les chemins que vous ajouterez  dans le  groupe

#### Effet de chemin  Reflet Mirroir

Choisir le mode centre horizontal de la page , le reste des paramètres est sans importance

#### Effet de chemin Tourner les copies
* Choisir le mode normal
* 6 copies
* angle de départ 0
* angle de rotation 60
* laisser les autres paramètres tels quels
* cocher distribuer régulièrement
* Avec l'effet de chemin sélectionné, sélectionner l'outil noeud pour afficher les poignées de la rotation et aller placer le centre de la rotation exactement au centre de la page

### Construire le mandala

Ajoutez des chemins dans ce groupe pour construire votre mandala. Je commence par des objets dont les extrémités sont sur les guides à 0° et 60°, si tout est bien réglé vous devez  voir les copies bien jointives.
Faites en sorte que chaque objet en touche au moins un autre (une petite approximation de moins de 0.5 mm est possible)


![Mandala simple](/assets/images/tutorials/mandala/simplemandala.svg) 
[Télécharger le fichier exemple mandala simple ](/assets/images/tutorials/mandala/simplemandala.svg){: download="simplemandala.svg" }




  
  
