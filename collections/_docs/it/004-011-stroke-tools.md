---
title: "Strumenti: Tracciato"
permalink: /docs/stroke-tools/
last_modified_at: 2026-06-19
toc: true
---
## Autorouting del Punto Filza

Questo strumento **sostituirà** il tuo set di punti filza con un nuovo set di punti filza in un ordine logico, evitando il maggior numero possibile di salti. Saranno aggiunti dei percorsi secondari, se necessario. I punti filza risultanti manterranno tutti i parametri impostati sui punti originali, inclusa la lunghezza del punto, il numero di ripetizioni, il numero di ripetizioni del punto a "fagiolo", ecc. I percorsi secondari manterranno solo la lunghezza del punto, ma saranno impostati per avere una sola ripetizione e nessun numero di ripetizioni del punto a "fagiolo".

### Utilizzo

- Seleziona tutti i punti filza (preparati con i parametri) che desideri organizzare.
- Esegui `Estensioni > Ink/Stitch > Strumenti: Tracciato > Autorouting del punto filza...`
- Abilita le opzioni desiderate e fai clic su "Applica".

Suggerimento: per impostazione predefinita, verrà scelto il nodo più a sinistra come punto di partenza e il nodo più a destra come punto di fine (anche se questi non sono nodi terminali). Puoi sovrascrivere questo comportamento collegando i comandi "Posizione di inizio/fine per l'autorouting del punto filza".
{: .notice--info }

### Opzioni

- Abilitare **Aggiungi nodi alle intersezioni** di solito produce un routing migliore, poiché i percorsi secondari iniziano/terminano preferenzialmente alle intersezioni e ai nodi terminali. Dovresti disabilitare questa opzione solo se hai aggiunto manualmente dei nodi dove desideri che i percorsi siano suddivisi.
- Abilita **Sostituisci i salti con tagli** per utilizzare dei tagli invece dei salti. I comandi di taglio vengono aggiunti al file SVG, quindi puoi modificarli/eliminarli come preferisci.
- Abilita **Mantieni l'ordine dei punti filza** se preferisci mantenere l'ordine precedente.

## Conversione da Satin a Tracciato

