# Introduzione

L’applicativo sviluppato durante il tirocinio è uno strumento di
estrazione di entità con nome da file PDF. Utilizzando librerie come
SpaCy, PyPDF2 e pdftotext, l’applicazione analizza il contenuto del file
PDF e estrae le entità con nome. Il risultato dell’elaborazione viene
successivamente memorizzato in una pagina HTML per una gestione più
semplice e intuitiva del contenuto, anche in vista di un eventuale
utilizzo del programma come servizio web. Operando da linea di comando,
questa soluzione offre un’esperienza utente semplice ed efficiente, con
la possibilità di personalizzare l’elaborazione utilizzando i parametri
che vederemo in seguito.

# Architettura interna

Il sistema è stato progettato per essere facilmente convertibile in un
servizio web in modo da renderlo accessibile a un pubblico più ampio e
senza la necessità di installare alcun software aggiuntivo. Questo è
stato possibile grazie all’utilizzo di un’architettura modularizzata,
dove le funzionalità principali sono state divise in moduli distinti e
indipendenti tra di loro.

Attualmente, il software è composto da tre moduli principali: il modulo
di configurazione, il modulo che gestisce l’elaborazione dei file PDF e
il modulo che gestisce i task di NLP. La separazione dei moduli rende
più semplice l’aggiunta di funzionalità o la modifica di specifiche
parti del sistema senza influire sulla stabilità e sul funzionamento
degli altri moduli.

Inoltre, la separazione tra la logica del software e il layer di
presentazione o interfaccia rende possibile utilizzare le stesse
funzionalità del sistema attraverso diverse interfacce, come ad esempio
un’app desktop o API. Ad esempio, usando il framework Flask, possiamo
creare degli endpoint REST, ai quali passando i parametri opportuni e
validandoli con il modulo di configurazione, potremmo esporre il task di
NLP al web. L’output, essendo un normale file html, potrebbe essere
consultato attraverso un redirect a tale file, esponendo opportunamente
la cartella di output mediante un web server. Nelle prossime sezioni
esploreremo i vari moduli del sistema, esaminando le loro funzionalità
attuali e la possibilità di espansione. Infine, daremo un’occhiata
all’interfaccia utente attuale.

## Modulo di configurazione

Il modulo di configurazione è stato progettato per gestire in modo
organizzato e universale tutti i parametri necessari all’esecuzione
delle operazioni di analisi e elaborazione all’interno del sistema.
Attualmente, questo modulo esporta un dizionario Python che rappresenta
il contenitore dei parametri, nonché un metodo che verifica la validità
di questi ultimi, prima di avviare le operazioni di elaborazione.

Il dizionario contiene i seguenti parametri: "File", "Modello",
"Posizione dell’EntityRuler", "Pattern" e "Flag Serve". La verifica
della validità dei parametri è fondamentale, poiché il metodo verifica
che siano presenti sia il modello SpaCy che il file PDF, prima di
avviare le operazioni di elaborazione. Questo garantisce che vi siano i
due elementi fondamentali per poter estrarre le entità con nome.

Inoltre, il modulo di configurazione è estendibile e flessibile,
rendendo possibile l’aggiunta di nuove funzionalità al programma in modo
semplice ed efficiente. Ad esempio, possono essere introdotte
funzionalità di formattazione delle informazioni o di validazione e
conversione del body di una richiesta HTTP nel formato richiesto. Questo
rende il sistema adattabile alle diverse esigenze e flessibile nelle
future evoluzioni delle operazioni.

## Modulo PDF

