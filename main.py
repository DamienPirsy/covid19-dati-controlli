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

    logging.info(print_log_header('start'))
    logging.debug("Start processing source files")

    files = glob.glob(os.path.join(config['source_dir'], config['source_glob']))
    if len(files) > 0 :
        process_pdf_files(files)
    else:
        logging.warning("No files found!")
 
    logging.debug("Start processing exported files")
    exported = glob.glob(os.path.join(os.getcwd(), config['output_dir'], "*.{}".format(config['format'])))
    if len(exported) > 0:
        result = process_ouput_files(exported)
    else:
        logging.warning("No exported files!")

    logging.info("Files processed")

#df = get_as_list(result)
#df = get_as_date_dict(result)
#df = get_as_one(result)
#df = get_pure_list(result)