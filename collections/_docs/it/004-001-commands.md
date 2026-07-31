---
title: "Comandi Visivi"
permalink: /docs/commands/
last_modified_at: 2026-01-22
toc: true
---
I comandi visivi possono essere utilizzati per specificare informazioni aggiuntive su come ricamare il design. Possono essere utilizzati, ad esempio, per indicare alla macchina di tagliare il filo dopo aver completato un elemento specifico del ricamo o per indicare quando mettere in pausa e dove fermarsi, in modo da poter aggiungere uno strato di tessuto al design dell'appliqué in modo più comodo.

Non tutte le macchine da ricamo saranno in grado di leggere ed elaborare le informazioni fornite da alcuni di questi comandi. Se questa funzione non funziona per te, consulta il manuale della tua macchina per verificare le sue capacità.
{: .notice--warning }

In `Estensioni > Ink/Stitch > Comandi`, troverai quattro opzioni:

* [Aggiungi comandi](#add-commands-)
* [Aggiungi comandi per i livelli](#add-layer-commands-)
* [Associa i comandi agli oggetti selezionati](#attach-commands-to-selected-objects-)
* [Visualizza](#view)

**È necessario duplicare oggetti con comandi?** Un modo comune per copiare oggetti in Inkscape è la duplicazione. Prima di duplicare oggetti con comandi, assicurati che "Ricollega le copie duplicate" sia abilitata in `Modifica > Preferenze > Comportamento > Copie`.
{: .notice--info }

**Posizionamento dei comandi** In molti casi, i comandi sono puntatori a posizioni specifiche. Per posizionare un comando, seleziona semplicemente il simbolo e spostalo con il mouse o i tasti freccia. Quando ti sposti con i tasti freccia, puoi premere il tasto Shift per spostarti rapidamente; il tasto Alt viene utilizzato per una regolazione fine.
{: .notice--info }

## Aggiungi Comandi ...

Questi comandi influiscono sull'intero design di ricamo.

### ![origine](/assets/images/docs/visual-commands-origin.jpg) Origine

Specifica il punto di origine (0,0) per i file di ricamo. Impostare le origini è particolarmente utile per le persone che hanno accesso completo all'intero campo di cucitura a cui la loro macchina è in grado di raggiungere, indipendentemente dall'archetto utilizzato.

### ![posizione di arresto](/assets/images/docs/visual-commands-stop-position.jpg) Posizione di arresto

La macchina da ricamo si sposta in questo punto prima di ogni comando di arresto. Ciò consente di spingere il telaio di ricamo verso l'utente per rendere più semplici i passaggi dell'appliqué.

## Aggiungi Comandi per i Livelli ...

Questi comandi verranno aggiunti al livello attualmente selezionato.

### ![simbolo di ignorare il livello](/assets/images/docs/visual-commands-ignore-layer.jpg) Ignora livello

Tutti gli oggetti in questo livello non verranno esportati nei file di ricamo. Un uso comune di questo comando è nei file didattici in cui non si desidera che Ink/Stitch visualizzi il testo esplicativo.

## Associa i Comandi agli Oggetti Selezionati ...

Questi comandi verranno associati agli oggetti attualmente selezionati.

* Seleziona uno o più oggetti.
* Esegui `Estensioni > Ink/Stitch > Comandi > Associa i comandi ...`
* Abilita i comandi desiderati e applica.
* I comandi Avvia/Arresta/Taglia: il centro del simbolo indica il punto in cui verrà eseguito l'effetto.

### ![simbolo di posizione di partenza](/assets/images/docs/visual-commands-start.jpg) ![simbolo di posizione di fine](/assets/images/docs/visual-commands-end.jpg) Posizione di partenza/fine

Definisce (1) il punto di partenza o (2) il punto di fine di un'area di punto in riempimento o di una colonna in satin.

### ![simbolo di posizione di partenza per operazioni automatiche](/assets/images/docs/visual-commands-auto-route-running-stitch-start.jpg) ![simbolo di posizione di fine per operazioni automatiche](/assets/images/docs/visual-commands-auto-route-running-stitch-end.jpg) Posizione di partenza/fine per operazioni automatiche

Definisce (1) il punto di partenza o (2) il punto di fine per un'operazione automatica.

Utilizza un solo punto di partenza e un solo punto di fine per ogni operazione automatica.
{: .notice--warning }

Le operazioni automatiche possono essere eseguite su colonne in satin ([Strumenti: Satin > Percorso satin automatico](/docs/satin-tools/#auto-route-satin-columns)) o su contorni.

I contorni hanno due tipi diversi per il percorso automatico:

* [Strumenti: Contorno > Percorso punto in maglia automatico](/docs/stroke-tools/#autoroute-running-stitch) (uno o due passaggi per sezione).
* [Strumenti: Contorno > Punto a stella](/docs/stroke-tools/#redwork) (esattamente due passaggi per sezione).

Viene utilizzato solo il punto di partenza per il punto a stella, poiché il punto a stella termina sempre nel punto di partenza.

### ![simbolo di bersaglio](/assets/images/docs/visual-commands-ripple-target.png) Posizione del bersaglio

Definisce il punto di destinazione di un'area di punto a onda o di un riempimento circolare.

### ![simbolo di punto di taglio del satin](/assets/images/docs/visual-commands-satin-cut-point.jpg) Punto di taglio del satin

Divide una colonna in satin nel punto specificato da questo comando. Dopo averlo associato, esegui "[Taglia la colonna in satin](/docs/satin-tools/#cut-satin-column)".

### ![simbolo di arresto](/assets/images/docs/visual-commands-stop.jpg) Arresto

Le macchine da ricamo commerciali con più aghi di solito passano da un colore all'altro senza interruzioni. A volte *si desidera* una pausa (ad esempio, per tagliare il tessuto dell'appliqué), quindi "ARRESTO dopo" aggiunge un cambio di colore aggiuntivo che può essere assegnato a un'istruzione di arresto speciale tramite l'interfaccia utente della macchina (ad esempio, C00 sulle macchine Barudan). Un uso comune è applicare la schiuma imbottita dopo aver eseguito il ricamo normale, applicare il tessuto dell'appliqué e persino rallentare la macchina in un determinato punto per determinati tipi di ricamo senza dover controllare costantemente la macchina.

### ![simbolo di taglio](/assets/images/docs/visual-commands-trim.jpg) Taglia

"Taglia dopo" indica alla macchina da ricamo di tagliare il filo dopo che l'oggetto assegnato è stato ricamato. Non tutte le macchine domestiche supportano la funzione di taglio all'interno di un blocco di colori. Viene utilizzato principalmente per prevenire lunghi punti tra gli oggetti di ricamo ed evitare il taglio del filo da parte dell'operatore dopo il ricamo.

### ![simbolo di ignorare](/assets/images/docs/visual-commands-ignore.jpg) Ignora oggetto

Gli oggetti con questo comando verranno esclusi dall'output del piano di cucito.

## Elimina Comandi

### Elimina singoli comandi

Seleziona il gruppo di comandi e elimina.

### Elimina tutti i comandi nel documento

* Esegui `Estensioni > Ink/Stitch > Risoluzione dei problemi > Rimuovi impostazioni di ricamo`
* Scegli di rimuovere tutti o tipi specifici di comandi dal documento.
* Clicca su `Applica`.

## Comando di salto del punto per il taglio

`Comandi > Comando di salto del punto per il taglio`

Inserisce comandi di taglio per evitare i punti di salto.
{% include upcoming_release.html %}
È possibile scegliere tra un comando di taglio o di arresto.

**Informazioni:** Non utilizzare questa opzione se puoi ottimizzare il percorso. Il taglio del filo deve essere evitato il più possibile. Scopri le opzioni che Ink/Stitch offre per un [migliore percorso](/tutorials/routing/).
{: .notice--info }

## Visualizza

### Mostra/Nascondi i comandi degli oggetti

Alterna la visibilità dei comandi degli oggetti. I comandi rimarranno funzionali anche quando nascosti.

`Estensioni > Ink/Stitch > Comandi > Visualizza > Mostra/Nascondi i comandi degli oggetti`

### Scala i simboli dei comandi

Imposta la dimensione dei simboli dei comandi in tutto il documento: `Estensioni > Ink/Stitch > Comandi > Visualizza > Scala i simboli dei comandi...`

Utilizza l'anteprima in tempo reale per vedere l'effetto durante la scalatura.