Il modulo PDF è responsabile di gestire completamente la lavorazione dei
file PDF. Tuttavia, a differenza dei file di testo normali, i file PDF
richiedono l’utilizzo di librerie specifiche per poter essere utilizzati
all’interno del programma. Al momento, il modulo PDF dispone di un unico
metodo utilizzato, che consente di estrarre il testo dal file PDF e di
inserire ogni pagina del testo in una lista Python. Tuttavia, anche
questo modulo può essere facilmente ampliato nel momento in cui è
necessario implementare ulteriori funzionalità all’interno del sistema.
Ad esempio, come menzionato nel capitolo 1, sono state attualmente
implementate le librerie pdftotext e PyPDF2, dove la prima viene
utilizzata per estrarre il testo e la seconda per estrarre informazioni
sul file PDF come autore, capitoli, ecc. La seconda libreria è stata
utilizzata per creare uno script che sia in grado di analizzare il testo
e di estrapolare la struttura dei capitoli. Attualmente questa funzione,
sebbene presente, non è in uso, ma può essere facilmente implementata
nel momento in cui si dispone di un’interfaccia che consente di caricare
il file PDF, e una volta ottenuti i capitoli, decidere quali di questi
utilizzare per estrarre le entità con nome.

## Modulo NLP

Il modulo NLP svolge un ruolo fondamentale nel sistema ed è alimentato
dalla potente libreria SpaCy. Questo modulo si occupa di coordinare i
vari step di elaborazione del NLP forniti da SpaCy e di altre
funzionalità importanti, offrendo un unico punto di accesso tramite una
API intuitiva e facilmente utilizzabile. In questo modo, il modulo rende
disponibili solo alcuni metodi pubblici al chiamante, mentre gli altri
sono privati e destinati esclusivamente all’utilizzo interno, garantendo
una gestione ottimale delle risorse e delle funzionalità offerte. Questa
organizzazione del modulo rende più semplice l’utilizzo delle
funzionalità di NLP e garantisce una maggiore flessibilità nelle future
espansioni del sistema.

Il modulo consente di caricare in memoria il modello, adeguare la
pipeline in base alla configurazione di avvio e restituirla al
chiamante. Per fare ciò, sarà necessario passare l’intero dizionario di
configurazione e il modulo si occuperà di caricare la pipeline in modo
corretto.

Il modulo include anche un metodo per l’effettiva estrazione delle
entità da un documento. Questa operazione è stata implementata
utilizzando il multithreading per migliorare le prestazioni. L’utilizzo
del multithreading permette di aumentare l’efficienza nell’elaborazione
delle pagine di un documento, poiché consente di eseguire le operazioni
su più pagine contemporaneamente, anziché attendere che venga completata
l’elaborazione di ogni singola pagina. In questo modo, il tempo totale
di elaborazione non è determinato dalla somma dei tempi di elaborazione
di ciascuna pagina, ma dalla durata dell’elaborazione più lunga tra
tutte le pagine, il che significa che le pagine più complesse possono
essere elaborate in parallelo con quelle più semplici, aumentando la
velocità complessiva dell’intero processo. Inoltre, poiché
l’elaborazione è effettuata in modo asincrono, è stato necessario
progettare un sistema di ordinamento per evitare che le pagine vengano
visualizzate in ordine errato. Questo è stato ottenuto creando una lista
di dimensioni pari al numero di pagine del documento e inserendo il
risultato dell’elaborazione nello stesso indice della pagina iniziale.

Infine, il modulo include un metodo per memorizzare l’output in una
pagina HTML con le entità evidenziate, che può essere visualizzata sia
in locale che tramite un server web.

Il modulo NLP offre una grande flessibilità, in quanto una volta
caricata la pipeline di SpaCy, questa viene restituita al chiamante e
può essere manipolata prima di essere passata al metodo di elaborazione.
Dopo aver ottenuto il risultato di elaborazione, è possibile
implementare soluzioni di output illimitate, invece di passare
direttamente al metodo che genera l’output in formato HTML. Questa
flessibilità rende possibile l’espansione futura del modulo NLP per
soddisfare le esigenze specifiche del progetto.

## Interfaccia linea di comando

