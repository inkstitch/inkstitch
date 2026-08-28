---
title: "Motivi di cucito"
permalink: /docs/stitches/patterns/
last_modified_at: 2026-04-06
toc: true
---
I motivi sono creati tramite posizionamenti speciali dei punti.

![Motivo](/assets/images/docs/stitch-type-pattern.png)

[Scarica il file di esempio](/assets/images/docs/pattern.svg)

## Generare Motivi

In Ink/Stitch, puoi generare motivi aggiungendo o rimuovendo punti da qualsiasi elemento di ricamo esistente.

1. **Crea uno o più elementi di ricamo.** Questo può essere una colonna in raso o un'area riempita. I motivi funzionano anche con i tracciati, ma potrebbero non essere l'opzione migliore.

2. **Crea uno o più percorsi di motivo.** Un motivo è composto da tracciati o aree riempite (o entrambi contemporaneamente). I tracciati verranno utilizzati per aggiungere punti, mentre i motivi con un'area riempita rimuoveranno i punti dall'elemento di ricamo.

3. Seleziona sia l'elemento di ricamo che il motivo e premi `Ctrl+G` per **raggrupparli insieme**.

4. **Converti in motivo.**

  Seleziona solo il motivo ed esegui `Estensioni > Ink/Stitch > Modifica > Selezione in motivo`.
  Questo aggiungerà un marcatore di inizio al elemento del motivo per indicare che non verrà ricamato, ma verrà utilizzato come motivo per tutti gli elementi nello stesso gruppo.
  Gli elementi nei sottogruppi dello stesso gruppo non saranno interessati.

  ![Gruppi di motivi](/assets/images/docs/en/pattern.png)

  {% include upcoming_release.html %}

  Intervallo: È possibile impostare un intervallo per i motivi con un colore del tratto.
  Questo valore determina a quale motivo saltare l'aggiunta di nodi alle intersezioni del percorso.
  Valori multipli sono separati da spazi.

  Offset: I motivi con un colore del tratto iniziano solo dopo questo numero di intersezioni del percorso.

## Rimuovere il Marcatore del Motivo

Rimuovi il marcatore del motivo eseguendo `Estensioni > Ink/Stitch > Modifica > Selezione in Motivo`, seleziona l'opzione `Rimuovi il marcatore del motivo`.

### Rimozione manuale del marcatore del motivo

Il marcatore del motivo può essere rimosso nel pannello di riempimento e tratto (`Ctrl+Shift+F`). Apri la scheda "Stile del tratto" e imposta la prima lista a tendina in "Marcatori" sulla prima opzione (vuota).

![Rimuovi motivo](/assets/images/docs/en/stitch-type-remove-pattern.png)

### File di esempio che includono punti motivo

{% include tutorials/tutorial_list key="stitch-type" value="Pattern Stitch" %}
