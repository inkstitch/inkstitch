---
title: "Punto a Onda"
permalink: /docs/stitches/ripple-stitch/
last_modified_at: 2025-12-29
toc: true
---
## Descrizione

Il punto a onda è una combinazione di punto dritto e riempimento. Si comporta come un punto dritto, seguendo un percorso/tratto. Allo stesso tempo, si comporta come un riempimento, espandendosi dalla linea per coprire o riempire un'area. Crea bande morbide che assomigliano a onde, da cui il nome.

Le forme chiuse verranno riempite con una spirale (onde circolari). Le forme aperte verranno cucite avanti e indietro (onde lineari).

{% include folder-galleries path="butterfly-fill-project/ripple/" captions="1: Onda semplice da una forma chiusa; 2: Onda guidata come punto satin." %}

[<i class="fa fa-download"></i> Scarica i file di esempio](/assets/images/stitch-type-butterflies/ripple_stitch.zip)

## Creazione

{% include video id="cyvby3KJM10" provider="youtube" %}

### Onde Circolari

1. Crea un percorso chiuso e applica un colore al tratto.
2. Mantienilo come un singolo percorso. Evita percorsi combinati come forme con fori.
3. Facoltativo: Crea [un punto di riferimento o delle guide.](#guiding-ripples)
4. Apri la finestra di dialogo Params: Extensions, Ink/Stitch, quindi [Params](#params).
5. Imposta il metodo su Ripple.
6. Regola le impostazioni di Ripple come desideri.
7. Clicca su Applica.

![Esempi di onde circolari](/assets/images/docs/circular-ripple.svg)

[Scarica gli esempi](/assets/images/docs/circular-ripple.svg){: download="circular-ripples.svg" }

### Onde Lineari

Le onde lineari possono essere create in vari modi. Può essere una semplice curva o può essere costruita come una colonna a punto satin.

* Crea una forma aperta (un tratto semplice, due tratti combinati o anche una colonna a punto satin).
* Crea [un punto di riferimento o delle guide](#guiding-ripples) (facoltativo).
* Apri la finestra di dialogo dei parametri (`Extensions > Ink/Stitch > Params`) e imposta il `metodo` su `Ripple`.
* Imposta i [parametri](#params) come desideri e applica.

![Esempi di onde lineari](/assets/images/docs/linear-ripple.svg)

[Scarica gli esempi](/assets/images/docs/linear-ripple.svg){: download="linear-ripples.svg" }

## Onde a Ciclo

I cicli sono ammessi e benvenuti in qualsiasi percorso a onda. Usa i cicli per ottenere effetti speciali e piacevoli.

![Cuciture a onda con ciclo](/assets/images/docs/ripple-loops.svg)

[Scarica gli esempi](/assets/images/docs/ripple-loops.svg){: download="ripple-loop.svg" }

## Guida delle Onde

Le onde con solo **un sottopercorso** (forma chiusa o una semplice curva di Bézier) possono essere guidate utilizzando uno dei tre metodi seguenti.

## Punto di Riferimento

Definisci la posizione di riferimento dell'onda con il [comando visivo](/docs/commands/):

* Apri `Extensions > Ink/Stitch > Commands > Attacca i comandi agli oggetti selezionati...`
* Seleziona `Posizione di riferimento` e applica.
* Seleziona il simbolo e spostalo nella posizione desiderata.

Se non vengono fornite informazioni di guida, il centro del percorso viene utilizzato come punto di riferimento.

## Linea Guida

* Nel gruppo più esterno (nessun sottogruppo) dell'oggetto a punto a onda, crea una curva di tratto utilizzando lo strumento Bézier, partendo vicino alla curva dell'onda e proseguendo allontanandoti da essa.
* Seleziona quella curva ed esegui `Extensions > Ink/Stitch > Edit > Selection to guide line`.
* Seleziona la curva dell'onda ed esegui params. Adatta i parametri come desideri.

## Guida Satin

Con le guide satin, avrai la possibilità di guidare le onde con precisione utilizzando il metodo delle barre e delle maglie a punto satin. La larghezza della guida satin avrà anche un effetto sulla larghezza dell'onda. La posizione della forma a onda originale verrà ignorata e inizierà dove inizia il satin.

* Nel gruppo più esterno dell'oggetto a punto a onda, crea un oggetto simile a una [colonna a punto satin](/docs/stitches/satin-column/) con barre e maglie.
* Seleziona l'oggetto appena creato ed esegui `Extensions > Ink/Stitch > Edit > Selection to guide line`.
* Seleziona l'oggetto a onda ed esegui params. Adatta i parametri come desideri.

Il motivo per le onde guidate con il satin può essere regolato nella sua direzione con l'aiuto di una cosiddetta linea di ancoraggio.

* Disegna una linea dal punto più alto al punto più basso attraverso il motivo. La posizione corrisponde alle maglie a punto satin.
* Seleziona la linea e contrassegnala come linea di ancoraggio tramite `Extensions > Ink/Stitch > Edit > Selection to anchor line`.

![onda guidata con satin](/assets/images/docs/ripple_satin_guide.svg)

[Scarica](/assets/images/docs/ripple_satin_guide.svg){: download="satin_guided_ripples.svg" }

## Ritaglio

{% include upcoming_release.html %}

Le cuciture a onda possono essere ritagliate per formare il contorno.

* Crea la cucitura a onda.
* Crea la forma di ritaglio (deve essere sopra la cucitura a onda).
* Seleziona entrambi e esegui `Object > Clip > Set clip`.

## Parametri

{% include upcoming_release_params.html %}

{% include params.html stitch_type='ripple-stitch'%}

## File di Esempio che Includono Cuciture a Onda

{% include tutorials/tutorial_list key="stitch-type" value="Punto a Onda" %}
