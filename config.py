#! /usr/bin/env python
# coding: utf8
# @Time: 17-12-17
# @Author: yyq


import os
import sys
import logging

run_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
g_share = {}


def init_logger(log_name):
    logfile = run_path + '/log/' + log_name + ".log"
    logger = logging.getLogger(log_name)
    log_handler = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.ERROR)
    logger.setLevel(logging.INFO)
    return logger


test_logger = init_logger("test_logger")
