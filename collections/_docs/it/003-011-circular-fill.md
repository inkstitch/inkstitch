---
title: "Riempimento Circolare"
permalink: /docs/stitches/circular-fill/
last_modified_at: 2024-06-07
toc: true
---
## Descrizione

Il riempimento circolare riempie una forma con una spirale ricamata. Il centro della spirale è posizionato al centro della forma. Un punto di riferimento può essere utilizzato per definire un centro della spirale personalizzato.

{% include folder-galleries path="butterfly-fill-project/circular/" captions="1: Riempimento circolare utilizzando più livelli; 2: Riempimento circolare con una sottile gradazione di colore" %}

[<i class="fa fa-download"></i> Scarica i file di esempio](/assets/images/stitch-type-butterflies/circular_fill.zip)

## Creazione

*   Crea un **percorso chiuso con un colore di riempimento**. La forma può avere dei fori.
*   Apri la finestra di dialogo dei parametri (`Estensioni > Disegno/Cucitura > Parametri`) e seleziona `Riempimento Circolare` come metodo di riempimento.
    Imposta i parametri come desideri e applica.

## Imposta il centro della spirale

Per impostazione predefinita, il centro della spirale è il centro geometrico della forma.
Si noti che questo non è uguale al centro della cornice di delimitazione.

Per modificare il comportamento predefinito, seleziona la forma di riempimento circolare e associa il comando `Posizione di riferimento` alla forma.
Il centro del simbolo del comando sarà il nuovo centro della spirale.

Leggi [come associare comandi agli oggetti](/docs/commands/).

## Imposta punti di inizio e fine

Imposta i punti di inizio e fine per gli oggetti di riempimento automatico utilizzando i [comandi visivi](/docs/commands/).

## Parametri

Esegui `Estensioni > Disegno/Cucitura > Parametri` per modificare le impostazioni in base alle tue esigenze.

{% include params.html stitch_type='circular_fill'%}

## Sottostrato

Il sottostrato nel riempimento circolare è lo stesso del riempimento automatico e utilizza l'angolo di riempimento che può essere definito nei parametri del sottostrato [(/docs/stitches/fill-stitch#underlay).

## File di esempio che includono punti di cucitura di riempimento circolare

{% include tutorials/tutorial_list key="stitch-type" value="Circular Fill" %}