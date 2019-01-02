#!/usr/bin/env python

from subprocess import Popen, PIPE

from .upgrade import Upgrade

class Yay:

    def __init__(self, context):
        self.context = context

    def refresh_available_packages(self):
        process = Popen(["yay", "-Sy", "--noconfirm"])
        process.wait()

    def list_upgrades(self):
        return list(self._yield_upgrades())

    def upgrade_packages(self, packages):
        process = Popen(["yay", "-S"] + list(map(lambda package: package.name, packages)) + ["--noconfirm"])
        process.wait()

    def _yield_upgrades(self):
        process = Popen(["yay", "-Qu", "--devel", "--noconfirm"], stdin=None, stdout=PIPE)
        lines = map(lambda b: b.decode("utf-8").strip(), iter(process.stdout.readline, b""))
        yield from Upgrade.parse_lines(lines)
