---
title: "Dépannage"
permalink: /fr/docs/troubleshoot/
last_modified_at: 2025-12-29
toc: true
---
## Dépistage de problèmes avec des objets {#troubleshoot-objects}

Ink/Stitch peut parfois être déroutant. Surtout pour les débutants. Mais si vous utilisez Ink/Stitch pendant un certain temps, vous recevrez également des messages d'erreur, indiquant que quelque chose s'est mal passé et que votre forme ne peut pas être affichée pour une raison quelconque.

Ink/Stitch est livré avec une extension de dépannage, conçue pour vous aider à comprendre les erreurs tout en vous indiquant la position exacte du problème. Elle vous indiquera comment résoudre chaque type d'erreur et donnera des conseils utiles sur les formes présentant des problèmes, même si elles ne causent pas d'erreur dans Ink/Stitch.

### Usage

* (Optionnel) Sélectionnez les objets que vous souhaitez tester. Si vous n'en sélectionnez aucun, l'ensemble du document sera testé.
* Lancer `Extensions > Ink/Stitch > Résolution de problèmes > Dépistage de problèmes avec des objets`
* Choisissez ce que vous voulez détecter : erreurs, avertissements, ou aavertissements sur les types d'objet. 

Vous recevrez soit un message indiquant qu'aucune erreur ne peut être trouvée, soit un nouveau calque contenant les informations de dépannage sera ajouté à votre document SVG. Utilisez le panneau des objets(Ctrl + Shift + O) pour supprimer le calque une fois que vous avez terminé.

![Troubleshoot Example](/assets/images/docs/fr/troubleshoot.jpg)

**Astuce:** Il est possible qu'un objet contienne plus d'une erreur. Les formes de remplissage affichent uniquement la première erreur qui apparaîtra. Exécutez l'extension à nouveau si vous recevez encore des messages d'erreur.
{: .notice--info }

Cette extension vous signale aussi
* la présence de colonnes satin avec deux rails et exactement deux traverses (car cela peut conduite a une mauvaise interprétation de la colonne par Ink/Stitch).
* la présence de colonnes satins sans aucune traverse
* la présence d'éléments de broderie comportant à la fois une couleur de trait et une couleur de fond.


## Informations sur l'élément {#element-info}

Cette extension affiche des informations sur divers paramètres des éléments de broderie sélectionnés.

![Element info](/assets/images/docs/en/element_info.png)

{% include upcoming_release.html %}
Le bouton 'Copier' de l'onglet d'aide permet de copier toutes les informations dans le presse papier.


## Supprimer tous les paramètres de broderie {#remove-embroidery-settings}

Utilisez cette fonction si vous souhaitez supprimer les informations qu'Ink/Stitch a enregistré dans votre document.
Ceci peut être particulièrement utile lorsque vous copier/coller des broderies en provenance d'un autre document.
Cette extension supprimera les paramètres de broderie de votre broderie toute entière ou bien uniquement des objets sélectionnés:
* Sélectionnez des objets (sautez cette étape si vous voulez supprimer toutes les informations de broderie)
* Exécutez `Extensions > Ink/Stitch > Supprimez tous les paramètres de broderie...`
* Sélectionnez une ou plusieurs des options proposées et cliquez sur "Appliquer"
* Avant d'appliquer vous pouvez choisir de supprimer aucune/toutes ou certaines commandes
* Avant d'appliquer vous pouvez choisir de supprimer un paramètre particulier
![Remove embroidery settings - GUI](/assets/images/docs/fr/supprimer_parametres_broderie.png)

## Nettoyer le document {#cleanup-document}

Parfois vous trouverez de très petites formes et des objets laissés par les différentes opération effectuées pendant la conception de votre fichier svg.
Ink/Stitch  offre une fonction de nettoyage de votre document qui empêche ces objets de causer des problèmes.

* Exécutez `Extensions > Ink/Stitch > Résolution de problèmes > Nettoyer le document...`
* Choisissez quels types d'objets doivent être supprimés et définissez un seuil
* Cliquez sur "Appliquer"
* Il est aussi possible de choisir de supprimer les groupes et calques vides
* Cochez l'option "essayer" pour obtenir la liste des noms des éléments qui seraient supprimés avec le paramétrage choisi, sans rien réellement supprimer

## Mettre à jour le svg d'Ink/Stitch 

Un ficher créé avec une version plus ancienne d'Ink/Stitch  se mettra a jour automatiquement.

Toutefois si un fichier est déjà marqué comme mis à jour, il n'y aura plus de vérification de présence d'anciens éléments: Si des objets sont copiés ou importés d'un ancien fichier dans un nouveau fichier, il est possible que certains paramètres ne soient plus reconnus correctement.

Dans ce cas, une mise à jour manuelle peut être effectués sur ces éléments

* Sélectionnez les éléments à mettre à jour:
* Lancez `Extensions > Ink/Stitch > Résolution de problèmes > Mettre à jour le svg d'Ink/Stitch`

Remarque : Cette opération est inutile si n'importe quelle fonction Ink/Stitch a été préalablement exécutée dans le fichier d'origine des éléments. Il suffit par exemple de sélectionner n'importe quoi dans l'ancien fichier, d'ouvrir le dialogue de paramétrage et de cliquer 'Appliquer et Fermer ' sans rien changer pour que l'ancien fichier soit mis à jour. 
{: .notice--info }


