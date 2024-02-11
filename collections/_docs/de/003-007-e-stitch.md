---
title: "E-Stich"
permalink: /de/docs/stitches/e-stitch/
last_modified_at: 2023-04-22
toc: true
---
## Beschreibung

[![E-Stitch Dolphin](/assets/images/docs/e-stitch-example.jpg){: width="200x"}](/assets/images/docs/e-stitch.svg){: title="Download SVG File" .align-left download="e-stitch.svg" }
E-Stich dient als einfacher (und doch festem) Deckstich für Applikationen. Er ist besonders geeignet für Baby-Kleidung, da ihre Haut besonders empfindlich ist.

![E-Stitch Detail](/assets/images/docs/e-stitch-detail.jpg)

## Funktionsweise

Bereite deinen Pfad genauso vor, wie du es für [Satinsäulen](/de/docs/stitches/satin-column) tun würdest. Dann aktiviere die Funktion "E Stich" im [Parameter-Dialogfenster](/de/docs/params/#satinsäule). Gleichzeitig macht es Sinn, den Wert "Zick-Zack Abstand" für diese Stichart zu erhöhen.

**Tipp:** Sollten die Spitzen in die falsche Richtung zeigen, benutze einfach das Werkzeug ["Satinsäule umkehren"](/de/docs/satin-tools/#satinsäule-umkehren), bzw. aktiviere die Option "Seiten umkehren" in den Parametereinstellungen.
{: .notice--info }

## Parameter

Einstellung||Beschreibung
---|---|---
Benutzerdefinierte Satinsäule       | ☑ |Muss aktiviert sein, damit diese Einstellungen wirksam werden.
Methode                             | |`E-Stich` auswählen
Maximale Stichlänge                 | ![Maximum stitch length](/assets/images/docs/params-satin-maximum_stitch_length.png) | Stiche die diesen Wert übersteigen, werden geteilt.
Kurzstich-Einzug                    | | Stiche in Bereichen mit hoher Dichte werden um diesen Wert verkürzt (%)
Kurzstich-Dichte                    | | Verkürzt Stiche falls der Abstand zwischen den Stichen schmaler als dieser Wert ist (mm).
Zick-Zack Abstand (Spitze zu Spitze)|![Zig-zag spacing example](/assets/images/docs/params-satin-zig-zag-spacing.png)|Spitze-zu-Spitze Abstand zwischen Zick-Zacks
Zugausgleich (%)                    |![Pull compensation example](/assets/images/docs/params-satin-pull_compensation.png)|Zusätzliche Zugkompensation, die als Prozentwert der ursprünglichen Breite variiert. Zwei durch ein Leerzeichen getrennte Werte können für einen asymmetrischen Effekt verwendet werden.
Zugausgleich                        |![Pull compensation example](/assets/images/docs/params-satin-pull_compensation.png)|Satinstiche [ziehen den Stoff zusammen](/tutorials/push-pull-compensation/), was zu einer Säule führt, die schmaler ist, als in Inkscape geplant. Diese Einstellung erweitert jedes Nadeleinstichpaar von der Mitte der Satinsäule nach außen. Es muss experimentell bestimmt werden, wie viel Kompensation für deine Kombination aus Stoff, Faden und Stabilisator benötigt wird. Zwei durch ein Leerzeichen getrennte Werte können für einen asymmetrischen Effekt genutzt werden
Eine Seite umkehren                 |![Reverse Rung](/assets/images/docs/satin-reverse-rung.png) | Diese Einstellung kann helfen eine Satinsäule zu reparieren, die seltsam aussieht (siehe Bild).
Seiten umkehren                     | | Kehrt die Seiten der Satinsäule um (links und rechts). Dies beeinflusst z.B. an welcher Seite der Faden startet und endet. Aber auch jede andere seitenbezogene Einstellung ist hiervon betroffen.
Vernähen erlauben                   | |Vernäht bei Bedarf an den ausgewählten Positionen
Vernähen erzwingen                  | |Vernäht den Faden nach diesem Element, auch dann, wenn der Abstand zum Folgeobjekt geringer ist als in den [Ink/Stitch Einstellungen](/de/docs/preferences/) definiert.
Anstecher                           | |Wähle die [Anstecher](/de/docs/stitches/lock-stitches) Variante (Anfang).
Verstecher                          | |Wähle die [Verstecher](/de/docs/stitches/lock-stitches) Variante (Ende).
Fadenschnitt                        | |Schneidet den Faden nachdem dieses Objekt genäht wurde
Stopp                               | |Stoppt die Maschine nachdem dieses Objekt genäht wurde und springt zur Stopp-Position (sofern vorhanden)
Zufälliger Prozentwert (Erweitern)  |![Random width increase](/assets/images/docs/params-satin-random-width-increase.png)| Lengthen stitch across rails at most this percent. Two values separated by a space may be used for an aysmmetric effect.
Zufälliger Prozentwert (Verkleinern)|![Random width decrease](/assets/images/docs/params-satin-random-width-decrease.png)| Shorten stitch across rails at most this percent. Two values separated by a space may be used for an aysmmetric effect.
Zufallswert Zick-Zack-Abstand (Prozent)|![Random zigzag spacing](/assets/images/docs/params-satin-random-zigzag-spacing.png)| Maximale randomisierte Abweichung der Stichabstände in Prozent
Zufälliges Zittern für Zwischenstiche|![Random split stitch jitter](/assets/images/docs/params-satin-random-split-stitch-jitter.png)| Wenn die Option für randomisierte Zwischenstiche aktiviert ist, wird die Stichlänge für Zwischenstiche randomisiert. Ist die Option deaktiviert, bezieht sich der Wert auf die Zwischenstich-Positionen
Randomisierte Zwischenstiche         |☑ | Kontrolliert ob die Zwischenstiche mittig liegen oder sich zufällig über die Stichkänge verteilen (dies kann ggf. die Stichanzahl erhöhen).
Minimale Stichlänge für randomisierte Zwischenstiche|  | Wenn leer, wird der Wert für die maximale Stichlänge verwendet. Kleinere Werte erlauben einen Übergang von Einzelstich zu Teilstich.
Zufallszahl                          | | Zufallswert für randomisierte Attribute. Falls leer wird die Element-ID verwendet.
{: .params-table }

Die Parametereinstellungen der Unterlagen unterscheiden sich nicht zu den [Parametern der Satinsäule](/de/docs/stitches/satin-column).

## Beispieldateien die E-Stich enthalten

{% include tutorials/tutorial_list key="stichart" value="E-Stich" %}

