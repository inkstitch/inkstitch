---
title: "Suggerimenti per Inkscape"
permalink: /docs/inkscape-tips/
last_modified_at: 2023-04-30
toc: true
---

## Basi di Inkscape
Questi sono i concetti fondamentali che dovresti comprendere per utilizzare Ink/Stitch. Se non hai mai utilizzato Inkscape prima, ti consigliamo di seguire un tutorial di Inkscape prima di utilizzare Ink/Stitch.

* Sono disponibili diversi tutorial interattivi all'interno di Inkscape stesso, selezionando `Aiuto > Tutorial` nel menu, incluso il tutorial di base riportato di seguito.
* [Tutorial di base su inkscape.org](https://inkscape.org/doc/tutorials/basic/tutorial-basic.html) - Panoramica rapida degli strumenti e dei comandi più comuni.
* [Anatomia della finestra di Inkscape su tavmjong.free.fr](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Anatomy.html) - Schema delle parti della finestra di Inkscape.
* [Tutorial sull'interfaccia di Roy Torley](https://roy-torley.github.io/Inkscape_Tutorial/Tutorial01/Tutorial01.html) - Un'altra panoramica dell'interfaccia e della navigazione.
* [Basi su tavmjong.free.fr](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Basics.html) - Ulteriori dettagli su come manipolare gli oggetti.

### Vettori

Gli elementi all'interno del tuo file Inkscape sono _immagini vettoriali_, che utilizzano equazioni matematiche per definire le forme. Sono composti da punti chiamati _nodi_ e da _segmenti_ che collegano i nodi. Puoi modificare le forme vettoriali spostando i nodi e modificando gli angoli dei segmenti con lo Strumento Nodi, oppure utilizzando gli altri strumenti di Inkscape. Quando utilizzi gli altri strumenti, come allungare una forma con lo Strumento Selezione, Inkscape sta effettivamente modificando molti nodi contemporaneamente in background.

Una forma vettoriale è _chiusa_ quando forma un ciclo completo (come un cerchio o un quadrato) e ogni nodo è collegato a altri due nodi. Una forma è _aperta_ quando ha due estremità libere che non sono collegate (come una spirale o una linea retta). Il contorno di una forma è chiamato _tratto_ e l'area all'interno di una forma chiusa è chiamata _riempimento_.

[Leggi di più su come funzionano i vettori su Sketchpad.net](http://sketchpad.net/drawing1.htm)

### Disegno e Selezione
Le icone sul lato sinistro della finestra mostrano tutti gli strumenti per creare e interagire con il tuo progetto. Inkscape ha diversi strumenti per creare diversi tipi di oggetti, come lo Strumento Rettangolo (`F4`), lo Strumento Ellisse (`F5`), lo Strumento Stella (`*`), lo Strumento Spirale (`F9`), lo Strumento Matita (`F6`) e lo Strumento Testo (`F8`). La maggior parte di essi viene utilizzata trascinando sulla tela dove desideri posizionare gli angoli della tua forma. Ogni strumento di disegno ha opzioni univoche (mostrate nella barra di controllo dello strumento sopra la tela) con cui puoi sperimentare per ottenere risultati diversi. Scopri di più su come creare [Forme](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Shapes.html), [Percorsi](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths.html) o [Testo](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Text.html) tramite questi link.

L'icona superiore nel pannello della Cassetta degli Strumenti è lo Strumento Selezione, che puoi anche attivare premendo `F1`. Clicca su un oggetto con lo Strumento Selezione per trascinarlo sulla tela e per visualizzare le maniglie per la trasformazione. Cliccando sull'oggetto una volta vengono mostrate le maniglie per il ridimensionamento, e cliccandolo una seconda volta si passa alle maniglie per la rotazione. Tieni premuto `Shift` per selezionare più oggetti contemporaneamente. Puoi anche selezionare molti oggetti trascinando su di essi. [Scopri di più su come trasformare gli oggetti qui.](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Transforms.html)

Un altro modo per selezionare gli oggetti è aprire il pannello Livelli e Oggetti (`Oggetto > Livelli e Oggetti...` nel menu) e fare clic su un nome nell'elenco. Puoi selezionare gli oggetti in questo modo indipendentemente dallo strumento attivo.

Per utilizzare un comando di menu su un oggetto (ad esempio, per convertirlo in un percorso), devi prima selezionare l'oggetto.

### Oggetti e Percorsi
Un _oggetto_ è qualsiasi parte del tuo file che puoi manipolare individualmente. Puoi vedere un elenco di tutti gli oggetti nel tuo file selezionando `Oggetto > Oggetti...` nel menu. Conoscere come sono definiti i tuoi oggetti è molto importante per i tuoi file di ricamo, quindi è una buona idea tenere aperta questa finestra quando lavori con Ink/Stitch.

Ci sono molti tipi di oggetti in Inkscape, come percorsi, rettangoli, cerchi, poligoni, spirali e testo. Diversi strumenti creano diversi tipi di oggetti, ciascuno con regole diverse su come interagire con essi.

Un _percorso_ è la rappresentazione più basilare di una forma vettoriale: è solo una serie di nodi e segmenti che descrivono la forma. Una volta creato un percorso, puoi utilizzare solo strumenti di base per modificarlo, e funziona allo stesso modo indipendentemente dall'aspetto del percorso. Altri tipi di oggetti memorizzano le informazioni sulla forma in un modo più specifico che consente di modificarla facilmente. Ad esempio, dopo aver disegnato un oggetto poligono con lo Strumento Stella, puoi utilizzare i controlli dello strumento per modificare rapidamente il numero di angoli della forma. Se avessi disegnato la stessa forma come un percorso, dovresti spostare manualmente ogni punto per aggiungere più angoli. Tuttavia, i percorsi possono essere trasformati in qualsiasi forma desideri, mentre altri tipi di oggetti hanno delle limitazioni sulla loro forma.

Ink/Stitch può funzionare con tutti i tipi di oggetti, ma il testo deve essere convertito in oggetto.

Puoi convertire qualsiasi oggetto in un percorso selezionando l'oggetto (cliccandolo con lo Strumento Selezione o cliccando sul suo nome nel pannello Oggetti) e quindi premendo `Shift + Ctrl + C` o selezionando `Percorso > Oggetto in Percorso` nel menu. Una volta diventato un percorso, puoi utilizzare lo Strumento Nodi per apportare modifiche precise ai punti e alle curve.

Fai attenzione quando converti gli oggetti in percorsi, perché non è possibile convertire i percorsi in oggetti. Per questo motivo, potresti voler duplicare prima il tuo oggetto e convertire la copia in un percorso, salvando la forma originale nel caso in cui decida di modificarla in seguito.

Gli oggetti speciali sono utili per:
* Testo o forme geometriche semplici
* Modificare la geometria di un'intera forma
* Punto di partenza per un nuovo progetto

I percorsi sono utili per:
* Apportare modifiche precise a una piccola sezione di una forma
* Disegnare forme a mano libera uniche
* Preparare il tuo progetto finito per il ricamo

Puoi controllare il tipo di un oggetto nella descrizione che appare nella barra di stato nella parte inferiore dello schermo quando è selezionato. Tieni presente che _non_ puoi capire se qualcosa è un percorso guardando il suo nome nel pannello Oggetti, perché Inkscape assegna nomi come "path1234" a cerchi e spirali, oltre che a percorsi effettivi.

### Tratto e Riempimento
Fai apparire il pannello Riempimento e Tratto premendo `Shift+Ctrl+F` o selezionando `Oggetto > Riempimento e Tratto...` dal menu per controllare il colore e lo stile del riempimento e del tratto di un percorso. Il colore e lo stile esatti del tuo percorso sono per lo più irrilevanti per il file di ricamo, ma devi sapere come modificarli perché Ink/Stitch utilizza lo stile del tratto per determinare il tipo di punto da utilizzare e inserisce richieste di cambio di filo in base al fatto che i percorsi abbiano lo stesso colore.

Questo pannello è piuttosto intuitivo. Per i percorsi che Ink/Stitch trasformerà in aree di cucitura in riempimento, la scheda Riempimento deve essere impostata su "colore piano" (secondo quadrato) e la scheda Pittura del Tratto deve avere la X selezionata (primo quadrato). Per tutti gli altri tipi di cucitura, seleziona la X sulla scheda Riempimento e seleziona "colore piano" sulla scheda Pittura del Tratto. Utilizza la scheda Stile del Tratto per scegliere un tratto solido o tratteggiato, a seconda del tipo di cucitura che desideri.

Il colore può essere impostato anche utilizzando la tavolozza nella parte inferiore dello schermo; fai clic su un colore per utilizzarlo per il riempimento o fai shift-clic per utilizzarlo per il tratto.

### Lavorare con i Percorsi
Usa il secondo strumento dall'alto, lo Strumento Nodi (attivato anche con `F2`), per modificare direttamente i punti e le linee di un percorso. Seleziona un percorso con lo Strumento Nodi per visualizzare i marcatori su tutti i suoi nodi. Questi marcatori di nodo possono quindi essere trascinati con il cursore, aggiunti, rimossi e altro ancora. Vedrai anche delle maniglie che si estendono da ogni nodo, che puoi trascinare per regolare gli angoli dei segmenti di linea. Questo strumento funziona solo su oggetti _percorso_, come spiegato di seguito: se non vedi apparire dei punti grigi lungo l'oggetto dopo averlo selezionato, significa che non è un percorso. [Scopri di più sullo Strumento Nodi qui.](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-Editing.html)

Due comandi importanti quando si preparano i percorsi per Ink/Stitch sono Combina (`Ctrl+K` o `Percorso > Combina`) e Separa (`Shift+Ctrl+K` o `Percorso > Separa`). Ad esempio, la creazione di colonne in satin in Ink/Stitch richiede due linee che vengono combinate in un unico percorso. Questi comandi non apportano modifiche alla forma effettiva o ai nodi all'interno di un percorso; invece, modificano il modo in cui Inkscape lo classifica.

Il comando _Combina_ prende tutti i percorsi attualmente selezionati e li unisce in un singolo percorso. Inkscape tratterà quindi quei percorsi come un'unità singola per la selezione e la trasformazione. Puoi vedere che l'elenco contiene un numero inferiore di oggetti dopo una combinazione. Il risultato della combinazione è un _percorso composto_, che contiene più linee.

Il comando _Separa_ prende un percorso composto e isola ogni linea continua in un oggetto separato. Divide il percorso composto nel maggior numero possibile di percorsi separati senza eliminare alcun segmento. Dopo aver utilizzato Separa, l'elenco Oggetti sarà più lungo.

Esistono altri comandi per combinare o dividere i nodi effettivi in un percorso, in un modo che modifica effettivamente la forma stessa invece di modificare solo il modo in cui Inkscape lo gestisce. [Leggi le operazioni sui percorsi qui.](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-Combining.html)

### Livelli
Tutti gli oggetti in Inkscape sono impilati l'uno sull'altro in un ordine specifico. Ink/Stitch utilizzerà questo ordine per determinare cosa deve essere cucito per primo. Puoi visualizzare l'ordine nel pannello Oggetti (`Oggetto > Oggetti...` nel menu). Ink/Stitch trasforma il percorso nella parte inferiore dell'elenco nella prima istruzione e procede verso l'alto nell'elenco. Puoi modificare l'ordine trascinando i nomi all'interno del pannello Oggetti, oppure premendo `Page Up` e `Page Down`.

Puoi fare doppio clic su un nome di oggetto per rinominarlo, il che può aiutarti a tenere traccia dei tuoi livelli. Vedrai anche tre icone a sinistra del nome di ogni oggetto in questo pannello. Fai clic sull'icona a forma di occhio per nascondere qualcosa dalla visualizzazione e fai clic sull'icona a forma di lucchetto per impedirne la modifica.

I _gruppi_ e i _livelli_ possono rendere più semplice la gestione dei tuoi oggetti e del loro ordine. Una volta formato un gruppo, fare clic su un elemento nel gruppo seleziona l'intero gruppo, consentendo di modificare tutti gli elementi del gruppo contemporaneamente. Per raggruppare oggetti, seleziona tutti gli oggetti con `Shift+clic`, quindi premi `Ctrl+G` o fai clic su `Oggetto > Gruppo`. Il gruppo appare anche come elemento espandibile nell'elenco Oggetti e gli oggetti possono essere spostati dentro e fuori dal gruppo (o da un gruppo all'altro) trascinandoli nel pannello Oggetti. Un gruppo può contenere altri gruppi. Tuttavia, il modo più sicuro sembra essere quello di `Modifica > Taglia` un oggetto da un gruppo e quindi `Modifica > Incolla` in un altro. Devi selezionare un oggetto nel gruppo di destinazione in modo che l'oggetto incollato vada in quel gruppo.

I livelli funzionano in modo simile ai gruppi, ma il loro scopo principale è quello di controllare più facilmente l'ordine dei tuoi oggetti. Un nuovo livello viene creato con il pulsante + sotto l'elenco Oggetti, oppure premendo `Shift+Ctrl+N`. Gli oggetti possono essere spostati da un livello all'altro trascinandoli nell'elenco Oggetti, proprio come i gruppi, ma possono anche essere spostati rapidamente nel livello superiore o inferiore premendo `Ctrl+Page Up` o `Ctrl+Page Down`.

[Leggi di più sui livelli nel tutorial di Roy Torley qui.](https://roy-torley.github.io/Inkscape_Tutorial/Tutorial06/Tutorial06.html)

## Tutorial generali di Inkscape
* [Tutorial sulle forme su inkscape.org](https://inkscape.org/doc/tutorials/shapes/tutorial-shapes.html) - Come disegnare e modificare oggetti a forma geometrica.
* [Tutorial avanzato su inkscape.org](https://inkscape.org/doc/tutorials/advanced/tutorial-advanced.html) - Disegno e modifica di percorsi e testo.
* [Indice della guida di Inkscape su tavmjong.free.fr](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/index.html) - Guida approfondita a tutti gli aspetti di Inkscape.
* [Tutorial di Inkscape di TJ Free su Youtube](https://www.youtube.com/playlist?list=PLqazFFzUAPc5lOQwDoZ4Dw2YSXtO7lWNv) - Serie di video tutorial che copre un'ampia gamma di usi.

## Tutorial specifici per strumenti

### Tracciamento di un'immagine
Puoi convertire un'immagine raster (come un JPEG o un PNG) in un percorso importando/incollando un'immagine, quindi utilizzando `Percorso > Traccia bitmap...`. Questo è un processo complicato che di solito richiede molti tentativi ed errori. Funziona meglio con immagini con bordi netti e pochi colori.
* [Tutorial sul tracciamento su inkscape.org](https://inkscape.org/doc/tutorials/tracing/tutorial-tracing.html)
* [Tutorial video di TJ Free su Youtube](https://www.youtube.com/watch?v=E7HwLTQu2FI)

### Modelli a mosaico

Crea modelli a mosaico con `Modifica > Clona > Crea cloni a mosaico...`.

Leggi di più sui [Mosaici su tavmjong.free.fr](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Tiles.html). Fai clic attraverso l'indice, dove troverai informazioni dettagliate su tutte le parti del dialogo di tiling.

### Strumenti di modifica del percorso
##### Ornamenti con Spiro
* [Come creare una spirale o un ornamento utilizzando Inkscape - Youtube](https://www.youtube.com/watch?v=YHddGNae3-c)

##### Forma Linea
* [Ellisse - Youtube](https://www.youtube.com/watch?v=TDI2ViYw4KY)
* [Personalizzato - Youtube](https://www.youtube.com/watch?v=wiqUrzzHszI)

### Strumento Tweak
* [Strumento Tweak (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Tweak.html)

### Strumento Spray
* [Strumento Spray (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Spray.html)

### Gomma
* [Gomma (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Eraser.html)

### Effetti del percorso attivi

* [Panoramica degli effetti del percorso attivi (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects.html)
* [Strumento di piegatura (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-BendTool.html)
* [Deformazione con busta (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-EnvelopeDeformation.html)
    ([Esempio video](https://www.youtube.com/watch?v=8XbIsw48vTk))
* [Interpolazione sottopercorsi (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-InterpolateSubPaths.html)
* [Modello lungo il percorso (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-PatternAlongPath.html)
    ([Esempio video](https://www.youtube.com/watch?v=3Bhg727wYMc))
* [Schizzo (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-Sketch.html)
* [Cucitura sottopercorsi (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-StitchSubPaths.html)
* [Ruvidità (Youtube)](https://www.youtube.com/watch?v=130Dbt0juvY)