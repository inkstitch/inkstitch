---
title: "Personalizzare Ink/Stitch"
permalink: /docs/customize/
last_modified_at: 2026-01-03
toc: true
---

## Scorciatoie

È possibile velocizzare il lavoro in Ink/Stitch assegnando delle scorciatoie. Queste scorciatoie riducono la navigazione nei menu e supportano un flusso di lavoro più efficiente. Queste scorciatoie si concentrano su azioni specifiche per l'embroidery e su regolazioni comuni del layout, contribuendo a rendere il lavoro in Ink/Stitch più fluido.

L'elenco seguente descrive le scorciatoie incluse nel file scaricabile.

Diverse scorciatoie sostituiscono le impostazioni predefinite di Inkscape. Le alternative nei menu o nelle barre degli strumenti rimangono disponibili per tali azioni.
{: .notice--warning }

| Tasti di scelta rapida | Effetto | Sostituisce |
|-------------|--------|----------|
| PageUp | Sposta verso l'alto | Oggetto > Alza. I pulsanti nella barra degli strumenti si applicano anche |
| PageDown | Sposta verso il basso | Oggetto > Abbassa. I pulsanti nella barra degli strumenti si applicano anche |
| Ctrl + R | Inverte la direzione di un percorso | |
| Ctrl + Shift + ' | Ridisponi gli oggetti in base all'ordine di selezione | |
| Ctrl + Shift + P | Apri le Preferenze | Modifica > Preferenze |
| Ctrl + Shift + L | Apri la simulazione live | |
| Ctrl + Shift + > | Anteprima del piano di cucitura accanto alla tela | Percorso > Divisione. Usa Ctrl + / al posto |
| Ctrl + Shift + O | Separa gli oggetti di riempimento | Oggetto > Proprietà dell'oggetto |
| Ctrl + Shift + I | Esporta in PDF | |
| Ctrl + Shift + Q | Inserimento di testo | Oggetto > Seleziona e CSS |
| Ctrl + Shift + Canc | Risoluzione dei problemi degli oggetti e rimozione degli errori | |
| Ctrl + Shift + ! | Associa comandi agli oggetti selezionati | |
| Ctrl + Shift + U | Converti il tratto in satin | Oggetto > Raggruppa. Usa Ctrl + G al posto |
| Ctrl + Shift + J | Inverti le barre della colonna satin | |
| Ctrl + Shift + B | Taglia la colonna satin | Percorso > Unione. Usa Ctrl + + al posto |
| Ctrl + Shift + = | Instrada automaticamente gli oggetti satin | |


