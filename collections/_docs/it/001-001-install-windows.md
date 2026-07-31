---
title: "Installa Ink/Stitch su Windows"
permalink: /docs/install-windows/
excerpt: "Come installare rapidamente Ink/Stitch."
last_modified_at: 2025-11-19
toc: true
---
{% comment %}
## Video Guide

Forniamo anche video tutorial per principianti sul nostro <i class="fab fa-youtube"></i> [canale YouTube](https://www.youtube.com/c/InkStitch). Guarda il processo di installazione per <i class="fab fa-windows"></i> [Windows](https://www.youtube.com/watch?v=U5htzWZSjA8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=4).
{% endcomment %}

## Requisiti

Ink/Stitch è un'estensione di Inkscape. Pertanto, è necessario installare una versione aggiornata di [Inkscape](https://inkscape.org/release/) (almeno la versione 1.0.2) prima dell'installazione.

È consigliabile scaricare Inkscape dal sito web. La versione di Inkscape disponibile nel Microsoft Store, in particolare, potrebbe causare problemi durante l'installazione di Ink/Stitch.

## Download

Utilizza il pulsante sottostante per scaricare l'ultima versione.

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-64bit.exe" class="btn btn--info btn--large"><i class="fa fa-download"></i> Scarica Ink/Stitch {{ site.github.latest_release.tag_name }} per Windows 64bit</a></p>

**Ultima versione:** {{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

Firma del codice gratuita fornita da [SignPath.io](https://about.signpath.io) tramite certificato di [SignPath Foundation](https://signpath.org).<br>Consulta la nostra [politica di firma del codice](/code-signing-policy).
{: .notice--info }

### Suggerimenti per il download tramite Microsoft Edge

Microsoft Edge potrebbe non scaricare immediatamente il file o potrebbe mettere in pausa il download. Segui questi passaggi per completare il download.

* Seleziona il link di download (sopra).
* Edge mostra un simbolo di avviso. Seleziona il simbolo, quindi seleziona il testo del messaggio.

  ![Messaggio di avviso di download](/assets/images/docs/en/windows-download/01-warning-message.png)

* Appariranno un'icona binaria e un pulsante del menu (ellissi). Seleziona il pulsante del menu.

  ![Messaggio di avviso con pulsante del menu](/assets/images/docs/en/windows-download/02-warning_message02.png)

* Si apre un piccolo menu. Seleziona `Mantieni`.

  ![Messaggio di avviso con menu](/assets/images/docs/en/windows-download/03-keep.png)

* Edge visualizza un altro avviso. Seleziona `Mostra altro`.

  ![Altro messaggio di avviso](/assets/images/docs/en/windows-download/04-show-more.png)

* Appariranno tre nuove opzioni.

   Se desideri contribuire a migliorare l'esperienza di download per i futuri utenti, seleziona `Segnala questa app come sicura`.

  Seleziona `Mantieni comunque` per completare il download.

  ![L'opzione "Mantieni comunque" viene visualizzata per la prima volta](/assets/images/docs/en/windows-download/05-keep_anyway.png)

## Installazione

Esegui il programma di installazione scaricato.

Windows potrebbe impedirne l'esecuzione automatica finché il certificato di Windows non avrà acquisito una maggiore attendibilità. Fino ad allora, dovrai concedere il permesso al programma di installazione per l'esecuzione.

Seleziona `Più informazioni` quando viene visualizzato questo messaggio.

![Programma di installazione di Ink/Stitch](/assets/images/docs/en/windows-install/installer01.png)

Seleziona `Esegui comunque`.

![Programma di installazione di Ink/Stitch](/assets/images/docs/en/windows-install/installer02.png)

Il programma di installazione punterà automaticamente alla cartella delle estensioni di Inkscape. Il percorso è già impostato per te. Non è necessario modificare questa cartella. Seleziona `Avanti`.

![Programma di installazione di Ink/Stitch](/assets/images/docs/en/windows-install/installer03.png)

Poiché Inkscape è già installato, la cartella delle estensioni esiste già. Seleziona `Sì` per continuare.

![Programma di installazione di Ink/Stitch](/assets/images/docs/en/windows-install/installer04.png)

Il programma di installazione mostra un riepilogo delle impostazioni di installazione. Seleziona `Installa`.

![Programma di installazione di Ink/Stitch](/assets/images/docs/en/windows-install/installer05.png)

Al termine del processo, Ink/Stitch è pronto per essere utilizzato.

![Programma di installazione di Ink/Stitch](/assets/images/docs/en/windows-install/installer06.png)

## Esecuzione di Ink/Stitch

Apri Inkscape per iniziare a utilizzare Ink/Stitch. Puoi trovare Ink/Stitch in `Estensioni > Ink/Stitch`.

![Menu di Ink/Stitch](/assets/images/docs/en/windows-install/inkstitch-extensions-menu.png)

## Disinstallazione di Ink/Stitch

### Disinstallazione di Ink/Stitch (versione 2.1.0 e successive)

Apri il menu Start di Windows e seleziona `Impostazioni`.

![Disinstallazione di Ink/Stitch](/assets/images/docs/en/windows-install/uninstall01.png)

Seleziona `App`.

![Disinstallazione di Ink/Stitch](/assets/images/docs/en/windows-install/uninstall02.png)

Scorri fino a Ink/Stitch.
Seleziona `Ink/Stitch` e quindi seleziona `Disinstalla`.

![Disinstallazione di Ink/Stitch](/assets/images/docs/en/windows-install/uninstall03.png)

Conferma di voler disinstallare Ink/Stitch.

![Disinstallazione di Ink/Stitch](/assets/images/docs/en/windows-install/uninstall04.png)

Ink/Stitch è stato rimosso dal tuo computer. Clicca su `OK`.

![Disinstallazione di Ink/Stitch](/assets/images/docs/en/windows-install/uninstall05.png)

### Disinstallazione di versioni di Ink/Stitch precedenti alla versione 2.1.0

Se stai utilizzando una versione precedente di Ink/Stitch, devi rimuoverla manualmente dalla cartella delle estensioni di Inkscape.

Apri Inkscape e vai su `Modifica`, quindi `Preferenze`, quindi `Sistema`. Seleziona il pulsante per aprire la cartella delle estensioni. Una volta aperta, trova la cartella Ink/Stitch ed eliminala. Potrebbe essere necessario eliminare prima eventuali sottocartelle e file.

![Cartella delle estensioni di Inkscape](/assets/images/docs/en/extensions-folder-location-win.jpg)

## Rimani aggiornato sugli aggiornamenti di Ink/Stitch

Puoi seguire gli aggiornamenti di Ink/Stitch tramite il nostro feed di notizie o tramite il feed delle nuove versioni su GitHub.

* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [News di Ink/Stitch (Sito web)](/feed.xml)<br />
* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Nuove versioni su GitHub](https://github.com/inkstitch/inkstitch/releases.atom)<br>

Puoi visualizzare l'attività del progetto su GitHub se desideri rimanere aggiornato sulle modifiche e sui progressi dello sviluppo. <iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe