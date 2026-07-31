---
title: "Lettering"
permalink: /docs/lettering/
last_modified_at: 2025-05-20
toc: true
---
## Strumento di Lettering

Il modulo di testo crea testo su più righe. Scegli il font giusto per il tuo progetto da un'ampia varietà di font pre-digitalizzati.

![Estensioni di Lettering](/assets/images/docs/en/lettering.png)

### Utilizzo

* Esegui `Estensioni > Ink/Stitch > Lettering > Lettering`
* Inserisci il tuo testo (è possibile utilizzare più righe)
* Regola la famiglia di caratteri e la scala.<br>
  **⚠ Avviso**: Per ottenere i migliori risultati, si prega di considerare i limiti di scala nella descrizione del font.
* Clicca su `Applica e Esci`.
* Posiziona il tuo testo all'interno del documento SVG.

### Filtri dei font

* **Filtro della dimensione del font**

  I font sono progettati per un intervallo di dimensioni specifico. Il filtro della dimensione del font aiuta a ridurre l'elenco dei font, mostrando solo quelli adatti alla dimensione desiderata.
  Un filtro del font attivo (diverso da 0) imposterà il valore di scala corretto quando si seleziona un font.

* **Glifi**

  Se selezionato, vengono elencati solo i font che contengono tutte i glifi del tuo testo.

* **Categorie dei font**

  Filtra i font per categorie, ad esempio, ottieni solo i font per applicazioni o solo i font calligrafici.

### Opzioni
{% include upcoming_release_params.html %}
* **Scala**

  Definisce la dimensione di output del font rispetto alla dimensione originale del font (%).
  Si consiglia di utilizzare l'opzione di scala, invece di ridimensionare il font sulla tela.
  In questo modo, puoi assicurarti di rimanere all'interno dei parametri per cui il font è stato progettato.

* **Allineamento del testo**

  Allinea il testo su più righe: sinistra, centro, destra, blocco (predefinito), blocco (letterspacing).

* **Spaziatura tra le lettere**

  Aggiungi questa larghezza (mm) tra le lettere.

* **Spaziatura tra le parole**

  Aggiungi questa larghezza (mm) tra le parole.

* **Altezza della riga**

  Aggiungi questa altezza (mm) tra le righe.

* **Ordinamento dei colori**

  Ordina i colori dei font multicolore per evitare un gran numero di modifiche del filo.

* **Cucire le righe di testo avanti e indietro**

  Con questa opzione abilitata, la prima riga verrà cucita da sinistra a destra e la seconda da destra a sinistra, ecc.
  Questo darà alla tua macchina per cucire percorsi più brevi.

* **Aggiungi trim**

  Aggiunge comandi TRIM in base all'opzione scelta (Mai, dopo ogni riga, dopo ogni parola, dopo ogni lettera).

* **Usa simboli di comando**

  Quando si aggiungono trim, utilizzare simboli di comando.Altrimenti, utilizza l'impostazione del parametro trim.

* ****

### Impostazioni predefinite

Puoi salvare e caricare le tue impostazioni di font preferite.

## Lettering lungo un percorso

I caratteri Ink/Stitch sono progettati con cura. Se provi a trasformarli con strumenti comuni, potrebbero non funzionare come previsto. Ciò significa che posizionare le lettere lungo un percorso richiederà molto lavoro. Pertanto, abbiamo creato uno strumento per aiutarti in questo.

![Un testo allineato lungo un percorso mentre si utilizzano le varie opzioni](/assets/images/docs/text_along_path_alignment.png)

### Utilizzo

* Seleziona un percorso e un gruppo di lettere.
* Esegui `Estensioni > Ink/Stitch > Lettering > Lettering lungo il percorso...`
* Se `stretch` è abilitato, Ink/Stitch estenderà gli spazi tra le lettere, in modo che il testo utilizzi l'intero percorso.
  Altrimenti, manterrà le distanze dal testo originale.
* Clicca su applica.

Il lettering seguirà la direzione del percorso. Inverti il percorso se necessario (`Percorso > Inverti`).
{: .notice--info}

## Libreria dei font

Una panoramica dei font disponibili può essere trovata nella [libreria dei font](/fonts/font-library/).

## Ordinamento dei colori

Quando si ricama con diverse lettere, è possibile che si desideri ordinare i colori per evitare molte modifiche del filo.
Quando i colori appaiono nello stesso ordine in ogni lettera e quando ogni colore viene utilizzato solo su percorsi consecutivi all'interno di una lettera (questo è vero per tutti i font Ink/Stitch multicolore, ad eccezione di Infinipicto), ecco come ordinare rapidamente i colori di un lettering:

