---
title: "Installazione di più versioni"
permalink: /developers/inkstitch/multiversion/
last_modified_at: 2024-02-13
toc: true
---
L'installazione di più versioni di Ink/Stitch può essere molto utile durante lo sviluppo.

Questo semplifica l'esecuzione di test e il confronto tra versioni.

## Configurazione dei file di menu di Ink/Stitch

Per installare più versioni di Ink/Stitch, i file di menu di Inkscape devono avere un ID univoco.

Ecco un esempio di come utilizzare due estensioni Ink/Stitch:

- installare Inkstitch in due posizioni diverse (ad esempio, _inkstitch_ e _inkstitch-k_).
- assicurarsi che il comando `make inx` venga eseguito in entrambe le posizioni (questo genererà anche i file in `inx/locale/`).
- nella seconda posizione, generare file inx modificati: `generate-inx-files -a k`.
- installare i file inx nella directory delle estensioni di Inkscape:
  - creare un collegamento simbolico `.config/inkscape/extensions/inkstitch   -> inkstitch`.
  - creare un collegamento simbolico `.config/inkscape/extensions/inkstitch-k -> inkstitch-k`.
- modificare il file `.config/inkscape/keys/default.xml` se necessario.
- avviare Inkscape con entrambe le estensioni Inkstitch abilitate:
  - prima versione: `Estensioni > Ink/Stitch`.
  - seconda versione: `Estensioni > Ink/Stitch-k`.