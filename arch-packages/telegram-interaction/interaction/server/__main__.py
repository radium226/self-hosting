#!/usr/bin/env python

from interaction.server import InteractionServer
from interaction.context import Context
import sys
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    system = False
    try:
        system = bool(sys.argv[1])
    except:
        pass

    context = Context(system)
    server = InteractionServer(context)
    try:
        server.start()
    except:
        server.stop()
