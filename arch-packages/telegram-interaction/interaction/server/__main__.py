#!/usr/bin/env python

from interaction.server import InteractionServer
from interaction.context import Context
import sys
import logging
import argparse

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser()
    parser.add_argument("--system", action="store_true", default=False)
    args = parser.parse_args()

    context = Context(args.system)
    server = InteractionServer(context)
    try:
        server.start()
    except:
        server.stop()
