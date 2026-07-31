---
title: "Visualizzazione"
permalink: /docs/visualize/
last_modified_at: 2026-04-06
toc: true
---
## Simulatore

Seleziona gli oggetti che desideri visualizzare in un'anteprima simulata. Se desideri simulare l'intero progetto, seleziona tutto (`Ctrl+A`) o niente.

Quindi, esegui `Estensioni > Ink/Stitch > Visualizzazione e Esportazione > Simulatore` e goditi la visualizzazione.

![Simulatore](/assets/images/docs/en/simulator.jpg)
{: style="border: 2px solid gray; padding: 5px;"}

### Pulsanti e Scorciatoie

Pulsante | Effetto | Scorciatoie
-------- | -------- | --------
**Controlli**||
|<img src="/assets/images/docs/icons/backward_command.png" >|Torna al comando precedente|<key>Pagina giù</key>
|<img src="/assets/images/docs/icons/backward_stitch.png" >|Torna al punto di cucitura precedente|<key>←</key>
|<img src="/assets/images/docs/icons/forward_stitch.png" >|Avanza di un punto di cucitura|<key>→</key>
|<img src="/assets/images/docs/icons/forward_command.png" >|Vai al comando successivo|<key>Pagina su</key>
|<img src="/assets/images/docs/icons/direction.png" >|Inverti la direzione dell'animazione|
|<img src="/assets/images/docs/icons/play.png"> | Avvia/metti in pausa l'animazione|<key>spazio</key> / <key>p</key>
|<img src="/assets/images/docs/icons/restart.png" >|Riavvia|<key>r</key>
**Velocità**||
|<img src="/assets/images/docs/icons/slower.png" >|Rallenta il rendering|<key>↓</key>
|<img src="/assets/images/docs/icons/faster.png" >|Accelera il rendering|<key>↑</key>
**Mostra**||
|<img src="/assets/images/docs/icons/npp.png" >|Punto di penetrazione dell'ago|<key>o</key>
|<img src="/assets/images/docs/icons/jump.png" >|Salti|
|<img src="/assets/images/docs/icons/trim.png" >|Tagli|
|<img src="/assets/images/docs/icons/stop.png" >|Arresti|
|<img src="/assets/images/docs/icons/color_change.png" >|Cambi di colore|
**Informazioni**||
|<img src="/assets/images/docs/icons/info.png" >|Informazioni sul progetto|
**Impostazioni**||
|<img src="/assets/images/docs/icons/change_background.png" >|Cambia il colore di sfondo|
|<img src="/assets/images/docs/icons/cursor.png" >|Mostra il mirino|
|<img src="/assets/images/docs/icons/page.png" >|Mostra la pagina|
|<img src="/assets/images/docs/icons/settings.png" >|Apri la finestra delle impostazioni per impostare la velocità, la larghezza della linea e la dimensione del punto dell'ago|

È anche possibile **ingrandire** e **spostare** la simulazione con il mouse.

## Anteprima del Piano di Cucitura

L'anteprima del piano di cucitura inserisce un piano di cucitura sulla tela. A seconda delle impostazioni, l'anteprima del piano di cucitura verrà posizionata sopra il progetto
o sul lato destro della tela (opzione: sposta il piano di cucitura accanto alla tela).

Per accedere all'anteprima del piano di cucitura, esegui `Estensioni > Ink/Stitch > Visualizzazione e Esportazione > Anteprima del Piano di Cucitura...`.

### Opzioni

![Modalità di rendering semplici e realistiche](/assets/images/docs/stitch-plan-preview-modes.jpg)

<i>Da sinistra a destra: 1. Modalità di rendering semplice, 2. Modalità di rendering semplice con punti ago, 3. Modalità di rendering realistica.<br>
Fonte dell'immagine: [Pixabay](https://pixabay.com/vectors/fox-red-fox-creature-mammal-svg-2530031/)</i>

- **Visibilità dello strato del progetto** definisce la visibilità dello strato originale del progetto.
  - **invariata** lascialo così com'è
  - **nascosto** nascondi il progetto originale
  - **minore opacità** mostra il progetto originale con minore opacità
- **Modalità di rendering**
  - **Semplice**: disegno a linee semplice
  - **Realistica**: anteprima realistica come immagine png nella tela (8-bit)
  - **Realistica Alta Qualità**: anteprima realistica come immagine png nella tela (16-bit)
  - **Realistica Vettoriale (lenta)**: Output vettoriale con filtri realistici

    "Lenta" significa che potrebbe rallentare Inkscape dopo il processo di rendering e persino farlo bloccare.
    Quindi, usalo con cautela con progetti complessi e salva il tuo progetto prima di eseguire il rendering del piano di cucitura.
    {: .notice--warning }

