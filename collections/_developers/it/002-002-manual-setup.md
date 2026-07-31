---
title: "Installazione Manuale per Linux e macOS"
permalink: /developers/inkstitch/manual-setup/
last_modified_at: 2026-04-08
toc: true
after_footer_scripts:
  - /assets/js/copy_code.js
---
Un'installazione manuale consente di modificare il codice durante l'esecuzione dell'estensione.

## Come Installare Ink/Stitch Manualmente

La versione di Python richiesta per lavorare con Ink/Stitch è >= 3.11.0.
Si consiglia di utilizzare `pyenv` per gestire l'ambiente virtuale Python, ma qualsiasi altro gestore di ambienti virtuali dovrebbe funzionare (ad esempio, `conda`, `uv`, ecc.).

### 1. Clona il codice sorgente dell'estensione

```
git clone --recurse-submodules https://github.com/inkstitch/inkstitch
```

### 2. Dipendenze Python

Sono necessari alcuni moduli Python aggiuntivi.
In alcuni casi, questa estensione utilizza funzionalità che non sono disponibili nelle versioni dei moduli preinstallati nelle distribuzioni, quindi si consiglia di installarli direttamente con pip.

```
python -m pip install -r inkstitch/requirements.txt
```

### 3. Prepara i file INX

Ora dobbiamo creare i file per il menu di Inkscape:

```
cd inkstitch
make manual
```

Quando in seguito si aggiunge o si modifica un file di modello per le estensioni Ink/Stitch, è sufficiente eseguire:

```
make inx
```

### 4. Crea un collegamento simbolico nella directory delle estensioni di Inkscape

```
cd ~/.config/inkscape/extensions
ln -s /path/to/inkstitch
```

### 5. Configura l'ambiente Python di Inkscape

Per impostazione predefinita, Inkscape utilizzerà l'interprete Python del sistema. Nelle distribuzioni Linux più recenti, lo standard [PEP668](https://peps.python.org/pep-0668/) impedisce di installare direttamente pacchetti Python nell'interprete Python del sistema.
Per aggirare questa limitazione, dobbiamo indicare a Inkscape di utilizzare l'interprete Python che abbiamo installato nel passaggio 2:

* Aprire il file `preferences.xml`.<br>
  La posizione può essere trovata in `Modifica > Preferenze > Sistema > Preferenze utente`.
* Chiudere Inkscape prima di modificare il file.<br>
  Altrimenti, verrà sovrascritto quando Inkscape viene chiuso.
* Cercare il termine `<group id="extensions" />` e aggiornarlo con l'interprete Python corretto.

  **Esempio:** Utilizzare `<group id="extensions" python-interpreter="/usr/local/bin/python3" />` dove `/usr/local/bin/python3` è il valore restituito da `which python3`.

Per maggiori informazioni, consultare la [documentazione di Inkscape](https://inkscape.gitlab.io/extensions/documentation/authors/interpreters.html#selecting-a-specific-interpreter-version-via-preferences-file).

### 6. Avvia Inkscape.

Le modifiche al codice Python avranno effetto la prossima volta che l'estensione viene eseguita. Le modifiche ai file di descrizione dell'estensione (`*.inx`) avranno effetto la prossima volta che Inkscape viene riavviato.