Il [simulatore](/docs/visualize/#simulation-shortcut-keys) di Ink/Stitch offre anche tasti di scelta rapida.

\* **Sposta verso l'alto** e **Sposta verso il basso** offrono un controllo preciso sull'ordine dei punti. Questo funziona bene con il pannello degli oggetti (`Oggetto > Oggetti...`). L'ordine di sovrapposizione determina la sequenza in cui gli elementi vengono cuciti, a partire dal basso e spostandosi verso l'alto.<br><br>** Per gli oggetti satin e a punto reazionario, questo cambia la direzione del punto. Questo funziona meglio quando è selezionata l'opzione **Mostra la direzione del percorso sui contorni** in `Modifica > Preferenze > Strumenti > Nodo`. Quando viene selezionato un vertice in modalità modifica nodo e viene premuto `Ctrl+R`, Inkscape inverte un sottopercorso all'interno di un oggetto. Questo aiuta ad allineare entrambe le barre di un satin in modo che puntino nella stessa direzione.
{: .notice--info }
{: style="font-size: 70%" }

### Scarica e importa le scorciatoie personalizzate

* [Scarica il file delle scorciatoie di Ink/Stitch](/assets/files/inkstitch.xml)
* Vai a `Modifica > Preferenze > Interfaccia > Tastiera`
* Clicca su `Importa...`
* Seleziona e apri il file scaricato

Ora potrai utilizzare le scorciatoie. Sono incluse nel file delle scorciatoie predefinito standard.

Se desideri definire le tue scorciatoie personalizzate, inserisci semplicemente le combinazioni di tasti desiderate nella finestra di dialogo delle scorciatoie.
Utilizza la funzione di ricerca per trovare le estensioni più rapidamente. [Ulteriori informazioni](http://wiki.inkscape.org/wiki/index.php/Customizing_Inkscape)
{: .notice--info }

## Preferenze di Inkscape
Raccomandiamo le seguenti preferenze di Inkscape:
### Strumenti
#### Bounding Box
Si consiglia di lavorare con bounding box geometrici in modo che le dimensioni dell'oggetto non tengano conto dello spessore dei contorni.

#### Abilitazione dei contorni e della direzione

Conoscere le direzioni dei percorsi è importante quando si lavora con Ink/Stitch. Si consiglia di abilitare le caselle di controllo **Mostra la direzione del percorso sui contorni** e **Mostra il contorno temporaneo per i percorsi selezionati** in `Modifica > Preferenze > Strumenti > Nodo`.

Assicurati che anche **Mostra il contorno del percorso** sia abilitato nella `Barra di controllo degli strumenti`, come puoi vedere nell'immagine sottostante.

[![Contorni e direzioni](/assets/images/docs/en/customize-path-outlines.png)](#)

#### Strumenti, Stili degli strumenti di disegno

È utile definire gli stili degli strumenti matita e penna impostando:
- la barra di controllo degli strumenti (menu Mostra/Nascondi)
- lo strumento matita o penna
- un oggetto creato con questo strumento che ha lo stile desiderato per lo strumento
- fare doppio clic sullo stile dello strumento visualizzato a destra della barra di controllo dello strumento per aprire le preferenze
- fare clic su "Acquisisci stile dalla selezione"

### Interfaccia
Lingua: scegli la tua lingua e non l'impostazione predefinita del sistema. Altrimenti, i menu di ink/stitch non verranno tradotti correttamente.

#### Fattore di correzione dello zoom

Per l'embroidery, è essenziale avere un'idea delle dimensioni reali del disegno. Inkscape ha un'impostazione per adattare i livelli di zoom alle dimensioni del tuo display.

* Vai a `Modifica > Preferenze > Interfaccia`
* Tieni un righello sullo schermo e regola lo slider finché la lunghezza corrisponde

![Correzione dello zoom](/assets/images/docs/en/customize-zoom-correction.png)


#### Posizione dell'origine
Per un utilizzo più semplice delle griglie di punto croce, si consiglia di selezionare "Origine nell'angolo in alto a sinistra, asse y rivolto verso il basso".

### Comportamento
#### Soglia di semplificazione
Il valore predefinito della soglia di semplificazione nella scheda Comportamento è un po' aggressivo. Ridurlo a 0.001 ti permetterà di semplificare i tuoi percorsi con meno effetti sulla loro forma.

#### Clonazioni
Per un corretto utilizzo dei comandi di ink/stitch, è necessario selezionare la casella "Collega le clonazioni duplicate".

### Input/Output
In Auto-salvataggio, abilita l'auto-salvataggio.


## Griglie

Per allineare correttamente le forme vettoriali, puoi utilizzare la funzionalità della griglia di Inkscape. Vai su `Visualizza` e abilita `Griglia di pagina`. Nella `Barra di controllo dello snapping` assicurati che `Snappa alle griglie` sia abilitato. È anche possibile regolare la spaziatura e l'origine delle griglie in `File > Proprietà del documento > Griglie`.

![Griglie](https://user-images.githubusercontent.com/11083514/40359052-414d3554-5db9-11e8-8b49-3be75c5e9732.png)

## Lavorare con i modelli

Se decidi di utilizzare Ink/Stitch più frequentemente, potresti stancarti di creare ripetutamente le stesse configurazioni. Puoi creare un modello per la tua configurazione di base per l'embroidery. Una volta organizzate le impostazioni, salvale come file modello nella cartella dei modelli (`File > Salva come modello...`). Ora puoi accedervi tramite `File > Nuovo da modello > Personalizzato`.

Se utilizzi principalmente Inkscape per l'embroidery, puoi selezionare l'opzione "Imposta come modello predefinito".

**Suggerimento:** Ottieni [modelli predefiniti](/tutorials/resources/templates/) dalla nostra sezione dei tutorial.
{: .notice--info }

## Installa le palette di colori del filo

Ink/Stitch viene fornito con molte palette di colori dei produttori di fili che possono essere installate. Questo ti consente di creare progetti tenendo presente i colori corretti.
I colori appariranno nel file PDF e saranno inclusi anche nel file di embroidery della tua macchina, se il formato del file lo supporta.

[Leggi di più](/docs/thread-color/#install-thread-color-palettes-for-inkscape)
