#! /usr/bin/env python
# coding: utf8
# @Time: 17-12-17
# @Author: yyq

import logging
import os
import signal
import sys
import time

from config import g_share

from daemon import Daemon
from test import TestHandler


class MainAgent(Daemon):
    def __init__(self, run_path, pid_file):
        Daemon.__init__(self, run_path, pid_file)

        self.threads = []
        self.logger = self.__get_logger()

    # @property
    # def main_logger(self):
    #     return self.logger
    #
    # @main_logger.setter
    # def main_logger(self):

    def __get_logger(self):
        logfile = self.run_path + '/log/main.log'
        logger = logging.getLogger('main')
        _handler = logging.FileHandler(logfile)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        _handler.setFormatter(formatter)
        logger.addHandler(_handler)
        logger.setLevel(logging.WARNING)
        logger.setLevel(logging.ERROR)
        logger.setLevel(logging.INFO)
        return logger

    def stop_signal(self, *args):
        g_share["stop_tag"] = 1

    def check_threads(self):
        while 1:
            if g_share["stop_tag"] == 1:
                self.logger.info("main log: thread join start")
                for i in self.threads:
                    i.join()
                    self.logger.info("main log: thread join ok, %s" % repr(i))
                break
            else:
                time.sleep(1)
        self.logger.info("main log: program end.")

    def run(self):
        self.logger.info("main log: program start.")
        signal.signal(signal.SIGTERM, self.stop_signal)

        self.logger.info("main log: recv signal")
        g_share["stop_tag"] = 0
        self._run()

    def _run(self):
        for i in range(3):
            _handle = TestHandler(i)
            self.threads.append(_handle)
            _handle.start()

        self.check_threads()


if __name__ == "__main__":
    run_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
    handle = MainAgent(run_path, run_path + "/pid/y.pid")
    handle.main()
