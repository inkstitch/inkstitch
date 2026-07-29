---
title: "Strumenti: Riempimento"
permalink: /docs/fill-tools/
last_modified_at: 2026-01-01
toc: true
---
## Separazione di Oggetti Riempiti

Gli oggetti riempiti funzionano meglio se sono elementi singoli, senza bordi sovrapposti. A volte, queste condizioni non sono facili da soddisfare e la tua forma potrebbe avere piccoli anelli che sono impossibili da vedere in Inkscape.

Pertanto, i messaggi di errore per le aree di riempimento si verificano frequentemente e sono fastidiosi per gli utenti. Questa estensione ti aiuterà a correggere le forme di riempimento danneggiate. Eseguila su ogni forma di riempimento che ti causa problemi. Riparerà il tuo elemento di riempimento e separerà le forme con bordi sovrapposti nelle loro parti, se necessario.

### Utilizzo

* Seleziona uno o più oggetti riempiti.
* Esegui: Estensioni > Ink/Stitch > Strumenti: Riempimento > Separa oggetti riempiti

### Semplice o Complesso

Scegli sempre "semplice" quando possibile. Mantiene i fori e corregge l'errore di "bordo sovrapposto" dividendo gli anelli in oggetti separati o li elimina se sono troppo piccoli per essere ricamati.

Mentre "semplice" divide gli anelli, non rispetta i sottocanali sovrapposti. Li tratta come oggetti separati. "Complesso" è in grado di riconoscere i percorsi sovrapposti e gestirli correttamente.

"Separa oggetti riempiti" può essere espresso in funzioni Inkscape native:
1. Percorso > Unisci (Risolvi problemi dei sottocanali)
2. Percorso > Separa (Separa oggetti)
3. Elimina gli oggetti troppo piccoli per essere ricamati.
4. Percorso > Combina (se desideri preservare i fori)
5. Percorso > Combina (se desideri preservare ancora più fori)

**Informazioni:** Per i percorsi sovrapposti, il passaggio 1 viene eseguito solo da "complesso".
{: .notice--info}

![Separa oggetti riempiti](/assets/images/docs/en/break_apart.jpg)
[Scarica SVG](/assets/images/docs/en/break_apart.svg)

## Conversione in blocchi di gradiente

La conversione in blocchi di gradiente suddivide un riempimento con un gradiente lineare in più blocchi di colore solido e spaziatura di riga adattata.

### Utilizzo

1. Applica un gradiente di colore lineare a un elemento.

  ![gradiente lineare](/assets/images/docs/en/linear-gradient.png)
2. Esegui `Estensioni > Ink/Stitch > Strumenti: Riempimento > Converti in blocchi di gradiente`

  ![blocchi di colore](/assets/images/docs/color_blocks.png)

## Assistente per il punto croce

L'assistente per il punto croce può fornire assistenza in vari modi durante la creazione di [modelli di punto croce](/docs/stitches/cross-stitch).

![Un fungo in due versioni: percorso vettoriale e contorno pixelizzato](/assets/images/docs/cross_stitch_assistant.jpg){: .align-right style="max-width: 400px" }
Ti aiuta a:
* Controllare e adattare la lunghezza della cucitura diagonale
* Creare la griglia della pagina per l'allineamento del punto croce (e supporto visivo durante il lavoro sui punti croce)
* Pixelare e combinare il contorno degli elementi selezionati, per evitare punti di salto, sovrapposizioni e per ottenere una migliore rappresentazione del posizionamento del punto croce
* Applicare parametri per il punto croce agli elementi selezionati
* Convertire immagini bitmap in elementi di riempimento per il punto croce

### Utilizzo

* Facoltativo: seleziona elementi di riempimento e/o immagini bitmap. Senza una selezione, puoi adattare solo la griglia della pagina.
* Apri l'estensione dell'assistente in `Estensioni > Ink/Stitch > Strumenti: Riempimento > Assistente per il punto croce`
* Imposta i parametri, le opzioni di output e le impostazioni bitmap (vedi sotto)
* Fai clic su `Applica`

#### Impostazioni

* **Impostazioni della griglia**

  Per garantire che le aree adiacenti siano ben coordinate, le cuciture a punto croce sono allineate secondo una griglia.
  Ciò significa che il motivo di ricamo potrebbe cambiare a seconda della posizione di un elemento sulla tela.
  Per pianificare questo meglio, è utile regolare la griglia della pagina in base alle dimensioni del motivo del punto croce. Questo rende più facile stimare visivamente le posizioni delle cuciture.

  **Verifica che la griglia della pagina sia allineata all'angolo in alto a sinistra della pagina.**<br/>
  Se non lo è, dovrai regolare manualmente la griglia in `File > Proprietà documento... > Griglie`.
  Troverai un'impostazione "Allinea alla pagina" che non può essere accessibile tramite il plugin Ink/Stitch.
  Impostala nell'angolo in alto a sinistra.
  {: .notice--warning }

  Quando si specifica la dimensione della griglia, **le lunghezze delle cuciture** delle croci diagonali non sono immediatamente evidenti.
  Tuttavia, le lunghezze delle cuciture giocano sempre un ruolo importante nel ricamo a macchina.
  L'Assistente per il punto croce ha quindi un campo per visualizzare e adattare le lunghezze delle cuciture diagonali.

