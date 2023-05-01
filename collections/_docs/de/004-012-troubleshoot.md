---
title: "Troubleshoot Objects"
permalink: /de/docs/troubleshoot/
excerpt: ""
last_modified_at: 2020-04-27
toc: false
---
## Fehlerbehebung

Ink/Stitch kann verwirrend sein. Besonders für Anfänger. Aber auch, wenn du Ink/Stitch schon länger benutzt, erhälst du immer wieder Fehlermeldungen, die besagen, dass etwas schiefgelaufen ist und ein Objekt aus irgendeinem Grund nicht funktioniert.

Ink/Stitch hat ein Hilfsmittel diese Fehler verständlicher zu machen. Es zeigt die genaue Position wo das Problem liegt und erklärt wie man es lösen kann. Auch für problematische Objekte, die keine Fehlermeldung verursachen, können Warnhinweise angezeigt werden.

## Funktionsweise

* (Optional) Wähle die Objekte aus, die du testen möchtest. Ist kein Objekt ausgewählt, läuft der Test für das gesamte Dokument.
* Öffne `Erweiterungen > Ink/Stitch > Troubleshoot Objects`

Entweder erhälst du eine nun Nachricht, dass kein Fehler gefunden wurde oder es wird eine neue Ebene mit den Fehlerinformationen in das Dokument eingefügt. Nutze das Objekt-Panel (Strg + Shift + O) um diese Ebene nach der Fehlerbehebung wieder zu löschen.

![Troubleshoot Example](/assets/images/docs/de/troubleshoot.jpg)

**Tipp:** Es ist möglich, dass ein Objekt mehrere Fehler enthält. Objekte mit Füllstich zeigen aber in der Regel nur den zuerst aufgetretenen Fehler an. Nutze das Troubleshoot-Werkzeug erneut, wenn du weitere Fehlermeldungen erhälst.
{: .notice--info }


## Stickeinstellungen entfernen

Benutze diese Funktion um von Ink/Stitch gespeicherte Informationen aus deinem Dokument zu entfernen.
Das ist besonders dann nützlich, wenn du Objekte aus Stick-Projekten in andere Dateien zu kopieren.

Die Erweiterung entfernt alle Stickparameter aus dem gesamten Dokument oder von ausgewählten Objekten:
* Markiere die gewünschten Objekte
  (überspringe diesen Schritt, wenn du alle Stickinformationen aus dem gesamten Dokument entfernen willst)
* Öffne `Erweiterungen > Ink/Stitch > Fehlerbehebung > Entferne Stickeinstellungen...`
* Wähle die gewünschten Optionen und klicke auf "anwenden"

![Remove embroidery settings - GUI](/assets/images/docs/en/remove-embroidery-settings.png)

## Dokument bereinigen

Manchmal entstehen während der Arbeit an SVG-Dateien sehr kleine Objekte, die gar nicht gewünscht sind (z.B. beim Bitmap-Tracing). Ink/Stitch bietet eine Funktion an, diese winzigen Objekte zu entfernen. So wird verhindert, dass sie Fehler in der Ausgabe produzieren.

* Öffne `Erweiterungen > Ink/Stitch > Fehlerbehebung > Dokument bereinigen...`
* Wähle welche Objekttypen behandlet werden sollen und definiere den Schwellwert
* Anwenden

## Update Ink/Stitch svg

If you open a file created with an older version of Ink/Stitch you may need to update it:
* Select all objects
* Run `Extensions > Ink/Stitch > Troubleshoot > Update Ink/Stitch svg`

If you import an older file as part of a new file,  or copy/paste from an old file to a new one, you should
* Select all old objects
* Run `Extensions > Ink/Stitch > Troubleshoot > Update Ink/Stitch svg`


