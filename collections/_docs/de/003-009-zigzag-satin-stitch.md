---
title: "Zick-Zack (Satin)"
permalink: /de/docs/stitches/zigzag-satin-stitch/
last_modified_at: 2024-05-22
toc: true
---
{% include upcoming_release.html %}

## Beschreibung

"Zick-Zack" ist eine Satinsäule mit einem Zick-Zack-Muster.

![Point Satin Zigzag](/assets/images/docs/en/compare-satin-zigzag.png)

## Funktionsweise

Bereite deinen Pfad genauso vor, wie du es für [Satinsäulen](/de/docs/stitches/satin-column) tun würdest. 
Dann aktiviere die Funktion "Zigzag" im [Parameter-Dialogfenster](/de/docs/params/#satinsäule). 

## Parameter

Einstellung||Beschreibung
---|---|---
Benutzerdefinierte Satinsäule       | ☑ |Muss aktiviert sein, damit diese Einstellungen wirksam werden.
Methode                             | |`Zigzag` auswählen
Kurzstich-Einzug                    | ![Short Stitch example](/assets/images/docs/params-satin-short_stitch_inset.png) | Stiche in Bereichen mit hoher Dichte werden um diesen Wert verkürzt (%)
Kurzstich-Dichte                    |![Short Stitch example](/assets/images/docs/params-satin-short_stitch_distance.png)  | Verkürzt Stiche falls der Abstand zwischen den Stichen schmaler als dieser Wert ist (mm).
Zick-Zack Abstand (Spitze zu Spitze)|![Zig-zag spacing example](/assets/images/docs/params-satin-zig-zag-spacing.png)|Spitze-zu-Spitze Abstand zwischen Zick-Zacks
Zugausgleich (%)                    |![Pull compensation example](/assets/images/docs/params-satin-pull_compensation.png)|Zusätzliche Zugkompensation, die als Prozentwert der ursprünglichen Breite variiert. Zwei durch ein Leerzeichen getrennte Werte können für einen asymmetrischen Effekt verwendet werden.
Zugausgleich                        |![Pull compensation example](/assets/images/docs/params-satin-pull_compensation.png)|Satinstiche [ziehen den Stoff zusammen](/tutorials/push-pull-compensation/), was zu einer Säule führt, die schmaler ist, als in Inkscape geplant. Diese Einstellung erweitert jedes Nadeleinstichpaar von der Mitte der Satinsäule nach außen. Es muss experimentell bestimmt werden, wie viel Kompensation für deine Kombination aus Stoff, Faden und Stabilisator benötigt wird. Zwei durch ein Leerzeichen getrennte Werte können für einen asymmetrischen Effekt genutzt werden
Konturlinien umkehren               |![Reverse Rung](/assets/images/docs/satin-reverse-rung.png) | Optionen:<br /> ◦ Automatisch, die Standardeinstellung dreht eigenständig gegenläufige Außenkonturen<br />◦ Nicht umkehren, deaktiviert automatisches drehen<br />◦ Erste Konturlinie umkehren<br />◦ Zweite Konturlinie umkehren <br />◦ Beide Konturlinien umkehren
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
Maximale Stichlänge                 | ![Maximum stitch length](/assets/images/docs/params-satin-maximum_stitch_length.png) | Stiche die diesen Wert übersteigen, werden geteilt.
Zwischenstich-Methode | Optionen:<br /> ◦ Standard  <br />◦ Einfach <br />◦ Stichversatz |![default](/assets/images/docs/param_split_satin_default.png) ![simple](/assets/images/docs/param_split_satin_simple.png) ![stager](/assets/images/docs/param_split_satin_stagered.png)
Randomisierte Zwischenstiche         |☑ | Kontrolliert ob die Zwischenstiche mittig liegen oder sich zufällig über die Stichkänge verteilen (dies kann ggf. die Stichanzahl erhöhen).
Stichversatz                         |![Stagger example](/assets/images/docs/params-fill-stagger.png) | Die Einstellung bestimmt, wie viele Reihen die Stiche voneinander entfernt sind, bevor sie in die gleiche Position münden.  Fractional values are allowed and can have less visible diagonals than integer values ** aktiv nur  mit "Stichversatz" Zwischenstich-Methode **
Minimale Stichlänge für randomisierte Zwischenstiche|  | Wenn leer, wird der Wert für die maximale Stichlänge verwendet. Kleinere Werte erlauben einen Übergang von Einzelstich zu Teilstich.
Zufallszahl                          | | Zufallswert für randomisierte Attribute. Falls leer wird die Element-ID verwendet.
{: .params-table }

Die Parametereinstellungen der Unterlagen unterscheiden sich nicht zu den [Parametern der Satinsäule](/de/docs/stitches/satin-column).

## Beispieldateien die Zigzag Satin stitch enthalten

{% include tutorials/tutorial_list key="stitch-type" value="zigzag-satin-stitch" %}


