---
title: "Dépannage"
permalink: /fr/docs/troubleshoot/
excerpt: ""
last_modified_at: 2022-01-16
toc: true
---
## Dépistage de problèmes avec des objets

Ink/Stitch peut parfois être déroutant. Surtout pour les débutants. Mais si vous utilisez Ink/Stitch pendant un certain temps, vous recevrez également des messages d'erreur, indiquant que quelque chose s'est mal passé et que votre forme ne peut pas être affichée pour une raison quelconque.

Ink/Stitch est livré avec une extension de dépannage, conçue pour vous aider à comprendre les erreurs tout en vous indiquant la position exacte du problème. Elle vous indiquera comment résoudre chaque type d'erreur et donnera des conseils utiles sur les formes présentant des problèmes, même si elles ne causent pas d'erreur dans Ink/Stitch.

## Usage

* (Optionel) Sélectionnez les objets que vous souhaitez tester. Si vous n'en sélectionnez aucun, l'ensemble du document sera testé.
* Lancer `Extensions > Ink/Stitch > Résolution de problèmes > Dépistage de problèmes avec des objets`

Vous recevrez soit un message indiquant qu'aucune erreur ne peut être trouvée, soit un nouveau calque contenant les informations de dépannage sera ajouté à votre document SVG. Utilisez le panneau des objets(Ctrl + Shift + O) pour supprimer le calque une fois que vous avez terminé.

![Troubleshoot Example](/assets/images/docs/fr/troubleshoot.jpg)

**Astuce:** Il est possible qu'un objet contienne plus d'une erreur. Les formes de remplissage affichent uniquement la première erreur qui apparaîtra. Exécutez l'extension à nouveau si vous recevez encore des messages d'erreur.
{: .notice--info }

## Supprimer tous les paramètres de broderie

Utilisez cette fonction si vous souhaitez supprimer les informations qu'Ink/Stitch a enregistré dans votre document.
Ceci peut être particulierement utie lorsque vous copier/coller des broderies en provenance d'un autre document.
Cette extension supprimera les paramètres de broderie de votre broderie toute entière ou bien uniquement des objets selectionnés:
* Sélectionnez des objets (sautez cette étape si vous voulez supprimer toutes les informations de broderie)
* Exécutez `Extensions > Ink/Stitch > Supprimez tous les paramètres de broderie...`
* Sélectionnez une ou plusieurs des options proposées et cliquez sur "Appliquer" 

![Remove embroidery settings - GUI](/assets/images/docs/en/remove-embroidery-settings.png)

## Nettoyer le document

Parfois vous trouverez de très petites formes et des objets laissés par les différentes opération effectuées pendant la conception de votre fichier svg.
Ink/Stitch  offre une fonction de nettoyage de votre document qui empêche ces objets de causer des problèmes.

* Exécutez `Extensions > Ink/Stitch > Résolution de problèmes > Nettoyer le document...`
* Choisissez quels types d'objets doivent être supprimés et définissez un seuil
* Cliquez sur "Appliquer"

{% include upcoming_release.html %}
## Update Ink/Stitch svg

To use older svg files that you created with inkstitch version 1.2.2 or older, you may need to run this extension. 
In  particular, if you import some older design as part of your new design, you should select the older elements and run this extension.


