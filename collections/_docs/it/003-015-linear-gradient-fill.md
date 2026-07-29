---
title: "Riempimento con Gradiente Lineare"
permalink: /docs/stitches/linear-gradient-fill/
last_modified_at: 2024-05-06
toc: true
---
## Descrizione

Il riempimento con gradiente lineare utilizza il colore del gradiente lineare di Inkscape per creare gradienti senza soluzione di continuità con un posizionamento coerente dei punti.

{% include folder-galleries path="butterfly-fill-project/linear_gradient/" captions="1:Gradiente blu-viola;2:Gradiente rosso-giallo" %}

[<i class="fa fa-download"></i> Scarica i file di esempio](/assets/images/stitch-type-butterflies/linear_gradient_fill.zip)

## Creazione

* Crea un percorso chiuso. La forma può avere dei fori.
* Nella finestra di dialogo "Riempimento e Tracciato", seleziona un gradiente lineare come riempimento e regola i colori. Sulla tela, regola l'angolo del gradiente. L'angolo del punto avrà un angolo di 90 gradi rispetto alla direzione del gradiente.
  ![gradiente lineare](/assets/images/docs/en/linear-gradient.png)
* Apri la finestra di dialogo dei parametri ("Estensioni > Ink/Stitch > Parametri") e seleziona "Riempimento con Gradiente Lineare" come metodo di riempimento.
  Imposta i parametri come desideri e applica.

<!--

Tutorial?!?

[![Esempio di Riempimento con Gradiente Lineare](/assets/images/docs/linear-gradient.jpg){: width="200x"}](/assets/images/docs/linear-gradient.svg){: title="Scarica il file SVG" download="linear-gradient.svg" } -->

## Imposta i Punti di Inizio e di Fine

Imposta i punti di inizio e di fine per gli oggetti di riempimento automatico utilizzando i [comandi visivi](/docs/commands/).

## Parametri

Esegui "Estensioni > Ink/Stitch > Parametri" per modificare le impostazioni in base alle tue esigenze.

{% include params.html stitch_type='linear_gradient_fill'%}

## Sottostrato

Il sottostrato nel riempimento con gradiente lineare è lo stesso per il riempimento automatico e utilizza l'angolo di riempimento, che può essere definito nei parametri del sottostrato [(/docs/stitches/fill-stitch#underlay).

## File di Esempio che Includono Punti con Gradiente Lineare

{% include tutorials/tutorial_list key="stitch-type" value="Riempimento con Gradiente Lineare" %}