* Seleziona una lettera nel pannello degli oggetti.
* Seleziona il percorso da ricamare per primo di questa lettera (l'ultimo percorso per questa lettera nel pannello degli oggetti).
* Modifica/Seleziona lo stesso/ lo stesso tratto di colore.
* Raggruppa, questo gruppo finirà nell'ultimo tratto da ricamare della lettera.
* Sposta questo gruppo nella parte superiore della sua lettera.

ripeti fino a quando tutti i colori non sono raggruppati, partendo sempre dalla selezione dell'ultimo percorso di una lettera.

## Lettering in batch

Il lettering in batch consente di creare facilmente più file di testo.

![Un patch con quattro nomi diversi](/assets/images/docs/batch-lettering.png)

* Prepara un file di progettazione.
  Se il file contiene un percorso con l'etichetta `lettering in batch`, questo verrà utilizzato per la posizione del testo.
  Funzionerà allo stesso modo di [Lettering lungo un percorso](/docs/lettering/#lettering-along-path).
* Vai su `File > Salva una copia...` e clicca sulla piccola freccia sul campo di selezione del formato file per aprire un elenco dei formati file disponibili.
* Scegli `Ink/Stitch: lettering in batch (.zip)`
* Naviga nella cartella di output desiderata e clicca su Salva.

### Opzioni

* **Testo:** Inserisci il testo; per impostazione predefinita, ogni nuova riga verrà inserita in un file separato.
* **Separatore personalizzato:** Per impostazione predefinita, viene utilizzato una nuova riga. Specifica un altro separatore se desideri che il tuo file di testo contenga testo su più righe.
  Il testo verrà diviso e inserito in un nuovo file con ogni occorrenza del separatore personalizzato.

* **Nome del font:** Il nome del font che desideri utilizzare. Consulta la [libreria dei font](/fonts/font-library/) per trovare un elenco dei font disponibili.
* **Scala (%):** Valore di scala per ridimensionare un font. Il valore verrà limitato all'intervallo di scala disponibile per il font specifico.
* **Ordinamento dei colori:** Indica se i font multicolore devono essere ordinati per colore o meno.
* **Aggiungi trim:** Indica se devono essere aggiunti i trim o meno (mai, dopo ogni riga, parola o lettera).
* **Usa simboli di comando:** Indica se i trim devono essere aggiunti come simboli di comando o come opzione parametro (rilevante solo per l'output SVG).
* **Allineamento del testo su più righe:** Definisce come il testo su più righe deve essere allineato.
* **Lettering lungo un percorso**
  * **posizione orizzontale del testo:** La posizione orizzontale del testo lungo il percorso `lettering in batch`.
  * **posizione verticale del testo:** La posizione verticale in relazione al percorso `lettering in batch`.
* **Formati file:** Inserisci un elenco separato da virgole di [formati file](/docs/file-formats/#writing).

[Scarica il file di esempio](/assets/images/docs/batch_lettering_template_example.svg){: title="Scarica file SVG" download="batch_lettering_template_example.svg" }

### Utilizzo da riga di comando

Ecco un esempio minimo per l'utilizzo da riga di comando dell'estensione di lettering in batch.

```
./inkstitch --extension=batch_lettering --text="Hello\nWorld" --font="Abecedaire" --file-formats="svg,dst" input_file.svg > output_file.zip
```

#### Opzioni

Opzione             |Tipo di input|Valori
---------- --------|----------|------
`--text`           |stringa    |non deve essere vuoto
`--separator`      |stringa    |predefinito: '\n'
`--font`           |stringa    |deve essere un nome di font valido
`--scale`          |intero   |predefinito: 100
`--color-sort`     |stringa    |off, all, line, word<br>predefinito: off
`--trim`           |stringa    |off, line, word, glyph<br>predefinito: off
`--command_symbols`|booleano      |predefinito: False
`--text-align`     |stringa    |left, center, right, block, letterspacing<br>predefinito: left
`--file-formats`   |stringa    |deve essere almeno un formato di output valido

## Creazione di nuovi font per Ink/Stitch

Leggi il [tutorial sulla creazione di font](/tutorials/font-creation/).

Contattaci se desideri pubblicare il tuo font nello strumento di lettering di Ink/Stitch su [GitHub](https://github.com/inkstitch/inkstitch/issues).

## File di esempio che includono il lettering

{% include tutorials/tutorial_list key="techniques" value="Lettering" %}