* **Parametri, pixelatura e impostazioni bitmap**

  È possibile impostare direttamente i parametri di riempimento per il punto croce qui, in base alla spaziatura della griglia.

#### Opzioni di output

* **Applica impostazioni della griglia**: qui decidi la maggior parte di ciò che l'assistente farà.

   * Parametri: se selezionata, i parametri per il punto croce verranno applicati a tutti gli elementi di riempimento selezionati, in base alla scheda Parametri dell'assistente per il punto croce.
   * Pixelatura: se selezionata, l'Assistente per il punto croce pixelizza automaticamente gli elementi di riempimento selezionati in base alle impostazioni della griglia. Ciò consente di adattare direttamente le forme alla griglia e di identificare visivamente con precisione le posizioni delle cuciture.
     * Aggiungi nodi: è possibile scegliere di aggiungere nodi a ogni intersezione della griglia. Questo rende più facile adattare manualmente il contorno della forma.
       Nelle griglie non quadrate, i nodi potrebbero non corrispondere alle intersezioni verticali della griglia.
* **Gestione degli elementi**:
  * Rimuovi le sovrapposizioni: decidi se le sovrapposizioni devono essere mantenute o meno.

* **Configura la griglia della pagina**:
  * Definisci se adattare o meno la griglia della pagina
  * Definisci il colore della griglia
  * Scegli se rimuovere o meno le griglie per il punto croce precedentemente impostate nel documento.
    Le tue griglie manuali non verranno rimosse, ma disabilitate.

#### Impostazioni bitmap

* **Converti bitmap**: se selezionata, tutte le immagini bitmap selezionate vengono convertite in forme di riempimento
* **Un punto per pixel**: seleziona se desideri convertire le immagini di pixel art
* **Selezione del colore**: scegli tra specificare un numero di colori, in tal caso puoi anche scegliere l'algoritmo di riduzione del colore. Gli algoritmi proposti daranno risultati diversi e il migliore dipende davvero dalla tua immagine
  * un elenco di colori RGB, ad esempio impostato su `0 0 0 255 255 255` per ottenere un'immagine in bianco e nero
  * una tavolozza colori GIMP
   * oppure aggiungi tratti con i colori che desideri utilizzare e aggiungili alla selezione prima di utilizzare l'assistente.
* La **saturazione, la luminosità e il contrasto** dell'immagine originale possono essere modificati qui per ottenere risultati migliori
* **Soglia di trasparenza**: i pixel con almeno tale trasparenza vengono ignorati.
* **Colore di sfondo**: definisci il colore di sfondo qui, questo ti permetterà di rimuovere lo sfondo.
* **Rimuovi sfondo**: decidi cosa fare con i riempimenti con il colore di sfondo

Nella nostra sezione tutorial puoi trovare istruzioni dettagliate su come convertire le immagini in ricami a punto croce.
{: .notice--info}

## Riempimento Knockdown

Metodo di supporto per generare
* un'area di riempimento sotto tutti gli elementi selezionati, facoltativamente con un offset positivo o negativo. Questo può essere molto utile quando si lavora con tessuti ad alto pelo (di solito con un offset positivo) o per creare un sottofondo globale (di solito con un offset negativo)
* un'area rettangolare o circolare attorno a tutti gli elementi selezionati (ma non sotto). Questo può essere utile per creare un effetto di rilievo.

![Una figura con un punto di riempimento circostante](/assets/images/docs/knockdown.png)

* Seleziona elementi
* Apri `Estensioni > Ink/Stitch > Strumenti: Riempimento > Selezione a Riempimento Knockdown`
* Adatta le impostazioni
* Fai clic su applica
* Adatta le impostazioni di riempimento nel dialogo dei parametri (`Estensioni > Ink/Stitch > Parametri`)

{% include upcoming_release.html %}
Il parametro della spaziatura delle righe è stato calcolato in base all'impostazione della lunghezza della cucitura nell'estensione "Selezione a riempimento knockdown"
 
### Impostazioni

#### Scheda Opzioni

* Mantieni i fori: scegli se la forma deve contenere fori
* Offset: l'offset (mm) attorno alla selezione. L'offset può essere positivo o negativo
* Metodo (arrotondato, smussato, smussato): influenza l'aspetto dei bordi
* Limite smussatura: influenza l'aspetto dei bordi

#### Scheda Rilievo

