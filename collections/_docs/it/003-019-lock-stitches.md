---
title: "Punti di Blocco e di Fissaggio"
permalink: /docs/stitches/lock-stitches/
last_modified_at: 2024-09-01
toc: true
---
## Descrizione

I punti di blocco e di fissaggio sono piccoli punti all'inizio (fissaggio) o alla fine (blocco) di un blocco di colore o prima e dopo i punti di salto o i comandi di taglio. Aiutano a fissare il filo.

## Fattori Influenzanti (Quando si Applicano i Punti di Blocco)

Il file di ricamo contiene diversi oggetti di ricamo che verranno ricamati uno dopo l'altro. I punti di blocco vengono impostati quando, tra gli oggetti, c'è un cambio di colore, un comando di taglio o una distanza elevata. L'opzione "Consenti punti di blocco" può impedire l'uso dei punti di blocco, mentre "Forza punti di blocco" assicurerà che siano presenti.

### Lunghezza Minima del Punto di Salto

La lunghezza minima del punto di salto può essere impostata in `Estensione > Ink/Stitch > Preferenze` e in base all'oggetto nel dialogo dei parametri.

Definisce se il punto tra due oggetti è un punto di salto o un punto normale.
Solo se la distanza tra due oggetti è maggiore del valore di "lunghezza minima del punto di salto", viene applicato un punto di salto. Solo se viene utilizzato un punto di salto, vengono aggiunti punti di blocco alla fine del primo oggetto e punti di fissaggio all'inizio del secondo oggetto.

![Tre linee, la prima distanza è di 1 mm, la seconda distanza è di 3 mm, la lunghezza minima del punto di salto è impostata su 2. Non ci sono punti di blocco nel primo oggetto e non ci sono punti di fissaggio nel secondo](/assets/images/docs/lock_stitch_min_jump.svg)
{: .border-shadow }

Tuttavia, ci sono altri parametri che possono influenzare se i punti di blocco e di fissaggio vengono applicati.

### Cambi di Colore

I punti di blocco e di fissaggio vengono applicati prima e dopo un cambio di colore.

### Comandi di Taglio

Ink/Stitch inserisce punti di blocco nell'oggetto con il comando di taglio e punti di fissaggio nel successivo.

