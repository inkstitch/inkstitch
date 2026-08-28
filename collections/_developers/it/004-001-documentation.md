---
title: "Documentazione"
permalink: /developers/documentation/
last_modified_at: 2020-10-04
toc: true
---
Vogliamo descrivere ogni possibile funzione con testo, immagini e/o video. Vogliamo anche fornire istruzioni sul processo di installazione e offrire una panoramica del miglior flusso di lavoro. Inoltre, vogliamo fornire file di esempio che altri utenti possono utilizzare. Sarebbe anche utile avere alcune immagini di esempio di design ricamati per dimostrare ciò che Ink/Stitch è in grado di fare.

Un'altra parte della documentazione, seppur ancora incompleta, sarà quella di aiutare altri sviluppatori a iniziare a esplorare il codice e consentire loro di introdurre nuove funzionalità in Ink/Stitch o qualsiasi altra cosa a cui possano pensare.

## Partecipa
Questo sito web richiede molta cura, generando nuovi contenuti e aggiornando quelli esistenti con l'evoluzione di Ink/Stitch. Possiamo utilizzare qualsiasi aiuto.

Non è necessario sapere come creare un sito web, poiché utilizziamo [Markdown](https://help.github.com/articles/basic-writing-and-formatting-syntax/) per la formattazione del testo. Tutti i file necessari per creare il sito web sono disponibili nel ramo [gh-pages-branch](https://github.com/inkstitch/inkstitch/tree/gh-pages) di GitHub.

Se sei interessato ad aiutare con la documentazione, segnala un problema su [github](https://github.com/inkstitch/inkstitch/issues) e facci sapere che sei disposto ad aiutare.

## Lavorare con Github-Pages

Github-Pages utilizza [Jekyll](https://jekyllrb.com/), un generatore di pagine statiche. È anche possibile installarlo localmente per scopi di test. Per istruzioni, consulta il loro sito web.
Stiamo utilizzando il tema [Minimal Mistakes Theme](https://mmistakes.github.io/minimal-mistakes/), con pochissime personalizzazioni.

### Struttura di Base dei File

* `_collections/_posts/language` notizie
* `_collections/_docs/language` documentazione
* `_collections/_tutorials/language` pagine principali dei tutorial
* `_collections/_tutorial/language` tutorial specifici
* `_collections/_developers/language` documentazione per sviluppatori
* `_pages/language` pagine statiche come "about", "terms" o "sitemap"
* `assets/language` file multimediali (immagini) e stile del sito web (CSS)
* `_data/navigation_language.yml` dati per ogni navigazione presente nel sito web

### Modifica dei File Esistenti
Modifica il contenuto a tuo piacimento. Stila il tuo testo con [markdown](https://help.github.com/articles/basic-writing-and-formatting-syntax/), che viene utilizzato anche con i problemi di Github, ecc.

Prima di salvare il file, modifica anche la data in cima alla pagina.

### Aggiunta di Nuovi File

#### Docs, Tutorial, Sviluppatori
Quando aggiungi nuove pagine, tieni presente la numerazione nel nome del file (per documenti e tutorial).

I numeri sono impostati per consentirci di utilizzare i link "precedente/successivo" sotto l'articolo per la navigazione. Si applicano anche alla struttura del menu laterale, che dovresti aggiornare quando aggiungi nuove pagine.

La modifica dei nomi dei file non impedirà al sito web di trovare i file, poiché utilizzano i permalink. Quindi, puoi tranquillamente modificare i numeri in base alle tue esigenze.

Ogni pagina dovrebbe iniziare con qualcosa di simile a questo:

```
---
title: "Titolo"
permalink: /permalink-univoco
excerpt: "Breve descrizione di cosa tratta il documento"
last_modified_at: yyyy-mm-dd # ad esempio, 2018-05-05
toc: true # imposta su false o elimina se non desideri visualizzare un indice
---
```

#### Post (Notizie)

I nomi dei file per i post seguono una certa struttura. Dovrebbero essere denominati in questo modo: yyyy-mm-dd-titolo.md

Ogni post dovrebbe iniziare con la seguente voce:

```
---
title: "Alcune Notizie"
date: yyyy-mm-dd
categories: news-category
---
```

### Funzionalità Aggiuntive

#### Gallerie

Aggiungere gallerie è diventato molto semplice: carica i file in una nuova cartella all'interno di `/assets/images/galleries/`.
Quindi aggiungi:

```
{% raw %}
```
{% include folder-galleries path="new-folder-name/" %}
```
{% endraw %}
dove desideri visualizzare una galleria contenente il contenuto di `new-folder-name`.

Se desideri fornire immagini di anteprima per un caricamento più rapido, aggiungi -th al nome del file. Ad esempio, `image.jpg` utilizzerebbe `image-th.jpg` come anteprima. Entrambi i file devono essere nella stessa cartella specificata nell'istruzione include.

#### Categorizzazione dei tutorial

I file dei tutorial nella cartella `_tutorial` dovrebbero contenere alcune parole chiave nell'intestazione per descrivere il tutorial specifico. Potrebbe essere simile a questo:

```
---
permalink: /tutorials/applique/
title: Applique
last_modified_at: 2018-05-11
excerpt: "File di esempio di applique"
image: "/assets/images/tutorials/samples/Applique Color Change.svg"
language: en
tutorial-type:
  - Sample File
  - Text
stitch-type:
  - Running Stitch
  - Fill Stitch
  - Satin Stitch
techniques:
  - Applique
field-of-use:
user-level: Beginner
---
```

Queste categorie possono quindi essere utilizzate per elencare i tutorial con una parola chiave specifica, ad esempio:
```
{% raw %}
```
{% include tutorials/tutorial_list key="stitch-type" value="Fill Stitch" %}
```
{% endraw %}
mostrerebbe un elenco di tutti i file di tutorial che hanno "fill stitch" specificato nell'intestazione.

Possono anche essere utilizzati per visualizzare un elenco completo di categorie. In questo caso, le categorie devono essere specificate per ogni chiamata di elenchi di tutorial. Esempio:

```
{% raw %}
```
{% assign tutorial_cats = 'Tutorial Type*Stitch Type*Techniques*Field Of Use*User Level' | split: '*' %}
{% include tutorials/display_tutorials tutorial_cats=tutorial_cats %}
```
{% endraw %}

```
