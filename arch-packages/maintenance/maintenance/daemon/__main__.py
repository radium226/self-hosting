#!/usr/bin/env python

from maintenance.context import Context
from maintenance.logging import info
from maintenance.daemon import MaintainerDaemon
import signal
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--system", action="store_true", default=False)
    args = parser.parse_args()

    context = Context(args.system)
    daemon = MaintainerDaemon.start(context)
    def signal_handler(signal_number, frame):
        info("SIGINT captured! Stopping daemon... ")
        daemon.stop()

    signal.signal(signal.SIGINT, signal_handler)
    daemon.idle()
