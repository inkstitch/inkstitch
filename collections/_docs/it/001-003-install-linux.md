---
title: "Installa Ink/Stitch su Linux"
permalink: /docs/install-linux/
excerpt: "Come installare rapidamente Ink/Stitch."
last_modified_at: 2025-06-17
toc: true
after_footer_scripts:
  - /assets/js/copy_code.js
---
{% comment %}
## Guida Video

Forniamo anche video tutorial per principianti sul nostro <i class="fab fa-youtube"></i> [canale YouTube](https://www.youtube.com/c/InkStitch). Guarda il processo di installazione per <i class="fab fa-linux"></i> [Linux](https://www.youtube.com/watch?v=Dkb5UvsZUNg&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=2).
{% endcomment %}

## Requisiti

Ink/Stitch è un'estensione di Inkscape. Scarica e installa [Inkscape](https://inkscape.org/release/) versione 1.0.2 o superiore prima di installare Ink/Stitch.

## Installazione

{% assign tag_name = site.github.latest_release.tag_name %}
Scarica l'ultima versione (Ink/Stitch {{ tag_name }}) per Linux

{% assign tag_name = tag_name | slice: 1,tag_name.size %}

* x86_64:
  [tar.xz]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux-x86_64.tar.xz),
  [sh]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux-x86_64.sh),
  [rpm]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-1.x86_64.rpm),
  [deb]({{ site.github.releases_url }}/latest/download/inkstitch_{{ tag_name }}_amd64.deb)
* i386:
  [tar.xz]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux32-i386.tar.xz),
  [sh]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux32-i386.sh),
  [rpm]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-1.i386.rpm),
  [deb]({{ site.github.releases_url }}/latest/download/inkstitch_{{ tag_name }}_i386.deb)
* arm64:
  [tar.xz]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux-aarch64.tar.xz),
  [sh]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux-aarch64.sh),
  [rpm]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-1.aarch64.rpm),
  [deb]({{ site.github.releases_url }}/latest/download/inkstitch_{{ tag_name }}_arm64.deb)
* Arch linux: <https://aur.archlinux.org/packages/inkstitch>
* NixOS: <https://search.nixos.org/packages?channel=unstable&show=inkscape-extensions.inkstitch>

