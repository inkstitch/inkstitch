---
title: "Export pdf"
permalink: /fr/docs/print-pdf/
excerpt: ""
last_modified_at: 2022-01-22
toc: true
---
## Accéder à l'aperçu avant impression

Exécuter `Extensions > Ink/Stitch  > Visualiser et exporter > Export pdf` pour exporter le dessin pour impression. Vous avez la possibilité de régler certains paramètres, de choisir parmi différents modèles et de les envoyer à votre imprimante (PDF) une fois que vous avez terminé.

## Personnalisation

### Champs modifiables et logo personnalisé

Vous remarquerez de nombreux champs modifiables dans l'aperçu avant impression. Cliquez avec votre souris sur les champs et entrez votre texte. Les personnalisations des champs d'en-tête seront automatiquement renseignées sur chaque page.
N'oubliez pas de choisir votre propre logo en cliquant sur le logo Ink/Stitch. Cela ouvrira un sélecteur de fichiers, choisissez votre logo et cliquez sur `Ouvrir`.

**Astuce:** Si vous modifiez l'ordre des objets après avoir rempli les notes de l'opérateur, utilisez couper (`Ctrl+X`) et coller (`Ctrl+V`) pour les déplacer aux bons endroits.
{: .notice--warning }

### Aperçu de broderie

L'aperçu de conception comporte également différentes options. Vous pouvez ajuster la taille en cliquant sur `Ajuster`, `100%` ou `Ctrl + Scroll` pour modifier l'échelle. Cliquez sur votre dessin et déplacez-le à l'intérieur du canevas vers un endroit différent. Il est également possible d'appliquer les transformations à toutes les pages en cliquant sur `Appliquer à tous`.

Par défaut, l'aperçu avant impression utilise le mode de tracé de lignes. Choisissez `Réaliste` si vous souhaitez un aperçu réaliste du rendu. Cela prendra un peu de temps pour calculer cette vue, mais cela vaut la peine d'attendre. Ce paramètre doit être activé sur chaque page où vous souhaitez l’utiliser.

![Dessin réaliste](/assets/images/docs/en/print-realistic-rendering.jpg){: width="450x" }

### Paramètres

Cliquer sur `Paramètres` pour accéder aux options suivantes.

#### Mise en page

Réglage|Description
---|---
Taille d'impression|Vous avez le choix entre `Letter` et `A4`.
Disposition d'impression|Il y a deux types de disposition différents:<br />⚬ **Mise en page pour l'opérateur de la machine à broder** avec  blocs de couleur, nom des fils, nombre de points, et notes personnelles<br />⚬ **Mise en page orientée client** conçu pour que vous puissiez l'envoyer à votre client<br />⚬ **Vue du motif sur une page entière** Une page entière montrant le design uniquement, affiche éventuellement le pied de page<br />⚬ **Custom page** offre un espace pour le texte libre (par exemple, instructions pour les projets tout-dans-le cadre)
Enregistrer par défaut|*Les paramètres de mise en page* peuvent être enregistrés comme paramètres par défaut. La prochaine fois que vous ouvrirez un aperçu avant impression, il utilisera vos paramètres par défaut. Linux, par exemple enregistrera les paramètres d'impression par défaut à `~/.config/inkstitch/print_settings.json`.

#### Durée estimée

Vous pouvez renseigner la vitesse de la machine (points/minute), la durée d'un changement de fil, la durée d'une coupe de fil. Vous pouvez aussi choisir sur quelles vues la durée estimée doit être affichée.

#### Fil Estimé

Vous pouvez affiner cette estimation en modifiant les valeurs longueur de fil supérieur sur longueur du trajet effecté, et longueur du fil de bobine sur longueur du trajet effectué.

#### Conception

Paramètre|Description
---|---
Palette de fil|Change la palette de fabricant. Ink/Stitch choisira les noms de couleurs correspondants à votre choix. Il supprimera toutes les modifications que vous avez peut-être déjà effectuées.

## Imprimer / Enregistrer PDF

Cliquez sur `Imprimer` pour ouvrir la page dans votre visionneuse PDF à partir de laquelle vous pouvez imprimer vos documents. Assurez-vous que le format d'impression correspond à vos paramètres.  Vous pouvez également cliquer sur `Enregistrer PDF`. Cela enregistrera en PDF.

## Retour dans Inkscape

Fermez la fenêtre d’aperçu avant impression pour revenir à Inkscape.
