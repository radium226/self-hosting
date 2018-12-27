#!/bin/env python

import os
from setuptools import setup

def version():
    return os.environ["VERSION"]

def name():
    return os.path.basename(os.getcwd())

setup(
    name=name(),
    version=version(),
    description="System Maintenance",
    license="GPL",
    zip_safe=True,
    install_requires=[],
    scripts=[],
    packages=[
        "system.tools.ansible",
        "system.tools.git",
        "system.tools.yay",
        "system.maintenance",
        "system.prompt"
    ]
)