**Ultima versione:** {{ site.github.latest_release.published_at | date: "%d.%m.%Y"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

### Installazione DEB e RPM

Fai doppio clic sul file deb scaricato e segui il processo di installazione.

RPM: [GPG-Key](/assets/files/inkstitch.gpg)

### Installazione SH

Utilizza questa versione se stai utilizzando la versione AppImage di Inkscape o se desideri semplicemente installare Ink/Stitch solo per il tuo utente.
Questo script è utile anche se il tuo sistema non supporta i pacchetti deb o rpm.

Apri il terminale e vai nella cartella in cui si trova lo script scaricato ed esegui lo script di installazione, ad esempio:

```
cd Downloads
sh inkstitch-{{ tag_name }}-linux.sh
```

#### Opzioni avanzate

Questo script tenterà di determinare automaticamente dove installare le estensioni di Inkscape. Se sbaglia, puoi impostare una di queste variabili d'ambiente:

* `INKSCAPE_PATH` (es: /usr/bin/inkscape)

  Il percorso dell'eseguibile di Inkscape. Questo script chiederà a quel programma dove installare le estensioni passando l'argomento `--user-data-directory`.

* `INKSCAPE_EXTENSIONS_PATH` (es: $HOME/.config/inkscape/extensions)

  Il percorso della directory delle estensioni di Inkscape. Utilizza questo per ignorare il metodo `--user-data-directory` e specificare una directory.

Se preferisci installarlo manualmente, esegui questo script con l'opzione `--extract` per generare il file inkstitch-&lt;versione&gt;.tar.xz originale nella directory corrente.

### Installazione TAR.XZ

Vai su `Modifica > Preferenze > Sistema` e verifica dove si trova la tua cartella `Estensioni utente`.

![Posizione della cartella delle estensioni](/assets/images/docs/en/extensions-folder-location-linux.jpg)

Estrai l'archivio Ink/Stitch in questa cartella.

```
$ cd ~/.config/inkscape/extensions
$ tar -xvf ~/Downloads/inkstitch-{{ tag_name }}-linux.tar.xz
```

## Esegui Ink/Stitch

Apri Inkscape.

Troverai Ink/Stitch sotto `Estensioni > Ink/Stitch`.

## Aggiorna Ink/Stitch

### Versioni recenti

Se desideri aggiornare un'installazione `deb` o `rpm`, scarica semplicemente il nuovo pacchetto ed esegui l'installazione come descritto sopra. Questo sostituirà la vecchia installazione.
Lo `script di installazione` rimuoverà anche la versione precedentemente installata di Ink/Stitch prima di installare Ink/Stitch.

Questo è valido solo per le installazioni precedenti che hanno utilizzato lo stesso metodo. Se hai installato Ink/Stitch in un altro modo, segui le istruzioni per gli aggiornamenti precedenti.

### Versioni precedenti a Ink/Stitch v2.1.0 o versione tar.xz

Elimina prima i vecchi file dell'estensione. Vai alla directory dell'estensione e rimuovi ogni file e cartella che inizia con "inkstitch".

Quindi, procedi come descritto sopra.

Le directory delle estensioni possono essere visualizzate in Inkscape sotto <code class="language-plaintext highlighter-rouge">Modifica > Preferenze > Sistema</code>.

## Restare informati sugli aggiornamenti

Iscriviti a un feed di notizie per tenere traccia degli aggiornamenti di Ink/Stitch:<br />
* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Feed di GitHub per le nuove versioni](https://github.com/inkstitch/inkstitch/releases.atom)
* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Notizie di Ink/Stitch](/feed.xml)
* <p>Oppure segui il progetto su GitHub <iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Risoluzione dei problemi

### Ink/Stitch non viene eseguito / è grigio

**Verifica il percorso di installazione**

Controlla se hai estratto Ink/Stitch nella cartella corretta. Se la `cartella delle estensioni utente` non funziona correttamente, puoi provare a installare nella `cartella delle estensioni di Inkscape`.
Puoi anche trovarla in `Modifica > Preferenze > Sistema`.

**Verifica la versione di Ink/Stitch**

Verifica di aver scaricato Ink/Stitch per Linux ([Scarica](#download)).

**Verifica l'autorizzazione/la proprietà**

Alcuni utenti segnalano che falsi problemi di autorizzazione/proprietà possono causare questo problema.

### AttributeError: 'NoneType' object has no attribute 'title' in inkstitch.py

Questo errore ci è stato segnalato da utenti che hanno installato Inkscape tramite snap. È noto che Snap causa problemi all'esecuzione di Ink/Stitch con Inkscape.
Prova un altro metodo di installazione. Qualsiasi metodo descritto su [https://inkscape.org/](https://inkscape.org/releases/latest/) andrà bene.

### Alcuni dialoghi di Ink/Stitch scompaiono dopo pochi secondi o non vengono visualizzati affatto

#### Utilizza X11

Questo problema può essere causato da Wayland. Avvia Inkscape con il seguente comando:

```
export GDK_BACKEND=x11 && inkscape
```

Quando si utilizza il pacchetto Inkscape flatpak, il comando è il seguente:

```
flatpak --env=GDK_BACKEND=x11 run org.inkscape.Inkscape
```

#### Estendi il timeout per mutter

Nelle versioni di mutter ≥ 3.35.92, è possibile impostare il timeout utilizzato per verificare se una
finestra è ancora attiva. Questo è utile anche per il reindirizzamento X tramite SSH con
alta latenza.

Ad esempio, è possibile impostare il timeout a 60 s (60000 ms) utilizzando:

```gsettings set org.gnome.mutter check-alive-timeout 60000```

### ImportError: libnsl.so.1: impossibile aprire il file dell'oggetto condiviso. File non trovato

Installa la libreria mancante.

Ad esempio, su **Fedora**, installa libnsl con il seguente comando:

```
sudo dnf install libnsl
```

### Ho installato Ink/Stitch nella mia lingua nativa, ma i dialoghi vengono visualizzati in inglese

**Traduzione incompleta**

È possibile che non tutte le stringhe siano state tradotte. Ciò è indicato dal fatto che **alcune stringhe di testo sono in inglese e altre nella tua lingua nativa**.
Se desideri completare la traduzione, consulta la nostra [descrizione per i traduttori](/developers/localize/).

**Impostazione della lingua**

Dobbiamo distinguere tra il menu Estensioni in Inkscape e i dialoghi.
La selezione del file ZIP causa la visualizzazione solo del menu Estensioni in una determinata lingua.
I dialoghi sono costruiti in modo diverso. Utilizzeranno la lingua del tuo sistema operativo.
Se Ink/Stitch non è sicuro di quale lingua utilizzare, utilizzerà l'inglese.
Puoi indicare esplicitamente a Inkscape di utilizzare la tua lingua nativa come segue:
  * Vai su Modifica > Preferenze > Interfaccia (Ctrl + Shift + P)
  * Imposta la tua lingua
  * Riavvia Inkscape

![Preferenze > Interfaccia](/assets/images/docs/en/preferences_language.png)