La conversione da satin a tracciato convertirà una colonna di satin nella sua linea centrale. Questo può essere utile quando decidi, in un secondo momento del processo di progettazione, di trasformare una colonna di satin in un punto filza. Puoi anche usarlo per modificare lo spessore della tua colonna di satin, quando la compensazione del tiraggio non è sufficiente. In questo caso, utilizza questa funzione per convertire la tua colonna di satin in un punto filza, imposta la larghezza del tratto nel pannello di riempimento e del tratto e esegui la funzione ["Converti linea in satin"](/docs/satin-tools/#convert-line-to-satin).

Questo funziona meglio con colonne di satin uniformemente spaziate.

![Esempio di conversione da satin a tracciato](/assets/images/docs/en/satin_to_stroke.png)

### Utilizzo

1. Seleziona la/le colonna/e di satin che desideri convertire in un punto filza.
2. Esegui `Estensioni > Ink/Stitch > Strumenti: Tracciato > Conversione da satin a tracciato...`
3. Scegli se desideri mantenere la/le colonna/e di satin selezionata/e o se desideri sostituirle.
4. Fai clic su "Applica".

## Riempimento a Tracciato

Le sagome riempite non hanno mai un bell'aspetto quando ricamate, ma è molto lavoro convertire una sagoma riempita in una colonna di satin o in un punto filza. Questo strumento ti aiuta in questa operazione.

È paragonabile alla funzionalità di Inkscape di `Percorso > Traccia bitmap > Tracciamento della linea centrale` (e presenta problemi simili). Ma invece di convertire immagini raster, troverà la linea centrale di oggetti vettoriali con un riempimento.

Puoi migliorare il risultato definendo delle linee di taglio.

![Riempimento a tracciato](/assets/images/docs/en/fill_to_stroke.png)

### Utilizzo

* (Facoltativo) Disegna delle linee di taglio alle intersezioni/giunzioni. Sono semplici elementi di tratto. Questo è particolarmente utile quando si mirano a colonne di satin. Si prega di notare che ogni elemento di tratto deve tagliare l'elemento di riempimento in modo che ogni lato del riempimento sia completamente disconnesso.
* Seleziona uno o più oggetti riempiti che desideri convertire in una linea centrale, insieme alle linee di taglio, se le hai definite in precedenza.
* Esegui `Estensioni > Ink/Stitch > Strumenti: Tracciato > Riempimento a tracciato`
* Imposta le opzioni e applica
* Utilizza lo strumento nodo per eseguire eventuali correzioni necessarie.

### Opzioni

* Mantieni l'originale: abilita questa opzione se desideri mantenere l'oggetto/gli oggetti originale/i. Altrimenti, verranno rimossi.
* Soglia per i punti morti (px): questo rimuove le linee più piccole. Nella maggior parte dei casi, il valore migliore è la larghezza approssimativa della linea dell'oggetto originale in pixel.
* Linea tratteggiata: imposta su "vero" se desideri ottenere un punto filza per il contorno.
* Larghezza della linea (px): se desideri convertire direttamente in una colonna di satin, imposta questo valore sulla larghezza della colonna di satin. Nella maggior parte dei casi, vorrai mantenere questo valore basso, in modo che sia più facile controllare e correggere i contorni prima della conversione.
* Linee di taglio: chiudi gli spazi: le linee di taglio creano degli spazi che possono essere chiusi abilitando questa opzione. Questa opzione sarà utile solo se non è prevista una conversione in colonna di satin.

## Salto a Tracciato

Questo creerà un punto filza dalla posizione finale del primo elemento alla posizione iniziale del secondo elemento. Posiziona questo punto filza sotto i punti superiori e evita i salti.

### Utilizzo

* Seleziona due o più oggetti.
* Esegui `Estensioni > Ink/Stitch > Strumenti: Tracciato > Salto a tracciato`

### Opzioni

* Converti i salti più lunghi di (mm): un valore di 0 imposta di default la lunghezza minima del punto filza.
* Converti i salti più corti di (mm): un valore di 0 significa che non c'è limite di dimensione.
* Connetti solo all'interno di gruppi o livelli
* Non connettere dopo taglio, stop o punti di blocco forzati

### Impostazioni di output
* Unisci i nuovi tratti con il tratto precedente/successivo se dello stesso tipo
* Unisci i sottopercorsi

e per le connessioni non unite solo
* Lunghezza minima del punto filza
* Tolleranza

## Redwork

Il redwork è un antico metodo di ricamo a mano in cui i ricamatrici si assicuravano di cucire ogni linea esattamente due volte.

Questo strumento **sostituirà** il tuo set di punti filza con un nuovo set di punti filza in un ordine logico.
La principale differenza con il `Autorouting del punto filza` è che garantisce che i percorsi vengano percorsi esattamente due volte.

### Utilizzo

* Seleziona i punti filza che desideri tracciare.
* Esegui `Estensioni > Ink/Stitch > Strumenti: Tracciato > Redwork...`
* Imposta le opzioni desiderate e fai clic su "Applica".

### Opzioni

* Collega le linee a una distanza inferiore a (mm)

L'estensione redwork è in grado di rendere gruppi disconnessi di punti filza in un'unica operazione.
D'altra parte, alcune delle tue linee potrebbero non essere collegate, il che lascia piccoli spazi.
Con questa opzione, puoi definire fino a quale distanza questi spazi devono essere eliminati.
Le linee con una distanza maggiore di questo valore verranno considerate disconnesse.
I gruppi disconnessi hanno punti di salto tra di loro.
* Lunghezza minima del percorso (mm)

Rimuovi i percorsi più corti di questo valore dal risultato.
I percorsi più brevi possono essere il risultato dell'operazione di routing (ad esempio, linee che non sono collegate, ma hanno una sovrapposizione minima).
I percorsi più corti della [lunghezza minima del punto filza](/docs/preferences/#minimum-jump-stitch-length-mm) definiti possono di solito essere rimossi.
Ma se ci sono percorsi consecutivi più corti, sarà meglio abbassare il valore.
* Lunghezza del punto redwork (mm)

Imposta la lunghezza del punto per tutti i percorsi risultanti.
* Numero di ripetizioni del punto a "fagiolo" redwork

Imposta il [numero di ripetizioni del punto a "fagiolo"](/docs/stitches/bean-stitch/) per i punti dello strato superiore (non sui percorsi secondari).

* Ordina per colore: lavora con ogni colore in modo indipendente
* Combina elementi: combina elementi consecutivi dello stesso tipo
* Mantieni i percorsi originali: indica se eliminare o meno gli elementi originali

### Posizione di inizio e fine

Il redwork inizia e termina sempre nello stesso punto. Tuttavia, puoi definire questo punto con un [comando di posizione di inizio/fine per l'autorouting del punto filza](/docs/commands/#--startingending-position-for-auto-route-of-running-stitch).

## Outline

Questa estensione aiuta a ricostruire un oggetto originale quando si ha solo il file di cucito, ma non il file di progettazione SVG.

### Utilizzo

- Seleziona uno o più oggetti.
- Esegui `Estensioni > Ink/Stitch > Strumenti: Tracciato > Outline...`
- Attiva l'anteprima in tempo reale per vedere il risultato effettivo.
- Regola le impostazioni finché non sei soddisfatto del risultato.
- Fai clic su "Applica".

![Percorso di cucito a outline](/assets/images/docs/outline.png)

## Tutorial sull'utilizzo di Strumenti: Tracciato

{% include tutorials/tutorial_list key="tool" value="Stroke" %}