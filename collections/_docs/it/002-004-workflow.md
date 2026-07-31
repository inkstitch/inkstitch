---
title: "Workflow"
permalink: /docs/workflow/
last_modified_at: 2025-12-29
toc: true
---
![Ink/Stitch workflow](/assets/images/docs/en/workflow-chart.svg)

## ![Create Icon](/assets/images/docs/workflow-icon-create.png) Step 1: Preparare un'Immagine Vettoriale

Inizia con un disegno che desideri trasformare in un file di ricamo. Questo può essere un nuovo disegno creato da zero o un'immagine esistente. Il disegno deve essere in formato vettoriale (SVG) in modo che possa essere modificato in Inkscape e preparato per l'uso con Ink StItch.

### Creare una Nuova Immagine Vettoriale in Inkscape

#### Creare Percorsi

Inkscape offre diversi strumenti per creare immagini vettoriali. Puoi disegnare forme, utilizzare lo strumento Bezier per creare percorsi personalizzati, aggiungere testo o importare grafica e convertirla in oggetti vettoriali modificabili. Questi strumenti ti consentono di creare o perfezionare un disegno prima di prepararlo per il ricamo con Ink/Stitch.

* ![freehand lines icon](/assets/images/docs/inkscape-tools-freehand.png) Linee a mano libera (<key>P</key>)
* ![freehand lines icon](/assets/images/docs/inkscape-tools-bezier.png) Curve Bezier (<key>B</key>)

Esplora anche gli altri strumenti nella barra degli strumenti. Ad esempio, puoi utilizzare strumenti di forma predefiniti come rettangoli, cerchi, stelle e poligoni per creare elementi puliti e coerenti nel tuo disegno. Queste forme possono essere successivamente modificate, combinate e convertite in percorsi per la preparazione al ricamo.

* ![square icon](/assets/images/docs/inkscape-tools-square.png) Rettangolo
* ![circle icon](/assets/images/docs/inkscape-tools-circle.png) Cerchio
* ![polygon icon](/assets/images/docs/inkscape-tools-polygon.png) Stella/Poligono
* ![spiral icon](/assets/images/docs/inkscape-tools-spiral.png) Spirale

#### Modificare i Percorsi

Modifica oggetti e percorsi con:
* ![node tool icon](/assets/images/docs/inkscape-tools-select.png) Strumento di selezione (<key>S</key>) e
* ![node tool icon](/assets/images/docs/inkscape-tools-node.png) Strumento di modifica dei nodi (<key>N</key>)

Usa lo **strumento di selezione** per ridimensionare, ruotare e spostare gli oggetti nel loro insieme. Passa allo **strumento dei nodi** per modificare i singoli nodi e regolare le forme dei percorsi con maggiore precisione.

Puoi anche applicare effetti ai percorsi selezionando **Percorso > Effetti sul percorso**. Gli effetti sui percorsi offrono modi aggiuntivi per modificare e perfezionare le forme vettoriali senza modificare permanentemente il percorso originale.

### Utilizzare un'Immagine o una Grafica Esistente

Quando crei un disegno basato su un'immagine o una grafica esistente, importala in Inkscape su un livello separato. Lavorare in questo modo mantiene l'immagine di origine disponibile come riferimento mentre crei forme vettoriali sopra di essa.

