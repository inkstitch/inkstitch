---
title: "Esecuzione di Ink/Stitch dalla riga di comando"
permalink: /docs/command-line/
last_modified_at: 2024-07-13
---
Le estensioni Ink/Stitch possono essere eseguite dalla riga di comando.

## Esempio di codice per la riga di comando

### Esportazione in formato ZIP

Ad esempio, se si desidera esportare il file in un archivio ZIP (con file dst, pes e threadlist), è possibile eseguire il seguente comando:

```
./inkstitch --extension=zip --format-dst=True --format-pes=True --format-threadlist=True input-file.svg > output-file.zip
```

### Piano di cucitura

Ecco un esempio di come generare un file SVG per il piano di cucitura di due elementi specifici, che nasconderà i livelli originali del disegno, visualizzerà i punti dell'ago e sarà posizionato direttamente sopra il disegno originale.

```
./inkstitch --extension=stitch_plan_preview --id=path1 --id=path2 --move-to-side=False --layer-visibility=hidden --needle-points=True input.svg > output.svg
```

## Opzioni della riga di comando di Inkscape

Per un manuale completo delle opzioni della riga di comando di Inkscape, consultare la [pagina del manuale](https://inkscape.org/doc/inkscape-man.html).

Si prega di notare che è anche possibile utilizzare Ink/Stitch in combinazione con altre azioni di Inkscape. È possibile visualizzare l'elenco completo delle azioni disponibili tramite:

```
inkscape --action-list
```