---
title: "Strumenti per Font"
permalink: /docs/font-tools/
last_modified_at: 2025-12-29
toc: true
---
Una raccolta di strumenti adatti a creatori di font o a chi desidera aggiungere font aggiuntivi allo strumento di lettering Ink/Stitch [lettering tool](/docs/lettering).

Leggi il [tutorial di creazione di font Ink/Stitch](/tutorials/font-creation) per istruzioni dettagliate.
{: .notice--info }


## Converti Font SVG al Livello dei Glifi
Questa estensione consente di convertire un font SVG al livello dei glifi, come richiesto dallo strumento di lettering.

{% include upcoming_release.html %}
Consente il posizionamento dei font specificando l'altezza target del glifo specificato.
## Directory Font Personalizzata

Questa estensione consente di definire una directory nel tuo file system in cui desideri archiviare font aggiuntivi da utilizzare con lo strumento di lettering.

Posiziona ogni font in una sottodirectory della tua directory font personalizzata. Ogni cartella del font deve contenere almeno una variante del font e un file JSON.
Inoltre, è consigliabile salvare anche un file di licenza.

{% include upcoming_release.html %}

Le **varianti del font** dovevano essere denominate con una freccia, che indicava la direzione del punto che era stata utilizzata per la creazione (`→.svg`, `←.svg`, ecc.).
Ora, i nomi devono essere ltr.svg per la direzione da sinistra a destra e rtl.svg per la direzione da destra a sinistra.

È anche possibile creare una cartella denominata ltr (o rtl) e inserire più file di font per questa specifica direzione.

Come requisito minimo, il file JSON deve includere il nome del font.

## Modifica JSON

