#! /usr/bin/env python
# coding: utf8
# @Time: 17-12-17
# @Author: yyq


import os
import sys
import time
import atexit
from signal import SIGTERM


class Daemon(object):
    def __init__(self, run_path, pid_file, stdout='/dev/null', stderr='/dev/null'):
        self.stdout = stdout
        self.stderr = stderr
        self.pid_file = pid_file
        self.run_path = run_path

    def __daemonize(self):
        """
        unix double-fork to daemon.
        """
        try:
            # first fork
            pid = os.fork()
            if pid > 0:
                # first parent exist
                os._exit(0)
        except OSError as e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            os._exit(1)

        # Call setsid to create a new session.
        os.setsid()

        try:
            # second fork
            pid = os.fork()
            if pid > 0:
                os._exit(0)
        except OSError as e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            os._exit(1)

        # Change the current working directory to / to avoid interfering with mounting and unmounting
        os.chdir("/")
        # Set file mode creation mask to 000 to allow creation of files with any required permission later.
        os.umask(0)

        # Close unneeded file descriptors inherited from the parent
        # (there is no controlling terminal anyway): stdout, stderr, and stdin.
        sys.stdout.flush()
        sys.stderr.flush()
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+', 0)
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        atexit.register(self.del_pid)
        pid = str(os.getpid())
        open(self.pid_file, "w+").write("%s\n" % pid)

    def del_pid(self):
        os.remove(self.pid_file)

    def start(self):
        """
        start the daemon
        :return:
        """
        try:
            pf = open(self.pid_file, "r")
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pid_file %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pid_file)
            sys.exit(1)

        self.__daemonize()
        self.run()

    def stop(self):
        try:
            pf = open(self.pid_file, "r")
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pid_file %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pid_file)
            return

        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError as e:
            err = str(e)
            if err.find("No such process") > 0:
                if os.path.exists(self.pid_file):
                    os.remove(self.pid_file)
            else:
                print(str(err))
                sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    def run(self):
        """
        override this method when u subclass daemon. It will be called after start() or restart().
        """

    def main(self):
        if len(sys.argv) >= 2:
            if 'start' == sys.argv[1]:
                self.start()
            elif 'stop' == sys.argv[1]:
                self.stop()
            elif 'restart' == sys.argv[1]:
                self.restart()
            else:
                sys.stderr.write("Unknown command\n")
                sys.exit(2)
            sys.exit(0)
        else:
            sys.stderr.write("usage: %s start |stop |restart\n" % sys.argv[0])
            sys.exit(2)
