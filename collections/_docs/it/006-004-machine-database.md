---
title: "Database delle macchine"
permalink: /docs/machine-database/
last_modified_at: 2020-04-12
classes: wide

inkstitch-formats:
 - read: 100, 10o, BRO, DAT, DSB, DST, DSZ, EMD, EXP, EXY, FXY, GT, INB, JEF, JPX, KSM, MAX, MIT, NEW, PCD, PCM, PCQ, PCS, PEC, PES, PHB, PHC, SEW, SHV, STC, STX, TAP, TBF, TXT, G-CODE, U01, VP3, XXX, ZXY
   write: CSV, DST, EXP, JEF, PEC, PES, SVG, TXT, G-CODE, U01, VP3

machine-database:
  - brand: Janome
    machines:
    - name: Memory Craft 400E
      file-formats: JEF, DST, DAT
      features: TRIM
      inkstitch-version: 1.27.2
      comments:
    - name: Memory Craft 550E
      file-formats: JEF, JEF+, JPX
      features:
      inkstitch-version: 2.20.0
      comments: prossimamente
  - brand: Brother
    machines:
    - name: Innov-is F560
      file-formats: PMV
      features: My Custom Stitch
      inkstitch-version: 3.2.2
      comments: Problemi minori con il conteggio dei punti, l'allineamento e la scala, ma possono essere risolti. <br><a href="https://github.com/inkstitch/inkstitch/pull/3929#issuecomment-3211128167">Ulteriori informazioni</a>
    - name: PE-800
      file-formats: PES, PEC, DST
      features:
      features: TRIM
      inkstitch-version: 1.28
      comments: Disabilitare la casella di controllo "ties" nei parametri, perché questa macchina aggiunge automaticamente i legami.

headlines:
  - machine: "Macchina"
  - file-formats: "Formati di file"
  - features: "Caratteristiche"
  - inkstitch-version: "Testato con la versione di Ink/Stitch"
  - comments: "Commenti"

---
**Nota:** Come puoi vedere, questo database è solo in fase di pianificazione. Non prendere i dati sul serio in questo momento.
{: .notice--warning }

{% include machine-list %}
