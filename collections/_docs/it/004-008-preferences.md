---
title: "Preferenze"
permalink: /docs/preferences/
last_modified_at: 2026-04-06
toc: true
---
Le preferenze si trovano in `Estensioni > Ink/Stitch > Preferenze`.

È possibile impostare valori globali che verranno applicati a ogni nuovo documento SVG, oppure impostare valori specifici per il documento che sovrascriveranno i valori globali.
Se si sceglie un valore locale come predefinito, questo imposterà il valore globale al valore locale.

**Tutti gli elementi del documento sono influenzati da questi parametri.**

## Impostazioni di output

### Lunghezza minima del punto di cucitura (mm)

Se la distanza tra due percorsi consecutivi è inferiore a questo valore, i punti di blocco alla fine del primo percorso e i punti di ancoraggio all'inizio del secondo percorso vengono creati solo se *Forza i punti di blocco* è abilitato nel percorso corrispondente. Se la distanza è maggiore, i punti di blocco e i punti di ancoraggio sono conformi alle loro impostazioni.

A partire dalla versione 3.1.0, è possibile sovrascrivere il valore globale per singoli elementi nel [dialogo dei parametri](/doc/params).

### Lunghezza minima del punto (mm)

#### Creazione

I punti più piccoli di questo valore verranno eliminati (eccezione: punti di blocco). Questo valore viene utilizzato solo alla fine del calcolo del piano di cucitura per filtrare i punti troppo corti. Si prega di notare che il comportamento potrebbe non essere quello previsto: ad esempio, se la lunghezza minima del punto è impostata su 2 mm e si hanno punti di cucitura diritti con una lunghezza massima del punto di 1,5 mm, ogni altro punto viene eliminato, con conseguente percorso di cucitura diritto con punti di 3 mm.

La simulazione tiene conto di questi parametri.

Questi sono i risultati della simulazione per punti di cucitura dritti con una *lunghezza minima del punto* impostata su 0,5 mm nelle preferenze e poi impostata su 2 mm.

![simulazione](/assets/images/docs/preference_msl_paths.png)

Quando la *lunghezza minima del punto* è impostata su 2 mm, tranne per i punti di blocco, ogni altro punto viene eliminato, poiché 1,5 è inferiore a 2 e 1,5 + 1,5 è maggiore di 2. Il numero di punti viene dimezzato. Se impostassimo la *lunghezza minima del punto* su 3,1, otterremmo punti di cucitura dritti da 4,5 mm.

A partire dalla versione 3.1.0, è possibile sovrascrivere il valore globale per singoli elementi nel [dialogo dei parametri](/doc/params).

#### Effetto sull'arricciatura

La *lunghezza minima del punto* influisce anche sui **lati dei riempimenti** (in modo simile alla funzione "salta l'ultimo punto della riga", che è una buona opzione per i riempimenti densi) se impostata su un valore inferiore alla *distanza tra le righe*. Influisce anche sugli **angoli acuti** dei punti di cucitura dritti, dove la lunghezza effettiva del punto potrebbe essere molto inferiore alla *lunghezza del punto di cucitura diritto* (la tolleranza è importante in questo caso).

| *Lunghezza minima del punto* | Riempimento automatico con distanza tra le righe di 0,25 | Riempimento guidato con distanza tra le righe di 0,25 | Lunghezza del punto di cucitura diritto di 1,5 mm ma disegno molto piccolo (10 mm di larghezza) |
---|---|---|---|
0 | ![quadrato 0](/assets/images/docs/preference_fill_0.png) | ![quadrato 0](/assets/images/docs/preference_guided_0.png) | ![punto](/assets/images/docs/preference_running_stitch_0.png) |
0,5 | ![quadrato 0,5](/assets/images/docs/preference_fill_half.png) | ![quadrato 0,5](/assets/images/docs/preference_guided_half.png) | ![punto](/assets/images/docs/preference_running_stitch_half.png) |
1 | ![quadrato 1](/assets/images/docs/preference_fill_1.png) | ![quadrato 1](/assets/images/docs/preference_guided_1.png) | ![punto](/assets/images/docs/preference_running_stitch_1.png) |

Influisce anche sui **punti di raso** e quindi sui font. Non si desidera che ciò accada con **font piccoli** come *Ink/Stitch Small* o *Glacial Tiny*:

| *Lunghezza minima del punto* | *Ink/Stitch Small* | *Glacial Tiny* |
---|---|---|
0 o 0,5 | ![ink_stitch_O](/assets/images/docs/preference_ink_small_0.png) | ![glacial_O](/assets/images/docs/preference_glacial_0.png) |
1 | ![ink_stitch_1](/assets/images/docs/preference_ink_small_1.png) | ![glacial_1](/assets/images/docs/preference_glacial_1.png) |

I **punti manuali** sono anch'essi influenzati dalla preferenza della lunghezza minima del punto. È possibile sfruttare questo aspetto per ridurre il numero di punti manuali senza ottenere punti molto corti. Potrebbe verificarsi una certa deformazione, ma di solito il risultato è piuttosto buono.

**Proprietari di macchine W6:** Impostare il valore globale della lunghezza minima del punto almeno a 0,3 mm, altrimenti la cucitura potrebbe avere punti mancanti in luoghi in cui non ce lo si aspetterebbe.
{: .notice--warning }

### Larghezza minima del punto di raso

{% include upcoming_release.html %}

Se un tratto può essere renderizzato come punto di raso dipende dalla larghezza del tratto e da questo valore di preferenza per la larghezza minima del punto di raso.
La larghezza del tratto deve essere maggiore dell'impostazione della preferenza, altrimenti questo elemento verrà trattato come un punto di cucitura diritto.

Per evitare di creare punti duri, si consiglia di utilizzare solo punti di raso più larghi di 1 mm. L'uso di fili sottili è un'eccezione a questa regola.

### Solo per questo documento: Ruota all'esportazione

{% include upcoming_release.html %}

Questa opzione ruota il ricamo di 90°. È utile quando la macchina da ricamo non ruota automaticamente per adattarsi al telaio.

### Solo globale: Dimensione della cache (mb)

Definisce lo spazio sull'unità disco rigida che può essere occupato dai piani di cucitura memorizzati nella cache.

Più alto è il valore, più piani di cucitura possono essere memorizzati nella cache.

Un piano di cucitura memorizzato nella cache non deve essere renderizzato di nuovo, il che velocizza notevolmente i tempi di rendering.

Il valore predefinito è 100.

È possibile cancellare la cache dalle preferenze globali.