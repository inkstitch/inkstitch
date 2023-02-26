---
title: "Stitch patterns"
permalink: /da/docs/stitches/patterns/
excerpt: ""
last_modified_at: 2023-01-14
toc: true
---
Patterns are created by special stitch positioning.

![Pattern](/assets/images/docs/stitch-type-pattern.png)

[Download sample file](/assets/images/docs/pattern.svg)

## Lav mønsterfyld

I Ink/Stitch kan du generere mønstre ved enten at tilføje sømme eller fjerne sømme fra et eksisterende broderielement.

1. **Opret broderielement(er) embroidery element(s).**  Dette kan enten være en satinsøjle eller fyldområde. Mønstre vil også fungere på streger, men de er muligvis ikke det bedste mål for mønstre.

2. **Opret mønstersti(er).**  Et mønster består af streger eller udfyldningsområder (eller begge på samme tid). Strøg vil blive brugt til at tilføje sting, mens mønstre med fyld fjerner sting fra broderielementet.

3. Vælg begge, broderielementet og mønsteret, og tryk på Ctrl+G for at **gruppere** dem sammen.

4. **Konverter til mønster.** Vælg kun mønsteret og kør `Extensions > Ink/Stitch > Edit > Selection to pattern`. Dette vil tilføje en startmarkør til mønsterelementet for at angive, at det ikke vil blive broderet, men vil blive brugt som et mønster for alle elementer i samme gruppe. Elementer i undergrupper af den samme gruppe vil ikke blive påvirket.

   ![Pattern groups](/assets/images/docs/en/pattern.png)

## Fjern mønstermarkøren

Mønstermarkøren kan fjernes i fyld- og stregpanelet (`Ctrl+Shift+F`). Åbn fanen Stregstil og sæt den første rulleliste i "Markører" til den allerførste (tomme) mulighed.

![Remove pattern](/assets/images/docs/en/stitch-type-remove-pattern.png)

### Eksempel-filer inkluderet mønsterfyld 

{% include tutorials/tutorial_list key="stitch-type" value="Pattern Stitch" %}

