# big_data_project_2020

Questo progetto consiste nella raccolta di tutti i tweet riconducibili all'argomento "Covid-19" del 2020 (o parte di essi) ed analizzare come il fenomeno è mutato nel tempo, ad esempio mostrare la crescita del volume di tweet nel tempo, oppure mostrare come l'andamento del campo "sentiment" dei tweet varia durante le varie fasi della pandemia.
Sono stati usati i dati dei tweet per allenare un modello di machine learning (probabilmente una SVM) a predire il sentimento del testo del tweet in maniera binaria come positivo o negativo. Per fare ciò il sentiment, che nel dataset è un valore continuo compreso tra il valore -1 ed il valore 1, è stato convertito in un valore binario.
Infine sono stati eseguiti dei test sull’elaborazione dei dati partendo da due istanze e sono state aumentate man mano fino a cinque misurandone le prestazioni che verranno poi messe a confronto.


1. [Struttura](#Struttura)

## Struttura
* proj: contiene gli script dell'applicazione
* bigdata-terraform-aws-instance: contiene gli script necessari alla creazione dell'ambiente su AWS
