---
title: "Cucitura Manuale"
permalink: /docs/stitches/manual-stitch/
last_modified_at: 2026-01-03
toc: true
---
## Descrizione

Le cuciture manuali vengono create utilizzando ciascun nodo di un percorso come punto di penetrazione dell'ago.

{% include folder-galleries path="butterfly-fill-project/manual/" captions="1: Percorso manuale - ogni nodo rappresenta un punto di cucitura" %}

[<i class="fa fa-download"></i> Scarica i file di esempio](/assets/images/stitch-type-butterflies/manual_stitch.zip)

## Creazione

1. Crea un percorso. Lo stile o la larghezza della linea non vengono utilizzati nella creazione di una cucitura manuale.
2. Apri `Estensioni > Ink/Stitch > Parametri`.
3. Scegli `Posizionamento manuale della cucitura`.

Ogni nodo di un percorso rappresenta un punto di penetrazione dell'ago. Non tiene conto delle curve di Bézier.

![Posizionamento della cucitura manuale](/assets/images/docs/manual-stitch-placement.png)

È possibile ottenere una rappresentazione chiara del percorso della cucitura manuale come segue:
1. Seleziona tutti i nodi (`F2` quindi `Ctrl`+`A`).
2. Clicca su ![Trasforma i nodi selezionati in angoli](/assets/images/docs/tool-controls-corner.jpg){: title="Trasforma i nodi selezionati in angoli" } nella `Barra di controllo degli strumenti`.

## Parametri

Apri `Estensioni > Ink/Stitch > Parametri` per modificare i parametri in base alle tue esigenze.

{% include params.html stitch_type='manual-stitch'%}

## File di esempio che includono la cucitura manuale

{% include tutorials/tutorial_list key="stitch-type" value="Cucitura Manuale" %}