* Forma: se impostata su "Nessuno", l'estensione crea un'area di riempimento knockdown sotto gli elementi selezionati, tenendo conto del valore dell'offset (dalla scheda opzioni). Se, d'altra parte, desideri un effetto di rilievo, scegli tra rettangolo e cerchio per creare un riempimento knockdown attorno agli elementi selezionati (escludendo l'area sotto gli elementi selezionati).
* Usa solo la forma: incide l'intera forma (rettangolo o cerchio) senza escludere la forma del motivo.
* Offset forma: qualsiasi valore positivo estenderà l'area del rilievo. L'area esclusa può essere modificata utilizzando il parametro offset nella scheda opzioni.
* Metodo (arrotondato, smussato, smussato): influenza l'aspetto dei bordi

Nota: se il parametro forma è impostato su cerchio o rettangolo, l'area esclusa è esattamente ciò che sarebbe stato un riempimento knockdown con la forma impostata su "Nessuno". Se l'offset della forma è 0, il cerchio/rettangolo più piccolo che contiene l'area esclusa. Se l'offset della forma è positivo, il bordo esterno del cerchio/rettangolo viene esteso in ogni direzione secondo questo valore. L'area esclusa rimane invariata.
## Tartan

L'editor delle strisce può essere trovato in `Estensioni > Ink/Stitch > Strumenti: Riempimento > Tartan`

![Un'immagine di un ippocampo resa con riempimento tartan](/assets/images/docs/en/tartan_stripe_editor.png)

### Personalizzazione

#### Posizionamento

Il motivo può essere ruotato, ridimensionato (%) e traslato (mm) come un'unica entità.

#### Impostazioni del motivo

* Simmetria: i motivi possono essere riflessi o ripetuti.
 * Un motivo riflesso invertirà le strisce ogni seconda volta (senza ripetere il punto di pivot). Ciò significa che un motivo con tre colori (verde, nero, giallo) verrà renderizzato come segue:
 verde, nero, giallo, nero, verde, nero, giallo, ...
 * Un motivo ripetuto ripeterà semplicemente l'intero motivo più e più volte: verde, nero, giallo, verde, nero, giallo, verde, ...

* Uguale conteggio di fili per ordito e trama
 * se disabilitato puoi definire set di colori diversi per ordito e trama
 * se abilitato ordito e trama sono gli stessi

#### Strisce

* Aggiungi colori con il pulsante `Aggiungi`
* Rimuovi i colori facendo clic su `X` dietro una striscia
* Modifica le posizioni delle strisce facendo clic e trascinando `⁝` (usa con cautela)
* Abilita, disabilita il rendering delle strisce con la casella di controllo (☑)
* Quando il conteggio dei fili è uguale, le linee verticali definiscono l'ordito, le linee orizzontali definiscono la trama
* Fai clic sul campo colorato per selezionare un altro colore
* Quando desideri modificare un colore in più strisce contemporaneamente, abilita `Collega colori` e i colori uguali si aggiorneranno contemporaneamente

### Codice della tavolozza

Il codice Ink/Stitch è ciò che verrà salvato nel file SVG, ma può anche essere modificato direttamente.

Un codice della tavolozza ha un aspetto simile a questo: `(#000000)/5.0 (#FFFFFF)/?5.0`.

* Le strisce sono separate da spazi
* Ogni colore è racchiuso tra parentesi tonde `(#000000)`
* Una barra (`/`) indica un ordine simmetrico/riflesso, mentre tre punti all'inizio e alla fine del codice (`...`) rappresentano un motivo ripetuto asimmetrico `...(#000000)5.0 (#FFFFFF)?5.0...`.
* Una barra verticale (`|`) è un separatore per ordito e trama e dovrebbe essere utilizzata solo se sono diversi nel conteggio dei fili

**Informazioni:** Il [Registro scozzese dei tartan](https://www.tartanregister.gov.uk/) ha un'enorme collezione di motivi tartan registrati. Ink/Stitch è in grado di utilizzare il loro codice che inviano via e-mail e convertirlo nel codice colore Ink/Stitch. Si prega di rispettare le loro particolari normative sulla licenza. Assicurati di definire la larghezza di un filo di tartan prima di fare clic su `Applica`.<br><br>Ecco un esempio di codice che puoi provare: `...B24 W4 B24 R2 K24 G24 W2...` ([fonte](https://www.tartanregister.gov.uk/threadcount))
{: .notice--info}

### Impostazioni di ricamo

Nelle impostazioni di ricamo, puoi decidere se vuoi rendere il tartan come un singolo elemento di ricamo o se vuoi ricevere più elementi SVG che puoi modificare e trasformare a tuo piacimento.

#### Elemento di ricamo

Rendere un tartan come un elemento di ricamo si tradurrà in un aspetto uniforme con un posizionamento ottimale dei punti. Puoi impostare vari parametri che possono essere ulteriormente perfezionati nel dialogo dei parametri.

Si prega di fare riferimento ai parametri che verranno visualizzati solo qui: la `Larghezza minima della striscia per i riempimenti`. Le strisce più piccole di questo valore verranno renderizzate come punto a catena/punto a fagiolo sulla parte superiore delle strisce di riempimento. Gli elementi possono essere modificati sulla tela dopo aver fatto clic su `Applica`.

**Informazioni:** Per AutoFill, il percorso finale sarà migliore di quanto mostrato nel simulatore. Fai clic su `Applica` per eseguire il piano di cucitura e vedere il risultato finale.
{: .notice--info}

## Tutorial sull'utilizzo di Strumenti: Riempimento

{% include tutorials/tutorial_list key="tool" value="Riempimento" %}