Questa estensione consente di modificare un file di informazioni del font esistente. Se il font non ha un file JSON, creane uno con [genera JSON](#generate-json).

Questa estensione aggiorna anche l'elenco dei glifi.

### Utilizzo

* Esegui `Estensioni > Ink/Stitch > Gestione dei font > Modifica JSON`
* Regola i dettagli del tuo font, come nome, descrizione, informazioni sulla licenza, parole chiave e informazioni sul kerning.
* Clicca su applica.

## Campionamento dei Font

Questa estensione crea un elenco di tutte le lettere in un font. Aiuta i creatori di font a testare il risultato di un nuovo font.
{% include upcoming_release.html %}
Rende visibili solo i glifi sbloccati (sensibili). Ciò consente un campionamento parziale durante la creazione del font.

### Utilizzo

* Esegui `Estensioni > Ink/Stitch > Gestione dei font > Campionamento dei font`
* Seleziona un font, regola le impostazioni.
* Clicca su applica.

### Opzioni

* Font: il font che vuoi utilizzare.
* Direzione del punto: l'impostazione predefinita è da sinistra a destra.
* Scala: in percentuale.
* Larghezza massima della riga: gli interruzioni di riga verranno scelti di conseguenza.
* Ordinamento per colore: indica se un font multicolore deve essere ordinato per colore o meno (il font deve impostare i valori dell'indice di [ordinamento per colore](#set-color-index)).

## Forza il blocco dei punti

A volte, i font piccoli possono sfilacciarsi se i fili vengono tagliati dopo che la macchina da ricamo ha terminato il lavoro.

Pertanto, è importante che anche i punti di connessione all'interno di una distanza inferiore al corpo del font rispetto alla lunghezza minima del punto di salto (predefinito: 3 mm) abbiano punti di blocco.

Questa estensione aiuta ad aggiungere punti di blocco forzati. Si può scegliere di limitare l'aggiunta di punti di blocco solo alle colonne di raso.

### Utilizzo

* Esegui `Estensioni > Ink/Stitch > Gestione dei font > Forza il blocco dei punti...`
* Aggiorna le impostazioni in base al font.
* Clicca su applica.

### Opzioni

* Riduci al raso: aggiungi punti di blocco forzati solo alle colonne di raso.

* Aggiungi punti di blocco forzati in base alla distanza:
  * Distanza minima (mm): non aggiungere punti di blocco se la distanza dall'elemento successivo è inferiore a questa.
  * Distanza massima (mm): non aggiungere punti di blocco se la distanza dall'elemento successivo è superiore a questa.

* Aggiungi un attributo di blocco forzato all'ultimo elemento di ogni glifo.
{% include upcoming_release.html %}
* Aggiungi un attributo di blocco forzato all'ultimo elemento di ogni gruppo.

## Genera JSON

Questa estensione è stata creata per aiutarti a creare il file JSON.
A seconda del metodo utilizzato per generare il file del font, potrebbe includere informazioni aggiuntive sul kerning nel file JSON.
Leggi [**come generare un font SVG con informazioni sul kerning**](/tutorials/font-creation).
Se hai generato il file SVG senza informazioni sul kerning, questa estensione può comunque aiutarti a configurare il file JSON con informazioni di base.

### Informazioni sul Font
{% include upcoming_release_params.html %}
Consente il posizionamento dei font specificando l'altezza target del glifo specificato.

|Opzione                 |Descrizione
|-----------------------|-------------------------------------
|Nome (obbligatorio)       |Il nome del tuo font
|Descrizione            |Informazioni aggiuntive sul tuo font
|Licenza del font          |Tipo di licenza per questo font Ink/Stitch
|Nome del font originale              |nome del font TTF sottostante, se presente|
|URL del font originale                |URL del font sottostante.|
|File del font (obbligatorio)  |Quando hai utilizzato FontForge per generare il file SVG del font, Ink/Stitch leggerà le informazioni sul kerning dal tuo font per includerle nel file JSON.<br/>Inoltre, il file del font verrà utilizzato per determinare il percorso di output.<br/><br/>Un file `font.json` verrà salvato nella cartella del file SVG del tuo font.
|Parole chiave               |Abilita le categorie a cui si applica il tuo font

### Impostazioni del Font

|Opzione                 |Descrizione|
|-----------------------|-------------------------------------|
|Gliceme predefinito          |il glifo da visualizzare se il glifo richiesto dall'utente non è disponibile nel file del font (glifo mancante)
|Routinaggio automatico del raso        |▸ Abilitato<br/>Ink/Stitch genererà un [routing ragionevole per le colonne di raso](/docs/satin-tools/#auto-route-satin-columns) nel tuo font quando utilizzato nello strumento di lettering.<br/><br/>▸ Disabilitato<br/>Ink/Stitch utilizzerà i glicemi così come sono. Disabilita questa opzione se ti sei già preso cura del routing nel tuo font.
|Reversibile             |indica se il tuo font può essere cucito in avanti e indietro o solo in avanti. Spunta questa opzione solo se hai creato varianti del font.
|Ordinabile               |indica se il tuo font può essere ordinato per colore o meno. Questo funziona solo se gli elementi nel tuo font contengono un [indice di ordinamento per colore](#set-color-index)
|Combina indici        |un elenco separato da virgole degli indici di ordinamento per colore. Gli elementi con questo indice verranno combinati in un singolo elemento. Utile per ridurre i cambi di colore per tipi di punti multicolore come il tartan.
|Forza la lettera minuscola/maiuscola      |▸ Nessuno<br/>Scegli questa opzione se il tuo font contiene lettere maiuscole e minuscole (predefinito).<br/><br/>▸ Maiuscole<br/>Scegli questa opzione se il tuo font contiene solo lettere maiuscole.<br/><br/>▸ Minuscole<br/>Scegli questa opzione se il tuo font contiene solo lettere minuscole.
|Scala minima / Scala massima  |Definisci quanto i tuoi glicemi possono essere ridimensionati senza perdere qualità durante la cucitura

### Kerning

I campi seguenti sono facoltativi, sono necessari solo se il tuo file SVG non contiene informazioni sul kerning.

Se le informazioni sul kerning non possono essere trovate, questi valori verranno utilizzati al loro posto.

|Opzione                 |Descrizione|
|-----------------------|-------------------------------------|
|Forza i valori definiti   |Non utilizzare le informazioni del file del font, ma i valori definiti di seguito.
|Interlinea (px)           |Definisce l'altezza della riga del tuo font. Lascia a `0` per consentire a Ink/Stitch di leggerlo dal tuo file del font (predefinito a 100 se le informazioni non possono essere trovate).
|Spaziatura tra le parole (px)      |La larghezza del carattere "spazio"

## Lettere in font

"Lettere in font" è uno strumento per convertire le lettere da ricamo pre-digitalizzate in un font da utilizzare con lo strumento di lettering Ink/Stitch.

Il font digitalizzato deve soddisfare determinate **condizioni** per essere importato:
* Un file per ogni glifo in un formato di ricamo che Ink/Stitch può leggere
* Il nome del gliceme deve essere posizionato alla fine del nome del file. Un nome di file valido per la lettera A maiuscola sarebbe, ad esempio, `A.pes` o `Example_Font_A.pes`.

Spesso, i font acquistati sono organizzati in sottocartelle, perché ogni lettera è disponibile in più formati di file di ricamo. Non è necessario modificare la struttura dei file in questo caso. Lo strumento "Lettere in font" cercherà i file del font anche nelle sottocartelle.
{: .notice--info }

### Utilizzo

* Imposta il formato di file di ricamo da cui desideri importare le lettere (idealmente, scegli un formato di file in grado di archiviare informazioni sul colore).
* Seleziona la cartella del font in cui sono memorizzate le lettere. Se sono organizzate in sottocartelle, scegli la cartella principale.
* Scegli se desideri importare i comandi o meno (avviso: l'importazione di comandi su larga scala rallenterà il sistema).
* Clicca su applica e attendi...
* Dopo l'importazione, sposta la linea di base nella posizione corretta e posiziona le lettere di conseguenza. Il bordo sinistro della tela influenzerà anche il posizionamento delle lettere tramite lo strumento di lettering.
* Salva il tuo font come `.svg` in una nuova cartella all'interno della tua [directory font personalizzata](#custom-font-directory).
* Esegui [`Genera JSON`](#generate-json) per rendere disponibile il font e salva il file JSON nella stessa cartella del tuo font. Non selezionare "Routinaggio automatico del raso" per i font pre-digitalizzati e lascia la scala a 1.
* Se necessario, puoi regolare le informazioni sul kerning utilizzando l'estensione [`Gestione dei font > Modifica file JSON`](#edit-json).
* Se il tuo font è colorato, puoi renderlo ordinabile utilizzando [indici di ordinamento per colore](#set-color-index).

## Organizza i glicemi
{% include upcoming_release.html %}

L'obiettivo di questa estensione è aiutare i digitalizzatori di font a organizzare il proprio lavoro passo dopo passo.

Ad ogni passaggio, un gruppo di glifi viene posizionato nella parte superiore dello stack di oggetti e il creatore del font deve digitalizzare questi glicemi prima di passare al passaggio successivo.

I passaggi sono organizzati per dividere il lavoro in blocchi più piccoli e massimizzare il riutilizzo delle lettere già digitalizzate.

È davvero necessario testare ciò che si fa ad ogni passaggio, perché verrà copiato per altre lettere e si vuole evitare di dover correggere lo stesso errore più volte:

Utilizza il campionamento dei font per generare un file con tutte le lettere sbloccate
- esegui la risoluzione dei problemi e correggi tutti gli errori rilevati
- utilizza la simulazione per rilevare salti indesiderati. È meglio farlo con le lettere ingrandite il più possibile
- l'anteprima realistica può aiutarti a trovare errori
- ma le cuciture reali sono il test definitivo

### Passaggio 1

Il codice rimuove silenziosamente i livelli indesiderati (ad esempio, percorsi vuoti o percorsi inesistenti).

In questo passaggio, devi digitalizzare solo la virgola, il trattino e il punto.

### Passaggio 2

In questo passaggio, devi digitalizzare tutte le lettere che sono state raggruppate nei tre gruppi: maiuscole, minuscole e altre.

Ad esempio, troverai una copia del punto nel gliceme "i" e "j"; spetta a te decidere se questo è utile o meno.

Solo le lettere semplici devono essere digitalizzate (nessuna lettera accentata in questi gruppi).

### Passaggio 3

In questo passaggio, devi digitalizzare numeri, simboli e alcune punteggiature.

Troverai parti di alcuni glicemi già inclusi, ad esempio, nel ";" troverai il "." e la "," digitalizzati nel passaggio 1.

Spetta a te posizionarli correttamente o eliminarli. Inoltre, la "1" contiene la "l" e la "I". Se sono troppo diversi dalla "1" per essere utili, eliminali.

### Passaggio 4

Ultima parte della punteggiatura: creare la punteggiatura di chiusura utilizzando la punteggiatura di apertura.

Ad esempio, troverai la "(" nel ".)". Spetta a te restituirla, posizionarla e modificarla se necessario.

Normalmente, a questo punto, tutto è precompilato con il tuo lavoro già svolto.

### Passaggio 5

Apici, virgolette e accenti acuti singoli

Esistono diversi tipi di apici e virgolette a seconda della lingua utilizzata.

Se ne hai creato almeno uno, l'estensione ne aggiunge altri qui.

Lo stesso vale per le virgolette. Normalmente, non c'è niente da fare per loro.

In questo passaggio, devi digitalizzare gli accenti acuti singoli; quando possibile, vengono precompilati con un simbolo equivalente che è già stato elaborato.

Non dimenticare di rimuovere le parti non necessarie!

### Passaggio 6

Accenti complessi:

In questo passaggio, si gestiscono gli altri segni diacritici.

Questi riutilizzano il lavoro svolto nel passaggio precedente.

Questi accenti complessi sono doppi o hanno la stessa forma di un accento semplice ma una posizione diversa.

I livelli sono precompilati, ma è necessario eseguire un po' di lavoro di posizionamento, motivo per cui una lettera che utilizza l'accento ha a volte un elemento inserito nel suo livello in modo da sapere dove posizionare il nuovo accento.

Non dimenticare di rimuovere le parti non necessarie!

### Passaggio 7

Lettere con un singolo accento:

Troverai il loro livello precompilato con la lettera e l'accento; spetta a te comporli per creare la lettera composta.

### Passaggio 8

Lettere con due o più accenti..... solo se hai scelto di includerne alcuni.

Puoi anche utilizzare questa estensione con qualsiasi file di font per:
- controllare la presenza di duplicati
- organizzare le lettere per categoria.

Nota: sì, puoi lasciare le lettere raggruppate; non influisce sullo strumento di lettering.

## Rimuovi il Kerning

**⚠ Avviso**: Le modifiche apportate da questo strumento non possono essere annullate. Assicurati di salvare una **copia** del tuo file prima di eseguire questi passaggi.
{: .notice--warning }

Il tuo font è pronto per essere utilizzato. Ma se hai creato il tuo font con FontForge, ora contiene molte informazioni che potrebbero non essere necessarie per il funzionamento del font e che potrebbero rallentarlo leggermente.
Ink/Stitch include uno strumento per ripulire il tuo font SVG.

1. Assicurati di salvare una **copia** del tuo font. Le informazioni aggiuntive potrebbero non essere necessarie per il funzionamento del font, ma potrebbero essere utili quando vuoi aggiungere altri glicemi.
2. Esegui `Estensioni > Ink/Stitch > Strumenti per font > Rimuovi il kerning`
3. Seleziona il file del tuo font.
4. Clicca su applica.

## Imposta indice colore

Imposta un indice per informare lo strumento di lettering su dove posizionare gli elementi selezionati quando l'ordinamento per colore è abilitato.

* In un file di font, seleziona gli elementi dello stesso colore.
* Apri l'estensione `Estensioni > Ink/Stitch > Gestione dei font > Imposta indice colore`
* Imposta il numero dell'indice.
* Applica.

Il file JSON deve specificare se un font è ordinabile per colore. Utilizza [Modifica JSON](#edit-json) e abilita l'opzione "Ordinabile" nella scheda "Impostazioni font".
{: .notice--warning }
