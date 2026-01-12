---
title: QR code
permalink: /fr/tutorials/qr-code/
last_modified_at: 2026-01-11
language: fr
excerpt: "Create a cross Stitch QR Code"
image: "/assets/images/tutorials/qr-code/qr-code.jpg"
tutorial-type:
  - Sample File
stitch-type: 
  - Cross Stitch
  - Fill Stitch
field-of-use:
user-level: Beginner
---

{% include upcoming_release.html %}

Grâce à l'extension Inkscape **Rendu > Code-barres - QR code > QR code** et au point de croix Ink/Stitch, vous pouvez facilement broder un QR code fonctionnel :

![Cross Stitch QR Code](/assets/images/tutorials/qr-code/qr-code.jpg)

## Utilisation de l'extension QR code

![Extension Menu](/assets/images/tutorials/qr-code/QR_extension_fr.jpg)

### Champ de texte

Dans le champ de texte, saisissez le texte à coder. Pour ce tutoriel, j'ai utilisé l'URL suivante :

https://inkstitch.org/tutorials/qr-code/

N'oubliez pas le « https:// » au début.

Si vous souhaitez créer un QR code pour partager vos informations Wi-Fi, le champ de texte doit contenir un texte similaire à celui-ci:

```
WIFI:S:<SSID>;T:<WPA|WEP|>;P:<mot_de_passe>;;
```

Par exemple, si votre SSID Wi-Fi est « My_Wifi », votre mot de passe est « Hello » et votre protocole de sécurité est WAP, saisissez ceci dans le champ Texte :

```
WIFI:S:My_Wifi;T:WPA;P:Hello;;
```
### Niveau de correction d'erreur

Choisissez un niveau élevé ; cela facilitera la broderie.

### Taille
Ici, vous choisissez la largeur des carrés en pixels. Vous aurez besoin de la même taille en mm pour l'extension de point de croix.

**J'ai choisi une largeur de 8 px pour mes carrés**, ce qui correspond à 2,12 mm pour Ink/Stitch.

### Appliquer
Après application, vous obtenez deux objets : un rectangle (supprimez-le) et le code QR sous forme de tracé unique (conservez-le).

![Résultat de l'extension](/assets/images/tutorials/qr-code/generated_QR_code.jpg)

## Préparation du code QR pour le point de croix Ink/Stitch
- Sélectionnez le tracé du QR code et déplacez-le dans le coin supérieur gauche de l'écran en définissant X=0 et Y=0 dans la barre d'outils d'Inkscape. Cela alignera votre tracé QR code avec la grille de point de croix.

- **Étape très importante** : Après avoir réglé l'option **Comportement > Incréments > Éroder/Dilater de :** des préférences d'Inkscape à 0,5 px (**vérifiez votre unité !**)
dilater légèrement le tracé du QR code à l'aide de  **Inkscape > Chemin > Dilater**

## Utilisation du point de croix Ink/Stitch

Sélectionnez le tracé du QR code préparé et appliquez les paramètres. Choisissez un remplissage point de croix **avec une taille de motif de 2,12**.

Comme vous pouvez le voir sur la capture d'écran ci-dessous, vous obtenez un QR code brodable.

![Menu Extension](/assets/images/tutorials/qr-code/First_trial_fr.jpg)

Nous pouvons améliorer l'expérience de broderie en réduisant le nombre de sauts.

Grâce au niveau de correction d'erreur élevé choisi, nous pouvons simplifier le code en supprimant les petites zones tout en conservant un QR code fonctionnel.

- Commencez par utiliser l'outil **Ink/Stitch > Outils Remplissage > Assistant point de croix** (avec un **espacement de grille de 2,12 mm)** pour pixelliser le tracé du QR code : cela le divisera en plusieurs zones connectées.

- Utilisez ensuite **Ink/Stitch > Dépannage > Nettoyer le document** pour supprimer les zones de surface inférieures à 65 pixels carrés (8 x 8 + 1). Cela supprimera toutes les formes carrées.

- Dans mon exemple, 5 carrés sont supprimés.

- Vérifiez que le QR code fonctionne toujours. C'est le cas, essayons de le simplifier davantage.

- Répétez l'opération pour supprimer les zones de surface inférieures à 129 pixels carrés (2 x 64 + 1).

- Dans mon exemple, 4 formes sont supprimées.

- Vérifiez que le QR code fonctionne toujours.

Il ne me reste plus que 9 formes que je peux réordonner pour obtenir une broderie plus fluide, comme ceci :

![Extension Menu](/assets/images/tutorials/qr-code/Second_trial_fr.jpg)
