---
title: "Vernähstiche"
permalink: /de/docs/stitches/lock-stitches/
last_modified_at: 2023-02-27
toc: true
---
An- und Verstecher sind kleine Stiche am Anfang (Anstecher) oder am Ende (Verstecher) eines Farbblocks oder vor und nach einem Sprungstich oder Fadenschnitt-Befehl. Sie helfen den Faden zu sichern.

Ink/Stitch bietet verschiedene Vernähstich-Typen an und erlaubt sogar die Definition eigener Vernähstiche.

Ink/Stitch allows you to add trim commands

*  either as a visual command  using  Extension < Ink/Stitch < Commands < Attach commands to selected objects
* or by ckecking "Trim after" in the parameters dialog
  
The embroidery file contains several embroidery objects that will be embroidered one after another. 

When the distance between the end of an object and the begining of the next one is larger than the  "minimum  jump stitch length"  as defined in Extension > Ink/Stitch > Preferences, then there is a jump in between the objects. In that  case,   lock stitches are added  at the end of the first object and tack stitches at the begining of the second one except if their respective  "allow lock stitches" parameter do not  allow one (or both) of them.

If this distance is smaller thant the "minimum jump stitch length", then the needle move to go from first object to second object is not a jump, but a regular stitch and no tack down stitches is added to the first object and no lock stitches to the second one, regardless t their respective "allow lock stitch parameter" value.

It is however possible to force small distance jumps to have  lock and tack stitches. Check the "force lock stitch" parameter of the **before jump** object to add lock stitches before jump and tack stitches after jump. This overides the "allow lock stitches"  parameters. Beware not to check "force lock stitch" on  the after jump object, as you would then force the "lock stitches" for it, not the "tack stitches", plus you would force lock stitches for next object, whatever its distance from after jump object.

## Standart-Vernähstiche

![Lock stitch variants](/assets/images/docs/lock-stitches.png)
{: .img-half }

1. Halbstich. Dies ist der Standartwert und die einzige Option für Vernähstiche älterer Ink/Stitch Versionen. Eine Skalierung ist nicht möglich, da sich dieser Stich an der Stichlänge des Elements orientiert: zwei halbe Stiche zurück, zwei halbe Stiche nach vorn.
2. Pfeil, skaliert in %
3. Vor und zurück, skaliert in mm
4. Schleife, skaliert in %
5. Kreuz, skaliert in %
6. Stern, skaliert in %
7. Dreieck, skaliert in %
8. Zick-Zack, skaliert in %
9. Benutzerdefiniert. Skaliert in % oder mm abhängig von der eingegebenen Pfad-Variante.

## Benutzerdefinierte Vernähstiche

Benutzerdefinierte Vernähstiche können entweder als SVG-Pfad definiert werden (skaliert in %) oder durch relative Schritte die sich nach der mm Angabe skalieren.

### Benutzerdefinierter SVG-Pfad

Der SVG-Pfad wird immer so abgebildet, als ob er ein Pfad für einen Anstecher ist. Wird er als Verstecher genutzt dreht sich der Pfad automatisch um. Der letzte Knoten des Pfades wird nicht gestickt, sondern dient lediglich als Richtungsangabe wie sich der Pfad an den Ursprungspfad anschließen soll.

or instance the triangle lock stitches corresponds to the custom path  M -0.26,0.33 H 0.55 L 0,0.84 V 0 L 0.34,0.82 (this is the d attribute of the path). 
On next image, this are the black paths, on one copy its last segment is colored green for clarity.

![Triangle lock stitch](/assets/images/docs/triangle_lock.png)

Both red and blue path have a triangle tack down.

The custom svg path is rotated in such away that its last segment (green) has the same direction as the begining of red and blue paths. It is only used to compute this rotation angle, and is not part of the actual tack down, and will not be embroidered.


### Benutzerdefinierter Pfad in mm

Benutzerdefinierte Werte für die absolute Skalierung in mm werden mit einem Leerzeichen getrennt. Beispielsweise wird ein Pfad mit den Werten 1 1 -1 -1 und einer Skalierungsangabe von 0.7 mm zweimal 0.7 mm vorwärts wandern und zweimal 0.7 mm rückwärts. Dezimalwerth-Angaben sind möglich (z.B. 0.5 2.2 -0.5 - 2.2).
