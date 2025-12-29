---
title: "Troubleshoot Objects"
permalink: /de/docs/troubleshoot/
last_modified_at: 2024-05-09
toc: true
---
## Fehlerbehebung

Ink/Stitch kann verwirrend sein. Besonders für Anfänger. Aber auch, wenn du Ink/Stitch schon länger benutzt, erhälst du immer wieder Fehlermeldungen, die besagen, dass etwas schiefgelaufen ist und ein Objekt aus irgendeinem Grund nicht funktioniert.

Ink/Stitch hat ein Hilfsmittel diese Fehler verständlicher zu machen. Es zeigt die genaue Position wo das Problem liegt und erklärt wie man es lösen kann. Auch für problematische Objekte, die keine Fehlermeldung verursachen, können Warnhinweise angezeigt werden.

## Funktionsweise

* (Optional) Wähle die Objekte aus, die du testen möchtest. Ist kein Objekt ausgewählt, läuft der Test für das gesamte Dokument.
* Öffne `Erweiterungen > Ink/Stitch > Troubleshoot Objects`
* Chose what you want to detect among errors, warnings and object type warning.

Entweder erhälst du eine nun Nachricht, dass kein Fehler gefunden wurde oder es wird eine neue Ebene mit den Fehlerinformationen in das Dokument eingefügt. Nutze das Objekt-Panel (Strg + Shift + O) um diese Ebene nach der Fehlerbehebung wieder zu löschen.

![Troubleshoot Example](/assets/images/docs/de/troubleshoot.jpg)

**Tipp:** Es ist möglich, dass ein Objekt mehrere Fehler enthält. Objekte mit Füllstich zeigen aber in der Regel nur den zuerst aufgetretenen Fehler an. Nutze das Troubleshoot-Werkzeug erneut, wenn du weitere Fehlermeldungen erhälst.
{: .notice--info }

## Element Info

Diese Erweiterung sammelt Informationen über verschiedene Parameter für eine Auswahl von Stickobjekten.

![Element info](/assets/images/docs/en/element_info.png)

The 'Copy' button on the help tab allows you to copy all the information to the clipboard.

## Stickeinstellungen entfernen

Benutze diese Funktion um von Ink/Stitch gespeicherte Informationen aus deinem Dokument zu entfernen.
Das ist besonders dann nützlich, wenn du Objekte aus Stick-Projekten in andere Dateien zu kopieren.

Die Erweiterung entfernt alle Stickparameter aus dem gesamten Dokument oder von ausgewählten Objekten:
* Markiere die gewünschten Objekte
  (überspringe diesen Schritt, wenn du alle Stickinformationen aus dem gesamten Dokument entfernen willst)
* Öffne `Erweiterungen > Ink/Stitch > Fehlerbehebung > Entferne Stickeinstellungen...`
* Wähle die gewünschten Optionen und klicke auf "anwenden"

### Optionen

* Parameter entfernen
* Befehle entfernen

  (Alle/Keine/bestimmte Befehle)
* Druckeinstellungen aus den SVG Metadaten entfernen

![Stickeinstellungen entfernen - GUI](/assets/images/docs/en/remove-embroidery-settings.png)

## Dokument bereinigen

Manchmal entstehen während der Arbeit an SVG-Dateien sehr kleine Objekte, die gar nicht gewünscht sind (z.B. beim Bitmap-Tracing). Ink/Stitch bietet eine Funktion an, diese winzigen Objekte zu entfernen. So wird verhindert, dass sie Fehler in der Ausgabe produzieren.

* Öffne `Erweiterungen > Ink/Stitch > Fehlerbehebung > Dokument bereinigen...`
* Wähle welche Objekttypen behandlet werden sollen und definiere den Schwellwert
* `Anwenden`
* Leere Gruppen oder Ebenen können optional entfernt werden
* Bei aktiviertem Testdurchlauf werden lediglich die Namen der Elemente die entfernt werden würden angezeigt ohne sie zu entfernen

## Ink/Stitch SVG aktualisieren

Wird eine Datei, die mit einer älteren Version von Ink/Stitch erstellt wurde, geöffnet, aktualisiert Ink/Stitch diese Datei automatisch.

Ist eine Datei aber bereits als aktualisiert markiert, wird nicht erneut auf alte Elemente überprüft.
Sollten nun also Design-Elemente aus einer alten Datei in eine neue Datei hineinkopiert/importiert werden, kann es sein, dass einzelne Parameter nicht mehr richtig erkannt werden.

In diesem Fall kann ein manuelles Update für einzelne Elemente durchgeführt werden:

* Wähle die Elemente aus, die aktualisiert werden sollen.
* Führe die Funktion unter `Erweiterungen > Ink/Stitch > Fehlerbehebung > Ink/Stitch SVG aktualisieren` aus

**Tipp**: Diese Operation wird überflüssig, wenn auch in der Quelldatei der zu kopierenden Design-Elemente zuvor eine Ink/Stitch-Funktion ausgeführt wurde. Wähle hierzu einfach ein Element in der alten Datei aus, öffne die Parameter und klicke ohne Änderungen vorzunehmen aud `Anwenden und Schließen`.
{: .notice--info }