Alcune immagini funzionano bene con la [funzione di tracciatura automatica](https://inkscape.org/en/doc/tutorials/tracing/tutorial-tracing.html) di Inkscape. Puoi accedere a questa funzione da **Percorso > Traccia bitmap** o utilizzando **Maiusc+Alt+B**. I risultati spesso migliorano se si semplifica prima l'immagine in un editor raster come [GIMP](https://www.gimp.org/) prima della tracciatura.

Dopo la tracciatura, perfeziona le forme vettoriali. Usa **Percorso > Semplifica** o **Ctrl+L** per ridurre la complessità non necessaria e rimuovere manualmente i nodi extra quando possibile. Cerca di ottenere un disegno pulito che utilizzi un piccolo numero di curve Bezier pur rappresentando accuratamente l'immagine originale.

La tracciatura automatica spesso crea oggetti minuscoli o frammentati che non funzionano bene per il ricamo. Per risolvere questo problema, pulisci il documento selezionando **Estensioni > Ink/Stitch > Risoluzione problemi > Pulisci documento**. Questo passaggio aiuta a rimuovere gli elementi problematici prima di passare alle impostazioni del punto.

Quando devi tracciare manualmente un'immagine, usa lo strumento di disegno a mano libera per disegnare i percorsi. Questo strumento crea percorsi con molti nodi Bezier, il che può rendere il disegno più difficile da gestire.

Dopo aver disegnato, semplifica le curve per ridurre la complessità. Meno nodi portano a percorsi più puliti e a risultati migliori quando si prepara il disegno per il ricamo.

**Suggerimento:** L'utilizzo di un'immagine SVG esistente può farti risparmiare tempo. Prova a cercare immagini con il tipo di file o il filtro impostato su SVG, quindi adatta la grafica vettoriale per il tuo disegno di ricamo.

{: .notice--info }

### Note sul Testo

Quando lavori con il testo, scegli il font con cura. I punti satin molto stretti (di 1 mm di larghezza o meno) spesso producono risultati scadenti, quindi lo spessore del font gioca un ruolo importante nella leggibilità. I font sans serif sono generalmente più facili da usare e producono una cucitura più uniforme.

Per i testi inferiori a 4 mm di altezza, le lettere minuscole possono essere difficili da cucire in modo pulito. In questi casi, le lettere maiuscole tendono a funzionare meglio. I font corsivi o calligrafici possono produrre risultati attraenti, anche se richiedono più regolazioni e test rispetto agli stili di font più semplici.

Ink/Stitch include font di ricamo pronti all'uso. Puoi inserire questi font nel tuo documento selezionando **Estensioni > Ink/Stitch > Lettering**. Questo strumento crea oggetti di testo già ottimizzati per i flussi di lavoro di ricamo.

## ![Vectorize](/assets/images/docs/workflow-icon-vectorize.png) Step 2: Convertire in Vettori di Ricamo e Parametrizzare

A questo punto, dovresti avere una versione vettoriale del tuo disegno. Il passaggio successivo è convertire questi oggetti vettoriali in formati che Ink/Stitch può interpretare e preparare per il ricamo.

### Utilizzare i Livelli e il Pannello degli Oggetti

A questo punto, l'utilizzo di livelli e gruppi aiuta a mantenere il disegno organizzato e più facile da gestire man mano che diventa più complesso.

Puoi gestire livelli, gruppi e singoli oggetti nel pannello degli oggetti. Apri il pannello con **Ctrl+Shift+O**. Questo pannello ti fornisce una panoramica della struttura del documento e ti consente di controllare come gli elementi sono disposti e modificati.

Puoi preservare l'immagine originale duplicando il suo livello:

- Fai clic con il pulsante destro del mouse sul livello. Se non è stato rinominato, appare come "Livello 1"
- Seleziona **Duplica**
- Fai clic sull'icona dell'occhio per nascondere il livello originale

Questo nasconde l'immagine di origine mantenendola disponibile come riferimento. Ink Stitch ignora i livelli, i gruppi e gli oggetti vettoriali che sono impostati su invisibili.

![Pannello degli oggetti](/assets/images/docs/en/objects-panel.png)

### Utilizzare i Gruppi

Utilizza i gruppi per organizzare gli oggetti correlati nel tuo disegno:

- Seleziona gli oggetti con il mouse
- Aggiungi o rimuovi oggetti tenendo premuto il tasto **Maiusc** mentre fai clic
- Premi **Ctrl+G** per raggruppare gli oggetti selezionati

Per annullare il raggruppamento degli oggetti:

- Seleziona uno o più gruppi
- Premi **Ctrl+Shift+G**

### Note sui Tipi di Punto

Ink/Stitch supporta diversi tipi di punto. Le tre categorie principali sono disponibili:

1. **Punti di riempimento**
   Questi punti riempiono una forma chiusa. Vengono utilizzati per aree più ampie e creano una superficie testurizzata e forniscono copertura mantenendo la flessibilità nel tessuto.

2. **Punti di contorno**
   Questi punti seguono la direzione di un percorso. Vengono utilizzati per contorni, linee sottili ed elementi decorativi in cui una linea cucita stretta funziona meglio di una forma riempita.

3. **Punti satin**
   Questi punti coprono forme strette con punti paralleli lisci. Corrono avanti e indietro su una forma, creando un aspetto lucido e rialzato che funziona bene per bordi, scritte e dettagli fini.

Configuri il comportamento del punto tramite **Oggetto > Riempimento e contorno** o premendo **Ctrl+Shift+F**. Esamina la tabella sottostante e segui i collegamenti per scoprire come configurare correttamente ogni tipo di punto.

Oggetto Percorso | Tipo di Punto
---|---
(Tratteggiato) contorno |[punto a spillo](/docs/stitches/running-stitch/), [punto manuale](/docs/stitches/manual-stitch/), [punto a zig-zag](/docs/stitches/zigzag-stitch/), [punto a fagiolo](/docs/stitches/bean-stitch/)
Due contorni combinati (con opzionali listelli) o un singolo contorno con una larghezza superiore a 0,3 mm| [colonna satin](/docs/stitches/satin-column), [punto E](/docs/stitches/e-stitch)
Percorso chiuso con un colore di riempimento | [punto di riempimento](/docs/stitches/fill-stitch/), [riempimento guidato](/docs/stitches/guided-fill/), [riempimento del contorno](/docs/stitches/contour-fill/), [riempimento a nido d'ape](/docs/stitches/meander-fill/), [riempimento circolare](/docs/stitches/circular-fill/), [punto croce](/docs/stitches/cross-stitch/)
{: .equal-tables }

### Impostare i Parametri del Punto

Il dialogo **Estensioni > Ink/Stitch > Parametri** controlla come Ink/Stitch genera i punti per gli oggetti selezionati. I parametri variano in base al tipo di punto e includono valori come lunghezza del punto, densità, sottofondo, direzione o compensazione di tiraggio.

Ogni parametro include una breve descrizione. Spiegazioni più dettagliate sono disponibili nella sezione [Parametri](/docs/params/) di questa documentazione. Utilizza questi riferimenti per comprendere come le modifiche influiscono sulla qualità e sull'aspetto del punto.

Quando aggiorni i valori dei parametri, Ink/Stitch mostra un'anteprima simulata. Questa anteprima ti aiuta a valutare il risultato prima di apportare modifiche al disegno. A seconda delle dimensioni e della complessità del file, l'anteprima potrebbe richiedere del tempo per essere visualizzata. Regola i valori secondo necessità fino a quando l'anteprima non riflette il risultato desiderato, quindi seleziona **Applica e chiudi**. Questa azione memorizza i valori dei parametri direttamente nel file SVG.

Una volta aggiornati i valori dei parametri, salva il file SVG. Se Inkscape inizia a rallentare o a non rispondere, chiudilo e riaprilo prima di continuare. Il riavvio può migliorare le prestazioni durante progetti più lunghi o complessi.

## ![Create Icon](/assets/images/docs/workflow-icon-order.png) Step 3: Pianificare l'Ordine dei Punti e Aggiungere Comandi

### Ordine dei Punti

Quando progetti per macchine da ricamo che non tagliano il filo durante la cucitura o non cambiano automaticamente i colori, pianifica attentamente il percorso di cucitura. Un percorso ben pianificato riduce i punti di salto visibili e limita i cambi di colore. Quando possibile, evita di cucire sopra i punti di salto, poiché tagliarli a mano in seguito può richiedere molto tempo ed essere frustrante.

L'ordine dei punti influisce anche sul comportamento del tessuto. Ogni punto tira e sposta leggermente il materiale, il che può causare distorsioni mentre il disegno viene creato. Questo può far arricciare o tirare il tessuto. Regola la direzione e la sequenza dei punti per tenerne conto e applica la compensazione necessaria. Per una spiegazione più dettagliata, consulta [Compensazione di spinta e trazione](/tutorials/push-pull-compensation/).

Dopo aver impostato i parametri per il disegno, ordina gli oggetti nella sequenza di cucitura corretta. Questo passaggio controlla come il disegno viene cucito sulla macchina.

Usa lo strumento Oggetti di Inkscape selezionando **Oggetti > Oggetti**. Questo pannello ti consente di riordinare gli oggetti in modo che la cucitura segua una sequenza logica. Regola l'ordine per limitare i cambi di colore e ridurre o nascondere i punti di salto.

Puoi anche utilizzare la funzione di ordinamento di Ink Stitch per riordinare gli oggetti in base all'ordine di selezione. Consulta [Riordina gli oggetti nell'ordine di selezione](/docs/edit/#re-stack-objects-in-order-of-selection) per i dettagli.

Ink/Stitch elabora gli oggetti nell'ordine in cui appaiono nel pannello degli oggetti, partendo dal fondo dell'ordine di impilamento e spostandosi verso l'alto. Questo ordine controlla direttamente il modo in cui il disegno viene cucito sulla macchina da ricamo. L'ultimo livello nell'elenco verrà cucito per primo e lo strato superiore verrà cucito per ultimo.

Quando la distanza tra due oggetti è ampia, Ink/Stitch inserisce automaticamente un punto di salto per spostare l'ago tra di essi. Il colore del filo è determinato dal colore dell'oggetto, quindi un cambio di colore da un oggetto all'altro si traduce in un comando di cambio colore nel file di ricamo esportato.

**Suggerimento:** Inkscape ti consente di modificare l'ordine di impilamento con i tasti **PageUp** e **PageDown**. I comandi più recenti, **Impila in alto** e **Impila in basso**, forniscono un controllo più preciso su come gli oggetti si muovono all'interno dell'impilamento.

Per una maggiore precisione, valuta la possibilità di associare **PageUp** e **PageDown** a questi comandi. Questa configurazione semplifica il controllo dell'ordine di cucitura durante la preparazione di un disegno per il ricamo. Consulta [Tasti di scelta rapida](/docs/customize/#shortcut-keys) per i dettagli.
{: .notice--info }

**Informazioni:** Puoi anche regolare l'ordine degli oggetti modificando direttamente la struttura SVG tramite l'editor XML di Inkscape. Apri con **Ctrl+Maiusc+X**. I pulsanti **Solleva** e **Abbassa** modificano l'ordine dei tag XML nel file SVG, il che influisce direttamente sull'ordine di cucitura.

Tieni presente che l'editor XML visualizza gli oggetti nell'ordine inverso rispetto al pannello degli oggetti. Gli elementi visualizzati nella parte superiore dell'elenco XML appaiono più in basso nell'ordine di impilamento all'interno del documento.
{: .notice--info }

### Comandi

I [comandi](/docs/commands/) possono anche aiutare a ottimizzare il percorso di cucitura. Questi strumenti ti consentono di definire punti di inizio e fine, spostare il telaio in posizioni specifiche e aggiungere istruzioni di taglio. L'utilizzo dei comandi ti offre un maggiore controllo su come il disegno viene cucito sulla macchina. Ti consentono di definire punti di inizio e fine, controllare tagli, salti, stop e cambi di colore e spostare il telaio in posizioni specifiche. L'utilizzo dei comandi aiuta a ridurre i punti di spostamento visibili, a limitare il taglio manuale e a migliorare il flusso di cucitura sulla macchina da ricamo.

## ![Create Icon](/assets/images/docs/workflow-icon-visualize.png) Step 4: Visualizzare il Tuo Disegno

Ink/Stitch offre tre modi per visualizzare il tuo disegno prima dell'esportazione:

- [Simulatore](/docs/visualize/#simulator)
  Mostra come il disegno viene cucito passo dopo passo.

- [Anteprima di stampa](/docs/print-pdf/)
  Crea una panoramica stampabile del disegno, utile per pianificare colori, dimensioni e posizionamento.

- [Anteprima del piano di cucitura](/docs/visualize/#stitch-plan-preview)
  Visualizza l'ordine dei punti e i percorsi direttamente nel documento. Puoi annullare questa visualizzazione con **Ctrl+Z**.

## ![Create Icon](/assets/images/docs/workflow-icon-export.png) Step 5: Salvare il File di Ricamo

Dopo aver posizionato gli oggetti nell'ordine di cucitura corretto, esporta il disegno in un formato compatibile con la macchina. Seleziona **File > Salva una copia** e scegli un formato supportato dalla tua macchina da ricamo. Molte macchine supportano DST, mentre alcuni modelli Brother funzionano meglio con PES. Consulta [Importazione ed esportazione](/docs/import-export/) per i dettagli sul formato.

Salva anche il disegno nel formato SVG. Mantenere il file SVG ti consente di riaprire il progetto in Inkscape e modificare le impostazioni, l'ordine dei punti o i dettagli del disegno in seguito.

## ![Create Icon](/assets/images/docs/workflow-icon-testsew.png) Step 6: Eseguire un Test di Cucitura

Il test aiuta a rivelare le opportunità di miglioramento. Prepara un tessuto di prova che corrisponda il più possibile al materiale finale. Utilizza lo stesso stabilizzatore e lo stesso tipo di tessuto. Per le magliette, scegli un tessuto maglia simile, poiché i tessuti a maglia richiedono una stabilizzazione significativa.

Cuci il disegno osservando la macchina. Cerca spazi vuoti che suggeriscano una distorsione del tessuto. Controlla anche le aree in cui i punti sono troppo densi e la macchina ha difficoltà a cucire. Questi segni indicano spesso una densità di punti impostata troppo alta e segnalano che è necessario apportare modifiche prima della produzione finale.

## ![Create Icon](/assets/images/docs/workflow-icon-optimize.png) Step 7+: Ottimizzare

Dopo il test di cucitura, torna al disegno e regola le impostazioni come necessario. Spesso sono necessarie diverse iterazioni per ottenere il risultato desiderato e piccole modifiche possono migliorare significativamente la qualità e l'aspetto del punto.
