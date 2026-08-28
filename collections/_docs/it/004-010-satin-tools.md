---
title: "Strumenti: Satin"
permalink: /docs/satin-tools/
last_modified_at: 2026-04-08
toc: true
---
`Extensions > Ink/Stitch  > Strumenti: Satin` include una serie di utili strumenti che semplificano il lavoro con le [colonne satin](/docs/stitches/satin-column/).

**Esempio:**
* Crea un percorso utilizzando lo strumento di curve di Bézier (`B`).
* Esegui [Conversione in satin](#convert-line-to-satin).
* Utilizza la [finestra di dialogo Parametri](/docs/params/#satin-params) per impostare un sottosmalto.
* Esegui [Instradamento automatico del satin](#auto-route-satin-columns) per ottenere colonne satin ben orientate.

[![Conversione in satin](/assets/images/docs/en/satin-tools.svg)](/assets/images/docs/en/satin-tools.svg){: title="Scarica il file SVG" download="satin-tools.svg" }

**Suggerimento:** Per un accesso più rapido, [imposta le scorciatoie](/docs/customize/) per strumenti satin specifici.
{: .notice--info}

## Instradamento automatico delle colonne satin...

Questo strumento sostituirà i tuoi satin con un nuovo set di colonne satin in un ordine di cucitura logico. I sottosmalto e i punti di salto verranno aggiunti se necessario, e i satin verranno interrotti per facilitare i salti. I satin risultanti manterranno tutti i parametri impostati sui satin originali, inclusi il sottosmalto, la spaziatura a zig-zag, ecc.

### Utilizzo

**Suggerimento:** Per impostazione predefinita, selezionerà l'estremità più a sinistra come punto di partenza e l'estremità più a destra come punto finale (anche se questi si trovano a metà di un satin, come il bordo sinistro di una lettera "o"). Puoi sovrascrivere questo comportamento collegando i comandi ["Posizione di inizio/fine dell'instradamento automatico del satin"](/docs/commands/#--starting-ending-position-for-auto-route-satin).
{: .notice--info }

1. Seleziona le colonne satin (preparate con sottosmalto, ecc.).
2. Esegui `Extensions > Ink/Stitch  > Strumenti: Satin > Instradamento automatico delle colonne satin...`.
3. Abilita le opzioni desiderate e fai clic su "Applica".

### Opzioni

* Abilita **Taglio dei punti di salto** per utilizzare tagli invece di punti di salto. Qualsiasi punto di salto superiore a 1 mm viene tagliato. I comandi di taglio vengono aggiunti al file SVG, quindi puoi modificarli o eliminarli a tuo piacimento.

* Se preferisci mantenere l'ordine precedente (il che potrebbe essere il caso se hai satin sovrapposti), abilita l'opzione **Mantieni l'ordine delle colonne satin**.

* **Mantieni i percorsi originali** indicherà se gli elementi originali verranno rimossi o mantenuti.

## Conversione in satin

Questa estensione converte un tratto in una colonna satin con una larghezza specificata. Dopo la conversione, vedrai le due guide (i "rails") e (possibilmente) molte maglie, a seconda della forma della tua linea.

### Utilizzo

1. Disegna una curva di Bézier (`B`).
2. Imposta la larghezza del tratto nel pannello "Riempimento e tratto" ("scheda Stile del tratto"), a cui puoi accedere con `Shift+Ctrl+F`.
2. Esegui `Extensions > Ink/Stitch  >  Strumenti: Satin > Conversione in satin`.

## Taglio della colonna satin

Divide una colonna satin in un punto specificato. La divisione avviene al limite di una cucitura per garantire che le due colonne satin risultanti siano cucite esattamente come l'originale. Tutti i parametri impostati sulla colonna satin originale rimangono sulle due nuove colonne satin, e tutte le maglie vengono mantenute. Se una delle colonne satin non avesse più maglie, ne viene aggiunta una nuova.

### Utilizzo

1. Seleziona una colonna satin (un satin semplice non funziona).
2. Collega uno o più comandi "Punto di divisione del satin" utilizzando `Extensions > Ink/Stitch  > Comandi > Collega i comandi agli oggetti selezionati`.
3. Sposta il simbolo (o semplicemente l'estremità della linea di connessione) per puntare al punto esatto in cui desideri dividere il satin.
4. Seleziona nuovamente la colonna satin.
5. Esegui `Extensions > Ink/Stitch  > Strumenti: Satin > Divisione della colonna satin`.
6. Il comando di punto di divisione e la linea di connessione scompaiono, e apparentemente non è successo altro. Seleziona il tuo satin e vedrai che è stato diviso.

{% include upcoming_release.html %}
Puoi utilizzare più comandi sulla stessa colonna satin per dividerla in più parti in un'unica operazione.

## Riempimento satin

Il riempimento satin può essere utilizzato per convertire un riempimento in un satin. È una funzione semiautomatica e richiede un po' di lavoro manuale.

### Utilizzo

* Prepara i tuoi oggetti riempiti. Potrebbe essere necessario dividere il riempimento in forme più semplici utilizzando lo strumento di creazione di forme o altri strumenti di modifica del percorso in Inkscape.
* Assicurati che il riempimento abbia solo un colore di riempimento e non un colore di tratto.
* Crea maglie con un colore di tratto (e senza colore di riempimento). Le maglie aiutano a definire come la forma del riempimento verrà convertita.

  Assicurati di aggiungere un numero sufficiente di maglie.
  Soprattutto quando vuoi abilitare l'opzione `inizio/fine alla maglia`, che rimuoverà una porzione dalle estremità aperte.
  {: .notice--warning }
* Seleziona il riempimento e le maglie.
* Esegui `Extensions > Ink/Stitch > Strumenti: Satin > Riempimento satin...`.
* Abilita le opzioni desiderate.
* Fai clic su "Applica".

### Opzioni

Opzione               | Descrizione
---------------------|-------------
Inizio / fine alla maglia | Quando abilitata, le sezioni delle estremità aperte verranno rimosse dal satin. Si prega di notare che è necessario definire un numero sufficiente di maglie, altrimenti si vedranno parti mancanti. Questa opzione è utile, poiché nella maggior parte dei casi si desidera che il satin si interrompa alle estremità quando viene cucito.
Sottosmalto centrale | Aggiunge un sottosmalto centrale predefinito al(i) satin.
Sottosmalto del contorno | Aggiunge un sottosmalto del contorno predefinito al(i) satin.
Sottosmalto a zig-zag | Aggiunge un sottosmalto a zig-zag predefinito al(i) satin.
Mantieni i percorsi originali | Indica se gli elementi selezionati verranno rimossi o mantenuti.

### Intersezioni

Utilizza i ponti alle intersezioni per informare Ink/Stitch su come collegare le colonne satin.
Le intersezioni non collegate semplicemente lasciano uno spazio.

I ponti devono essere completamente all'interno dell'elemento di riempimento e non possono attraversare il contorno.
{: .notice--info}

![Conversione in satin con e senza ponte](/assets/images/docs/fill_to_satin_bridge.png)

### File di esempio

[Scarica il file di esempio per il riempimento satin](/assets/images/docs/fill_to_satin_playground.svg){: title="Scarica il file SVG" download="fill_to_satin_playground.svg" }

## Inversione delle guide delle colonne satin

Questo è un piccolo strumento per aiutarti a pianificare con precisione il percorso di cucitura. Ad esempio, puoi invertire le guide delle colonne satin per accorciare le connessioni tra due sezioni.

Una colonna satin che inizia originariamente sulla guida sinistra e termina sulla guida destra, inizierà sulla guida destra e terminerà sulla guida sinistra.

![Inversione delle colonne satin](/assets/images/docs/en/flip-satin-column.jpg)

### Utilizzo

* Seleziona una o più colonne satin.
* Esegui `Extensions > Ink/Stitch  > Strumenti: Satin > Inversione delle colonne satin`.

## Satin multicolore

Questa estensione crea copie di satin selezionati per simulare un satin multicolore.

![Satin multicolore](/assets/images/tutorials/multicolor_satin/solution.png)

Se vuoi capire come funziona internamente questa estensione, [leggi questo](/tutorials/multicolor_satin).

### Utilizzo

* Seleziona una o più colonne satin.
* Apri `Extensions > Ink/Stitch > Strumenti: Satin > Satin multicolore`.
* Imposta le opzioni e i colori preferiti nella scheda "Colorazione".
* Applica.

### Opzioni

#### Impostazioni generali

* Colori equidistanti: scegli se i colori sono equidistanti o meno.
  * Se selezionato, la larghezza del colore e i margini sono definiti per tutti i colori dal valore di "larghezza del colore monocromatico".
  * Se non selezionato, puoi scegliere indipendentemente la larghezza e i margini per ogni colore.
* Overflow sinistro (%): aggiunge un bordo irregolare sul lato sinistro del satin.
* Overflow destro (%): aggiunge un bordo irregolare sul lato destro del satin.
* Compensazione di trazione (mm): allarga le colonne satin e le fa sovrapporre le sezioni di colore per evitare spazi.
* Seed casuale: cambia il valore per cambiare l'aspetto dei parametri casuali.

* Mantieni il satin originale: indica se il satin originale deve essere eliminato o meno.
* Applica sottosmalto per colore: si applica solo quando la colonna satin originale ha sottosmalto.
  * Se selezionato, i sottosmalto verranno applicati a ciascun colore separatamente, escludendo le sezioni multicolore.
  * Se non selezionato, solo il primo colore utilizzerà un sottosmalto, coprendo l'intera area.

{: .notice--info}

![Interfaccia utente satin multicolore](/assets/images/docs/en/multicolor_satin_ui_01.png)

![Interfaccia utente satin multicolore](/assets/images/docs/en/multicolor_satin_ui_02.png)

## Conversione in satin tramite effetto di percorso attivo

Converte un tratto in una colonna satin utilizzando un effetto di percorso attivo. Ciò lo rende più adattabile in termini di larghezza e forma rispetto a una normale colonna satin.

**Evita gli angoli acuti.** Come per i normali satin, è meglio dividere il percorso negli angoli acuti. In alcuni casi, potrebbe essere necessario allungare i nodi o aggiungere più nodi per ottenere una larghezza coerente.
{: .notice--warning }

### Utilizzo

1. Seleziona un tratto o un effetto di percorso attivo satin.
2. Esegui `Extensions > Ink/Stitch > Strumenti: Satin > Conversione in satin tramite effetto di percorso attivo...`.
3. Imposta le dimensioni approssimative che desideri per il tuo satin.
4. Fai clic su "Applica".

### Opzioni

--|--
Pattern             | ![LPE-Patterns](/assets/images/docs/lpe_patterns.png) | Scelta del pattern da applicare ripetutamente alla colonna satin.
Larghezza minima (mm) | ![Min width](/assets/images/docs/lpe_min_width.png)   | Larghezza del pattern nel punto più stretto.
Larghezza massima (mm) | ![Max width](/assets/images/docs/lpe_max_width.png)   | Larghezza del pattern nel punto più ampio.
Lunghezza del pattern (mm) | ![Length](/assets/images/docs/lpe_length.png)         | Lunghezza del pattern.
Allungato           | ![Stretched](/assets/images/docs/lpe_stretched.png)   | Se selezionato, il pattern verrà allungato in modo che i pattern ripetuti occupino esattamente la lunghezza della linea; altrimenti, potrebbe esserci uno spazio alla fine della linea.
Aggiungi maglie           | ![Rungs](/assets/images/docs/lpe_rungs.png)           | Poiché i pattern (di solito) hanno tutti lo stesso numero di nodi su entrambe le guide, le maglie sono facoltative.
Specifico del percorso       |                                                       | ● Se selezionato, la colonna satin ha il proprio pattern. Una modifica di qualsiasi opzione influisce solo su questa colonna. È possibile applicare trasformazioni dell'elemento.<br>● Se non selezionato, il pattern è comune a tutte le colonne satin che utilizzano questo effetto e pattern. La modifica del pattern per uno di essi lo modifica per tutti. Le trasformazioni dell'elemento potrebbero portare a una larghezza di colonna inaspettata.

### Aggiorna e modifica il pattern

Ora puoi modificare il pattern nei seguenti modi.

* Aggiorna il percorso come qualsiasi altro percorso in Inkscape con lo strumento nodo.
* Modifica il pattern aprendo il dialogo degli effetti del percorso (`Percorso > Effetti del percorso`).
  * Allarga o stringi il pattern manipolando l'impostazione "larghezza".
  * Modifica l'elemento del pattern facendo clic su "Modifica su tela" nell'impostazione "origine del pattern".

    ![modifica su tela](/assets/images/tutorials/pattern-along-path/edit.png)
* Modifica il pattern eseguendo di nuovo questo strumento.
* Convertilo in un percorso normale (`Shift + Ctrl + C`) e rifinisci il percorso manualmente (a quel punto perderà la funzionalità dell'effetto di percorso).

### Applica effetto di percorso

Utilizza `Percorso > Oggetto a percorso` per convertire questo in una normale colonna satin.

## Riga a zigzag in satin

Quando tracci un pattern manualmente, questo strumento può essere utile per eseguirlo in un'unica operazione.
Invece di disegnare prima le due guide e poi più maglie, questo strumento consente di disegnare una linea quadrata o a zigzag che può quindi essere convertita in uno stile di colonna satin.

### Utilizzo

* Disegna la tua forma con lo stile di pattern preferito.
* Seleziona la forma ed esegui `Extensions > Ink/Stitch > Strumenti: Satin > Riga a zigzag in satin`.
  * Seleziona lo stile del tuo pattern (pattern).
  * Scegli se la linea risultante deve essere smussata o con linee rette.
  * Scegli se inserire o meno delle maglie. La linea risultante avrà sempre lo stesso numero di nodi su entrambe le guide.

### Stili di pattern

* Tutti i pattern iniziano e terminano con una maglia.
* Per lo stile di pattern **quadrato (1)** e **a denti di sega (2)**, disegna una maglia dopo l'altra.
* Lo stile **a zigzag (3)** crea maglie da ogni picco su ciascuna guida al punto medio tra i picchi dell'altra guida.

![Pattern della linea a zigzag](/assets/images/docs/zigzag-line-to-satin.png)

Se vedi qualcosa di simile all'immagine sottostante, è molto probabile che tu abbia scelto lo stile di pattern sbagliato per la configurazione del tuo tratto.

![Linea a zigzag pattern sbagliato](/assets/images/docs/zigzag-line-to-satin-wrong-pattern.png)

### Bordi netti con opzione di smussatura attivata

Quando utilizzi l'opzione di smussatura, è comunque possibile creare rapidamente bordi più netti (si prega di essere ragionevoli in termini di regole della colonna satin).

I bordi netti sono indicati da due punti vicini.

## Tutorial sull'utilizzo degli strumenti: Satin

{% include tutorials/tutorial_list key="tool" value="Satin" %}