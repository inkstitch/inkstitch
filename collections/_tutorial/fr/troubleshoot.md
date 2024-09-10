---
title: Résolution de problèmes dans Ink/Stitch
permalink: /fr/tutorials/troubleshoot/
last_modified_at: 2024-09-08
language: fr
excerpt: "Maîtriser  les messages d'erreur"
image: /assets/images/posts/de/troubleshoot.png

tutorial-type:
  - text

toc: true
---

N'ayez pas peur de signaler un bug ou un comportement ennuyeux du programme. Les développeurs s'appuient sur vos rapports et apprécient tout commentaire.


{: .notice--info }

## Identifier l'élément à problème

Si une erreur se produit, il est important de localiser l'élément problématique.

L'aperçu du plan de points peut être utilisé à cet effet. Avec un [raccourci clavier](/fr/docs/customize/#shortcut-keys) des petits groupes
ou des éléments individuels peuvent être rendus rapidement jusqu'à ce que l'élément défectueux soit identifié.

## Résolution de problèmes

* Si Ink/Stitch indique qu'il y a une erreur dans le programme, vous avez l'unique opportunité de contribuer à l'amélioration de Ink/Stitch
  et d'entrer en contact avec les sympathiques développeurs. Malheureusement, les outils standard Ink/Stitch ne font généralement pas grand-chose pour aider
  résoudre le problème.
* Toutes les autres erreurs peuvent être facilement traitées à l'aide des outils intégrés.


### Erreur dans le programme (Traçage)

* Enregistrez le fichier
* Si l'élément problématique a déjà été identifié, vous pouvez commencer à chercher des solutions de contournement:
  * Supprimer/modifier les paramètres
  * Changer le point de début/fin
  * Changez la forme (par exemple, évitez les zones étroites dans les points de remplissage)
  * Essayez tout ce qui vous vient à l'esprit
