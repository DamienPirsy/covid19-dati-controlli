# Covid19 Dati Controlli

<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here --->
![GitHub repo size](https://img.shields.io/github/repo-size/DamienPirsy/covid19-dati-controlli)
![GitHub stars](https://img.shields.io/github/stars/DamienPirsy/covid19-dati-controlli?style=social)
![GitHub forks](https://img.shields.io/github/forks/DamienPirsy/covid19-dati-controlli?style=social)
![](https://img.shields.io/github/last-commit/DamienPirsy/covid19-dati-controlli)

Covid19-Dati-controlli è un semplice repository che contiene i dati relativi ai controlli effettuati in Italia dall'inizio della quarantena al giorno corrente, così come pubblicati giornalmente sul sito del Viminale :point_right: [(https://www.interno.gov.it/it/coronavirus-i-dati-dei-servizi-controllo](https://www.interno.gov.it/it/coronavirus-i-dati-dei-servizi-controllo)

Il repository contiene i file pdf originali (1), i file convertiti in JSON (2), ed il programma in python usato per estrarre i dati.

Avevo semplicemente bisogno di un pretesto per iniziare ad usare concretamente Python 3 e per provare Panda, quale miglior modo se non usare dati concreti, open, e riutilizzabili da chiunque?

(1) Ho solo uniformato la nomenclatura, specialmente per quanto riguarda la data.
(2) L'estrazione dei dati dal pdf è stata fatta con `tabula`, il JSON contiente anche informazioni relative al posizionamento degli elementi all'interno della pagina (x, y, w e h)


## Contribuire

Il progetto è una bozza e quindi ancora **in sviluppo**, se qualcuno skillato in Panda / Matplotlib mi volesse aiutare ad estrapolare dati da questa raccolta, proponendo ad esempio alcune metodologie di analisi e/o rappresentazione grafica dei dati, gliene sarei grato :pray:

## Prerequisiti

Versione Python: 3.7+

Per usare lo script è necessario creare un ambiente in Anaconda/Miniconda con i pacchetti elencati nel file requirements.txt:

```
$ conda create --name <env> --file requirements.txt
```

## Utilizzo

I pdf da convertire devono essere salvati nella cartella "data". 
Attivare poi l'ambiente e richiamare lo script da CLI:

```python
$ conda activate <env>
(env) $ python3 main.py
```
questi vengono processati in file JSON (gli originali sono poi spostati nella cartella "processed") e resi disponibili per essere analizzati da Panda.

Per far questo al momento ci sono due metodi:

```python
#df = as_dataframe_list(result)
#df = as_pure_list(result)
```

`as_dataframe_list()` restituisce una lista di DataFrame Panda dove ogni elemento è il contentuo di un file, ad esempio:

```
                                          Tipo   Valore        Data
0                          PERSONE CONTROLLATE  107.879  2020-03-11
1          PERSONE DENUNCIATE EX ART. 650 C.P.    2.165  2020-03-11
2    PERSONE DENUNCIATE EX ART. 495 E 496 C.P.       35  2020-03-11
3             ESERCIZI COMMERCIALI CONTROLLATI   19.985  2020-03-11
4  TITOLARI ESERCIZI COMMERCIALI DENUNCIATI EX      119  2020-03-11
```

Mentre `as_pure_list()` restituisce la semplice lista con i dati "grezzi", come elaborati dal parser:

```python
{'Tipo': ['PERSONE CONTROLLATE', 'PERSONE DENUNCIATE EX ART. 650 C.P.', 'PERSONE DENUNCIATE EX ART. 495 E 496 C.P.', 'ESERCIZI COMMERCIALI CONTROLLATI', 'TITOLARI ESERCIZI COMMERCIALI DENUNCIATI EX'], 
'Valore': ['107.879', '2.165', '35', '19.985', '119'], 
'Data': ['2020-03-11', '2020-03-11', '2020-03-11', '2020-03-11', '2020-03-11']}
```

E' possibile avere il dato grezzo anche come lista di dizionari nel formato "tipo" => "valore" passando `return_list = True` alla funzione `process_output_files(files, return_list)`:

```python
[{'Tipo': 'PERSONE CONTROLLATE', 'Valore': '107.879', 'Data': '2020-03-11'}, 
{'Tipo': 'PERSONE DENUNCIATE EX ART. 650 C.P.', 'Valore': '2.165', 'Data': '2020-03-11'}, 
{'Tipo': 'PERSONE DENUNCIATE EX ART. 495 E 496 C.P.', 'Valore': '35', 'Data': '2020-03-11'}, 
{'Tipo': 'ESERCIZI COMMERCIALI CONTROLLATI', 'Valore': '19.985', 'Data': '2020-03-11'}, 
{'Tipo': 'TITOLARI ESERCIZI COMMERCIALI DENUNCIATI EX', 'Valore': '119', 'Data': '2020-03-11'}]
```

## Contatti

Per qualsiasi cosa mi trovate scrivendo a <damien.pirsy@gmail.com>