Il modulo per la gestione dell’interfaccia da riga di comando è stato
progettato per offrire una soluzione semplice ed intuitiva per
interagire con le funzionalità dell’applicativo. Questo modulo è
composto da due file, che lavorano in tandem per garantire un flusso di
lavoro efficiente.

Il primo file si occupa di leggere i parametri dalla linea di comando,
compilare e validare il dizionario di configurazione. La libreria
"getopt" è stata utilizzata per interpretare i parametri della linea di
comando, superando i limiti del comportamento di default di Python che
impone di passare i parametri in un certo ordine e non consente di
passare parametri opzionali. La libreria "getopt" invece permette di
definire flag semplici e flag con valore, che quando individuati al
momento dell’avvio, permettono di compiere specifiche azioni. Ad
esempio, nel nostro caso sono stati utilizzati flag come "model", "file"
e "dizionari" che richiedono un percorso per un determinato file, mentre
il flag "serve" è utilizzato solo per indicare al programma di avviare
il browser una volta terminata l’esecuzione.

Il secondo file gestisce il workflow dell’applicativo ed espone un solo
metodo, che permette di eseguire l’intera operazione di estrazione
importando e interagendo con i moduli descritti nei paragrafi sopra.
Inoltre, durante l’esecuzione dell’applicativo, vengono mostrati a
schermo messaggi informativi che forniscono indicazioni sullo stato di
avanzamento dell’elaborazione. Al termine, viene infine mostrato il
tempo totale impiegato per eseguire l’intera operazione.

L’interfaccia da riga di comando è stata progettata come una soluzione
temporanea per rendere semplice e intuitivo l’utilizzo delle
funzionalità dell’applicativo. Nonostante sia possibile estendere il suo
funzionamento per soddisfare eventuali esigenze future, essa rappresenta
un modo semplice ed efficiente per interagire con gli output del
tirocinio e sperimentare con le sue funzionalità. Nel prossimo
paragrafo, verranno proposti alcuni miglioramenti che possono essere
apportati per ottimizzare ulteriormente l’applicativo.

# Requisiti ed installazione

Per utilizzare questa applicazione, ci sono alcuni requisiti di sistema
che è necessario soddisfare. La prima cosa da fare è scaricare il
software dal repository GitHub, dove è caricato. Una volta scaricato, si
troverà all’interno della cartella un file chiamato *"requirements.txt"*
che elenca tutte le librerie necessarie per l’utilizzo
dell’applicazione. Queste librerie possono essere installate tramite
"pip", il gestore di pacchetti di Python, semplicemente eseguendo il
comando `pip install -r requirements.txt` dalla riga di comando.

Inoltre, per garantire il corretto funzionamento delle librerie di
estrazione PDF, è necessario installare un ulteriore software sul
proprio sistema, ovvero *"poppler"*. Se si sta lavorando su un Mac,
questo software può essere installato tramite *"brew"*, un gestore di
pacchetti per macOS.

Per quanto riguarda la versione di Python, è necessario che sia
installata almeno la versione 3.9. Le versioni minime delle librerie
necessarie sono indicate nel file *"requirements.txt"*.

È importante seguire questi passaggi per garantire che l’applicazione
funzioni correttamente e che sia possibile utilizzarla senza problemi.
Seguendo questi semplici passaggi, l’installazione sarà completata e
sarà possibile iniziare a utilizzare l’applicazione per estrarre entità
con nome da file PDF. Infine, il repo include anche il modello di
transfer learning ed il dizionario creati durante il tirocinio, che sono
entrambi inclusi nel repository. Tuttavia, è possibile utilizzare
qualsiasi modello o dizionario a proprio piacimento, in quanto il
sistema è in grado di caricare qualsiasi modello o dizionario
specificato al momento dell’avvio. In seguito verrà descritto come
strutturare correttamente i dizionari per l’esportazione in formato
json.

# Funzionamento dell’applicativo

