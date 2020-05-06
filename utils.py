# -*- coding: utf-8 -*-
import os
from datetime import datetime

def build_file_string(fileobj, config: dict) -> dict:
    o = {}
    o['source_file'] = os.path.join(os.getcwd(), config['source_dir'], os.path.basename(fileobj.name))
    o['filename'] = os.path.basename(fileobj.name).replace('.pdf', '.{}'.format(config['format']))
    o['output'] = os.path.join(os.getcwd(), config['output_dir'], o['filename'])
    o['processed'] = os.path.join(os.getcwd(), config['processed_dir'], os.path.basename(fileobj.name))
    return o

def print_log_header(name: str) -> str:
    """ un semplice accorgimento grafico nel logo """
    w = max(12, len(name)) + 10  #(* + 4 spazi) + nome + (4 spazi + *)
    return "\n{}\n*{}*\n{}".format( "*"*w, ('{: ^'+ str(w-2) +'}').format(name.upper()), "*"*w)

def format_date(date:str) -> str:
    ret = ''
    if date:
        ret = datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
    return ret

def is_not_blank(my_string: str) -> bool:
    if my_string and my_string.strip():
        return True
    return False