---
title: Installare Ink/Stitch su Windows
permalink: "/docs/install-windows/"
excerpt: Come installare rapidamente Ink/Stitch.
last_modified_at: 19/11/2025
toc: 'true'
---

{% comment %}

## Videoguida

Forniamo anche video tutorial per principianti sul nostro<i class="fab fa-youtube"></i> [Canale YouTube](https://www.youtube.com/c/InkStitch) . Guarda il processo di installazione per<i class="fab fa-windows"></i> [Windows](https://www.youtube.com/watch?v=U5htzWZSjA8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=4) . {% endcomment %}

## Requisiti

Ink/Stitch è un'estensione per Inkscape. Pertanto, prima dell'installazione è necessario avere installata una versione recente di [Inkscape](https://inkscape.org/release/) (almeno la 1.0.2).

È preferibile scaricare Inkscape dal sito web. La versione disponibile sul Microsoft Store, in particolare, potrebbe causare problemi durante l'installazione di Ink/Stitch.

## Download

Utilizza il pulsante qui sotto per scaricare l'ultima versione.

<p><a href="%7B%7B%20site.github.releases_url%20%7D%7D/latest/download/inkstitch-%7B%7B%20site.github.latest_release.tag_name%20%7D%7D-windows-64bit.exe" class="btn btn--info btn--large"><i class="fa fa-download"></i>Scarica Ink/Stitch {{ site.github.latest_release.tag_name }} per Windows 64 bit</a></p>

**Ultima versione:** {{ site.github.latest_release.published_at | date: "%Y-%m-%d" }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

Firma del codice gratuita fornita da [SignPath.io](https://about.signpath.io) con certificato rilasciato da [SignPath Foundation](https://signpath.org) .<br> Consulta la nostra [politica di firma del codice](/code-signing-policy) . {: .notice--info }

### Consigli per il download tramite Microsoft Edge

Microsoft Edge potrebbe non scaricare immediatamente il file o potrebbe mettere in pausa il download. Segui questi passaggi per completare il download.

- Seleziona il link per il download (sopra).

- Edge visualizza un simbolo di avviso. Seleziona il simbolo, quindi seleziona il testo del messaggio.

    ![Scarica il messaggio di avviso](/assets/images/docs/en/windows-download/01-warning-message.png)

- Appaiono un'icona a forma di cestino e un pulsante del menu (tre puntini). Seleziona il pulsante del menu.

    ![Scarica il messaggio di avviso con il pulsante del menu](/assets/images/docs/en/windows-download/02-warning_message02.png)

- Si apre un piccolo menu. Seleziona `Keep` .

    ![Scarica il messaggio di avviso con il menu](/assets/images/docs/en/windows-download/03-keep.png)

- Edge visualizza un altro avviso. Seleziona `Show more` .

    ![Un altro messaggio di avvertimento](/assets/images/docs/en/windows-download/04-show-more.png)

- Compaiono tre nuove opzioni.

    Se desideri contribuire a migliorare l'esperienza di download per gli utenti futuri, seleziona `Report this app as safe` .

    Seleziona " `Keep anyway` per completare il download.

    ![Alla fine compare l'opzione ](/assets/images/docs/en/windows-download/05-keep_anyway.png)

## Installazione

Eseguire il programma di installazione scaricato.

Windows potrebbe impedire l'esecuzione automatica del programma finché il certificato di Windows non avrà acquisito sufficiente attendibilità. Fino ad allora, sarà necessario concedere l'autorizzazione per l'esecuzione del programma di installazione.

Seleziona `Più informazioni` quando viene visualizzato questo messaggio.

![Installatore di inchiostro/punti](/assets/images/docs/en/windows-install/installer01.png)

Seleziona `Esegui comunque` .

![Installatore di inchiostro/punti](/assets/images/docs/en/windows-install/installer02.png)

Il programma di installazione indicherà automaticamente la cartella delle estensioni di Inkscape. Il percorso è già impostato. Non è necessario modificarlo. Seleziona `Avanti` .

![Installatore di inchiostro/punti](/assets/images/docs/en/windows-install/installer03.png)

Poiché Inkscape è già installato, la cartella delle estensioni esiste già. Seleziona `Si` per continuare.

![Installatore di inchiostro/punti](/assets/images/docs/en/windows-install/installer04.png)

Il programma di installazione mostra un riepilogo delle impostazioni di installazione. Seleziona `Installa` .

![Installatore di inchiostro/punti](/assets/images/docs/en/windows-install/installer05.png)

Al termine del processo, Ink/Stitch è pronto per l'uso.

![Installatore di inchiostro/punti](/assets/images/docs/en/windows-install/installer06.png)

## Run Ink/Stitch

Apri Inkscape per iniziare a usare Ink/Stitch. Puoi trovare Ink/Stitch in `Estensioni > Ink/Stitch` .

![Menu Inchiostro/Punto](/assets/images/docs/en/windows-install/inkstitch-extensions-menu.png)

## Disinstallare Inchiostro/Punto

### Disinstallare Ink/Stitch (v2.1.0 e versioni successive)

Apri il menu Start di Windows e seleziona `Impostazioni` .

![Disinstallare Inchiostro/Punto](/assets/images/docs/en/windows-install/uninstall01.png)

Seleziona `Apps` .

![Disinstallare Inchiostro/Punto](/assets/images/docs/en/windows-install/uninstall02.png)

Scorri fino a Inchiostro/Cucitura. Seleziona `Ink/Stitch` e poi seleziona `Disinstalla` .

![Disinstallare Inchiostro/Punto](/assets/images/docs/en/windows-install/uninstall03.png)

Conferma di voler disinstallare Ink/Stitch.

![Disinstallare Inchiostro/Punto](/assets/images/docs/en/windows-install/uninstall04.png)

Ink/Stitch è stato rimosso dal computer. Fare clic su `Ok` .

![Disinstallare Inchiostro/Punto](/assets/images/docs/en/windows-install/uninstall05.png)

### Disinstallare le versioni di Ink/Stitch precedenti alla v2.1.0

Se si utilizza una versione precedente di Ink/Stitch, è necessario rimuoverla manualmente dalla cartella delle estensioni di Inkscape.

Apri Inkscape e vai su `Modifica` , poi `Preferenze` e infine `Sistema` . Seleziona il pulsante per aprire la cartella delle estensioni. Una volta aperta, trova la cartella Ink/Stitch ed eliminala. Potrebbe essere necessario eliminare prima eventuali sottocartelle e file.

![cartella delle estensioni di Inkscape](/assets/images/docs/en/extensions-folder-location-win.jpg)

## Rimani informato sugli aggiornamenti di Ink/Stitch

È possibile seguire gli aggiornamenti di Ink/Stitch tramite il nostro feed di notizie o tramite il feed delle release su GitHub.

- <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News (Sito web)](/feed.xml)<br>
- <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Nuove versioni su GitHub](https://github.com/inkstitch/inkstitch/releases.atom)<br>

<p>You can view project activity on GitHub if you want to stay updated on changes and development progress. <iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&amp;repo=inkstitch&amp;type=watch&amp;count=true&amp;v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Risoluzione dei problemi

Questa sezione illustra i problemi più comuni che si possono riscontrare quando Ink/Stitch non viene visualizzato, quando i file vengono bloccati dal software antivirus o quando Inkscape non riesce a individuare la cartella corretta. Descrive inoltre come risolvere i problemi relativi al percorso di Python, i problemi di aggiornamento di Windows, i messaggi relativi alle DLL di Windows 8 e i problemi di visualizzazione della lingua.

### Errore: la cartella delle estensioni di Inkscape non è stata trovata!

Quando l'installazione non va a buon fine e termina con il messaggio `Error: Inkscape Extensions folder not found! Install and then run Inkscape to create the extension folder.` "

- Assicurati di aver effettivamente installato Inkscape e di averlo aperto e chiuso almeno una volta.

Se questo messaggio continua a comparire, la cartella delle estensioni di Inkscape potrebbe trovarsi in una posizione insolita (oppure si sta utilizzando la versione di Inkscape scaricata dal Microsoft Store).

- Scarica e installa Inkscape dal [sito web di Inkscape](https://inkscape.org/release/) (ed eseguilo almeno una volta) prima di riprovare

- oppure scarica il file zip [Ink/Stitch]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-64bit.zip) ed estrailo nella cartella delle estensioni di Inkscape.

    Puoi trovare la cartella delle estensioni aprendo Inkscape. All'interno di Inkscape, vai su `Modifica > Preferenze > Sistema` . Verranno visualizzati i percorsi di sistema. Nella riga `Estensioni utente` fai clic `apri` .

### Inchiostro/Punto non compare nel menu delle estensioni oppure è disattivato (in grigio).

**Software antivirus**

Alcuni antivirus potrebbero bloccare Ink/Stitch perché il programma di installazione utilizza un file compresso. Aggiungi la cartella dell'estensione di Ink/Stitch all'elenco delle eccezioni del tuo programma antivirus, reinstalla Ink/Stitch e riprova.

Se il tuo software antivirus ha eliminato dei file, potresti ricevere un messaggio di errore simile a questo:

```
Tried to launch: inkstitch\bin\inkstitch
  Arguments: ['inkstitch\bin\inkstitch', '--id=XXX', '--extension=XXX', 'C:\Users\XXX\AppData\Local\Temp\ink_ext_XXXXXX.svgXXXXX']
  Debugging information:

Traceback (most recent call last):
  File "inkstitch.py", line 35, in <module>
    extension = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  File "C:\Program Files\Inkscape\lib\python2.7/subprocess.py", line 325, in __init__ errread, errwrite)
  File "C:\Program Files\Inkscape\lib\python2.7/subprocess.py", line 575, in _execute_child startupinfo)
WindowsError: [Error 2] The system cannot find the file specified
```

### PYTHONPATH

Sono state segnalate delle comunicazioni relative a un messaggio di errore che inizia in questo modo:

```
Python path configuration:
PYTHONHOME = 'C:\Users\{username}\AppData\Roaming\inkscape\extensions\inkstitch\bin'
PYTHONPATH = (not set)
```

Reinstalla Inkscape. Assicurati che l'opzione "Aggiungi al percorso" sia selezionata quando viene visualizzata la domanda relativa a PYTHONPATH durante l'installazione.

### Windows 8: Messaggio di errore

![Impossibile avviare il programma perché il file api-ms-win-crt-math-l1-1-1-0.dll non è presente nel computer. Prova a reinstallare il programma per risolvere il problema.](/assets/images/docs/en/windows-install/win8.png) {: .img-half } ![Errore durante il caricamento della DLL Python 'C:\Users...\AppData\Roaming\inkscape\extensions\inkstitch\inkstitch\bin\python38.dll'. LoadLibrary: Impossibile trovare il modulo specificato.](/assets/images/docs/en/windows-install/win8a.png) {: .img-half }

Se visualizzi questi due messaggi di errore su Windows 8, scarica e installa [i pacchetti ridistribuibili di Microsoft Visual C++](https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2015-2017-2019-and-2022) . Scegli il file corrispondente all'architettura del tuo sistema.

### Ink/Stitch è visualizzato in inglese

**Traduzioni incomplete**

Se Ink/Stitch viene visualizzato in inglese, ma ti aspettavi un'altra lingua, le traduzioni potrebbero essere incomplete. Ciò è indicato dalla **visualizzazione di alcune stringhe di testo in inglese e altre nella lingua selezionata** . Se desideri contribuire al completamento della traduzione, puoi farlo qui [(descrizione per i traduttori)](/developers/localize/) .

**Impostazioni della lingua**

Se Ink/Stitch non riesce a identificare la lingua da visualizzare, utilizzerà l'inglese. È possibile impostarla direttamente in Inkscape.

- Vai su Modifica &gt; Preferenze &gt; Interfaccia (Ctrl + Maiusc + P)
- Seleziona la lingua
- Riavviare Inkscape

![Preferenze > Interfaccia](/assets/images/docs/en/preferences_language.png)
