---
title: "Installazione manuale: sistemi macOS più vecchi"
permalink: /developers/inkstitch/manual-build-old-macos/
last_modified_at: 2024-10-01
toc: true
---
Questa è una guida per la compilazione locale di Ink/Stitch. L'installazione manuale per gli sviluppatori è descritta nella [sezione di configurazione manuale](/developers/inkstitch/manual-setup/).
{: .notice--info}

## Requisiti per la compilazione

* MacPorts

  Si consiglia di utilizzare [macports](https://www.macports.org/) sui sistemi macOS più vecchi. Imposta il flag `-b` per installare pacchetti binari precompilati per velocizzare il processo.
* Strumenti da riga di comando per Mojave
* pyenv (vedi sotto)

Inoltre, durante il processo di compilazione, è necessario installare i seguenti pacchetti:

```
sudo port -v -b install gtk-devel libffi geos gettext gobject-introspection pkgconfig tcl curl sqlite3 readline
```

### Installazione di pyenv

Clona il repository pyenv:

```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

Compila pyenv:

```
cd ~/.pyenv && src/configure && make -C src
cd ..
```

Esegui questi comandi per far funzionare pyenv nel tuo terminale:

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
```

Per rendere effettive queste modifiche, esegui:

```
exec "$SHELL"
```

Compila Python:

```
env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install -v 3.8.9
```

Imposta la versione:

```
pyenv global 3.8.9
```

### Installazione delle dipendenze di Ink/Stitch

Aggiorna il gestore pip:

```
python -m pip install -v —-upgrade pip
```

Installa i pacchetti pip per ottenere inkstitch da GitHub:

```
git clone https://github.com/inkstitch/inkstitch
git clone https://github.com/inkstitch/pyembroidery.git
python -m pip install -r inkstitch/requirements.txt
python -m pip uninstall -y shapely
python -m pip cache remove shapely
python -m pip install -v shapely --no-binary shapely
python -m pip install pyinstaller
```

## Installazione manuale

Da questo punto in poi, è possibile procedere con un'installazione manuale. Consulta la [guida alla configurazione manuale](/developers/inkstitch/manual-setup/) sul sito web. Continua dal passaggio 4.

## Compilazione di Ink/Stitch

Ora Ink/Stitch è pronto per essere compilato.

Nella cartella inkstitch, esegui:

```
make distlocal
```

In caso di successo, il pacchetto di installazione di Ink/Stitch si troverà nella cartella `inkstitch/artifacts`.

Per pulire la directory di inkstitch, esegui:

```
make distclean
```