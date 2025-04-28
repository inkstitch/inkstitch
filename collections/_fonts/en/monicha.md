---
title: "Monicha"
permalink: /fonts/monicha/
last_modified_at: 2025-05-28
toc: false
preview_image:
  - url: /assets/images/fonts/monicha.jpg
    height: 24
data_title:
  - monicha
---
{%- assign font = site.data.fonts.monicha.font -%}
![monicha](/assets/images/fonts/monicha.jpg)

## Glyphs 

This font contains  {{ font.glyphs.size }} glyphs:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

At 100%, this font is approximatively   {{ font.size }} tall. 

It can be scaled up to  150% ({{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm)) but can not be scaled down.


## Description

Monicha is our first font with alternative characters.

For instance, these are different ways to write the firstname Sasha.

![monicha7](/assets/images/fonts/monicha7.jpg)


### The parentheses

The two usual parentheses ( and ) are binded to 
![monica parentheses](/assets/images/fonts/monicha/monicaparentheses.png)

Monicha contains also one more alternate versions of the letters a-z and A-Z.

**However, some restrictions on the use of these alternate letters should be observed to avoid overlapping satin columns.**

### How to access the alternative letters

There are four alternative letter families: alt1, alt2, alt3, and alt4.

For example, you'll get two alternative versions of the name Sasha by typing in the lettering
(Sash.alt2a.alt3) (i.e., S a s h.alt2 a.alt3 - but don't type the spaces) or Sa.alt3sh.alt3a.alt1

#### alt1: Small swashes

All lowercase letters have a small swash version that works particularly well on the last letter of a word.

<img src="/assets/images/fonts/monicha/alt1.png" alt="Little Scarf" title="Little Scarf"><br>

In the lettering, for example, type a.alt1 instead of a if you want to use this alternative version of a.

#### alt2: Curly swashes : b-d-h-k-l-t i-j-o-r-y

The rising letters (b-d-h-k-l-t) have an alternate version with a backward curly upper swash. The two preceding letters can not be a capital letter or another rising letter.

The alternate versions of i, j, r, and y have a backward curly low swash. They must not, on two letters, be followed by a descending letter (d-g-p-q-y-z).

<img src="/assets/images/fonts/monicha/alt2.png" alt="Long Scarf Underlining" title="Long Scarf Underlining"><br>

Exceptions to the restrictions: The image above also shows ligatures that have been added to the font: **l&l.alt2 r&i.alt2 t&h.alt2 t&t.alt2**

#### alt3: Long  or Medium Underscore a-c-d-e-h-i-k-l-m-n-o-r-t-u g-j-y

Letters with an underscore must not be followed by a descending letter or another letter with an underscore. For long underscores, the prohibition extends to the following two letters.

<img src="/assets/images/fonts/monicha/alt3.png" alt="Medium Scarf Underlining" title="Medium Scarf Underlining"><br>

Exceptions to the restrictions: The image above also shows ligatures that have been added to the font: **a&f.alt3 a&g.alt3 a&j.alt3**

### alt4: Heart at the beginning for capital letters, heart at the end for lowercase letters.

These alternative capital letters should only be used at the beginning of a word, and lowercase letters only at the end.

<img src="/assets/images/fonts/monicha/alt4.png" alt="Hearts" title="Hearts"><br>

<!--
Monicha is our first font with alternative characters.

For instance, these are different ways to write the firstname Sasha.

![monicha7](/assets/images/fonts/monicha7.jpg)

In addition to the "usual" european  character set, Monicha contains 50 alternative swash lower case letters hidden in the last glyphs of the list

### The parentheses

The two usual parentheses ( and ) are binded to 

![monica parentheses](/assets/images/fonts/monicha/monicaparentheses.png.png)

### How to access the alternative letters

You can't use directly the keyboard to access these alternative letters.

Instead some unusual unicode characters have been used to store them. You will have to copy/paste their code from this file to the lettering dialog window.

#### Small swashes

<details> <summary>All lower case letters </summary>

<img src="/assets/images/fonts/monichasmallswash.jpg" alt="Petite Echarpe" title="Petite Echarpe"><br>

To use these alternative letters, you will need to cut  their code from here and paste it in the lettering dialog.<br><br>

⒜	⒝	⒞	⒟	⒠	⒡<br>

⒢	⒣	⒤	⒥	⒦	<br>

⒧	⒨	⒩	⒪	⒫<br>

⒬	⒭	⒮	⒯	⒰<br>

⒱	⒲	⒳	⒴	⒵
	
</details>

####  Long underscoring swashes

<details> <summary> a-d-h-i-k-l-m-n-r-t-u </summary>

<img src="/assets/images/fonts/monichalongswash.jpg" alt="Echarpe Longue Soulignante" title="Echarpe Longue Soulignante"><br>

There are also 11 lower case letters with long underscoring swashes a-d-h-i-k-l-m-n-r-t-u.<br><br>

They must not be followed, over two letters, by downslope letters (such as g-j-p-q-y-z)
to avoid satin columns overlays. To access use one of these codes:<br>

<pre>Ⓐ			Ⓓ

	Ⓗ	Ⓘ		Ⓚ
	
Ⓛ	Ⓜ	Ⓝ

	Ⓡ		Ⓣ	Ⓤ</pre>

</details>

####  Medium length swashes 

<details> <summary> g-j-y </summary>

<img src="/assets/images/fonts/monichamediumswash.png" alt="Echarpe Moyenne Soulignante" title="Echarpe Moyenne Soulignante"><br>

There are 3 underscore medium length swash letters: g-j-y.<br><br>

They must not be followed by a downslope letter.<br><br>

To access use one of these codes:<br>

Ⓖ	Ⓙ	Ⓨ
	
</details>

####  Curly low swashes

<details> <summary> g-j-y </summary>

<img src="/assets/images/fonts/monichacurly.png" alt="Echarpe Basse Bouclée" title="Echarpe Basse Bouclée"><br>

These three letters feature a curly low swash version.<br><br>

They must not be followed by a downstroke letter over two letters.<br><br>

To access use one of these codes:<br>

ⓖ ⓙ ⓨ
	
</details>

####  Retrograde curly upper swashes

<details> <summary> b-d-h-k-l-t </summary>

<img src="/assets/images/fonts/monichacurlyup.png" alt="Echarpe Superieure Bouclée" title="Echarpe Superieure Bouclée"><br>

There are 6 retrograde curly upper swash letters b-d-h-k-l-t.<br><br>

The two previous letters should not  be rising letters, nor capital letter to avoid satin columns overlays.<br>

To access use one of these codes:<br><br>

ⓑ	ⓓ	ⓗ	ⓚ	ⓛ	ⓣ
	
</details>

#### And the last one

<details> <summary> o</summary>

<img src="/assets/images/fonts/monichao.png" alt="Echarpe Queue Droite" title="Echarpe Queue Droite"><br>

Finally there is also  a straight tail o:<br><br>

To access use this code:<br>

ⓞ

</details>
	-->
## In real life

{% include folder-galleries path="fonts/monicha/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/monicha/LICENSE)
