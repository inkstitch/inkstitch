---
title: "Installazione e Build Manuale per Windows"
permalink: /developers/inkstitch/windows-manual-build/
last_modified_at: 2026-04-09
toc: true
after_footer_scripts:
  - /assets/js/copy_code.js
---
**Informazioni:** Per questa descrizione, utilizziamo **`foo`** come nome utente. Ogni volta che compare **`foo`**, sostituiscilo con il tuo nome utente di Windows.
{: .notice--warning }

## Requisiti

Installa le seguenti dipendenze per la build locale o l'installazione manuale di Ink/Stitch.

* [Python](https://www.python.org/downloads/release/python-31313/)
  * Installa la **versione 3.11 o superiore** di Python e solo la **versione a 64 bit**.
  * Seleziona "Aggiungi Python a PATH". Questo permette all'ambiente bash di trovare Python.
  * Quindi, fai clic su "Installa ora".

* [Git for Windows](https://github.com/git-for-windows/git/releases/tag/v2.43.0.windows.1)

  Questo installa Git e fornisce anche un emulatore di terminale per scaricare il codice sorgente di Ink/Stitch ed eseguire script di build.

* [Inno Setup](https://jrsoftware.org/isdl.php)

  Questo fornisce il compilatore per creare il programma di installazione di Windows, necessario solo per creare il programma di installazione di Ink/Stitch e non è richiesto per l'installazione manuale.
  Utilizza le impostazioni predefinite.
* [make](https://sourceforge.net/projects/mingw-w64/files/External%20binary%20packages%20%28Win64%20hosted%29/make/)

  Questo fornisce il comando `make` per eseguire gli script di build.
  * Scarica `make-3.82.90-20111115.zip`.
  * Estrai il contenuto.
  * Crea la cartella `C:\Make\bin`.
  * Copia `make.exe` da `Downloads\make-3.82.90-20111115\make-3.82.90-20111115\bin_ix86` in `C:\Make\bin`.

  ![Cartella Make con make.exe](/assets/images/developers/windows-manual-build/make-path.png)

## PATH

L'ambiente bash richiede che i percorsi del software necessari per creare una build o un'installazione manuale siano impostati. Quindi, configuriamoli.

* Apri le impostazioni di Windows > Sistema > Informazioni > Impostazioni di sistema avanzate.

  ![Impostazioni di Windows](/assets/images/developers/windows-manual-build/WindowsSystem.png)

  ![Informazioni](/assets/images/developers/windows-manual-build/PATH1.png)

* Nelle Impostazioni avanzate, fai clic su "Variabili d'ambiente".

  ![Impostazioni avanzate](/assets/images/developers/windows-manual-build/PATH2.png)

* In "Variabili utente per [foo]", fai clic su "Path" (1) e poi su "Modifica..." (2).

  ![Variabili di ambiente](/assets/images/developers/windows-manual-build/PATH3.png)

* Per ciascuno dei percorsi seguenti, fai clic su "Nuovo", quindi copia e incolla il percorso del file:

  ```
  C:\Make\bin
  C:\Program Files (x86)\Inno Setup 6
  ```
  `make` è richiesto sia per l'installazione manuale che per la build locale. Inno Setup è necessario solo quando si crea il programma di installazione di Inkstitch.
* Dovrebbe apparire così:

  ![Variabili di ambiente](/assets/images/developers/windows-manual-build/Final-paths.png)

## Abilitare i nomi lunghi per Git

* Nella barra di ricerca, digita `cdm` e scegli "Esegui come amministratore".

  ![Esegui CMD come amministratore](/assets/images/developers/windows-manual-build/cmd-admin.png)

* Esegui il seguente comando:

  ```
  git config --system core.longpaths true
  ```

* Chiudi il prompt dei comandi; non abbiamo bisogno dei diritti di amministratore dopo questo.

## Scaricare Ink/Stitch

* Se hai già una versione di Ink/Stitch installata, [disinstallala](/docs/install-windows/#uninstall-inkstitch) per evitare doppie voci nel menu delle estensioni di Inkscape.

* Vai su "Modifica > Preferenze > Sistema" e apri la tua cartella delle estensioni.

  ![Cartella delle estensioni di Inkscape](/assets/images/docs/en/extensions-folder-location-win.jpg)

  Se non stai mirando all'installazione manuale ma vuoi creare sia Ink/Stitch che il suo programma di installazione, **non seguire questo passaggio**, ma scegli un'altra directory per salvare il codice sorgente di Inkstitch.
  {: .notice--warning }

* Fai clic con il pulsante destro del mouse nell'esplora file e fai clic su "Git Bash qui" per scaricare Ink/Stitch nella cartella delle estensioni.

  ![Menu contestuale](/assets/images/developers/windows-manual-build/GIT.png)
* Esegui il seguente comando nell'emulatore di terminale:

  ```
  git clone --recurse-submodules https://github.com/inkstitch/inkstitch
  ```

## Configurare Python

* Esegui i seguenti comandi nell'emulatore di terminale:
  ```
  python -m pip install --upgrade pip
  ```
* Ora siamo pronti per installare il resto delle dipendenze tramite il file requirements.txt di Ink/Stitch:
  ```
  python -m pip install -r inkstitch/requirements.txt
  ```
* Per il debug con pydevd, esegui anche:
  ```
  python -m pip install pydevd
  ```

## Installazione manuale per lo sviluppo di Ink/Stitch

* Abbiamo preparato tutto per configurare l'installazione manuale di Ink/Stitch. Vai nella cartella di Ink/Stitch, situata nella cartella delle estensioni, e apri l'emulatore di terminale:
  ```
  cd inkstitch
  make manual
  ```
* Ora puoi utilizzare l'installazione di Ink/Stitch. Le modifiche al codice Python avranno effetto la prossima volta che l'estensione viene eseguita.
* Dopo aver aggiunto un nuovo modello per nuove estensioni di Ink/Stitch, esegui il seguente comando per aggiornare le voci del menu di Inkscape:
  ```
  make inx
  ```
  Se esegui Ink/Stitch tramite Inkscape, chiudi e riapri Inkscape dopo aver eseguito il comando.

## Generare una build per testare l'aggiornamento su altri sistemi Windows

* Per creare Ink/Stitch, devi installare il pacchetto pip di pyinstaller.
  ```
  python -m pip install pyinstaller
  ```

* Ink/Stitch utilizza [7-zip](https://7-zip.org/) per comprimere il file di build. Devi quindi installarlo.
  Aggiungilo a PATH come descritto sopra come `C:\Program Files\7-Zip`
* Nell'emulatore di terminale, esegui:

  ```
  cd inkstitch
  make distlocal
  ```

* Nell'esplora file, troverai le build completate nella cartella `artifacts`.

  Non installare la versione di build se hai l'installazione manuale nella cartella delle estensioni, altrimenti avrai voci di menu duplicate.
  {: .notice--warning }

## Risoluzione dei problemi relativi ai moduli Python mancanti

Se, quando tenti di aprire Ink/Stitch, riscontri errori relativi a moduli Python mancanti: `ModuleNotFoundError: No module named 'diskcache'`,

È molto probabile che debba impostare manualmente la versione di Python nelle preferences.xml di Inkscape:

* In Inkscape, vai su Modifica > Preferenze > Sistema > Preferenze utente e fai clic su Apri.
* Nella tua cartella delle preferenze, individua `preferences.xml`.
* Chiudi Inkscape.
* Apri `preferences.xml` con un editor di testo.
* Cerca `<group id="extensions"`.
* Aggiungi l'attributo `python-interpreter="C:\Program Files\Python311\python.exe"`. Sostituisci il percorso con la versione di Python che stai utilizzando. Puoi trovare il percorso eseguendo `where python` in un prompt dei comandi.