Il programma è accessibile tramite linea di comando e prevede
l’inserimento di alcuni parametri per la sua esecuzione. Durante il suo
funzionamento, il software fornirà una serie di messaggi per indicare lo
stato attuale dell’elaborazione. Una volta completata l’elaborazione,
l’output prodotto sarà salvato nella cartella "output" situata nella
directory principale del programma. Il nome del file di output sarà
identico al nome del file PDF di origine, con la sola eccezione
dell’estensione, che sarà sostituita con ".html". Ad esempio, se il file
PDF di origine avesse come nome "Prova.pdf", il file di output prodotto
sarà "Prova.html". Vediamo ora nel dettaglio quali sono e come
funzionano i parametri che possono essere passati contestualmente
all’avvio del programma. Da notare che i parametri sono attivabili
mediante dei flag, dunque non è necessario rispettare alcun ordine.
Unico vincolo è che vengano passati almeno il modello ed il file da
analizzare in formato pdf.

## File da elaborare

Il file da elaborare, come indicato sopra deve essere necessariamente in
formato PDF, altrimenti, allo stato attuale del sistema, non sarà
possibile procedere con l’esecuzione del programma. Il file in questione
può essere passato attraverso il flag -f oppure in formato esteso –file
seguito poi dal path assoluto o relativo del file.

`python main.py -f files/Prova.pdf`

## Modello da caricare in memoria

Il percorso del modello, anche in questo caso assoluto o relativo, può
essere passato al programma mediante il flag -m oppure in formato esteso
–model. In questo caso, l’unico vincolo è che il modello sia nel formato
SpaCy, dal momento che l’intero sistema è stato realizzato su questa
libreria, e soprattutto che tale modello abbia nella sua pipeline la
componente NER, la quale svolge proprio il lavoro di estrazione delle
entità con nome mediante tecniche di machine learning applicate al NLP.

`python main.py -m models/my-model`

## Dizionari per componente EntityRuler

Nel capitolo <a href="#chap:strumenti" data-reference-type="ref"
data-reference="chap:strumenti">[chap:strumenti]</a> dedicato alla
presentazione degli strumenti, quando abbiamo analizzato il componente
EntityRuler abbiamo indicato la possibilità di aggiungerlo alla pipeline
prima o dopo il componente NER. Il sistema consente di scegliere in modo
arbitrario in che posizione caricare il componente. Per caricare
l’EntityRuler prima della componente NER è necessario passare il flag -b
o in forma estesa –before, inevece -a oppure –after per inserirlo dopo.
In entrambi i casi, è necessario far seguire il flag con il percorso,
assoluto o relativo, del file JSON contentente i patterns per il
riconoscimento delle entità con nome.

`python main.py –before pattern.json` oppure `python main.py –after
pattern.json`

### Come ottenere il json

Dalla documentazione di SpaCy abbiamo appreso che in fase di caricamento
dell’EntityRuler possiamo contestualmente caricare anche una lista di
pattern. Dunque possiamo ineserire in una struttura dati Python di tipo
List diversi pattern realizzati nel formato visto nel
capitolo e passare tale lista come argomento del metodo `add_patterns`. Per consentire la
portabilità dei dizionari, è stato deciso di utilizzare il formato
.json, in quanto facilmente ottenibile. Infatti, una volta creata la
lista Python, importando la libreria JSON è possibile esportare l’intera
struttura dati in un file con il metodo:

`json.dumps(patterns)`

Per riconvertire invece il JSON in una lista Python, possiamo chiamare
il metodo:

`patterns = json.loads(json_patterns.read())`

## Visualizzare l’output

Una volta completata l’elaborazione, il file ottenuto viene salvato
nella cartella "output". Si tratta di un file HTML e dunque
visualizzabile attraverso un qualunque browser. L’utente, se lo
desidera, può aggiungere al comando il flag -s oppure –serve, in questo
modo, una volta terminata l’elaborazione, il software, prima di
chiudersi, avvia il browser predefinito di sistema caricando
autonomamente il file.

`python main.py -s`