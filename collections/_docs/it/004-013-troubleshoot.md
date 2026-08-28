---
title: "Risoluzione dei problemi"
permalink: /docs/troubleshoot/
last_modified_at: 2025-12-29
toc: true
---

## Risoluzione dei problemi relativi agli oggetti

Ink/Stitch a volte può risultare complesso. Soprattutto per i principianti. Ma anche se si utilizza Ink/Stitch da un po', si possono ricevere messaggi di errore che indicano che qualcosa è andato storto e che la forma non può essere renderizzata per un motivo specifico.

Ink/Stitch include un'estensione per la risoluzione dei problemi, progettata per aiutare a capire l'errore e a individuare la posizione precisa del problema. Suggerisce come risolvere ogni tipo di errore e fornisce suggerimenti utili per le forme che presentano problemi, anche se non causano l'arresto anomalo di Ink/Stitch.

### Utilizzo

* (Facoltativo) Selezionare gli oggetti che si desidera testare. Se non si seleziona nulla, verrà testato l'intero documento.
* Eseguire `Estensioni > Ink/Stitch > Risoluzione dei problemi > Risoluzione dei problemi relativi agli oggetti`
 {% include upcoming_release.html %}
* Scegliere cosa rilevare tra errori, avvisi e avvisi relativi al tipo di oggetto.


Si riceverà un messaggio che indica se non è stato possibile trovare alcun errore oppure verrà aggiunta una nuova layer al documento SVG con le informazioni sulla risoluzione dei problemi. Utilizzare il pannello degli oggetti (Ctrl + Shift + O) per eliminare la layer una volta terminato.

![Esempio di risoluzione dei problemi](/assets/images/docs/en/troubleshoot.jpg)

**Suggerimento:** È possibile che un oggetto contenga più di un errore. Le forme riempite mostrano solo il primo errore che viene visualizzato. Eseguire nuovamente l'estensione se si ricevono ulteriori messaggi di errore.
{: .notice--info }

## Informazioni sull'elemento

Questa estensione fornisce informazioni su vari parametri degli elementi di cucitura selezionati.

![Informazioni sull'elemento](/assets/images/docs/en/element_info.png)

{% include upcoming_release.html %}
Il pulsante "Copia" nella scheda di aiuto consente di copiare tutte le informazioni negli appunti.



## Rimuovi impostazioni di ricamo

Utilizzare questa funzione per rimuovere le informazioni che Ink/Stitch ha memorizzato nel documento.
Questo può essere particolarmente utile se si copiano e si incollano oggetti da un progetto di ricamo in un altro documento.

Le estensioni rimuoveranno le impostazioni di ricamo dall'intero progetto o dagli oggetti selezionati:
* selezionare gli oggetti
  (saltare questo passaggio se si desidera cancellare tutte le informazioni di ricamo)
* Eseguire `Estensioni > Ink/Stitch > Risoluzione dei problemi > Rimuovi impostazioni di ricamo...`
* Selezionare una o tutte le opzioni fornite e fare clic su applica.

### Opzioni

* Rimuovi parametri
* Rimuovi comandi
  (tutti/nessuno/comando specifico)
* Rimuovi impostazioni di stampa dai metadati SVG

![Rimuovi impostazioni di ricamo - GUI](/assets/images/docs/en/remove-embroidery-settings.png)

## Pulisci documento

A volte si possono trovare forme molto piccole e oggetti residui derivanti da varie operazioni durante il processo di progettazione nel file SVG. Ink/Stitch offre una funzione per pulire il documento e impedire che tali oggetti causino problemi.

* Eseguire `Estensioni > Ink/Stitch > Risoluzione dei problemi > Pulisci documento...`
* Scegliere quali tipi di oggetti devono essere rimossi e definire una soglia
* Fare clic su applica
* È anche possibile eliminare gruppi o layer vuoti.
* Selezionare l'opzione "Test run" per visualizzare i nomi degli elementi che verranno rimossi con le impostazioni correnti senza rimuovere effettivamente nulla.

## Aggiorna svg Ink/Stitch

Un file creato con una versione precedente di Ink/Stitch verrà aggiornato automaticamente.

Tuttavia, se un file è già contrassegnato come aggiornato, non verrà controllato nuovamente per elementi obsoleti.
Se gli elementi di progettazione vengono copiati o importati da un file precedente in un nuovo file, è possibile che alcuni parametri non vengano riconosciuti correttamente.

In questo caso, è possibile eseguire un aggiornamento manuale per singoli elementi:

* Selezionare gli elementi da aggiornare
* Eseguire `Estensioni > Ink/Stitch > Risoluzione dei problemi > Aggiorna svg Ink/Stitch`

Suggerimento: questa operazione diventa superflua se è stata precedentemente eseguita una funzione Ink/Stitch nel file sorgente degli elementi di progettazione da copiare. Per farlo, selezionare un elemento nel vecchio file, aprire la finestra dei parametri e fare clic su "Applica e chiudi" senza apportare modifiche.
{: .notice--info }