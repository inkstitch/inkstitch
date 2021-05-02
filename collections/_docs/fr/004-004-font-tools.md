---
title: "Outils de police"
permalink: /fr/docs/font-tools/
excerpt: ""
last_modified_at: 2021-05-02
toc: true
---
Un ensemble d'outils adaptés aux créateurs de polices ou à ceux qui souhaitent ajouter des polices supplémentaires dans [l'outil de lettrage](/docs/lettering) d'Ink/Stitch.

Lisez le [Tutoriel de création de police pour Ink/Stitch](/fr/tutorials/font-creation) pour des instructions approfondies.

## Répertoire personnalisé de polices 

Cette extension vous permet de définir un répertoire dans votre système de fichiers dans lequel vous souhaitez stocker les polices supplémentaires pour l'outil de lettrage.

Placez chaque police dans un sous-répertoire de votre répertoire personnalisé de polices. Chaque dossier de polices doit contenir au moins une variante de police et un fichier json.
De plus, il est recommandé d'enregistrer également un fichier de licence.

Les variantes de police doivent être nommées avec une flèche, indiquant la direction de broderie pour laquelle elles ont été créées (`→.svg`, `←.svg`, etc.).

Le fichier json doit inclure au minimum le nom des polices.

## Générer  le fichier JSON
Cette extension est destinée à vous aider à créer le fichier json.
Selon la façon dont vous avez généré votre fichier de police, il peut inclure des informations de crénage supplémentaires dans le fichier json.
Lire [**comment générer une police svg avec des informations de crénage**](/tutorials/font-creation).
Si vous avez généré votre fichier svg sans informations de crénage, cette extension peut quand même vous aider à configurer votre fichier json avec des informations de base.

* **Nom**: le nom de votre police (obligatoire).
* **Description**: informations supplémentaires sur votre police (telles que des informations de taille, etc.)
* **Fichier de police** (obligatoire): Si vous avez utilisé FontForge pour générer votre fichier de police svg, Ink/Stitch lira les informations de crénage de votre police pour les inclure dans le fichier json.
 De plus, le fichier de police sera utilisé pour déterminer le chemin de sortie.
* **Agencement automatique des colonnes Satin**:
    * activé: Ink/Stitch générera une organisation raisonnable pour les colonnes de satin de votre police lorsqu'elle est utilisée dans l'outil de lettrage. [Plus d'information sur Agencement automatique des colonnes Satin](/fr/docs/satin-tools/#auto-route-satin-columns)
    * désactivé: Ink / Stitch utilisera les glyphes tels quels. Désactivez cette option, si vous vous avez créé vous-même l'agencement des colonnes satin dans votre police.
* **Reversible**: si votre police peut être brodée vers l'avant et vers l'arrière ou seulement vers l'avant
* **Forcer la casse**:
  * Non: choisissez cette option si votre police contient des lettres majuscules et minuscules (par défaut).
  * Upper: Choisissez cette option si votre police ne contient que des majuscules.
  * Lower: Choisissez cette option si votre police ne contient que des minuscules.
* **Glyphe par défaut**: le glyphe à afficher si le glyphe demandé par l'utilisateur n'est pas disponible dans le fichier de police (glyphe manquant)
* **Min Scale / Max Scale**: Définit dans quelle mesure vos glyphes peuvent être agrandis ou diminués sans perdre en qualité une fois brodés

Les champs suivants sont facultatifs, uniquement nécessaires lorsque votre fichier svg ne contient pas d'informations de crénage.
Si les informations de crénage ne peuvent être trouvées, ces valeurs seront utilisées en remplacement.

* **Force custom values**: Do not use the kerning information from the svg file, but use the given values instead.

* **Leading (px)**: Defines the line height of your font. Leave to `0` to let Ink/Stitch read it from your font file (defaults to 100 if the information cannot be found).
* **Word spacing (px)**: The width of the "space" character

A file `font.json` will be saved into the folder of your svg font file.

## Remove Kerning

**⚠ Warning**: Changes made by this tool cannot be reverted. Make sure to save a **copy** of your file before performing these steps.
{: .notice--warning }

Your font is ready to be used. But when you created your font with FontForge it now contains a lot information which isn't necessary for your font to work and could possibly slow it down a little.
Ink/Stitch comes with a tool to clean up your svg font.

1. Make sure you save a **copy** of your font. The additional information may not be necessary for the font to be used, but it can become handy when you want to add additional glyphs.
2. Run `Extensions > Ink/Stitch > Font Tools > Remove Kerning`
3. Choose your font file(s)
4. Click on apply
