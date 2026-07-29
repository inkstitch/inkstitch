---
title: "Cutwork"
permalink: /docs/cutwork/
last_modified_at: 2022-12-30
toc: true
---
Il "cutwork" nella ricamo a macchina descrive una tecnica in cui vengono utilizzate speciali aghi per praticare dei fori nel tessuto. Questi aghi sono generalmente forniti in un set di quattro. Ogni ago è in grado di tagliare in un intervallo di angoli specifico. Pertanto, è necessario suddividere un elemento in sezioni angolari corrispondenti agli angoli dei vostri aghi.

## Utilizzo

Ink/Stitch include uno strumento che vi aiuterà a suddividere i vostri elementi in base agli angoli degli aghi.

* Selezionate uno o più oggetti di tracciato.
* Aperte `Estensioni > Ink/Stitch > Segmentazione cutwork`.
  ![Finestra di segmentazione cutwork](/assets/images/docs/en/cutwork-segmentation.png)
* Impostate gli angoli e i colori in base alle vostre esigenze per il kit di aghi specifico.
* Applicate.

![Un cerchio suddiviso in pezzi tramite la segmentazione cutwork](/assets/images/docs/cutwork-segmentation.png)

A volte sarà necessario lasciare degli spazi nel bordo del foro, in modo che il tessuto ritagliato rimanga collegato alla parte principale. Questo impedirà alla macchina di tirare piccoli pezzi di tessuto ritagliato.

**Attenzione:** Non ruotate il vostro disegno dopo aver applicato questa funzione.
{: .notice--warning }

## Configurazione tipica degli aghi

Ago|Angolo|Inizio|Fine
--|--|--|--
<span class="cwd">&#124;</span>   | 90°  | 67  | 113
<span class="cwd">/</span>        | 45°  | 112 | 157
<span class="cwd">&#8213;</span>  | 0°   | 158 | 23
<span class="cwd">&#x5c;</span>   | 135° | 22  | 68


Marca | #1  | #2 | #3 | #4
--|--|--|--
Bernina                  | <span class="cwd">&#124;</span>                                | <span class="cwd">/</span>                                        | <span class="cwd">&#8213;</span>                                   | <span class="cwd">&#x5c;</span>
Pfaff, Husqvarna Viking, Inspira | Rosso <span class="cwd" style="background:red;">/</span> | Giallo <span class="cwd" style="background: yellow">&#8213;</span>| Verde <span class="cwd" style="background: green;">&#x5c;</span>   | Blu <span class="cwd" style="background: blue">&#124;</span>
Brother, Babylock        | Blu <span class="cwd" style="background: blue;">/</span>      | Viola <span class="cwd" style="background: purple;">&#8213;</span>| Verde <span class="cwd" style="background: green;">&#x5c;</span>  | Arancione <span class="cwd" style="background: #ff6000;">&#124;</span>
Janome                   | Rosso <span class="cwd" style="background: #ff3f7e;">&#8213;</span>  | Blu <span class="cwd" style="background: #00abff;">/</span>          | Nero <span class="cwd" style="background: #413f57; color: white;">&#124;</span>| Verde <span class="cwd" style="background: green;">&#x5c;</span>

## Cutwork con Bernina/Bernette

Salva il file .inf insieme al file .exp (date lo stesso nome) e la macchina riconoscerà le linee di cutwork e visualizzerà i numeri degli aghi corretti (come definiti nello strumento di segmentazione cutwork).

Utilizzate le seguenti impostazioni (questi sono i colori tipici, ma non sono importanti per il riconoscimento del cutwork):

Ago|Colore                                      |Inizio|Fine
------|-------------------------------------------|-----|---
1     |<span style="color: #ffff00">#ffff00</span>|67   |113
2     |<span style="color: #00ff00">#00ff00</span>|112  |157
3     |<span style="color: #ff0000">#ff0000</span>|158  |23
4     |<span style="color: #ff00ff">#ff00ff</span>|22   |68