- **Sposta il piano di cucitura accanto alla tela**
  Visualizza l'anteprima sul lato destro della tela. Se non è abilitata, il piano di cucitura verrà posizionato sopra il tuo progetto.
  In questo caso, potresti voler modificare la visibilità del tuo progetto per nasconderlo o ridurre l'opacità.
- **Punti ago** mostra i punti dell'ago se abilitato
- **Blocca** rende il piano di cucitura insensibile alle interazioni del mouse (rende più facile lavorare sugli elementi effettivi mentre il piano di cucitura è attivo)
- **Mostra simboli dei comandi**
- **Esegui cuciture di salto**

- **Aggiungi comando per ignorare lo strato**
- **Sovrascrivi l'ultimo piano di cucitura**
  Se selezionata, il nuovo piano di cucitura sostituirà quello precedente; deselezionala se desideri mantenere il piano di cucitura precedente.

### Flusso di lavoro di progettazione con scorciatoie

Imposta [scorciatoie](/docs/customize/#shortcuts) sia per "anteprima del piano di cucitura" che per "annulla piano di cucitura" (vedi sotto) e ciò supporterà molto il tuo flusso di lavoro di progettazione.

* Si consiglia di impostare la scorciatoia sul metodo "nessuna preferenza" nel menu delle scorciatoie.
  L'estensione verrà quindi eseguita direttamente (senza la finestra delle impostazioni) con le impostazioni applicate l'ultima volta.
* Abilita l'opzione "blocca", in modo da poter accedere a tutti i percorsi senza interferenze con l'elemento (gli elementi) del piano di cucitura.
* Assicurati che l'opzione "Sovrascrivi l'ultimo piano di cucitura" sia abilitata, altrimenti finirai con più piani di cucitura sulla tela.

{% include video id="vyTMwLvkkiw4vgwDcTJS6e" provider="diode" %}

## Annulla Piano di Cucitura

L'uso di un overlay del piano di cucitura con elementi nascosti o a bassa densità aiuta a ottenere un'idea visiva di come apparirà il progetto alla fine.
A volte può essere utile mantenere il piano di cucitura come aiuto visivo mentre si lavora su nuovi elementi.
Ma per l'esportazione o per le modifiche agli elementi esistenti durante il flusso di lavoro, avrai bisogno degli elementi originali.
Non è molto divertente eliminare il piano di cucitura, mostrare gli elementi originali o ripristinare l'opacità alla normalità.
Questa estensione è progettata per aiutare in questo flusso di lavoro.

Esegui `Estensioni > Ink/Stitch > Visualizzazione e Esportazione > Annulla Anteprima del Piano di Cucitura`.

## Mappa di Densità

* Seleziona gli oggetti se desideri la mappa di densità solo per alcuni oggetti, altrimenti esegui senza alcuna selezione.
* Esegui `Estensioni > Ink/Stitch > Visualizzazione e Esportazione > Mappa di Densità`.
* Imposta le gamme di colori e applica.
* Esamina (ingrandisci).
* Annulla con `Ctrl + Z`.

Questo visualizzerà punti rossi, gialli e verdi sopra i tuoi elementi in modo da poter identificare facilmente le aree ad alta densità.

### Opzioni

* Marcatori rossi / gialli

  Definisci, a partire da quanti punti di cucitura, i punti dovrebbero essere colorati di rosso o giallo.
* Visibilità dello strato del progetto

  Definisci se Ink/Stitch deve lasciare invariato lo strato del progetto, nasconderlo o ridurre l'opacità.
* Dimensione dell'indicatore

  Definisci la dimensione dei punti nell'unità del documento.

## Ordine di sovrapposizione

Questa estensione inserisce etichette numerate per gli elementi selezionati nel documento per visualizzare l'ordine di cucitura.

* Esegui `Estensioni > Ink/Stitch > Visualizzazione e Esportazione > Visualizza ordine di sovrapposizione...`.
* Scegli la dimensione del carattere.
* Clicca su applica.

![Visualizza ordine di sovrapposizione](/assets/images/docs/stacking_order.png)

## Stampa PDF

Le informazioni sull'anteprima di stampa PDF sono raccolte in un'altra sezione: [Ulteriori informazioni sull'esportazione PDF](/docs/print-pdf)
