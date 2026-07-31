---
title: "Coding style"
permalink: /developers/inkstitch/coding-style/
last_modified_at: 2025-03-10
toc: true
---
Siamo entusiasti che tu sia interessato a contribuire al codice di Ink/Stitch! Grazie per aver letto questa guida.

## Generale

Un obiettivo principale di Ink/Stitch è creare una base di codice che sia **piacevole da utilizzare** e **facile da capire** per programmatori di tutti i livelli di competenza ed esperienza. Cerchiamo di scrivere codice che sia espressivo, facile da capire e ben documentato. Il codice è una forma di comunicazione e cerchiamo di utilizzare il nostro codice per raccontare una storia sui problemi che stiamo cercando di risolvere.

L'embroidery digitale è un problema complesso. Molti dei problemi che stiamo risolvendo sono complessi, e quindi anche il codice che scriviamo potrebbe essere complesso. Questo è spesso inevitabile, ma quando accade, cerchiamo di organizzare il nostro codice per renderlo il più comprensibile possibile.

L'uso di commenti nel codice è incoraggiato, soprattutto per il codice relativo alle cuciture. Se lo scopo del nostro codice non sarà ovvio ai lettori con background diversi, un commento descrittivo può fare molto. È particolarmente utile descrivere non solo _cosa_ fa il nostro codice, ma _perché_ lo fa. Sentiti libero di includere un link ai problemi qui su GitHub per evitare di dover ripetere le stesse informazioni.

La verbosità può spesso essere preferibile alla brevità. Nomi di variabili più lunghi ed espressivi possono essere molto utili per la leggibilità. Dividere una complessa condizione `if` in più istruzioni `if`, anche se potrebbe sembrare inefficiente, può rendere più facile capire la logica del codice. Ottimizzare il nostro codice per la velocità o l'utilizzo della memoria può essere necessario a volte, ma sacrificiamo la leggibilità solo dopo un'attenta valutazione. In tali casi, un commento ben posizionato può essere molto utile.

## Convenzioni di Codifica

Per Python, cerchiamo di seguire [PEP8](https://www.python.org/dev/peps/pep-0008/). Per Javascript, cerchiamo di far "contento" [ESLint](https://eslint.org). In generale, cerca di privilegiare la leggibilità e la facilità di comprensione. Se PEP8 e ESLint rendono questo più difficile, allora violarli in modo ponderato potrebbe essere la soluzione giusta.

Seguire PEP8 è facile: basta eseguire `make style` nella directory principale. Puoi eseguirlo su ogni commit aggiungendo questo nel tuo `.git/hooks/pre-commit`:

```bash
#!/bin/bash

cd $(dirname "$0")/../..

errors=$(make style 2>&1)

if [ "$?" != "0" ]; then
    echo "$errors"
    exit 1
fi
```

Puoi ordinare gli import di Python con `isort`.

## Annotazioni di Tipo

Incoraggiamo l'uso di annotazioni di tipo nel codice Python.

Le annotazioni di tipo rendono il codice più facile da leggere e comprendere, ad esempio rendendo chiaro quali tipi di dati che le funzioni accettano come argomenti e restituiscono.
Gli editor e gli IDE possono anche leggere queste informazioni di tipo per fornire funzionalità come il completamento automatico.
Le annotazioni di tipo ci consentono anche di utilizzare il controllore di tipo [Mypy](https://mypy.readthedocs.io/en/stable/#) per verificare la presenza di errori.

Un'ottima risorsa su come utilizzare le annotazioni è la [guida rapida di Mypy](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html).
Copre la maggior parte degli usi e dei modelli comuni.
La pagina di [Mypy sui problemi comuni](https://mypy.readthedocs.io/en/stable/common_issues.html) è utile per capire i problemi comuni con il controllo dei tipi che potresti incontrare.
È importante notare che Mypy non esegue il controllo dei tipi su funzioni che non hanno annotazioni di tipo, ma man mano che introduciamo nuovo codice con annotazioni, avremo una copertura migliore.

Puoi eseguire Mypy sulle tue modifiche semplicemente [installando Mypy](https://mypy.readthedocs.io/en/stable/getting_started.html#installing-and-running-mypy) ed eseguendo `mypy` nella directory principale del progetto.
Il file `mypy.ini` del progetto imposta tutte le configurazioni rilevanti, quindi non sono necessari altri argomenti.
Mypy viene eseguito anche come parte delle build di questo progetto su Github.
Gli errori rilevati da Mypy non causeranno il fallimento della build, ma appariranno nelle richieste di pull in modo che tu e i revisori possiate vedere i potenziali problemi.

Gran parte del nostro codice, soprattutto quello più vecchio, manca di annotazioni di tipo.
Se desideri aggiungere annotazioni di tipo a codice più vecchio, o scoprire quali tipi vengono utilizzati in una parte della base di codice senza annotazioni, potresti trovare [MonkeyType](https://monkeytype.readthedocs.io/en/stable/) utile.
Puoi facilmente far raccogliere a MonkeyType informazioni sui tipi da Ink/Stitch in modo simile a come puoi utilizzare uno dei diversi profiler con Ink/Stitch.
Semplicemente copia `DEBUG_template.toml` in `DEBUG.toml`, e decommenta le righe in modo che le opzioni `profiler_type = "monkeytype"` e `profile_enable = True` siano impostate.
Dopo aver eseguito un comando Ink/Stitch, apparirà una finestra che ti indica come eseguire Monkeytype e utilizzare le informazioni sui tipi raccolte.
Eseguire più comandi aggiungerà informazioni al database dei tipi.

## Linee guida e commenti

La revisione del codice è importante nel nostro progetto e chiediamo che tutte le modifiche al codice vengano inviate come richieste di pull. Tuttavia, non siamo qui per fare i "gatekeeper"! Vogliamo incoraggiare i tuoi contributi e lavoreremo con te per aiutarti a rendere il tuo codice il più leggibile e comprensibile possibile se pensiamo che alcune modifiche sarebbero utili. Incoraggiamo anche a fornire feedback sulle richieste di pull, soprattutto per quanto riguarda la leggibilità. Tutto il feedback deve essere fornito in un modo gentile e costruttivo, come indicato nel nostro [Codice di condotta](https://github.com/inkstitch/inkstitch/blob/main/CODE_OF_CONDUCT.md).

Quando fornisci feedback, tieni presente i nostri obiettivi di rendere la base di codice **piacevole da utilizzare** e **facile da capire**. Potrebbe essere il caso che qualcuno faccia qualcosa in modo diverso da come lo avresti fatto tu. Se rispetta comunque questi obiettivi, potrebbe essere accettabile così com'è. La diversità di pensiero rende la nostra base di codice più forte.

## Programmazione orientata agli oggetti

La programmazione orientata agli oggetti è incoraggiata, ma non obbligatoria. Può spesso rendere il codice più facile da capire, ma non sempre. Scegliamo lo strumento migliore per esprimere la soluzione al nostro problema nel modo più chiaro possibile.

## Librerie di codice

Stiamo gradualmente spostando i nostri algoritmi più complessi dalle classi a librerie (ad esempio, `lib/stitches`). Questo mantiene le nostre classi (come quelle in `lib/elements`) più semplici e focalizzate. Se ci troviamo a scrivere codice che verrà utilizzato da più classi, cerchiamo di considerare la possibilità di metterlo in un modulo libreria e chiamare la libreria dalla classe. Il modulo libreria può, ovviamente, definire le proprie classi se questo ha più senso.
