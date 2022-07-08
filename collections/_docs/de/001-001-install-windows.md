---
title: "Installation von Ink/Stitch für Windows"
permalink: /de/docs/install-windows/
excerpt: "Wie wird Ink/Stitch installiert."
last_modified_at: 2022-04-25
toc: true
---
{% comment %}
## Video-Anleitung

Wir stellen Anfänger-Tutorials auf unserem <i class="fab fa-youtube"></i> [YouTube Kanal](https://www.youtube.com/c/InkStitch) zur Verfügung. Die Videos sind in englischer Sprache. Deutsche Untertitel können zugeschaltet werden. Schaue den Installationsprozess für <i class="fab fa-windows"></i> [Windows](https://www.youtube.com/watch?v=U5htzWZSjA8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=4) an.
{% endcomment %}

## Vorraussetzung

Ink/Stitch ist eine Inkscape Erweiterung. Installiere [Inkscape](https://inkscape.org/release/) Version 1.0.2 oder höher, bevor du Ink/Stitch installierst.

## Herunterladen

Lade die neueste Ink/Stitch Version herunter.

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows.exe" class="btn btn--primary btn--large"><i class="fa fa-download " ></i> Download Ink/Stitch {{ site.github.latest_release.tag_name }} für Windows</a></p>

**Aktuelle Version:** {{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

## Installation

Öffne das Ink/Stitch Installationsprogramm mit einem Doppelklick.

Bis unser Windows Zertifikat genügend Vertrauen erhalten hat, musst du der Ausführung des Installations-Skripts explizit zustimmen.

Klicke auf `Weitere Informationen`

![Ink/Stitch installer](/assets/images/docs/de/windows-install/installer01.png)

Jetzt klicke auf die Zusatzoption `Trotzdem ausführen`.

![Ink/Stitch installer](/assets/images/docs/de/windows-install/installer02.png)

Ink/Stitch muss in den Ordner für Inkscape Erweiterungen installiert werden. Der richtige Pfad ist bereits eingestellt. Klicke auf `Weiter`.

![Ink/Stitch installer](/assets/images/docs/de/windows-install/installer03.png)

Da Inkscape bereits installiert ist, gibt es den Installationsordner bereits. Bestätige, dass du Ink/Stitch in diesen Ordner installieren willst mit `Ja`.

![Ink/Stitch installer](/assets/images/docs/de/windows-install/installer04.png)

Das Installationsprogramm zeigt nun eine Zusammenfassung der Installationseinstellungen. Klicke auf `Installieren`.

![Ink/Stitch installer](/assets/images/docs/de/windows-install/installer05.png)

Ink/Stitch ist jetzt auf deinem Computer installiert.

![Ink/Stitch installer](/assets/images/docs/de/windows-install/installer06.png)

## Ink/Stitch ausführen

Öffne Inkscape. Du findest Ink/Stitch unter `Erweiterungen > Ink/Stitch`.

![Ink/Stitch menu](/assets/images/docs/de/windows-install/inkstitch-extensions-menu.png)

## Ink/Stitch deinstallieren

### Entferne Ink/Stitch Versionen ab v2.1.0

Öffne das Start-Menü in Windows. Klicke auf `Einstellungen`.

![Uninstall Ink/Stitch](/assets/images/docs/de/windows-install/uninstall01.png)

Klicke auf `Apps`.

![Uninstall Ink/Stitch](/assets/images/docs/de/windows-install/uninstall02.png)

Scrolle in `Apps und Features` nach unten bis du Ink/Stitch findest.
Klicke auf `Ink/Stitch` die Schaltfläche `Deinstallieren` wird sichtbar. Klicke darauf.

![Uninstall Ink/Stitch](/assets/images/docs/de/windows-install/uninstall03.png)

Bestätige, dass du Ink/Stitch entfernen willst.

![Uninstall Ink/Stitch](/assets/images/docs/de/windows-install/uninstall04.png)

Ink/Stitch wurde von deinem Computer entfernt. Klicke auf `Ok`.

![Uninstall Ink/Stitch](/assets/images/docs/de/windows-install/uninstall05.png)

### Entferne Ink/Stitch Versionen älter als v2.1.0

Öffne den Ordner für Inkscape Erweiterungen. Unter `Bearbeiten > Einstellungen > System > Benutzererweiterungen` kannst du einsehen, wo dieser sich befindet.

![Inkscape extensions folder](/assets/images/docs/de/extensions-folder-location-windows.jpg)

Entferne alle Dateien und Ordner die mit `inkstitch` beginnen.

## Informiere dich über Ink/Stitch Updates

Abonniere den News-Feed-Kanal um über Ink/Stitch updates informiert zu werden.

* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch Neuigkeiten (Webseite)](/feed.xml)<br />
* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Neue Versionen auf GitHub](https://github.com/inkstitch/inkstitch/releases.atom)<br>

<p>Alternativ kann auch die gesamte Programmentwicklung auf GitHub mitverfolgt werden: <iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Fehlerbehebung

### Ink/Stitch startet nicht / Menüpunkte sind grau

**Ink/Stitch-Version überprüfen**

Bitte überprüfe noch einmal, ob du die richtige Ink/Stitch Version für dein Betriebssytsem heruntergeladen hast.
Für Windows findest du den Download-Link unter [Herunterladen](#herunterladen) oben auf dieser Seite.

### Windows 8: Fehlermeldung

![The program can't start because api-ms-win-crt-math-l1-1-1-0.dll is missing from your computer. Try reinstalling the program to fix this problem](/assets/images/docs/en/windows-install/win8.png)
{: .img-half }
![Error loading Python DLL 'C:\Users\...\AppData\Roaming\inkscape\extensions\inkstitch\inkstitch\bin\python38.dll'. LoadLibrary: The specified module could not be found.](/assets/images/docs/en/windows-install/win8a.png)
{: .img-half }

Wenn du diesen beiden Fehlermeldungen auf Windows 8 begegnest, lade die [Microsoft Visual C++ Redistributable packages](https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2015-2017-2019-and-2022) herunter und installiere sie. Wähle die richtige Version für deine Systemarchitektur.

**Virus-Software**

Windows-Nutzer haben oft das Problem, dass Anti-Viren-Programme die Datei `inkstitch/inkstitch.py` als Virus erkennen und dementsprechend vom System entfernen.
Die Lösung für dieses Problem ist es, eine Ausnahme für den Ordner mit den Ink/Stitch-Dateien hinzuzufügen. Installiere Ink/Stitch anschließend erneut.

Die Fehlermeldung in so einem Fall würde in etwa so aussehen:

```
Tried to launch: inkstitch\bin\inkstitch
Arguments: ['inkstitch\bin\inkstitch', '--id=XXX', '--extension=XXX', 'C:\Users\XXX\AppData\Local\Temp\ink_ext_XXXXXX.svgXXXXX']
Debugging information:

Traceback (most recent call last):
File "inkstitch.py", line 35, in
extension = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
File "C:\Program Files\Inkscape\lib\python2.7/subprocess.py", line 325, in init
errread, errwrite)
File "C:\Program Files\Inkscape\lib\python2.7/subprocess.py", line 575, in _execute_child
startupinfo)
WindowsError: [Error 2] The system cannot find the file specified
```

**Installationspfad überprüfen**

Überprüfe, ob die Dateien evtl. in einen *Unterordner* extrahiert wurden.
Es ist wichtig, dass die Ink/Stitch-Dateien **direkt** in dem Ordner "Benutzererweiterungen" sind.

### PYTHONPATH

Es gab einige Bericht über Fehlermeldungen die so wie diese hier beginnen:

```
Python path configuration:
PYTHONHOME = 'C:\Users\{username}\AppData\Roaming\inkscape\extensions\inkstitch\bin'
PYTHONPATH = (not set)
```

Installiere Inkscape erneut. Stelle sicher, dass die Checkbox "Zu Pfad hinzufügen" (Add to path) aktiviert ist, wenn die Frage nach PYTHONPATH während der Installation auftaucht.

### Windows 7: Fehlermeldung

Wenn du die folgende Fehlermeldung erhälst, installiere bitte die Microsoft Windows Sicherheitsupdates auf deinem Computer.

```
Traceback (most recent call last):
File "Lib\site-packages\PyInstaller\hooks\rthooks\pyi_rth_multiprocessing.py", line 12, in
File "PyInstaller\loader\pyimod03_importers.py", line 495, in exec_module
File "multiprocessing_init_.py", line 16, in
File "PyInstaller\loader\pyimod03_importers.py", line 495, in exec_module
File "multiprocessing\context.py", line 6, in
File "PyInstaller\loader\pyimod03_importers.py", line 495, in exec_module
File "multiprocessing\reduction.py", line 16, in
File "PyInstaller\loader\pyimod03_importers.py", line 495, in exec_module
File "socket.py", line 49, in
ImportError: DLL load failed while importing _socket: Paramètre incorrect.
```

### Windows 8: Fehlermeldung

![The program can't start because api-ms-win-crt-math-l1-1-1-0.dll is missing from your computer. Try reinstalling the program to fix this problem](/assets/images/docs/en/windows-install/win8.png)
{: .img-half }
![Error loading Python DLL 'C:\Users\...\AppData\Roaming\inkscape\extensions\inkstitch\inkstitch\bin\python38.dll'. LoadLibrary: The specified module could not be found.](/assets/images/docs/en/windows-install/win8a.png)
{: .img-half }

Wenn diese beiden Fehlermeldungen bei einer Windows 8 installation auftauchen, bitte [Microsoft Visual C++ Redistributable packages](https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2015-2017-2019-and-2022) herunterladen und installieren. Wähle die passende Datei für dein System.

### Ink/Stitch wird auf englisch angezeigt

**Unvollständige Übersetzung**

Es möglich, dass die Übersetzung unvollständig ist. Das erkennt man daran, dass in einem Fenster sowohl englische, als auch anderssprachige Texte erscheinen.
Wenn du helfen willst, die Übersetzung zu vervollständigen, lese unsere [Beschreibung für Übersetzer](/de/developers/localize/).


**Spracheinstellungen**

Ink/Stitch wird bei unklarar Spracheinstellung immer auf die englisch Standardsprache zurückgreifen.
In Inkscape kann die Spracheinstellung manuell angepasst werden:
  * Öffne Bearbeiten > Einstellungen > Benutzeroberfläche (Strg + Shift + P)
  * Wähle deine Sprache
  * Schließe Inkscape und starte es erneut

![Einstellungen > Benutzeroberfläche](/assets/images/docs/de/preferences_language.png)
