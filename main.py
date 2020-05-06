# -*- coding: utf-8 -*-
import pandas as pd
import glob, os, re, json, logging
import tabula
from settings import config
from utils import *
from app_func import *
import matplotlib as plt

if __name__ == '__main__':

    #set up logging
    logging.basicConfig(filename=config['log_name'], level=logging.DEBUG,
                       format=config['log_format'], datefmt = config['log_date_format'])

    logging.info("Inizio elaborazione file sorgente")

    files = glob.glob(os.path.join(config['source_dir'], config['source_glob']))
    if len(files) > 0 :
        process_pdf_files(files)
    else:
        logging.warning("Nessun file presente!")
 
    logging.info("Inizio elaborazione file esportati")
    exported = glob.glob(os.path.join(os.getcwd(), config['output_dir'], "*.{}".format(config['format'])))
    if len(exported) > 0:
        result = process_ouput_files(exported)
    else:
        logging.warning("Nessun file esportato!")

    logging.info("File processati")

    #df = as_dataframe_list(result)
    #df = as_pure_list(result)
    