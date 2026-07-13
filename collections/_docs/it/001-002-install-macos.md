---
title: Installare Ink/Stitch su macOS
permalink: "/docs/install-macos/"
excerpt: Come installare rapidamente Ink/Stitch.
last_modified_at: 28/09/2024
toc: 'true'
---

{% comment %}

## Videoguida

Forniamo anche video tutorial per principianti sul nostro<i class="fab fa-youtube"></i> [Canale YouTube](https://www.youtube.com/c/InkStitch) .

Guarda il processo di installazione per<i class="fab fa-apple"></i> [macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3) . {% endcomment %}

## Download

Scarica l'ultima versione disponibile per la tua versione di macOS.

### Ventura e superiori

{% assign tag_name = site.github.latest_release.tag_name %} {% assign tag_name = tag_name | slice: 1, tag_name.size %}

<p><a href="%7B%7B%20site.github.releases_url%20%7D%7D/latest/download/inkstitch-v%7B%7B%20tag_name%20%7D%7D-osx-arm64.pkg" class="btn btn--info btn--large"><i class="fa fa-download "></i>Apple Silicon</a></p>

<p><a href="%7B%7B%20site.github.releases_url%20%7D%7D/latest/download/inkstitch-v%7B%7B%20tag_name%20%7D%7D-osx-x86_64.pkg" class="btn btn--info btn--large"><i class="fa fa-download "></i>Intel</a></p>

### High Sierra (10.13), Mojave (10.14), Catalina (10.15), Big Sur (11), Monterey (12)

<p><a href="%7B%7B%20site.github.releases_url%20%7D%7D/latest/download/inkstitch-%7B%7B%20tag_name%20%7D%7D-old-osx-x86_64.pkg" class="btn btn--info btn--large"><i class="fa fa-download "></i>Intel</a></p>

**Ultima versione:** [Ink/Stitch v{{ tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d" }})](https://github.com/inkstitch/inkstitch/releases/latest)

## Installazione

Ink/Stitch è un'estensione per Inkscape. Scarica e installa [Inkscape](https://inkscape.org/release/) versione 1.0.2 o superiore prima di installare Ink/Stitch. **Assicurati di aver <span style="text-decoration:underline;">installato ed eseguito</span> Inkscape <span style="text-decoration:underline;">prima</span> di installare Ink/Stitch** . Altrimenti l'installazione non andrà a buon fine. {: .notice--warning .bold--warning }

Se disponi di un processore ARM, assicurati che Rosetta sia installato con `softwareupdate --install-rosetta --agree-to-license` {: .notice--warning }

**Ventura e versioni successive:** fare clic sul file scaricato per eseguire il programma di installazione.

**High Sierra / Mojave / Catalina / Big Sur / Monterey:** Seguire le [istruzioni per i rilasci non autenticati.](#xxxx-cannot-be-opened-because-the-developer-cannot-be-verified)

Fai clic su `Continua` .

![Installa inchiostro/punto](/assets/images/docs/en/macos-install/installer01.png)

Fai clic su `Installa` .

![Installa inchiostro/punto](/assets/images/docs/en/macos-install/installer02.png)

Si aprirà una finestra di dialogo per l'inserimento della password. Inserisci la tua password utente e fai clic su `Installa Software` .

![Installa inchiostro/punto](/assets/images/docs/en/macos-install/installer03.png)

In alcuni casi il sistema invierà una richiesta se si consente al programma di installazione di salvare i file nella directory home. Ink/Stitch deve trovarsi nella cartella delle estensioni di Inkscape. Pertanto, rispondi a questa domanda con `Si` . {: .notice--info }

L'installazione è ora completa.

![Installa inchiostro/punto](/assets/images/docs/en/macos-install/installer04.png)

Ancora una domanda...

Vuoi conservare il file di installazione scaricato? La scelta è tua. Ink/Stitch non ne ha più bisogno.

![Installa inchiostro/punto](/assets/images/docs/en/macos-install/installer05.png)

## Procedura di installazione alternativa con Homebrew

Homebrew è un gestore di pacchetti per macOS. Per maggiori informazioni, consulta [https://brew.sh/](https://brew.sh/) {: .notice--info}

Si prega di rimuovere le versioni di Inkscape precedentemente installate. Brew installerà Inkscape insieme all'estensione Ink/Stitch. {: .notice--warning }

Apri il terminale e inserisci il seguente comando:

```
brew install inkstitch
```

## Run Ink/Stitch

Apri Inkscape. Troverai Ink/Stitch in `Estensioni > Ink/Stitch` .

![Menu Inchiostro/Punto](/assets/images/docs/en/macos-install/inkstitch-extensions-menu.png)

## Aggiornamento inchiostro/punto

Quando viene rilasciata una nuova versione di Ink/Stitch, scaricala ed esegui il programma di installazione come descritto sopra. In questo modo verrà rimossa automaticamente la vecchia versione di Ink/Stitch.

Le installazioni precedenti alla versione 2.1.0 devono essere rimosse manualmente. Accedi alla cartella delle estensioni e rimuovi l'installazione di Inkstitch prima di eseguire lo script di installazione.

**Suggerimento:** iscriviti a un canale di notizie per rimanere aggiornato sugli aggiornamenti di Ink/Stitch: <br><i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Feed GitHub sulle nuove versioni](https://github.com/inkstitch/inkstitch/releases.atom) <br><i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Notizie su inchiostro e cuciture](/feed.xml)<br> {: .notice--info }

## Risoluzione dei problemi

### Impossibile aprire 'xxxx' perché non è possibile verificare lo sviluppatore.

Questo messaggio viene visualizzato per le versioni destinate a sistemi macOS meno recenti e per le versioni di sviluppo.

- `Control + Click` sul file scaricato
- Seleziona `Apri` dal menu contestuale
- Se richiesto, inserisci il tuo nome utente e la password di amministratore per avviare il programma di installazione.

### Installazione non riuscita

Forniamo inoltre un file zip scaricabile che può essere estratto nella cartella delle estensioni utente (vedi sotto: conferma il percorso di installazione).

Per Ventura e versioni successive: [scarica ZIP (intel)]({{ site.github.releases_url }}/latest/download/inkstitch-v{{ tag_name }}-osx-x86_64.zip), [scarica ZIP (arm)]({{ site.github.releases_url }}/latest/download/inkstitch-v{{ tag_name }}-osx-arm64.zip)

Per le versioni precedenti di macOS [scarica il file ZIP]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-old-osx-x86_64.zip)

### L'Ink/stitch non scorre / è disattivato (in grigio)

**Conferma il percorso di installazione**

Controlla di aver estratto Ink/Stitch nella cartella corretta. Se la `Cartella estensioni utente` non funziona correttamente, puoi provare a installarlo anche nella `Cartella estensioni Inkscape` . Puoi trovarla anche in `Inkscape > Preferenze > Sistema` .

**Conferma la versione**

Verifica di aver scaricato Ink/Stitch per la tua versione di macOS ( [Scarica](#download) ).

### Ink/Stitch è visualizzato in inglese

**Traduzione incompleta**

È possibile che non tutto il testo sia stato tradotto. Ciò è indicato dal fatto che **alcune parti del testo sono in inglese e altre nella tua lingua madre** . Se desideri completare la traduzione, consulta la nostra [descrizione per i traduttori](/developers/localize/) .

**Impostazioni della lingua**

Se Inkscape/Stitch non è sicuro di quale lingua supportare, utilizzerà l'inglese come lingua di riserva. Puoi indicare esplicitamente a Inkscape di utilizzare la tua lingua madre nel seguente modo:

- Vai su Inkscape &gt; Preferenze &gt; Interfaccia (Ctrl + Maiusc + P)
- Imposta la tua lingua
- Riavviare Inkscape

![Preferenze > Interfaccia](/assets/images/docs/en/preferences_language.png)

## Disinstallare Ink/Stitch

Vai su `Inkscape > Preferences > System` e apri la cartella delle estensioni.

![cartella delle estensioni di Inkscape](/assets/images/docs/en/extensions-folder-location-macos.jpg)

Elimina ogni file e cartella inkstitch*.
