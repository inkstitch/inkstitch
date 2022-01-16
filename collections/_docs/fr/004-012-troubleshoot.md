---
title: "Dépannage"
permalink: /fr/docs/troubleshoot/
excerpt: ""
last_modified_at: 2019-10-25
toc: true
---
## Dépannage objets

Ink/Stitch peut parfois être déroutant. Surtout pour les débutants. Mais également si vous utilisez Ink/Stitch pendant un certain temps, vous recevrez des messages d'erreur, indiquant que quelque chose s'est mal passé et que votre forme ne peut pas être affichée pour une raison quelconque.

Ink/Stitch est livré avec une extension de dépannage, conçue pour vous aider à comprendre l'erreur tout en vous indiquant la position exacte du problème. Elle vous indiquera comment résoudre chaque type d'erreur et donnera des conseils utiles sur les formes présentant des problèmes, même si elles ne causent pas d'erreur dans Ink/Stitch.

## Usage

* (Optionel) Sélectionnez les objets que vous souhaitez tester. Si vous n'en sélectionnez aucun, l'ensemble du document sera testé.
* Lancer `Extensions > Ink/Stitch > Résolution de problèmes`

Vous recevrez soit un message indiquant qu'aucune erreur ne peut être trouvée, soit un nouveau calque contenant les informations de dépannage sera ajouté à votre document SVG. Utilisez le panneau des objets(Ctrl + Shift + O) pour supprimer le calque une fois que vous avez terminé.

![Troubleshoot Example](/assets/images/docs/en/troubleshoot.jpg)

**Astuce:** Il est possible qu'un objet contienne plus d'une erreur. Les formes de remplissage affichent uniquement la première erreur qui apparaîtra. Exécutez l'extension à nouveau si vous recevez encore des messages d'erreur.
{: .notice--info }

## Supprimer les réglages de broderie

Utilisez cette fonction si vous souhaitez supprimer les informations qu'Ink/Stitch a enregistré dans votre document.
Ceci peut être particulierement utie lorsque vous copier/coller des broderies en provenance d'un autre docment.
The extensions will remove embroidery settings from your entire design or from selected objects:
* select objects
  (skip this step if you want to clear all embroidery information)
* Run `Extensions > Ink/Stitch > Remove embroidery settings...`
* Select one or all of the given options and click apply

![Remove embroidery settings - GUI](/assets/images/docs/en/remove-embroidery-settings.png)

## Cleanup Document

Sometimes you will find very small shapes and leftover objects from various operations during your designing process in your SVG file. Ink/Stitch offers a function to clean up your document and prevent those objects from causing trouble.

* Run `Extensions > Ink/Stitch > Troubleshoot > Cleanup Document...`
* Choose which types of objects should be removed and define a threshold
* Click apply

