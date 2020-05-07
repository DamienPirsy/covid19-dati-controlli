# -*- coding: utf-8 -*-
from typing import Generator
from utils import *
from settings import config
import pandas as pd
import glob, os, re, json, logging
import tabula

def convert_to_file(file_desc, output:str, **kwargs) -> None:
    """ Converte il file pdf nell'output specificato

    Parameters
    ---------
    file_desc: 
        File descriptor / file handle
    output: str
        Nome del file di destinazione
    **kwargs
        Argomenti per la funzione "convert_into" di tabula
    
    """
    tabula.convert_into(file_desc, output_path=output, **kwargs)

def process_pdf_files(files: list) -> None:
    """ Legge la lista di PDF, converte i file e sposta gli originali

    Parameters
    ----------
    files: list
        Lista di file handlers
    
    """
    for _f in files:
        with open(_f, 'rb') as current_file:
            try: 
                _data = build_file_string(fileobj=current_file, config=config)
                logging.debug("Converting file: {}".format(_data['source_file']))
                convert_to_file(current_file, output=_data['output'], output_format=config['format'], pages='all')
                logging.debug("Done, moving it to processed folder")
                os.rename(_data['source_file'], _data['processed'])
            except Exception as e:
                logging.error(e)

def parse_content(json_content: str, date: str, w_check: re.Pattern, return_list=False) -> list:
    """ Elabora il contenuto del PDF

        La struttura tabellare viene recuperata senza grossi problemi.
        Ci sono due "righe" principali nella tabella (persone e attività), ciascuna con N righe
        per i relativi datai; l'allineamento verticale non rende semplice recuperare bene i valori; 
        la prima riga del testo non è necessariamente la stessa che contiene il valore, ed il valore non coincide 
        con la fine della riga. Esempio:
        -------------------------------------------------       _row
        Lorem ipsum dolor sit amet,         |                   _internal_row
        consectetur adipiscing elit,        |     100           _internal_row
        sed do eiusmod tempor incididunt    |                   _internal_row
        -------------------------------------------------       _row
        _internal_row[0]['text']             _internal_row[1]['text']

        Una possibile strategia è identificare le parole che indicano un inizio riga (es. CONTRALLATE | SANZIONATE)
        ed usarle come punto di riferimento (e chiave), ad esempio con questa regex:
        w_check = re.compile('(CONTROLLATE|SANZIONATE|DENUNCIATE|ESERCIZI)')
        Ci sono almeno 2 template diversi di documento, ed ogni documento risulta più o meno cosi:

        ---------------------------------------- _row
           lorem ipsum                  |  8     _internal_row          
           consectetur adipiscit        |        _internal_row          
           lorem ipsum dolor            |  7     _internal_row          
        ---------------------------------------- _row
           lorem ipsum                  |  5     _internal_row          
           quis nostrud exercitation    |  6     _internal_row          
           ullamco laboris              |        _internal_row          
           sed do eiusmod tempor        |  1     _internal_row          
           incididunt                            _internal_row 
        -----------------------------------------

    Parameters:
    -----------
    json_content: str
        contenuto trasformato in stringa json
    date: str
        data da utilizzare per i record
    w_check: re.Pattern
        regex per l'elaborazione dei dati
    return_list: boolean
        se True restitusce una lista di dizionari [{'Tipo': '', 'Valore': ''}]
        altrimenti restituisce un dizionario di liste {'Tipo': [......], 'Valore': [.....]}

    Returns:
    list 
      lista di dizionari, ognuno è un record
    
    """
    as_dict = {'Tipo' : [], 'Valore' : [], 'Data': []}
    as_list = []
    for _row in json_content:
        _tmp_row = []
        for _internal_row in _row['data']:
            if is_not_blank(_internal_row[0]['text']):
                _tupla = (_internal_row[0]['text'], _internal_row[1]['text'])
                _tmp_row.append(_tupla)
        doc = {}  # contenitore per la "riga di valori"
        for _r in _tmp_row:  #ora analizzo ogni tupla per capire quali elementi  prendere            
            if w_check.search(_r[0]):
                doc['Tipo'] = _r[0]
            if is_not_blank(_r[1]):
                doc['Valore'] = _r[1]
            if 'Tipo' in doc and 'Valore' in doc:  # se la riga di valori è "piena" reinizializzo
                doc['Data'] = date
                if return_list:
                    as_list.append(doc)
                else:
                    as_dict['Tipo'].append(doc['Tipo'])
                    as_dict['Valore'].append(doc['Valore'])
                    as_dict['Data'].append(doc['Data'])
                doc = {}
    if return_list:
        return as_list
    else:
        return as_dict

def process_ouput_files(files: list, return_list: bool =False) -> Generator[list, None, None]:
    """ Processa i file per Panda

    Parameters:
    ----------
    files: list
        Lista di dizionari
    
    Returns:
    ----------
    Generator
        lista di dizionari

    """
    regex_date = re.compile('(\d+)\.{}$'.format(config['format']), re.I)
    regex_words = re.compile('(CONTROLLATE|SANZIONATE|DENUNCIATE|ESERCIZI)')
    for _f in files:
        with open(_f, 'rb') as _current:
            try:
                _d = format_date(regex_date.search(_current.name)[1])
                yield parse_content(json.load(_current), _d, regex_words, return_list)
            except Exception as e:
                logging.error(e) 

def as_dataframe_list(iterable: Generator, **kwargs) -> list:
    """ Restituisce come lista di dataframes panda """
    return list(pd.DataFrame(x, **kwargs) for x in iterable)

def as_pure_list(iterable: Generator) -> list:
    """ Restituisce una lista di dati non processati da panda """
    return list(iterable)