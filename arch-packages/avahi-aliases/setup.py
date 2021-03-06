#!/bin/env python

import os
from setuptools import setup, find_packages

def version():
    try:
        return os.environ["VERSION"]
    except:
        with open("./VERSION.txt", "r") as f:
            return f.read().strip()

def name():
    try:
        return os.environ["NAME"]
    except:
        return os.path.basename(os.getcwd())

setup(
    name=name(),
    version=version(),
    description="Maintainer",
    license="GPL",
    zip_safe=True,
    scripts=["scripts/avahi-publish-alias"],
    install_requires=[],
    packages=["avahialias.publisher"]
)
