---
title: "Установка Ink/Stitch на Windows"
permalink: /ru/docs/install-windows/
excerpt: "Быстрая установка Ink/Stitch."
last_modified_at: 2021-12-02
toc: true
---
## Видео урок

У нас есть множество обучающих видео на нашем <i class="fab fa-youtube"></i> [YouTube канале](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw). Посмотрите процесс установки расширения на <i class="fab fa-windows"></i> [Windows](https://www.youtube.com/watch?v=U5htzWZSjA8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=4).

## Требования

* [Inkscape](https://inkscape.org/release/) Версия 1.0.2 или выше

Это все что вам нужно. Все необходимые библиотеки и внешние зависимости поставляются вместе с расширением, благодаря прекрасной утилите [pyinstaller](http://www.pyinstaller.org).

## Установка

### Скачать
Загрузите архив с расширением на нужном языке:
* <i class="fa fa-download " ></i> [Русский]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-ru_RU.zip)
* <i class="fa fa-download " ></i> [Английский]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-en_US.zip)
* <i class="fa fa-download " ></i> [Финский]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-fi_FI.zip)
* <i class="fa fa-download " ></i> [Французский]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-fr_FR.zip)
* <i class="fa fa-download " ></i> [Немецкий]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-de_DE.zip)
* <i class="fa fa-download " ></i> [Итальянский]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-it_IT.zip)
* <i class="fa fa-download " ></i> [Японский]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-ja_JP.zip)
* <i class="fa fa-download " ></i> [Нидерландский]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-nl_NL.zip)


**Последняя версия:** {{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

Выбранный выше язык влияет только на показ пунктов меню в Inkscape. Диалоги Ink/Stitch будут отображены на языке вашей ОС независимо от выбранного файла загрузки(если этот язык поддерживается).<br><br>Для вашего языка нет расширения? Помогите нам [перевести диалоги на ваш родной язык](/ru/developers/localize/).
{: .notice--info }


### Распаковка файлов

Перейдите в `Правка > Параметры > Система` и найдите путь до вашей папки `Пользовательских расширений`.

![Preferences: Extensions Folder](/assets/images/docs/en/extensions-folder-location-win.jpg)

Этот путь будет похож на `C:\Users\%USERNAME%\AppData\Roaming\inkscape\extensions`

Распакуйте архив с Ink/Stitch прямо в эту папку.

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
