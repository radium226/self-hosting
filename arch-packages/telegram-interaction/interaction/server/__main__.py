#!/usr/bin/env python

from interaction.server import InteractionServer
from interaction.context import Context

import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    context = Context()
    server = InteractionServer(context)
    try:
        server.start()
    except:
        server.stop()
