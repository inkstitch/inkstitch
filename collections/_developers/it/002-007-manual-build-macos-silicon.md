---
title: "Build Manuale: Apple Silicon"
permalink: /developers/inkstitch/apple-silicon-manual-build/
last_modified_at: 2024-10-01
toc: true
---
Questa è una guida per costruire Ink/Stitch localmente. L'installazione manuale per gli sviluppatori è descritta nella [sezione di configurazione manuale](/developers/inkstitch/manual-setup/).
{: .notice--info}

## Homebrew

Ink/Stitch utilizza Homebrew per installare le dipendenze. Visitate [https://brew.sh/](https://brew.sh/) e seguite le istruzioni sul sito web per l'installazione. Questo installerà anche gli strumenti da riga di comando per Xcode.

Seguite le ultime istruzioni dell'installazione di Homebrew, che configurano Homebrew per il vostro terminale aggiungendo codice al vostro `~/.zprofile`. Dovrebbe essere simile a questo (sostituite `foo` con il vostro nome utente):

```
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/foo/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

## Installazione delle dipendenze di Ink/Stitch

Ora possiamo installare le dipendenze di build di Ink/Stitch:

```
brew install python@3.9 gtk+3 pkg-config gobject-introspection geos libffi gettext pygobject3
```

Utilizzate il vostro editor di testo preferito per aggiungere la seguente riga a `~/.zprofile`:

```
export PATH=“$(brew --prefix)/opt/python@3.9/libexec/bin:$PATH”
```

Riavviate l'emulatore di terminale.

Scaricate il codice sorgente di Ink/Stitch e pyembroidery da GitHub e installate i pacchetti pip:

```
git clone https://github.com/inkstitch/inkstitch
git clone https://github.com/inkstitch/pyembroidery.git
python -m pip install -v —-upgrade pip
python -m pip install -r inkstitch/requirements.txt
python -m pip uninstall -y shapely
python -m pip cache remove shapely
python -m pip install -v shapely --no-binary shapely
python -m pip install pyinstaller
```

## Compilazione di Ink/Stitch

Ora Ink/Stitch è pronto per essere compilato.

Nella cartella inkstitch, eseguite:

```
make distlocal
```

In caso di successo, il pacchetto di installazione di Ink/Stitch si troverà in `inkstitch/artifacts`.

Per pulire la directory di inkstitch, eseguite:

```
make distclean
```