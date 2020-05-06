# -*- coding: utf-8 -*-
config = {}
config['log_name'] = 'app_log.log'
config['log_format'] = '%(asctime)s - %(levelname)s: %(message)s'
config['log_date_format'] = '%Y-%m-%d %I:%M:%S'
config['format'] = 'json'
config['source_dir'] = 'data'
config['output_dir'] = 'export'
config['source_glob'] = 'monitoraggio_serviz_controllo_giornaliero_*.pdf'
config['processed_dir'] = 'processed'