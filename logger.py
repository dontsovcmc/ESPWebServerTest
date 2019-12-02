# -*- coding: utf-8 -*-
__author__ = 'dontsov'

import logging
import os
import sys
from datetime import datetime

PROJ_DIR = os.path.normpath(os.path.dirname(__file__))
LOG_DIR = os.path.join(PROJ_DIR, 'logs')

base_name = datetime.utcnow().strftime('wmb_%d.%m.%Y_%H.%M')


class Logger(object):
    def __init__(self):
        log = logging.getLogger('')
        log.setLevel(logging.INFO)

        if not os.path.isdir('logs'):
            os.makedirs('logs')

        fh = logging.FileHandler(os.path.join('logs', base_name + '.log'), mode='w')
        fh.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        log.addHandler(fh)

        # Задействовать консоль для вывода лога
        console = sys.stderr
        if console is not None:
            # Вывод лога производится и на консоль и в файл (одновременно)
            console = logging.StreamHandler(console)
            console.setLevel(logging.INFO)
            console.setFormatter(formatter)
            log.addHandler(console)

Logger()

log = logging.getLogger('')