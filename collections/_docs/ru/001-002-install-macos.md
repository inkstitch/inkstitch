---
title: "Установка Ink/Stitch на macOS"
permalink: /ru/docs/install-macos/
excerpt: "Быстрая установка Ink/Stitch."
last_modified_at: 2021-12-02
toc: true
---
## Видео урок

У нас есть множество обучающих видео на нашем <i class="fab fa-youtube"></i> [YouTube канале](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw). Посмотрите процесс установки расширения на <i class="fab fa-apple"></i> [macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3).

**Внимание:** Видео для пользователей macOS уже устарело. Прочтите актуальную информацию в разделе ["Дополнительные шаги для Catalina и Big Sur"](#дополнительные-шаги-для-catalina-и-big-sur)
{: .notice--warning }

## Требования

* [Inkscape](https://inkscape.org/release/) Версия 1.0.2 или выше

Это все что вам нужно. Все необходимые библиотеки и внешние зависимости поставляются вместе с расширением, благодаря прекрасной утилите [pyinstaller](http://www.pyinstaller.org).

## Установка

### Скачать
Загрузите архив с расширением на нужном языке:

Язык| Catalina & Big Sur | High Sierra & Mojave | Sierra & El Capitan
---|---|---|---
**Русский** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-ru_RU.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-ru_RU.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-ru_RU.zip)|
{: .inline-table }
**Английский** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-en_US.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-en_US.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-en_US.zip)|
**Финский** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fi_FI.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-fi_FI.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-fi_FI.zip)|
**Французский** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fr_FR.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-fr_FR.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-fr_FR.zip)|
**Итальянский** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-it_IT.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-it_IT.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-it_IT.zip)|
**Японский** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-ja_JP.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-ja_JP.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-ja_JP.zip)|
**Немецкий** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-de_DE.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-de_DE.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-de_DE.zip)|
**Нидерландский** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-nl_NL.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-nl_NL.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-nl_NL.zip)|

**Последняя версия:**  [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }})](https://github.com/inkstitch/inkstitch/releases/latest)

Выбранный выше язык влияет только на показ пунктов меню в Inkscape. Диалоги Ink/Stitch будут отображены на языке вашей ОС независимо от выбранного файла загрузки(если этот язык поддерживается).<br><br>Для вашего языка нет расширения? Помогите нам [перевести диалоги на ваш родной язык](/ru/developers/localize/).
{: .notice--info }

### Распаковка файлов

Перейдите в `Правка > Параметры > Система` и найдите путь до вашей папки `Пользовательских расширений`.

![Preferences: Extensions Folder](/assets/images/docs/en/extensions-folder-location-macos.jpg)
  
Распакуйте архив с Ink/Stitch прямо в эту папку.

### Дополнительный шаги для Catalina и Big Sur

Новые версии macOS блокируют Ink/Stitch, если он скачан браузером. Вы получите сообщение такого вида: `Приложение 'xxxx' нельзя открыть, так как не удалось проверить разработчика`.

Для обхода этого сообщения запустите приложение Терминал. Кликинте по иконке с лупой на панели меню в правом верхнем углу (или нажмите <key>Command (⌘)</key>+<key>Пробел</key>). Найдите `Терминал` и откройте приложение.

В терминале введите такую команду:

```
xattr -r -d com.apple.quarantine ~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/
```

Замените `~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/` на верный путь, если ваша папка расширений Inkscape находится в другом месте (можно уточнить в меню `Правка > Параметры > Система`).

### Запуск Ink/Stitch

Перезапустите Inkscape.

Теперь Ink/Stitch будет доступен через меню `Расширения > Ink/Stitch`.

## Обновление

Сначала нужно убрать все файлы расширения текущей версии. Зайдите в папку расширений и удалите все файлы и папки, которые начинаются с inkstitch*.

Затем повторите шаги как при установке расширения с нуля.

**Совет:** Подпишитесь на канал новостей, чтобы быть в курсе обновлений Ink/Stitch:<br />
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Новые версии на GitHub](https://github.com/inkstitch/inkstitch/releases.atom)<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Новости Ink/Stitch](/feed.xml)<br />
{: .notice--info }

<p class="notice--info" style="margin-top: -3.5em !important;">Или следите за проектом на GitHub:<br /><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Решение проблем

### Ink/Stitch не отображается / не доступен

**Проверьте путь установки**

Проверьте что вы распаковали архив с Ink/Stitch в правильную папку. Если с папкой `Пользовательские расширения` не удается добиться работы расширения, попробуйте распаковать архив в папку `Inkscape extensions`.
Её тоже можно найти через меню `Правка > Параметры > Система`.

**Проверьте версию Ink/Stitch**

Убедитесь, что вы скачали Ink/Stitch версию для macOS ([Скачать](#/ru/download))

### Приложение 'xxxx' нельзя открыть, так как не удалось проверить разработчика

Прочтите ["Дополнительные шаги для Catalina и Big Sur"](#дополнительные-шаги-для-catalina-и-big-sur).

### ValueError: Null geometry supports no operations

Ink/Stitch на macOS может показывать такую ошибку:  `[...] ValueError: Null geometry supports no operations`.

Эта ошибка вызвана несовместимостью встроенной библиотеки shapely speedups, которая включена в Ink/Stitch.
Для возобновления работы Ink/Stitch, удалите библиотеку следующим образом:

* Откройте папку где установлен Ink/Stitch (обычно это: `~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/`)
* Если есть подпапка для Ink/Stitch откройте её
* Зажмите `Ctrl` при клике на файле приложения inkstitch и выберите `Показать Содержимое Пакета` 

  ![Show Package Contents](/assets/images/docs/en/macOS-nogeometry.png)

* Зайдите в папку `Contents > MacOS` и удалите папку с именем `shapely`

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
