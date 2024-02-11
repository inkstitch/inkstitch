---
title: "Konturfyld"
permalink: /da/docs/stitches/contour-fill/
last_modified_at: 2023-01-14
toc: true
---
## Hvad det er

![Contour fill detail](/assets/images/docs/contour-fill-detail.jpg)

Konturfyld dækker områder med sting, der følger konturen af et objekt.

## Hvordan bruge det

Lav en **closed path with a fill color**.

## Sæt start og ende punkt

Set start and end points for autofill objects with [Visual commands](/docs/commands/).

## Params

Kør `Extensions > Ink/Stitch  > Params`. Indstil Fill Method til `Contour Fill` og tilpasse indstillingerne til dine behov.

Indstillinger||Beskrivelse
---|---|---
Automatically routed fill stitching| ☑ |Skal være aktiveret for at disse indstillinger kan træde i kraft.
Fill method                        |Contour Fill|Contour Fill skal vælges til at sy spirallinjer af konturen
Contour Fill Strategy              |![Inner to Outer](/assets/images/docs/contour-fill-innertoouter-bottlenecks.jpg)<br>![Contour spirals](/assets/images/docs/contour-fill-spirals.jpg)|**Inner to outer** (default) er i stand til at fylde figurer med flaskehalse<br>**Single spiral** udfylder en form med en enkelt spiral fra ydersiden til indersiden<br>**Double spiral** udfylder en form med en dobbelt spiral, starter og slutter ved den udvendige kant af formen.
Join Style                         |Round, Mitered, Beveled |Metode til at håndtere kanterne, når størrelsen af konturen er reduceret for de inderste spiraler
Avoid self-crossing                |![Avoid self crossing effect](/assets/images/docs/contour-fill-self-crossing.jpg)|Om indre til ydre stikning får lov til at krydse sig selv eller ej
Clockwise                          ||Hvilken retning at bevæge sig rundt i konturen
Maximum fill stitch length         ||Længden af hvert sting i en række. "Max" skyldes, at et kortere sting kan bruges i starten eller slutningen af en række.
Spacing between rows               ||Afstand mellem rækker af stikninger
Running Stitch tolerance           |![Tolerance Sample](/assets/images/docs/contourfilltolerance.svg) |Alle sømme skal være inden for denne afstand af stien. En lavere tolerance betyder, at stingene vil være tættere sammen. En højere tolerance betyder, at skarpe hjørner kan være afrundede.
Allow lock stitches                ||Aktiverer hæftesting nogle i ønskede positioner
Force lock stitches                ||Sy hæftesting efter at have syet dette element, selvom afstanden til det næste objekt er mindre end defineret i værdien for collapse length i Ink/Stitch-præferencerne.
Trim After                         ||Klip tråden efter at have syet dette objekt.
Stop After                         ||Stop maskinen efter at have syet dette objekt. Før den stopper, vil den springe til stoppositionen (frame out), hvis den er defineret.

## Underlag

Underlag i Countour Fill følger ikke konturen, men bruger fyldningsvinklen, som kan defineres i [fill underlay params](/docs/stitches/fill-stitch#underlay).

## Eksempelfiler med konturfyld sting inkluderet
{% include tutorials/tutorial_list key="stitch-type" value="Contour Fill" %}
