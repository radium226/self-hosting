#!/bin/env python

import os
from setuptools import setup

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
    description="Interaction with Telegram",
    license="GPL",
    zip_safe=True,
    install_requires=[],
    scripts=[
        "scripts/interactiond",
        "scripts/interaction"
    ],
    packages=[
        "interaction.dbus",
        "interaction.context",
        "interaction.telegram",
        "interaction.server",
        "interaction.client"
    ]
)
