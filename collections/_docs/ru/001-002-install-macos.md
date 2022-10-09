---
title: "Установка Ink/Stitch на macOS"
permalink: /ru/docs/install-macos/
excerpt: "Быстрая установка Ink/Stitch."
last_modified_at: 2021-12-02
toc: true
---
## Видео урок

У нас есть множество обучающих видео на нашем <i class="fab fa-youtube"></i> [YouTube канале](https://www.youtube.com/c/InkStitch). Посмотрите процесс установки расширения на <i class="fab fa-apple"></i> [macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3).

**Внимание:** Видео для пользователей macOS уже устарело. Прочтите актуальную информацию в разделе ["Дополнительные шаги для Catalina и Big Sur"](#дополнительные-шаги-для-catalina-и-big-sur)
{: .notice--warning }

## Скачать

Download the latest release for your macOS version.

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx.pkg" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download Ink/Stitch {{ site.github.latest_release.tag_name }} for macOS<br /><span style="color:lightblue;">Big Sur / Monterey</span></a></p>
<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-sierra-capitan-catalina-osx.pkg" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download Ink/Stitch {{ site.github.latest_release.tag_name }} for macOS<br><span style="color:lightblue;">El Capitan / Sierra / High Sierra / Mojave / Catalina</span></a></p>

**Последняя версия:**  [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }})](https://github.com/inkstitch/inkstitch/releases/latest)

## Запуск Ink/Stitch

Ink/Stitch is an Inkscape extension. Download and install [Inkscape](https://inkscape.org/release/) Version 1.0.2 or higher before you install Ink/Stitch.
**Make sure, that you have <span style="text-decoration:underline;">installed and run</span> Inkscape <span style="text-decoration:underline;">before</span> installing Ink/Stitch**. Otherwise the installation will fail.<br><br>
Please note, that Inkscape 1.2 will not work on **El Capitan** and **Sierra**. If you use these macOS versions, please install [Inkscape 1.1.2](https://inkscape.org/release/1.1.2/platforms/).
{: .notice--warning .bold--warning }

**Big Sur - Monterey:** Click on the downloaded file to run the installer.

**El Capitan - Catalina:** `Ctrl+Click` on the downloaded file and click on `Open`.

Click on `Continue`.

![Install Ink/Stitch](/assets/images/docs/en/macos-install/installer01.png)

Click on `Install`.

![Install Ink/Stitch](/assets/images/docs/en/macos-install/installer02.png)

A password prompt will open. Enter your user password and click on `Install Software`.

![Install Ink/Stitch](/assets/images/docs/en/macos-install/installer03.png)

In some cases your system will send a request, if you allow the installer to save files into your home directory. Ink/Stitch needs to be in the Inkscape extensions folder. Therefore answer this question with `Yes`.
{: .notice--info }

Your installation is now complete.

![Install Ink/Stitch](/assets/images/docs/en/macos-install/installer04.png)

Just one more question ...

Do you want to keep the downloaded installer file? This is up to you. Ink/Stitch doesn't need it anymore.

![Install Ink/Stitch](/assets/images/docs/en/macos-install/installer05.png)

## Run Ink/Stitch

Open Inkscape. You will find Ink/Stitch under `Extensions > Ink/Stitch`.

![Ink/Stitch menu](/assets/images/docs/ru/macos-install/inkstitch-extensions-menu.png)

## Обновление

When a new Ink/Stitch version is released, download it and run the installer as described above. It will remove the old Ink/Stitch version by itself.

Installs older than 2.1.0 need to be removed manually. Go to the extensions folder and remove your inkstitch installation before running the installer script.

**Совет:** Подпишитесь на канал новостей, чтобы быть в курсе обновлений Ink/Stitch:<br />
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Новые версии на GitHub](https://github.com/inkstitch/inkstitch/releases.atom)<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Новости Ink/Stitch](/feed.xml)<br />
{: .notice--info }

<p>Или следите за проектом на GitHub:<br /><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Решение проблем

### Приложение 'xxxx' нельзя открыть, так как не удалось проверить разработчика

This can happen, if you run a development build release.

`Ctrl+Click` on the downloaded file and click on `Open`.

### Installation fails

We also provide a zip download file which can be extraced in the the user extensions folder (see below: confirm installation path).

For Big Sur and Monterey [dowload ZIP]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx.zip)

For older macOS versions [download ZIP]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-capitan-cataline-osx.zip)

### Ink/Stitch не отображается / не доступен

**M1 processors (Apple Silicon Mac)**

Most common issue is a missing Rosetta installation. To fix the issue run this command in your terminal: `softwareupdate --install-rosetta --agree-to-license` 

**Проверьте путь установки**

Проверьте что вы распаковали архив с Ink/Stitch в правильную папку. Если с папкой `Пользовательские расширения` не удается добиться работы расширения, попробуйте распаковать архив в папку `Inkscape extensions`.
Её тоже можно найти через меню `Правка > Параметры > Система`.

**Проверьте версию Ink/Stitch**

Убедитесь, что вы скачали Ink/Stitch версию для macOS ([Скачать](#/ru/download))

### Я скачал Ink/Stitch на своем родном языке, но диалоговые окна отображаются на английском

**Незавершенный перевод**

Возможно не все строки были переведены. В этом случае вы будете видеть **одновременно уже переведенные строки на вашем языке и некоторые строки на английском языке**.
Если вы хотите дополнить или исправить перевод, посмотрите [описание для переводчиков](/ru/developers/localize/).

**Настройки языка**

Если Ink/Stitch не поддерживает язык ОС, то будет выбран английский язык для отображения.
Вы можете явно указать предпочитаемый язык в Inkscape:
  * Перейдите в меню Правка > Параметры > Интерфейс (Ctrl + Shift + P)
  * Установите нужный язык
  * Перезапустите Inkscape

![Preferences > Interface](/assets/images/docs/en/preferences_language.png)
