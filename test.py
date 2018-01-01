# ！ /usr/bin/env python
# coding: utf8
# @Time: 17-12-17
# @Author: yyq

import time
from threading import Thread

from config import g_share, test_logger


class TestHandler(Thread):
    def __init__(self, *args, **kwargs):
        Thread.__init__(self)
        self.args = args

    def run(self):
        test_logger.info("%s start" % repr(self.args))
        while 1:
            if g_share["stop_tag"] == 1:
                test_logger.info("%s thread exit" % repr(self.args))
                break

            result = self.test_func()
            if not result:
                test_logger.info("%s no result" % repr(self.args))
                break
            time.sleep(1)

        test_logger.info("%s while over" % repr(self.args))

    def test_func(self):
        # print("%s test_func" % repr(self.args))
        test_logger.info("%s test_func" % repr(self.args))
        return 1
