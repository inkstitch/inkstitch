---
title: "Installa Ink/Stitch su macOS"
permalink: /docs/install-macos/
excerpt: "Come installare rapidamente Ink/Stitch."
last_modified_at: 2024-09-28
toc: true
---
{% comment %}
## Guida video

Forniamo anche video tutorial per principianti sul nostro <i class="fab fa-youtube"></i> [canale YouTube](https://www.youtube.com/c/InkStitch).

Guarda il processo di installazione per <i class="fab fa-apple"></i> [macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3).
{% endcomment %}

## Download

Scarica l'ultima versione disponibile per la tua versione di macOS.

### Ventura e versioni successive

{% assign tag_name = site.github.latest_release.tag_name %}
{% assign tag_name = tag_name | slice: 1, tag_name.size %}

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-v{{ tag_name }}-osx-arm64.pkg" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Apple Silicon</a></p>

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-v{{ tag_name }}-osx-x86_64.pkg" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Intel</a></p>

### High Sierra (10.13), Mojave (10.14), Catalina (10.15), Big Sur (11), Monterey (12)

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-old-osx-x86_64.pkg" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Intel</a></p>

**Ultima versione:** [Ink/Stitch v{{ tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }})](https://github.com/inkstitch/inkstitch/releases/latest)

## Installazione

Ink/Stitch è un'estensione di Inkscape. Scarica e installa [Inkscape](https://inkscape.org/release/) versione 1.0.2 o superiore prima di installare Ink/Stitch.
**Assicurati di aver installato ed eseguito Inkscape *prima* di installare Ink/Stitch**. Altrimenti, l'installazione fallirà.
{: .notice--warning .bold--warning }

Se hai un processore arm, assicurati che Rosetta sia installato con `softwareupdate --install-rosetta --agree-to-license`
{: .notice--warning }

**Ventura e versioni successive:** Clicca sul file scaricato per avviare l'installazione.

**High Sierra / Mojave / Catalina / Big Sur / Monterey:** Segui le [istruzioni per le versioni non firmate](#xxxx-cannot-be-opened-because-the-developer-cannot-be-verified)

Clicca su `Continua`.

![Installa Ink/Stitch](/assets/images/docs/en/macos-install/installer01.png)

Clicca su `Installa`.

![Installa Ink/Stitch](/assets/images/docs/en/macos-install/installer02.png)

Si aprirà una finestra di richiesta della password. Inserisci la tua password utente e clicca su `Installa software`.

![Installa Ink/Stitch](/assets/images/docs/en/macos-install/installer03.png)

In alcuni casi, il tuo sistema ti chiederà se consenti all'installatore di salvare file nella tua directory home. Ink/Stitch deve essere nella cartella delle estensioni di Inkscape. Pertanto, rispondi a questa domanda con `Sì`.
{: .notice--info }

L'installazione è ora completa.

![Installa Ink/Stitch](/assets/images/docs/en/macos-install/installer04.png)

Solo un'ultima domanda...

Vuoi conservare il file dell'installatore scaricato? Dipende da te. Ink/Stitch non ne ha più bisogno.

![Installa Ink/Stitch](/assets/images/docs/en/macos-install/installer05.png)

## Installazione alternativa con Homebrew

Homebrew è un gestore di pacchetti per macOS. Per maggiori informazioni, consulta <https://brew.sh/>
{: .notice--info}

Rimuovi le versioni precedenti di Inkscape installate. Brew installerà Inkscape insieme all'estensione Ink/Stitch.
{: .notice--warning }

Apri il terminale e inserisci il seguente comando:

```
brew install inkstitch
```

## Esecuzione di Ink/Stitch

Apri Inkscape. Troverai Ink/Stitch in `Estensioni > Ink/Stitch`.

![Menu di Ink/Stitch](/assets/images/docs/en/macos-install/inkstitch-extensions-menu.png)

## Aggiornamento di Ink/Stitch

Quando viene rilasciata una nuova versione di Ink/Stitch, scaricala ed esegui l'installazione come descritto sopra. Questo rimuoverà automaticamente la vecchia versione di Ink/Stitch.

Le installazioni precedenti alla versione 2.1.0 devono essere rimosse manualmente. Vai alla cartella delle estensioni e rimuovi la tua installazione di inkstitch prima di eseguire lo script di installazione.

**Suggerimento:** Iscriviti a un feed di notizie per rimanere aggiornato sulle novità di Ink/Stitch:<br />
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Feed di GitHub per le nuove versioni](https://github.com/inkstitch/inkstitch/releases.atom)<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Notizie di Ink/Stitch](/feed.xml)<br />
{: .notice--info }

## Risoluzione dei problemi

### "xxxx" non può essere aperto perché lo sviluppatore non può essere verificato

Questo messaggio viene visualizzato per le versioni più vecchie di macOS e per le versioni di sviluppo.

* Fai clic con il tasto `Control` sul file scaricato
* Scegli `Apri` dal menu contestuale
* Se richiesto, inserisci il tuo nome utente e la tua password per avviare il programma di installazione

### L'installazione fallisce

Forniamo anche un file ZIP che può essere estratto nella cartella delle estensioni dell'utente (vedi sotto: conferma il percorso di installazione).

Per Ventura e versioni successive: [scarica ZIP (Intel)]({{ site.github.releases_url }}/latest/download/inkstitch-v{{ tag_name }}-osx-x86_64.zip), [scarica ZIP (arm)]({{ site.github.releases_url }}/latest/download/inkstitch-v{{ tag_name }}-osx-arm64.zip)

Per le versioni più vecchie di macOS [scarica ZIP]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-old-osx-x86_64.zip)

### Ink/Stitch non viene eseguito / è grigio

**Conferma del percorso di installazione**

Verifica di aver estratto Ink/Stitch nella cartella corretta. Se la `cartella delle estensioni dell'utente` non funziona correttamente, puoi provare a installarlo nella `cartella delle estensioni di Inkscape`.
Puoi anche trovarla in `Inkscape > Preferenze > Sistema`.

**Conferma della versione**

Verifica di aver scaricato Ink/Stitch per la tua versione di macOS ([Download](#download)).

### Ink/Stitch viene visualizzato in inglese

**Traduzione incompleta**

È possibile che non tutto il testo sia stato tradotto. Questo è indicato dal fatto che **alcune parti del testo sono in inglese e altre nella tua lingua nativa**.
Se desideri completare la traduzione, consulta la nostra [descrizione per i traduttori](/developers/localize/).

**Impostazioni della lingua**

Se Ink/Stitch non è sicuro di quale lingua utilizzare, tornerà all'inglese.
Puoi indicare esplicitamente a Inkscape di utilizzare la tua lingua nativa come segue:
  * Vai a Inkscape > Preferenze > Interfaccia (Ctrl + Shift + P)
  * Imposta la tua lingua
  * Riavvia Inkscape

![Preferenze > Interfaccia](/assets/images/docs/en/preferences_language.png)

## Disinstallazione di Ink/Stitch

Vai a `Inkscape > Preferenze > Sistema` e apri la tua cartella delle estensioni.

![Cartella delle estensioni di Inkscape](/assets/images/docs/en/extensions-folder-location-macos.jpg)

Rimuovi ogni file e cartella inkstitch*.
