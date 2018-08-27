---
title: "Kontur Parameter"
permalink: /docs/stitches/stroke/
excerpt: ""
last_modified_at: 2018-08-26
toc: true
---
![Stichtyp - Kontur](/assets/images/docs/stitch-type-stroke.jpg)

Wähle eine Linie aus und öffne `Erweiterungen -> Ink/Stitch -> Parameter`.

![Kontur Parameter](/assets/images/docs/params-stroke.jpg)

Einstellung|Beschreibung
---|---
Satinstich entlang von Pfaden         | Muss aktiviert sein, damit diese Einstellungen wirksam werden.
Manuelle Stichplatzierung             | Aktiviere [Manueller Stichmodus] (#manual-stitch-mode)
Wiederholungen                        | ◦ Legt fest, wie oft der Pfad durchlaufen und zurücklaufen soll<br/>◦ Standard: 1 (einmal vom Anfang bis zum Ende des Pfades)<br/>◦ Ungerade Zahl: Stiche enden am Ende des Pfades<br/>◦ Gerade Zahl: Die Naht kehrt zum Anfang des Pfades zurück
Bean stitch Anzahl der Wiederholungen | ◦ Jeden Stich vervielfachen.<br/>◦ Ein Wert von 1 würde jeden Stich verdreifachen (vorwärts, rückwärts, vorwärts).<br/>◦ Ein Wert von 2 würde jeden Stich fünffach ausführen, usw.<br/>◦ Gilt nur für den Laufstich.
Laufstichlänge                        | Länge der Stiche im [Laufstich-Modus](#running-stitch-mode)
Zick-Zack Abstand (Spitze zu Spitze)  | ◦ Stichlänge im [Zig-Zag Modus](#zig-zag-stitch-mode-previously-simple-satin)<br>◦ Die Höhe wird durch die Linienbreite definiert
STOP (danach), TRIM (danach)          | [STOP after](/docs/params/#stop-after), [TRIM after](/docs/params/#trim-after)


**Info:** Wenn ein Objekt aus mehreren Pfaden besteht, werden diese der Reihe nach mit einem Sprung zwischen ihnen verknüpft.
{: .notice--info }

## Laufstich Modus

[![Laufstich Butterfly](/assets/images/docs/running-stitch.jpg){: width="200x"}](/assets/images/docs/running-stitch.svg){: title="Download SVG Datei" .align-left download="running-stitch.svg" }

Ein Laufstich kann erstellt werden, indem ein **gestrichelte Linie** auf einem Pfad plaziert wird. Jede Art von gestrichelten Linien kan verwendet werden, dabei ist die Linienbreite irrelevant.

Gehe zu `Objekt -> Füllung und Kontur ...` oder benutze `Umschalt + Strg + F` und wähle eine der gestrichelten Linien in der Registerkarte `Muster der Kontur`.

**Info:** Um das Abrunden der Ecken zu vermeiden, wird an den scharfen Ecken ein zusätzlicher Stich hinzugefügt.
{: .notice--info style="clear: both;" }

**Sample inklusive Laufstich**
{% include tutorial_list key="stitch-type" value="Running Stitch" %}

## Bean Stitch Modus

Bean Stitch beschreibt Wiederholungen von Laufstichen in den Richtungen vor und zurück. Dies führt zu einem dickeren Ergebnis.

Stelle im Laufstichmodus die Anzahl der Wiederholungen in `Anzhal der Wiederholungen` ein.
Ein Wert von 1 würde jeden Stich verdreifachen (vorwärts, rückwärts, vorwärts).
Ein Wert von 2 würde jeden Stich verfünffachen, usw.

## Manueller Stich Modus

[![Manueller Stich Blumen](/assets/images/docs/manual-stitch.jpg){: width="200x"}](/assets/images/docs/manual-stitch.svg){: title="Download SVG-Datei" .align-left download="manual-stitch.svg" }

Aktiviere `Manuelle Stichplatzierung`, um den manuellen Stichmodus zu verwenden. Linienstil oder die Linienbreite sind irrelevant. Im manuellen Stichmodus verwendet Ink/Stitch jeden Knoten eines Pfades als Nadeleinstichpunkt genau so, wie er platziert wurde. Hinweis: Es werden keine Tie-In oder Tie-Off Stiche automatisch hinzugefügt. Achte daher darauf, diese innerhalb des Pfades zu erstellen.

**Sample inklusive Manueller Stich**
{: style="clear: both;" }
{% include tutorial_list key="stitch-type" value="Manual Stitch" %}

## Zick-Zack Modus (vormals Simple Satin)
Zick-Zack-Stiche können durch Setzen einer **durchgehenden Linie** (ohne gestrichelte Linie) erstellt werden. Mit Ink/Stich werden Stiche entlang des Pfads mit der angegebenen Linienbreite erstellt.

Gehe zu `Objekt -> Füllung und Kontur ...` oder benutze `Umschalt + Strg + F` und stelle die gewünschte Linienbreite auf der Registerkarte `Muster der Kontur` ein.

**Info:** Es wird nicht empfohlen, den Zick-Zack-Modus zu verwenden, um einen Satinkolumne zu erstellen, benutze stattdessen eine [Satinkolumne](/docs/stitches/satin/).<br /><br />
Ink/Stitch zeichnet Zick-Zacks von Anfang bis Ende und von rechts nach link einer Linie, aber es macht nichts besonderes mit Kurven und Ecken. Schärfere Kurven und Ecken führen zu dürftigen Nähten an der Außenseite der Kurve und zu dichten Nähten an der Innenseite. Dies sieht nicht gut aus und kann sogar Löcher in den Innenseiten der Ecken erzeugen.<br /><br />
{: .notice--warning }

**Info:** Dies kann festgestellt werden, wenn die Linienbreite Fehler aufweist, wenn die Viewbox eine unterschiedliche Skalierung für X und Y hat - oder das Objekt (oder eine seiner Elterngruppen) das Attribut `transform` hat (was leicht passieren kann, wenn die Größe einer Gruppe in Inkscape geändert wurde).<br/><br/>
Benutze stattdessen eine [Satinkolumne](/docs/stitches/satin/).
{: .notice--warning }
