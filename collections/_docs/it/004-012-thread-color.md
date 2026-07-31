---
title: "Gestione dei Colori del Filo"
permalink: /docs/thread-color/
last_modified_at: 2025-03-29
toc: true
---
Inkscape supporta l'utilizzo di palette di colori. Le palette di colori aiutano Ink/Stitch a definire i nomi dei colori e a salvare informazioni aggiuntive come il nome del produttore del filo e il numero di catalogo del filo nel file di ricamo esportato.

A seconda delle capacità della tua macchina da ricamo, potrai visualizzare i nomi dei colori sullo schermo. Si prega di notare che alcuni formati di file di ricamo (ad esempio, DST) non memorizzano informazioni sui colori. Altri formati di file utilizzano un sistema di file multipli per memorizzare le informazioni sui colori. Ad esempio, per i file EXP, è comune salvare il formato colore INF insieme al file EXP per trasmettere le informazioni sul colore alla tua macchina.

Le definizioni dei colori sono mostrate nell'[output PDF](/docs/print-pdf/). È anche possibile [esportare le informazioni della lista dei fili](/docs/threadlist/) in un semplice file di testo.

Prima di poter utilizzare le funzionalità dei colori del filo, è necessario installare le palette di colori. Puoi definire le [tue palette personalizzate](/docs/thread-color/#install-custom-palette) o [installare quelle fornite con Ink/Stitch](/docs/thread-color/#install-thread-color-palettes-for-inkscape). Indipendentemente dal metodo scelto, riavvia Inkscape dopo aver installato le palette di colori.

## Installazione delle Palette

### Installazione delle Palette di Colori per il Filo in Inkscape

Ink/Stitch viene fornito con molte palette di colori dei produttori di fili che possono essere installate in Inkscape. Ciò consente di creare progetti con i colori corretti.
I colori appariranno nell'output PDF e saranno inclusi nel tuo file di ricamo, se il formato del tuo file supporta le rappresentazioni dei colori.

* Vai su `Estensioni > Ink/Stitch > Installa componenti aggiuntivi per Inkscape`
* Abilita l'opzione "Installa palette di colori per il filo"
* Clicca su "Applica"
* Riavvia Inkscape

### Installazione di una Palette Personalizzata

Se hai un file `.gpl` contenente la lista dei colori dei fili che stai effettivamente utilizzando, rendilo disponibile in Inkscape con questa estensione: `Estensioni > Ink/Stitch > Gestione dei Colori del Filo > Installa palette personalizzata...`. Dovrai riavviare Inkscape dopo questo processo.

Le palette di colori .gpl possono essere generate con [Genera Palette di Colori](#generate-color-palette).

## Generazione e Modifica delle Palette di Colori Personalizzate

### Generazione della Palette

Inkscape consente di generare file di palette di colori `.gpl`. Tuttavia, non ci consente di ordinare correttamente le campioni di colore.

Questa estensione esporterà i colori degli elementi di testo utilizzando il testo come nomi e numeri dei colori.

1. Importa un'immagine con i colori del filo che desideri utilizzare per la palette di colori.
2. Attiva lo strumento di testo e copia e incolla i nomi dei colori (se li hai) oppure digitati.
   Utilizza una riga per ogni colore.
   Se l'ultima parte del nome di un colore è un numero, questo verrà utilizzato come numero di catalogo.
3. Utilizza l'estensione `Estensioni > Ink/Stitch > Gestione dei Colori del Filo > Genera Palette > Dividi Testo` per dividere un blocco di testo con più righe in elementi di testo separati.
4. Attiva lo strumento di selezione del colore (D) e colora gli elementi di testo, utilizzando il tasto Tab per selezionare gli elementi di testo.
5. Seleziona gli elementi di testo ed esegui `Estensioni > Ink/Stitch > Gestione dei Colori del Filo > Genera Palette > Genera Palette di Colori...`
6. Specifica il nome per la tua palette di colori e fai clic su "Applica"
7. Riavvia Inkscape per attivare la nuova palette di colori.

{% include video id="4bcRVoKvzAw" provider="youtube" %}

### Palette in Testo

Le palette esistenti possono essere modificate come testo con Ink/Stitch.

* Importa colori e nomi dei colori con `Estensioni > Ink/Stitch > Gestione dei Colori del Filo > Palette in Testo`
* Modifica i colori, aggiorna i nomi dei colori o i numeri di catalogo o aggiungi altri colori.
* Esporta la tua palette con `Estensioni > Ink/Stitch > Gestione dei Colori del Filo > Genera Palette > Genera Palette di Colori...`
* Riavvia Inkscape.

## Lavorare con le Palette

### Utilizzo Generale

Le palette di Inkscape si trovano nella parte inferiore, a destra, delle campioni di colore.

![Palette di Inkscape](/assets/images/docs/palettes-location.png)

Fai clic sulla piccola freccia per aprire un elenco delle palette installate e scegli la palette dei colori del produttore in base al filo che desideri utilizzare.

Per applicare un colore a un elemento, seleziona l'elemento e fai clic sulle campioni di colore nella parte inferiore. Utilizza il `click sinistro` per un colore di riempimento e `shift + click sinistro` per un colore di tratto. Utilizza la "X" sul lato sinistro per rimuovere i colori.

### Applica Palette

Questa estensione applica i colori più vicini da una palette di fili specificata a un progetto. Questo verrà riconosciuto anche dal file di ricamo Ink/Stitch e dall'output PDF.

* Esegui `Estensioni > Ink/Stitch > Gestione dei Colori del Filo > Applica Palette`
* Seleziona la palette di colori a cui desideri applicare
* Fai clic su "Applica"

## Lavorare con le Liste dei Fili

### Esportazione della Lista dei Fili

Esporta le liste dei fili e i file di colori utilizzando la normale routine di esportazione dei file in Inkscape.
Le liste dei fili possono essere esportate anche all'interno del file zip di Ink/Stitch ([esportazione in batch](/docs/import-export/#batch-export)).

### Applicazione della Lista dei Fili

Ink/Stitch può applicare una lista dei fili a un progetto di ricamo. Questo è particolarmente utile se vuoi lavorare su file di ricamo esistenti che non supportano le informazioni sui colori (ad esempio, DST).

Potrebbe essere utile anche se desideri testare diverse impostazioni di colore. Puoi esportarle e importarle come preferisci. Ma fai attenzione a non modificare la quantità e l'ordine dei colori. In caso di modifica di questi elementi, è preferibile salvare l'intero file SVG.

* Esegui `Estensioni > Ink/Stitch > Gestione dei Colori del Filo > Applica Lista dei Fili`
* Scegli un file contenente le informazioni sul colore del filo.
* Definisci se il file contenente le informazioni sul colore è stato generato con Ink/Stitch o con altri mezzi.

  Se con altri mezzi: Seleziona la palette di colori Ink/Stitch per associare i colori.
* Fai clic su "Applica"