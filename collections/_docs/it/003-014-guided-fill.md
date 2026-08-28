---
title: "Riempimento Guidato"
permalink: /docs/stitches/guided-fill/
last_modified_at: 2024-05-06
toc: true
---
## Descrizione

Genera un riempimento curvo utilizzando linee guida.

{% include folder-galleries path="butterfly-fill-project/guided/" captions="1:Riempimento guidato con filo sfumato;2:Aree sovrapposte utilizzando il riempimento guidato per un effetto acquerello;3:Riempimento guidato utilizzando il metodo del buffer" %}

[<i class="fa fa-download"></i> Scarica i file di esempio](/assets/images/stitch-type-butterflies/guided_fill.zip)

## Creazione

*   Crea un **percorso chiuso con un colore di riempimento**. Questa forma può avere dei fori.
*   Crea una linea guida per definire le direzioni del punto:
    *   disegna una linea con un colore di tratto e senza un colore di riempimento
    *   seleziona quella linea
    *   esegui `Estensioni > Ink/Stitch > Modifica > Selezione in linea guida`
*   Seleziona entrambi e raggruppali (`Ctrl + G`).
*   Apri la finestra di dialogo dei parametri (`Estensioni > Ink/Stitch > Parametri`) e seleziona `Riempimento guidato` come metodo di riempimento.

Ogni gruppo può contenere più di un oggetto di riempimento, ma è efficace solo una linea guida e verrà utilizzata per guidare tutte le forme del gruppo, guidando ciascuna forma con l'intersezione della forma e della linea guida. In questo caso, una forma che non interseca la linea guida verrà riempita con un riempimento automatico regolare. Il gruppo può anche contenere oggetti di tratto regolari. Sulla tela, un marcatore permette di distinguere una linea guida da un tratto regolare.

![Gruppo di Riempimento Guidato](/assets/images/docs/guided-fill-group.svg)

Se il gruppo contiene più linee guida, solo una è efficace. Se la linea guida è un percorso composito, viene utilizzata solo una sottosequenza come linea guida. Tuttavia, è possibile utilizzare linee guida sinuose, che possono persino attraversare il bordo della forma più volte.

![Gruppo di riempimento guidato](/assets/images/docs/guided-fill-complex.svg)

## Strategie di Riempimento

Sono consentite tre strategie di riempimento per il riempimento guidato:

### Copia

Copia (il valore predefinito) riempirà la forma con copie spostate della linea. A seconda della linea guida, questo produrrà sovrapposizioni o una copertura irregolare.

### Offset parallelo

Offset parallelo assicurerà che ogni linea sia sempre a una distanza costante dalla sua vicina. Potrebbero essere introdotte angolazioni nette.

### Buffer

{% include upcoming_release.html %}

Il metodo del buffer utilizza offset attorno alla linea guida e permette anche che una linea guida sia composta da più sottosequenze.

## Imposta Punto di Inizio e Fine

Imposta i punti di inizio e fine per gli oggetti di riempimento automatico con [Comandi visivi](/docs/commands/).

## Parametri

Esegui `Estensioni > Ink/Stitch > Parametri` per modificare le impostazioni in base alle tue esigenze.

{% include params.html stitch_type='guided_fill'%}

## Sottostrato

Il sottostrato nel Riempimento Guidato non segue la linea guida, ma utilizza l'angolo di riempimento che può essere definito nei parametri del sottostrato [(/docs/stitches/fill-stitch#underlay).

## File di esempio che includono punti di riempimento guidati

{% include tutorials/tutorial_list key="stitch-type" value="Riempimento Guidato" %}