![Tre linee, le distanze sono di 1 mm, la lunghezza minima del punto di salto è impostata su 2. La linea centrale ha un comando di taglio che imposta un punto di blocco su di essa e un punto di fissaggio sull'oggetto successivo](/assets/images/docs/lock_stitch_trim.svg)
{: .border-shadow }

I comandi di taglio possono essere applicati con due metodi diversi:

*   utilizzando il comando `Estensione > Ink/Stitch > Comandi > Associa i comandi agli oggetti selezionati`
*   oppure selezionando "Taglia dopo" nel dialogo dei parametri.

### Consenti Punti di Blocco

L'opzione "Consenti punti di blocco" può sopprimere i punti di blocco e/o di fissaggio quando normalmente dovrebbero essere applicati.
{: .notice--info }

![Tre linee, le distanze sono di 3 mm, la lunghezza minima del punto di salto è impostata su 2. La linea centrale è impostata per consentire i punti di blocco solo alla fine. Pertanto, non ha punti di fissaggio](/assets/images/docs/lock_stitch_allow.svg)
{: .border-shadow }

Il parametro "consenti punti di blocco" può impedire i punti di blocco prima o dopo l'oggetto (o entrambi). Quindi, quando la distanza tra due oggetti è sufficientemente grande per un punto di salto, ma il primo oggetto ha impostato il parametro "consenti punti di blocco" su "Prima", non verranno impostati punti di blocco alla fine di questo oggetto.

### Forza Punti di Blocco

Tuttavia, è possibile forzare i punti di blocco e di fissaggio anche per gli oggetti con piccole distanze. Seleziona il parametro "forza punto di blocco" del primo oggetto per aggiungere punti di blocco prima del salto e punti di fissaggio dopo il salto (sul secondo oggetto).

![Tre linee, le distanze sono di 1 mm, la lunghezza minima del punto di salto è impostata su 2. La linea centrale ha un'impostazione di salto forzato, che imposta un punto di blocco su di essa e un punto di fissaggio sul successivo](/assets/images/docs/lock_stitch_force.svg)
{: .border-shadow }

Fai attenzione a non selezionare "forza punto di blocco" sul secondo oggetto, altrimenti forzeresti i "punti di blocco" per esso, non i "punti di fissaggio", e inoltre forzeresti i punti di blocco per l'oggetto successivo, indipendentemente dalla sua distanza dall'oggetto dopo il salto.

L'opzione "forza punti di blocco" applica sempre i punti di blocco e sovrascrive il parametro "consenti punti di blocco".
{: .notice--info }

## Tipi di Punto di Blocco

Ink/Stitch offre vari tipi di punti di blocco e di fissaggio e consente anche di definirne di personalizzati.

### Punti di Blocco Predefiniti

![Varianti del punto di blocco](/assets/images/docs/lock-stitches.png)
{: .img-half }

1.  Mezzo punto. Questo è il valore predefinito e l'unico punto di blocco disponibile nelle versioni precedenti di Ink/Stitch. Non ha opzioni di ridimensionamento, ma è relativo alla lunghezza del punto: due mezzi punti all'indietro e due mezzi punti in avanti.
2.  Freccia, scala in percentuale.
3.  Avanti e indietro, scala in mm.
4.  Farfalla, scala in percentuale.
5.  Croce, scala in percentuale.
6.  Stella, scala in percentuale.
7.  Triangolo, scala in percentuale.
8.  Zigzag, scala in percentuale.
9.  Personalizzato. Scala in percentuale o in mm a seconda del tipo di percorso.

### Punti di blocco personalizzati

I punti di blocco personalizzati possono essere definiti tramite un percorso SVG in unità mm (scala: percentuale) o con unità relative di passi da fare avanti e indietro (scala: mm).

#### Percorso SVG personalizzato

Il percorso SVG viene sempre creato come se fosse un punto di fissaggio (inizio) e un punto di blocco (fine), se posizionato alla fine verrà invertito.

Alla fine del percorso SVG c'è un nodo aggiuntivo per indicare l'angolo con cui il percorso si connette al punto di blocco. Questo nodo verrà rimosso quando l'angolo sarà stato elaborato.

Ad esempio, il punto di blocco a forma di triangolo corrisponde al percorso personalizzato M -0.26,0.33 H 0.55 L 0,0.84 V 0 L 0.34,0.82 (questo è l'attributo d del percorso).
Nell'immagine successiva, questi sono i percorsi neri, in una copia l'ultimo segmento è colorato di verde per maggiore chiarezza.

![Punto di blocco a forma di triangolo](/assets/images/docs/triangle_lock.png)

Sia il percorso rosso che quello blu hanno un punto di fissaggio a forma di triangolo rivolto verso il basso.

Il percorso SVG personalizzato viene ruotato in modo tale che il suo ultimo segmento (verde) abbia la stessa direzione dell'inizio dei percorsi rosso e blu. Viene utilizzato solo per calcolare l'angolo di rotazione e non fa parte del punto di fissaggio effettivo e non verrà ricamato.

#### Percorso mm personalizzato

I valori mm personalizzati sono separati da uno spazio. Ad esempio, un punto di blocco personalizzato con un valore di percorso di 1 1 -1 -1 con un'impostazione di scala di 0,7 mm si sposterà di 0,7 mm in avanti (due volte) e di 0,7 mm all'indietro (due volte). I valori del percorso possono essere anche decimali (ad esempio 0.5 2.2 -0.5 -2.2) se l'utente desidera percorrere solo frazioni della dimensione dell'impostazione.
