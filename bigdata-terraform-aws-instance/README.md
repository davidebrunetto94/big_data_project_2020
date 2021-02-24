# AWS - Terraform support

Premessa: questa guida è stata testata su un account AWS free-tier. 


1. [Contenuto del pacchetto](#Contenuto-del-pacchetto)
2. [Installazione AWS CLI](#Installazione-AWS-CLI)
3. [Installazione Terraform](#Installazione-Terraform)
4. [Preparazione Script](#Preparazione-Script)
5. [Esecuzione Script](#Esecuzione-Script)
6. [Eliminare l'ambiente](#Eliminare-l'ambiente)


## Contenuto del pacchetto
* main.tf: script terraform che crea l'ambiente su AWS
* variables.tf: contiene i parametri di configurazione per lo script
* install.sh: script che installa e configura i nodi con il software necessario


## Installazione AWS CLI
L’installazione di AWS CLI è un requisito indispensabile per l’utilizzo di Terraform con AWS.
Scaricare ed installare AWS CLI v2 per il proprio computer (https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).

Prima di proseguire è necessario possedere le seguenti informazioni relative al proprio account AWS: AWS Access Key ID e Secret Access Key.
Queste informazioni sono recuperabili da qui:
https://console.aws.amazon.com/iam/home?#/security_credentials.


Dalla shell digitare:
```
$ aws configure
```
verranno richiesti:
AWS Access Key ID
Secret Access Key
Default region name (ad es: “us-east-2”)
Default output format (ignorare e premere INVIO)


## Installazione Terraform
L’installazione di terraform è stata eseguita su un computer Macintosh attraverso il terminale e Homebrew.
Seguendo la guida ufficiale è possibile trovare la procedura per il sistema operativo in uso (https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/aws-get-started).
Per MacOs è stato prerequisito fondamentale installare i seguenti software:


* Homebrew:
```
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

* XCode:
```
$ xcode-select --install
```

* Gcc:
```
$ brew install --build-from-source gcc
```

Dopodiché è possibile seguire la guida ed eseguire quindi i seguenti comandi:
```
$ brew tap hashicorp/tap

$ brew install hashicorp/tap/terraform

$ brew upgrade hashicorp/tap/terraform
```

Verificare l’installazione con:
```
terraform -help
```


## Preparazione Script
Posizionarsi nella cartella “bigdata-terraform-aws-instance” .

Modificare il file ```variables.tf``` per cambiare i parametri secondo le proprie esigenze, in particolare:
* ```region:``` la regione in cui istanziare le macchine,
* ```instance_type:``` il tipo di macchine da istanziare (t2.micro è il tipo offerto dall’account aws free tier),
* ```ami_image:``` specifica l’immagine del SO desiderato,
* ```numOfSlaves:``` il numero di nodi slave,
* ```subnetId:``` specifica l’id della sottorete da utilizzare per gli indirizzi privati dei nodi.
Per trovare questa informazione, accedere al servizio AWS VPC, sul menù a sinistra aprire VIRTUAL PRIVATE CLOUD e selezionare “Subnets”: appariranno tutte le sottoreti. Se non ce ne sono, crearne una.
Annotare il subnet id da utilizzare nella variabile dello script terraform.
Nel campo IPv4 CIDR troviamo l’indirizzo della sottorete: gli indirizzi dei nostri nodi devono essere compresi all’interno di questa sottorete.
* ```mgmt_jump_private_ips:``` l’elenco degli indirizzi ip privati appartenenti alla propria sottorete aws.
Attenzione: se vengono modificato questi indirizzi ip è necessario che siano modificati anche sul file install.sh dalla riga 20 alla riga 25.

Generiamo una chiave SSH con questo comando:
```ssh-keygen -f <terraform_directory>/localkey```

Generiamo una coppia di chiavi dall’interfaccia di AWS:
Andare nel servizio EC2.
Sul menù a sinistra cercare la voce “Rete e sicurezza” in cui sarà possibile cliccare su “Coppie di chiavi”.
Cliccare sul bottone in alto a destra  “crea una coppia di chiavi”, inserire il nome “chiave_aws”, scegliere il formato .pem e proseguire alla creazione del file.
Salvare il file nella cartella di terraform.


E’ ora possibile procedere con l’esecuzione dello script.


## Esecuzione Script
Digitare il seguente comando per inizializzare la directory:
```terraform init```

Dopodichè è possibile lanciare il comando per creare ed avviare le istanze su AWS:
```terraform apply```

Quando verrà richiesto digitare la risposta ```yes```.

Attendere il completamento delle azioni.

Verranno create le istanze EC2 in cui verrà installato tutto il software necessario in automatico (java, spark-3.0.1, hadoop-2.7.7, Python 3.8) grazie allo script bash install.sh che verrà avviato sulle istanze.
Le istanze saranno nominate come master_1 e poi slave_1, slave_2, ecc…

Al termine verranno visualizzati col colore verde gli indirizzi DNS del master e degli slave.

Con questi indirizzi sarà possibile accedere alle istanze tramite il comando:
```ssh -i <terraform_directory>/chiave_aws.pem ubuntu@<DNS_pubblico>```


## Eliminare l'ambiente
Qualora volessimo annullare l’esecuzione del comando ```apply``` eseguiamo:
```terraform destroy```

Quando verrà richiesto digitare la risposta ```yes```.

Lo stesso comando possiamo utilizzarlo per eliminare le istanze dal momento in cui non ci serviranno più.
