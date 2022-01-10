---
title: "Установка Ink/Stitch на Linux"
permalink: /ru/docs/install-linux/
excerpt: "Быстрая установка Ink/Stitch."
last_modified_at: 2021-12-02
toc: true
---
## Видео урок

У нас есть множество обучающих видео на нашем <i class="fab fa-youtube"></i> [YouTube канале](https://www.youtube.com/c/InkStitch). Посмотрите процесс установки расширения на <i class="fab fa-linux"></i> [Linux](https://www.youtube.com/watch?v=Dkb5UvsZUNg&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=2).

## Требования

* [Inkscape](https://inkscape.org/release/) Версия 1.0.2 или выше

Это все что вам нужно. Все необходимые библиотеки и внешние зависимости поставляются вместе с расширением, благодаря прекрасной утилите [pyinstaller](http://www.pyinstaller.org).

## Установка

### Скачать
Download the latest release archive.

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux.zip" class="btn btn--info btn--large">Download Ink/Stitch {{ site.github.latest_release.tag_name }} for Linux</a></p>

**Последняя версия:** {{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

### Распаковка файлов

Перейдите в `Правка > Параметры > Система` и найдите путь до вашей папки `Пользовательских расширений`.

![Extensions folder location](/assets/images/docs/en/extensions-folder-location-linux.jpg)

Распакуйте архив с Ink/Stitch прямо в эту папку.

```
$ cd ~/.config/inkscape/extensions
$ unzip ~/Downloads/inkstitch-{{ site.github.latest_release.tag_name }}-linux-en_US.zip
```

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

Убедитесь, что вы скачали Ink/Stitch версию для Linux ([Скачать](#/ru/download))

**Проверьте владельца/права**

Некоторые пользователи сообщали, что у файлов были неверные права, препятствующие запуску расширения.

### AttributeError: 'NoneType' object has no attribute 'title' in inkstitch.py

Такая ошибка может возникать у пользователей, которые установили Inkscape через snap. Работа Ink/Stitch в Inkscape из Snap это известная проблема и решения пока нет.
Просто поробуйте другой метод установки Inkscape. Подойдет любой из лписанных на сайте [https://inkscape.org/](https://inkscape.org/releases/latest/). 

### Диалоги Ink/Stitch пропадают через несколько секунд

Эта проблема может быть вызвана wayland. Запустите Inkscape такой командой: `export GDK_BACKEND=x11 && inkscape`.

Это решение можно использовать до тех пор пока мы не переведем все приложения Ink/Stitch на electron. 

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
