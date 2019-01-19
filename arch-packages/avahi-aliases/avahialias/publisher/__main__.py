#!/usr/bin/env python

import argparse
from avahialias.publisher import AvahiAliasPublisher


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name")

    args = parser.parse_args()
    name = args.name

    publisher = AvahiAliasPublisher()
    publisher.publish(name + ".local")

    publisher.idle()
