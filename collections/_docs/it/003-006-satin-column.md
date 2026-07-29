---
title: "Colonna di Satin"
permalink: /docs/stitches/satin-column/
last_modified_at: 2026-04-08
toc: true
---
## Descrizione

Le colonne di satin vengono utilizzate per bordi, lettere o piccole aree da riempire.

{% include folder-galleries path="butterfly-fill-project/satin/" captions="1:Satin swirl;2:Satin con lunghezza del punto randomizzata e punti di spacco sfalsati;3:Satin multicolore" %}

[<i class="fa fa-download"></i> Scarica i file di esempio](/assets/images/stitch-type-butterflies/satin_column.zip)

## Creazione

Ink/Stitch offre diversi metodi per creare colonne di satin. Il metodo 1 non esegue alcuna conversione, ma interpreta un tratto come una colonna di satin. I metodi dal 2 al 5 convertono in una colonna di satin manuale, che può quindi essere modificata secondo necessità. Il metodo 5 offre maggiori possibilità di personalizzazione.

![Metodi](/assets/images/docs/satin_methods.svg)

1. [Tratto interpretato come satin](#1-render-stroke-as-satin): per colonne di satin con larghezza uniforme.
2. [Tratto convertito in satin](#2-stroke-to-satin): per colonne di satin con larghezza uniforme.
3. [Tratto convertito in effetto percorso dinamico satin](#3-stroke-to-live-path-effect-satin): colonna di satin modificabile con contorno opzionale decorato.
4. [Zigzag convertito in satin](#4-zigzag-line-to-satin): creazione di colonne di satin per tavolette grafiche e touchscreen.
5. [Riempimento convertito in satin](#5-fill-to-satin): crea colonne di satin a partire da riempimenti.
6. [Colonna di satin manuale](#6-manual-satin-column): per un controllo completo su ogni parte della colonna di satin.

### 1 - Rendere un tratto come satin

{% include upcoming_release.html %}

Questo metodo interpreta i percorsi con un colore di tratto direttamente come colonne di satin ed è quindi il metodo più semplice per creare colonne di satin di larghezza uniforme.

* Aggiungi un colore di tratto a un oggetto percorso (senza riempimento).
* Imposta la larghezza del contorno in base alla dimensione del punto di satin desiderato (il valore deve essere superiore a 1,5 mm; consulta [preferenze](/docs/preferences/#minimum-satin-stroke-width) per maggiori informazioni sulla larghezza minima del punto di satin).
* Esegui `Estensioni > Ink/Stitch > Parametri`.
* Apri la scheda "Colonna di Satin" e attiva "Colonne di Satin Personalizzate".

La posizione dei nodi può influenzare il modo in cui viene renderizzata la colonna di satin:

![Tratto convertito in satin. Lo stesso percorso con impostazioni dei nodi diverse](/assets/images/upcoming/3.3.0/stroke-to-satin-nodes.png){: width="600px"}

### 2 - Tratto in Satin

* Aggiungi un colore di tratto a un oggetto percorso (senza riempimento).
* Imposta la larghezza del tratto in base alla larghezza del punto di satin desiderato.
* Esegui `Estensioni > Ink/Stitch > Strumenti Satin > Converti tratto in satin`.
* Utilizza così com'è o personalizza le "barre" e/o i "filamenti".

Per maggiori informazioni su [Tratto in Satin](/docs/satin-tools/#convert-line-to-satin).

### 3 - Tratto in Effetto Percorso Dinamico Satin

Questo può essere utilizzato per creare una colonna di satin che può avere un contorno decorato o per creare una colonna di satin più facile da adattare in larghezza. Si prega di notare che, una volta utilizzato l'instradamento automatico su questo tipo di satin, l'effetto percorso dinamico verrà applicato e il percorso potrà essere adattato manualmente solo in seguito.

Utilizza `Percorso > Oggetto in percorso` per convertire questo in una colonna di satin standard.

Per maggiori informazioni su [Effetti Percorso Dinamici Satin](/docs/satin-tools/#stroke-to-live-path-effect-satin).

### 4 - Linea Zigzag in Satin

Questo metodo è utile quando si utilizza un touchscreen o una tavoletta grafica.

Per maggiori informazioni su [Linea Zigzag in Satin](/docs/satin-tools/#zigzag-line-to-satin).

### 5 - Riempimento in Satin

Il riempimento in satin può essere utilizzato per convertire un riempimento in una colonna di satin. È una funzione semi-automatica e richiede ulteriore lavoro manuale.

Per maggiori informazioni su [Riempimento in Satin](/docs/satin-tools/#fill-to-satin).

### 6 - Colonna di Satin Manuale

Una colonna di satin è definita da una forma composta da **due linee parallele**. Ink/Stitch disegnerà zig-zag avanti e indietro tra le due linee. Lo spessore della colonna si baserà sulla distanza tra le due linee.

* Combina due tratti con `Percorso > Combina` o premi `Ctrl+K`.
* [Controlla la direzione dei percorsi](/docs/customize/#abilitare-le-linee-guida-del-percorso--direzione). Entrambe le "guide" devono essere orientate nella stessa direzione. Se non lo sono, Ink/Stitch inverte automaticamente una di esse, ma avrai un maggiore controllo se inverti manualmente una delle guide, selezionando un nodo di una delle guide con lo *Strumento Editor di Nodi* (`N`) e eseguendo `Percorso > Inverti`. Questo invertirà solo la guida selezionata.
* Utilizza il metodo dei nodi o delle guide come descritto di seguito.
* Quindi seleziona la tua colonna di satin ed esegui i parametri tramite `Estensioni > Ink/Stitch > Parametri` o una [scorciatoia personalizzata](/docs/customize/).

### Controllo della direzione del punto

#### Metodo dei Nodi

[![Colonna di Satin Barca](/assets/images/docs/satin-column.jpg){: width="200x"}](/assets/images/docs/satin-column.svg){: title="Scarica il file SVG" .align-left download="satin-column.svg" }
A seconda della complessità del tuo disegno, questo metodo potrebbe richiedere molto tempo, perché i due percorsi devono avere **lo stesso numero di punti**. Ciò significa che ogni percorso sarà composto da un numero uguale di curve di Bézier. Ogni coppia di punti (uno su ciascuna guida) funge da "punto di controllo": Ink/Stitch si assicurerà che un "zig" vada da un punto all'altro.

#### Metodo delle Guide

[![Colonna di Satin chefshat](/assets/images/docs/satin-column-rungs-example.jpg){: width="200x"}](/assets/images/docs/satin-column-rungs.svg){: title="Scarica il file SVG" .align-left download="satin-column-rungs.svg" }
Il metodo delle guide ti darà maggiore controllo su come viene renderizzata la colonna di satin. Un posizionamento corretto dei punti su ciascuna delle due linee aiuta a ottenere la direzione corretta del punto. Tuttavia, ci sono situazioni in cui è necessario aggiungere linee di direzione ("guide") per le colonne di satin:

* In alcune aree angolari complesse.
* In disegni complicati in cui spostare i punti è sia difficile che richiede tempo.
* In situazioni speciali in cui si desidera che la direzione del punto sia insolita.
{: style="clear: both;" }

**Aggiunta manuale di guide**

* Assicurati che il percorso della colonna di satin esistente (con i due sottopercorsi) sia selezionato con lo strumento Editor di Nodi.
* Premi `P` o seleziona lo strumento Matita.
* Tieni premuto `Shift`.
* Clicca una volta all'inizio della guida.
* Clicca una seconda volta alla fine della guida.

  [![Guide in azione](https://edutechwiki.unige.ch/mediawiki/images/thumb/6/68/InkStitch-round-bird-2.png/300px-InkStitch-round-bird-2.png)](https://edutechwiki.unige.ch/mediawiki/images/6/68/InkStitch-round-bird-2.png)

  Disegno originale di [Liv Iko](https://thenounproject.com/liv_iko/collection/birds/?i=898697) modificato da [EDUTECH Wiki](https://edutechwiki.unige.ch/en/InkStitch)
{: style="font-size: 0.5rem;"}

**Informazioni:** Ti consigliamo vivamente di utilizzare almeno tre guide. Se utilizzi esattamente due guide (e due guide), è difficile per Ink/Stitch decidere quale sia quale.
{: .notice--warning }

## Posizione di inizio e fine

Le colonne di satin iniziano automaticamente nel punto più vicino all'elemento precedente e terminano nel punto più vicino all'elemento successivo.

Per disabilitare questo comportamento, apri il [dialogo dei parametri](/docs/params/) e disabilita le opzioni "inizio/fine nel punto più vicino".

In alternativa, aggiungi manualmente un punto di inizio o di fine collegando un [comando](/docs/commands/#collegare-comandi-agli-oggetti-selezionati-) alla colonna di satin.

## Parametri

L'esecuzione di `Estensioni > Ink/Stitch > Parametri` ti darà la possibilità di perfezionare la tua colonna di satin e di utilizzare un sottofondo.

La colonna di satin supporta tre tipi di sottofondo, di cui puoi utilizzare uno, due o tutti e tre contemporaneamente.

Leggi anche questo [eccellente articolo](https://www.mrxstitch.com/underlay/) sulla progettazione di colonne di satin.

### Parametro asimmetrico

Alcuni parametri della colonna di satin sono asimmetrici, il che significa che è possibile applicare valori diversi alle due guide.

Ad esempio, il "percentuale casuale di aumento della larghezza del satin" è un parametro asimmetrico. Se viene inserito un singolo valore, si applica a entrambe le guide; se vengono inseriti due valori separati da uno spazio, il primo si applica alla prima guida e il secondo si applica alla seconda guida.
![parametro asimmetrico](/assets/images/docs/asymetric_parameter.png)

Alcuni di questi parametri non fanno parte dell'ultima versione.
{: .notice--info}

### Strato superiore del satin

{% include upcoming_release_params.html %}

{% include params.html stitch_type='satin'%}

### Sottofondo Centrale

Questo è un punto di cucitura dritto al centro della colonna e avanti e indietro. Questo potrebbe essere tutto ciò di cui hai bisogno per colonne di satin sottili. Puoi anche usarlo come base per un sottofondo più elaborato.

![Parametri - Esempio di sottofondo centrale](/assets/images/docs/params-center-walk-underlay-example.jpg)

{% include params.html stitch_type='satin_center_underlay'%}

### Sottofondo del Contorno

Questo è un punto di cucitura che sale su un lato della colonna e torna giù sull'altro lato. Le file sono distanziate dal bordo della colonna per una quantità specificata. Per colonne piccole o medie, questo potrebbe essere sufficiente di per sé.

![Parametri - Esempio di sottofondo del contorno](/assets/images/docs/params-contour-underlay-example.jpg)

{% include params.html stitch_type='satin_contour_underlay'%}

### Sottofondo a Zigzag

Questo è essenzialmente una colonna di satin a bassa densità cucita all'estremità della colonna e di nuovo all'inizio. Quando abbinato al sottofondo del contorno, si ottiene il "sottofondo tedesco" menzionato in [questo articolo](https://www.mrxstitch.com/underlay/). Per colonne larghe o tessuti difficili, puoi utilizzare tutti e tre i tipi di sottofondo.

![Parametri - Esempio di sottofondo a zigzag](/assets/images/docs/params-zigzag-underlay-example.jpg)

{% include params.html stitch_type='satin_zigzag_underlay'%}

## Strumenti Satin

Assicurati di dare un'occhiata agli [Strumenti Satin](/docs/satin-tools/). Renderanno la tua esperienza con le colonne di satin molto più semplice.

## File di esempio che includono la colonna di satin

{% include tutorials/tutorial_list key="stitch-type" value="Satin Stitch" %}
