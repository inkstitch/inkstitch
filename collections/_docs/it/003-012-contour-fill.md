---
title: "Riempimento del Contorno"
permalink: /docs/stitches/contour-fill/
last_modified_at: 2025-04-12
toc: true
---
## Descrizione

Il riempimento del contorno copre le aree con punti che seguono il contorno di un oggetto.

{% include folder-galleries path="butterfly-fill-project/contour/" captions="1: Riempimento del contorno applicato all'intera forma; 2: Riempimento del contorno applicato a sezioni della forma" %}

[<i class="fa fa-download"></i> Scarica i file di esempio](/assets/images/stitch-type-butterflies/contour_fill.zip)

## Creazione

Crea un **percorso chiuso con un colore di riempimento**.

## Imposta Punto di Inizio e di Fine

Solo il punto di inizio può essere impostato con i [comandi visivi](/docs/commands/). Il comando per il punto di fine non è efficace con il riempimento del contorno.

## Parametri

Esegui `Estensioni > Inchiostro/Punto > Parametri`. Imposta il metodo di riempimento su `Riempimento del Contorno` e regola le impostazioni in base alle tue esigenze.

{% include params.html stitch_type='contour_fill'%}

## Sottostrato

Il sottostrato nel Riempimento del Contorno non segue il contorno, ma utilizza l'angolo di riempimento, che può essere definito nei [parametri del sottostrato di riempimento](/docs/stitches/fill-stitch#underlay).

## File di Esempio che Includono Punti di Riempimento del Contorno

{% include tutorials/tutorial_list key="stitch-type" value="Riempimento del Contorno" %}
