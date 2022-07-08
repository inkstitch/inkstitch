---
title: "Установка Ink/Stitch на Windows"
permalink: /ru/docs/install-windows/
excerpt: "Быстрая установка Ink/Stitch."
last_modified_at: 2021-12-02
toc: true
---
{% comment %}
## Видео урок

У нас есть множество обучающих видео на нашем <i class="fab fa-youtube"></i> [YouTube канале](https://www.youtube.com/c/InkStitch). Посмотрите процесс установки расширения на <i class="fab fa-windows"></i> [Windows](https://www.youtube.com/watch?v=U5htzWZSjA8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=4).
{% endcomment %}

## Требования

Ink/Stitch is an Inkscape extension. Download and install [Inkscape](https://inkscape.org/release/) Версия 1.0.2 или выше before you install Ink/Stitch.

## Скачать

Download the latest release.

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows.exe" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download Ink/Stitch {{ site.github.latest_release.tag_name }} for Windows</a></p>

**Последняя версия:** {{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

## Запуск Ink/Stitch

Double click to execute the downloaded file.

Until our windows certificate gained enough trust, you will need to allow the installer script to run.

Click on `More info`.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer01.png)

Now click on the additional option `Run anyway`.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer02.png)

Ink/Stitch needs to be installed into the Inkscape extensions folder. The path is already set for you. Click on `Next`.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer03.png)

Since you have Inkscape installed, the extensions folder already exists. Confirm that you want to install into this folder and click on `Yes`.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer04.png)

The installer will show you a summary of the installation settings. Click on `Install`.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer05.png)

Ink/Stitch is now installed on your computer.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer06.png)

## Run Ink/Stitch

Open Inkscape. You will find Ink/Stitch under `Extensions > Ink/Stitch`.

![Ink/Stitch menu](/assets/images/docs/en/windows-install/inkstitch-extensions-menu.png)

## Uninstall Ink/Stitch

### Uninstall Ink/Stitch versions up from v2.1.0

Open the start menu in Windows. Click on `Settings`.

![Uninstall Ink/Stitch](/assets/images/docs/en/windows-install/uninstall01.png)

Click on `Apps`.

![Uninstall Ink/Stitch](/assets/images/docs/en/windows-install/uninstall02.png)

In `Apps & features` scroll down until you find Ink/Stitch.
Click on `Ink/Stitch` and an uninstall button appears. Click on `Uninstall`.

![Uninstall Ink/Stitch](/assets/images/docs/en/windows-install/uninstall03.png)

Confirm that you want to uninstall Ink/Stitch.

![Uninstall Ink/Stitch](/assets/images/docs/en/windows-install/uninstall04.png)

Ink/Stitch has been removed from your computer. Click `Ok`.

![Uninstall Ink/Stitch](/assets/images/docs/en/windows-install/uninstall05.png)

### Uninstall Ink/Stitch versions older than v2.1.0

Go to `Edit > Preferences > System` and open your extensions folder.

![Inkscape extensions folder](/assets/images/docs/en/extensions-folder-location-win.jpg)

Remove each inkstitch* file and folder.

## Get informed about Ink/Stitch updates

Subscribe to a news feed channel to keep track on Ink/Stitch Updates.

* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News (Website)](/feed.xml)<br />
* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [New Releases on GitHub](https://github.com/inkstitch/inkstitch/releases.atom)<br>

<p>Alternatively watch all project activity on GitHub: <iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Обновление

Subscribe to a news feed channel to keep track on Ink/Stitch Updates.

* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Новости Ink/Stitch](/feed.xml)
* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Новые версии на GitHub](https://github.com/inkstitch/inkstitch/releases.atom)

<p>Или следите за проектом на GitHub:<br /><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Решение проблем

### Ink/Stitch не отображается / не доступен

**Проверьте путь установки**

Проверьте что вы распаковали архив с Ink/Stitch в правильную папку. Если с папкой `Пользовательские расширения` не удается добиться работы расширения, попробуйте распаковать архив в папку `Inkscape extensions`.
Её тоже можно найти через меню `Правка > Параметры > Система`.

**Антивирусное ПО**

Поскольку Ink/Stitch упакован в исполняемый файл, некоторые антивирусные программы могут пометить этот файл как потенциалььно опасный. В этом случае добавьте папку с расширением Ink/Stitch в список сисключений антивирусной программы, затем переустановите Ink/Stitch и попроуйте снова.

Если ваше антивирусное ПО удалит какие-либо файлы расширения, то вы будете видеть сообщения об ошибке, похожие на это:

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

**Проверьте версию Ink/Stitch**

Убедитесь, что вы скачали Ink/Stitch версию для Windows ([Скачать](#/ru/download))

### Windows 8: Error message

![The program can't start because api-ms-win-crt-math-l1-1-1-0.dll is missing from your computer. Try reinstalling the program to fix this problem](/assets/images/docs/en/windows-install/win8.png)
{: .img-half }
![Error loading Python DLL 'C:\Users\...\AppData\Roaming\inkscape\extensions\inkstitch\inkstitch\bin\python38.dll'. LoadLibrary: The specified module could not be found.](/assets/images/docs/en/windows-install/win8a.png)
{: .img-half }

If you come across these two error messages on Windows 8, download and install [Microsoft Visual C++ Redistributable packages](https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2015-2017-2019-and-2022). Choose the file for your system architecture.

### Я скачал Ink/Stitch на своем родном языке, но диалоговые окна отображаются на английском

**Незавершенный перевод**

Возможно не все строки были переведены. В этом случае вы будете видеть **одновременно уже переведенные строки на вашем языке и некоторые строки на английском языке**.
Если вы хотите дополнить или исправить перевод, посмотрите [описание для переводчиков](/ru/developers/localize/).

**Настройки языка**

Есть некоторое различие между отображением языка в меню и в диалоговых окнах. Выбор нужного ZIP-архива влияет только на язык опций в меню.
Диалоговые окна собираются по-другому. В них будет отображаться текст на языке вашей операционной системы.
Если Ink/Stitch не поддерживает язык ОС, то будет выбран английский язык для отображения.
Вы можете явно указать предпочитаемый язык в Inkscape:
  * Перейдите в меню Правка > Параметры > Интерфейс (Ctrl + Shift + P)
  * Установите нужный язык
  * Перезапустите Inkscape

![Preferences > Interface](/assets/images/docs/en/preferences_language.png)
