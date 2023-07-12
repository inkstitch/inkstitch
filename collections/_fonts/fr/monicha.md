---
title: "Monicha"
permalink: /fr/fonts/monicha/
last_modified_at: 2022-05-27
toc: false
preview_image:
  - url: /assets/images/fonts/monicha.jpg
    height: 24
---
{%- assign font = site.data.fonts.monicha.font -%}
![monicha](/assets/images/fonts/monicha.jpg)

## Glyphes 
Cette fonte comporte  {{ font.glyphs.size }} glyphes:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }


## Dimensions

Utilisée à 100%, cette fonte fait environ 28 mm. Elle peut être agrandie jusqu'à 150% (env 42 mm) mais ne doit pas être diminuée.

## Description

Monicha est notre première police à lettres multiformes.

Par exemple, voici des variations sur le prénom Sasha :

![Alternatives](/assets/images/fonts/monicha7.jpg)

Elle contient les majuscules, minuscules, lettres à accent, chiffres et ponctuations comme bon nombre des polices proposées jusqu'à présent. Les derniers glyphes de la liste servent à stocker les lettres alternatives.

### Les parentheses

Les deux parentheses "(" et ")" permettent d'accéder à ces deux ornements :

![monica parentheses](/assets/images/fonts/monicaparentheses.png)


Mais Monicha contient aussi 50 lettres minuscules à écharpes de plusieurs types stockées dans les derniers glyphes de la liste.

### Comment utiliser les lettres alternatives

Vous ne pouvez pas accéder directement à ces variations en utilisant une simple touche du clavier. Des caractères unicodes particuliers ont été utilisés pour stocker ces variations. Pour les utiliser il faut donc connaître leur code.

Pour faciliter l'usage de ces lettres, ce mode d'emploi répertorie les codes et il suffira de copier le code et de le coller dans le module lettrage.

####  Petite écharpe

<details><summary>Toutes les minuscules disposent d'une version à petite écharpe</summary>


<img src="/assets/images/fonts/monichasmallswash.jpg" alt="Petite Echarpe" title="Petite Echarpe"><br>

Que l'on obtient en utilisant un de ces codes :<br><br>

⒜	⒝	⒞	⒟	⒠	⒡<br>

⒢	⒣	⒤	⒥	⒦	<br>

⒧	⒨	⒩	⒪	⒫<br>

⒬	⒭	⒮	⒯	⒰<br>

⒱	⒲	⒳	⒴	⒵<br>
	
</details>

####  Écharpe longue soulignante
<details><summary>  a-d-h-i-k-l-m-n-r-t-u </summary>
	
<img src="/assets/images/fonts/monichalongswash.jpg" alt="Echarpe Longue Soulignante" title="Echarpe Longue Soulignante"><br>

Ces  11 lettres disposent de surcroît d'une longue écharpe soulignante.<br><br>

Elles ne doivent pas être suivies, sur deux lettres, par des lettres à jambage descendant (comme g-j-p-q-y-z) 
pour des raisons de superpositions de colonnes de satin.<br><br>

On les obtient en utilisant ces codes :<br>

<pre>Ⓐ			Ⓓ

	Ⓗ	Ⓘ		Ⓚ
	
Ⓛ	Ⓜ	Ⓝ

	Ⓡ		Ⓣ	Ⓤ</pre>

</details>

#### Écharpe soulignante moyenne 

<details><summary>  g-j-y </summary>

<img src="/assets/images/fonts/monichamediumswash.png" alt="Echarpe Moyenne Soulignante" title="Echarpe Moyenne Soulignante"><br>

Ces trois lettres disposent d'une écharpe soulignante moyenne.<br><br>

Elles ne doivent pas être suivies d'une lettre à jambage descendant.<br><br>

On les obtient en utilisant ces codes :<br>

Ⓖ	Ⓙ	Ⓨ

</details>

#### Écharpe basse bouclée 
<details><summary>  g-j-y </summary>

<img src="/assets/images/fonts/monichacurly.png" alt="Echarpe Basse Bouclée" title="Echarpe Basse Bouclée"><br>

Ces trois lettres disposent aussi d'une version à écharpe basse bouclée.<br><br>

Elles ne doivent pas, sur deux lettres, être suivies d'une lettre à jambage descendant.<br><br>

On les obtient en utilisant ces codes :<br>

ⓖ	ⓙ	ⓨ
	
</details>

#### Écharpe supérieure bouclée et rétrograde
<details><summary> b-d-h-k-l-t </summary>

<img src="/assets/images/fonts/monichacurlyup.png" alt="Echarpe Superieure Bouclée" title="Echarpe Superieure Bouclée"><br>

Il existe 6 lettres à écharpe supérieure bouclée et rétrograde b-d-h-k-l-t.<br><br>

Les deux lettres précédentes ne doivent être ni une majuscule ni une lettre montante.<br><br>

On les obtient en utilisant ces codes :<br>


ⓑ	ⓓ	ⓗ	ⓚ	ⓛ	ⓣ
	
</details>

#### Le petit dernier 
<details><summary> o</summary>

Il existe un o à queue droite<br>

<img src="/assets/images/fonts/monichao.png" alt="Echarpe Queue Droite" title="Echarpe Queue Droite"><br>

On l'obtient en utilisant ce code :<br>

ⓞ
</details>


##  Dans la vraie vie

{% include folder-galleries path="fonts/monicha/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/monicha/LICENSE)
