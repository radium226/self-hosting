#!/usr/bin/env python

from maintenance.context import Context
from maintenance.logging import info
from maintenance.daemon import MaintainerDaemon
import signal

if __name__ == "__main__":
    context = Context()
    daemon = MaintainerDaemon.start(context)
    def signal_handler(signal_number, frame):
        info("SIGINT captured! Stopping daemon... ")
        daemon.stop()

    signal.signal(signal.SIGINT, signal_handler)
    daemon.idle()
