---
title: "Manualle Installation"
permalink: /de/developers/inkstitch/manual-setup/
last_modified_at: 2019-05-05
toc: false
---
Eine manuelle Installation ermöglicht es am Quellcode zu arbeiten, während du Ink/Stitch benutzt.

1. Klone die Erweiterung und aktualisiere das Submodul pyembroidery

    ```
    git clone https://github.com/inkstitch/inkstitch
    cd inkstitch
    git submodule init
    git submodule update
    ```
2.  Installiere Python Abhängigkeiten

    Es werden ein paar Python Module gebraucht. In einigen Fällen benutzt Ink/Stitch Funktionen, die nicht automatisch durch die Distributionen mit Python mitgeliefert werden.
    Deshalb empfehlen wir sie mit pip zu installieren:

    ```
    pip2 install -r requirements.txt
    ```

    **Info:** Evtl. musst du auf einigen Plattformen wxPython entfernen und ein platform-spezifisches Paket [installieren](https://wiki.wxpython.org/How%20to%20install%20wxPython):<br />
       ⚫ Debian `python-wxgtk3.0`<br />
       ⚫ Ubuntu 16.04: `pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython`
    {: .notice--info }
 
    **Info:** Wenn du nur Python 2 installiert hast, kannst du evtl. auch einfach `pip` anstelle von `pip2` benutzen.
    {: .notice--info }

3.  Installiere Abhängigkeiten für Electron

    Die grafische Oberfläche von Ink/Stitch nutzt Electron.  Dazu brauchst du eine funktionsfähige Installation von NodeJS (Version 10 oder höher).  Sofern nicht vorhanden, installiere yarn mit `npm install yarn`.

    Installiere Electron mit den dazugehörigen Abhängigkeiten wie folgt:

    ```
    cd electron
    yarn install
    ```

4.  INX-Dateien vorbereiten

    ```
    make inx
    ```

    This will create `*.inx` files for each locale in `inx/<locale>`.

5.  Symbolische Links in den Inkscape extensions-Order setzen

    ```
    cd ~/.config/inkscape/extensions
    ln -s /path/to/inkstitch
    for i in inkstitch/inx/de_DE/inkstitch_*.inx; do ln -s $i; done;
    ln -s inkstitch/inkstitch.py
    ```

    Um eine andere Sprache im Ink/Stitch-Menü zu nutzen, ersetze `de_DE` mit einer anderen Sprache aus dem Ordner `inx/`.
    Ink/Stich Dialoge außerhalb von Inkscape nutzen die Systemsprache.

6.  Inkscape starten

    **Info:** Wenn Ink/Stitch `ImportError: No module named shapely` ausgibt, dann ist es gut möglich, dass Inkscape eine andere Python Version benutzt,
    als die in den installierten Abängigkeiten. Konfiguriere in Inkscape die Ausführungsdatei für Python in `preferences.xml`.
    Der Speicherort für `preferences.xml` kann in Inkscape unter `Bearbeiten > Einstellungen > System > Benutzereinstellungen` eingesehen werden.
    *Schließe Inkscape bevor du diese Datei bearbeitest*, anderenfalls wird sie beim Schließen von Inkscape wieder überschrieben.<br /><br />
    In `preferences.xml` aktualisiere `group id="extensions" \>` mit dem richtigen Python interpreter. Zum Beispiel,<br /><br />
    `<group id="extensions" python-interpreter="/usr/local/bin/python2" />`<br/><br/>
    wobei, `/usr/local/bin/python2` der Rückgabewert von `which python2` ist.
    {: .notice--warning }

**Info:** Änderungen am Python-Code werden wirksam, sobald die Erweiterung das nächste Mal gestartet wird. Änderungen an den Inkscape-Menü Dateien (`*.inx`) zeigen sich erst, nachdem Inkscape neu gestartet wurde.
{: .notice--info }