* Copiez la dernière ligne du message d'erreur et recherchez-la sur GitHub : <https://github.com/inkstitch/inkstitch>
* Si l'erreur n'a pas encore été signalée sur GitHub, assurez-vous d'envoyer un rapport d'erreur aux développeurs en joignant le fichier SVG problématique (<https://github.com/inkstitch/inkstitch/issues>).


### Outils de résolution de problèmes d'Ink/Stitch 

####  Dépistage de problèmes avec des objets

`Extensions > Ink/Stitch > Résolution de problèmes > Dépistage de problèmes avec des objets`

![Exemple de message d'erreur](/assets/images/docs/en/troubleshoot.jpg)
Messages d'erreur et suggestion de solutions.
[Dépistage de problèmes avec des objets](/docs/troubleshoot/#troubleshoot-objects) indique les  erreurs  (en rouge) et montre des avertissement sur les chemins potentiellement problématiques (en jaune).

Des suggestions de solutions sont données. Elles conduisent normalement à un fichier fonctionnel.

Les erreurs et avertissements affichés dans l'image ci-dessus sont désormais obsolètes ou révisés. Heureusement,  les frontières qui se croisent ne sont plus un si gros problème.
Au lieu de cela, un avertissement est émis, car les chemins de broderie peuvent  être mieux optimisés si l'élément a été décomposé manuellement.
(Exceptions confirment la règle : voir réduction des changements de couleurs pour les motifs tartan ou les dégradés de couleurs).

C'est de fait une bonne idée d'utiliser cette extension pour les avertissements, même si aucune erreur ne s'est produite!

#### Nettoyer le document

`Extensions > Ink/Stitch > Résolution de problèmes > Nettoyer le document...`

Des éléments trop petits sont des causes fréquentes d'erreur. Ils ne produisent jamais de bon résultat  et peuvent même déclencher des messages d'erreurs.
lIs peuvent être supprimés assez facilement avec cet outil. Les calques et groupes vides peuvent également être supprimés simplement.
Si vous ne savez pas quelles valeurs doivent être saisies ici, vous pouvez également lancer un test et consulter les noms et le nombre d'éléments à supprimer au préalable ou obtenez un aperçu à l'aide du Live Preview (cette fois avec le test désactivé).

[En savoir plus](/fr/docs/troubleshoot/#cleanup-document)

#### Information sur l'élément 

`Extensions > Ink/Stitch >  Résolution de problèmes > Information sur l'élément`


Un outil destiné à qui veut analyser la broderie . Cela vous donne accès à des mesures précises sur les éléments de broderies, tels que le nombre de points, la longueur maximum des points...

C’est encore une liste assez simple. S'il vous manque certaines informations, n'hésitez pas à exprimer vos souhaits sur [GitHub](https://github.com/inkstitch/inkstitch/issues).



[En savoir plus](/fr/docs/troubleshoot/#element-info)

#### Briser des objets de remplissage

`Extensions > Ink/Stitch > Outils Remplissage > Briser des objets de remplissages...`

Qui utilise Ink/Stitch depuis plusieurs années c'est que les frontières qui se croisent étaient une vraie nuisance.
Cet outil est né de ce problème qui heureusement a perdu de son importance.

Malgré l'amélioration de la situation pour les utilisateurs ex-désespérés d'Ink/Stitch, il n'a pas complètement perdu son utilité et peut toujours être utilisé pour nettoyer et séparer des chemins.
Les éléments individuels sont toujours mieux adaptés à l’optimisation des chemins que les chemins combinés et vous connaissez déjà les quelques exceptions.


[En savoir plus](/fr/docs/fill-tools/#break-apart-fill-objects)

#### Vérifier les paramètres

Certains [Paramètres Ink/Stitch](/docs/params/) sont faciles à comprendre. D’autres sont un peu plus sournois, et peuvent avoir un effet déroutant sur le résultat de la broderie.
Un exemple est la longueur minimale du point. Cette valeur peut être définie au niveau du document dans les préférences Ink/Stitch (Extensions > Ink/Stitch > Préférences).
Depuis la version v 3.1.0, il existe également la possibilité de définir la longueur minimale du point au niveau  de chaque objet.

![E-Stitch avec différentes valeurs pour la longueur minimale du point](/assets/images/tutorials/troubleshoot/min_stitch_len_effect.png)

Les deux points  en E présentés dans l'image ont les mêmes paramètres, mais sont dans des fichiers différents avec des valeurs différentes (dans les préférences du fichier)  pour la longueur minimale du point.
À gauche, la valeur de la longueur minimale du point est inférieure à l'espacement zigzag (distance crête à crête).

D'autres paramètres peuvent même conduire à ce qu'un élément ne puisse plus être rendu.
Un bon exemple de ceci est un motif en méandre avec une echelle trop grande pour un objet de remplissage trop petit.

#### Remove embroidery parameters

`Extensions > Ink/Stitch >  Résolution de problèmes > Supprimer les paramètres de broderie`

Si rien n'y fait, c'est peut être une bonne idée de repartir de zéro et de recommencer.

Cet outil peut être utilisé pour supprimer tous (ou certains) paramètres et/ou commandes des éléments sélectionnés. Vous pouvez aussi l'utiliser pour remettre les paramètres de la sortie pdf aux valeurs par défaut.


[En savoir plus](/fr/docs/troubleshoot/#remove-embroidery-settings)

### Inkscape: Editeur XML 

`Inkscape > Edition > Editeur XML `

Si vous souhaitez approfondir un peu le sujet, vous pouvez utiliser l'éditeur XML pour afficher et modifier
le code dans le fichier. Tous les paramètres Ink/Stitch peuvent être modifiés directement à partir de là.




### Tester, tester, tester

Ink/Stitch offre une large gamme de paramètres de réglages.

Tester les résultats de broderie à l’aide de différents paramètres fait partie du processus d’apprentissage lors de la numérisation de motifs de broderie.
Ink/Stitch propose un outil pour cette tâche : [Générer des échantillons de test à partir de la sélection](/fr/docs/edit/#generate-test-swatches-from-selection).

Il se trouve sous `Extensions > Ink/Stitch > Édition > Générer des échantillons de test à partir de la sélection`.

Cela vous permet de créer rapidement une grille avec des éléments dans lesquels un paramètre de broderie est continuellement modifié.



### Broder

Le processus physique de broderie lui-même peut être source d'erreur. 
Lorsque vous brodez, faites attention à 

* avoir une bonne stabilisation grâce à des stabilisateurs adaptés
* pratiquer un cerclage correct 
* changer régulièrement l'aiguille, en utilisant la bonne taille et le bon type d'aiguille pour le fil et le tissu
* vérifier que la tension des fils est correcte (fil de broderie et fil de canette)
* maîtriser la vitesse de broderie : la plus rapide n'est pas toujours la meilleure
* etc.....

