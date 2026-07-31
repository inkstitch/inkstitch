---
title: "Ricamo a Croce"
permalink: /docs/stitches/cross-stitch/
last_modified_at: 2026-03-27
toc: true

feature_row:
  - image_path: /assets/images/docs/cross_stitch_coverage.jpg
    alt: "Griglia del ricamo a croce con un riempimento. Le aree coperte dal riempimento per più del 50% mostrano una croce in superficie."
  - image_path: /assets/images/docs/cross_stitch_coverage02.jpg
    alt: "Stessa immagine di prima, ma l'elemento di riempimento si è spostato. Vengono create più croci."
---

{% include upcoming_release.html %}

## Descrizione

Il ricamo a croce imita le tecniche tradizionali di ricamo a mano.
Il ricamo a croce è caratterizzato da piccole croci regolari, che conferiscono all'immagine ricamata un aspetto piatto e squadrato.

{% include folder-galleries path="butterfly-fill-project/cross/" captions="1: Ricamo a croce con contorno a punto di semi." %}

[<i class="fa fa-download"></i> Scarica i file di esempio](/assets/images/stitch-type-butterflies/cross_stitch.zip)

## Creazione

* Disegna una forma chiusa con un colore di riempimento.
* Apri la finestra di dialogo dei parametri.
* Seleziona "Ricamo a croce" come metodo di riempimento.

### Griglie e il Parametro di Copertura

È importante comprendere il parametro di "copertura" del ricamo a croce.

Il parametro di copertura definisce la percentuale di sovrapposizione per ogni croce rispetto all'area di riempimento. Ciò significa che influenza se una croce venga creata in un punto specifico o meno.

Le croci sono allineate a una griglia nella dimensione del motivo. La griglia stessa è (per impostazione predefinita) allineata all'angolo in alto a sinistra della tela.

Ink/Stitch verifica quale percentuale di ogni campo della griglia è coperta dall'elemento di riempimento.
Se la copertura supera il valore specificato nell'opzione di copertura (per impostazione predefinita, 50%), viene creata una croce.

Nell'esempio seguente, solo i campi verdi sono coperti per più del 50% dal riempimento nero e ricevono una croce.
Quando l'elemento di riempimento nero viene spostato sulla tela, vengono create più croci.

{% include feature_row %}

Quando l'opzione "Allinea la griglia alla tela" è disabilitata, l'elemento può essere spostato sulla tela senza modificare il risultato del ricamo a croce.
Tuttavia, le aree adiacenti di ricamo a croce potrebbero essere disallineate.
{: .notice--info }

### Metodo del Ricamo a Croce

In Ink/Stitch, puoi scegliere tra vari metodi di ricamo a croce.

* **Ricamo a croce e ricamo a croce invertito**

  Questo è il metodo più comune. Due diagonali formano una croce.
  Quando due croci sono collegate solo diagonalmente, aggiungi un piccolo valore di espansione al riempimento sottostante per garantire una cucitura combinata.

  ![Metodo del ricamo a croce: ricamo a croce](/assets/images/docs/cross_stitch_method_cross_stitch.jpg)
* **Mezza cucitura e mezza cucitura invertita**

  Le mezze cuciture creano solo una metà della croce (una diagonale), seguendo il contorno della forma.

  ![Metodo del ricamo a croce: mezza croce](/assets/images/docs/cross_stitch_method_half_cross.jpg)
* **Croce verticale e croce verticale invertita**

  Una croce ruotata, che crea una croce verticale.
  Tieni presente che questo metodo di ricamo a croce potrebbe causare salti quando le aree sono collegate solo diagonalmente.

  ![Metodo del ricamo a croce: croce verticale](/assets/images/docs/cross_stitch_method_upright.jpg)

* **Croce verticale densa e croce verticale densa invertita**

  Vengono utilizzate più croci verticali per riempire la forma.

  La copertura è impostata al 50% in questo esempio.

  ![Metodo del ricamo a croce: croce verticale densa](/assets/images/docs/cross_stitch_method_dense_upright.jpg)
* **Croce doppia e croce doppia invertita**

  Una combinazione di ricamo a croce e cucitura verticale, con la croce verticale nella parte inferiore.
  
  ![Metodo del ricamo a croce: croce doppia](/assets/images/docs/cross_stitch_method_double_cross.jpg)

* **Croce smyrna e croce smyrna invertita**

  Una combinazione di ricamo a croce e cucitura verticale, con la croce verticale nella parte superiore.
  
  ![Metodo del ricamo a croce: croce smyrna](/assets/images/docs/cross_stitch_method_smyrna.jpg)

### Assistente del Ricamo a Croce

Ink/Stitch include un'estensione che ti aiuta a eseguire attività specifiche per il ricamo a croce contemporaneamente.

* Imposta una griglia per l'allineamento del ricamo a croce (e supporto visivo durante il lavoro sul ricamo a croce).
* Applica i parametri del ricamo a croce agli elementi selezionati.
* Pixelizza e combina il contorno degli elementi selezionati, per evitare punti di cucitura e ottenere una migliore rappresentazione del posizionamento del ricamo a croce.
* Converti immagini bitmap in elementi di riempimento per il ricamo a croce.

Calcola e visualizza anche la lunghezza del punto in base alle dimensioni della griglia. La lunghezza massima del punto nei parametri del ricamo a croce deve essere maggiore di questo valore.

[Leggi di più](/docs/fill-tools/#cross-stitch-assistant)

### Imposta il Punto di Inizio e di Fine

Per impostazione predefinita, un riempimento automatico inizia il più vicino possibile all'elemento di ricamo precedente e termina il più vicino possibile all'elemento di ricamo successivo.

Per modificare questo comportamento, imposta i punti di inizio e di fine per gli oggetti di riempimento automatico utilizzando i [comandi visivi](/docs/commands/).

## Parametri

Esegui `Estensioni > Ink/Stitch > Parametri` per regolare le impostazioni in base alle tue esigenze.

{% include params.html stitch_type='cross_stitch'%}

## File di Esempio che Includono il Ricamo a Croce

{% include tutorials/tutorial_list key="stitch-type" value="Ricamo a Croce" %}