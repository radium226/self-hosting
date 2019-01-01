#!/usr/bin/env python

from maintenance.dbus.interface import MaintainerInterface
from maintenance.dbus import SERVICE_NAME, BUS

class MaintainerDBusClient(object):

    def __init__(self):
        self.bus = BUS
        self.interface = self.bus.get(SERVICE_NAME, MaintainerInterface.OBJECT_PATH)

    def deploy(self, application_name):
        self.interface.Deploy(application_name)

    def run_ansible_playbook(self, playbook_name):
        self.interface.RunAnsiblePlaybook(playbook_name)
