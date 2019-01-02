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
    install_requires=[],
    scripts=[
        "scripts/maintenanced",
        "scripts/maintenance"
    ],
    packages=[
        "maintenance.daemon",
        "maintenance.context",
        "maintenance.dbus",
        "maintenance.dbus.server",
        "maintenance.dbus.client",
        "maintenance.dbus.interface",
        "maintenance.http",
        "maintenance.http.server",
        "maintenance.logging",
        "maintenance.tools",
        "maintenance.tools.ansible",
        "maintenance.tools.git",
        "maintenance.tools.yay",
        "maintenance.maintainer"
    ]
)
