#!/usr/bin/env python

from pydbus import SessionBus, SystemBus
from maintenance.dbus.interface import MaintainerInterface
from maintenance.dbus import SERVICE_NAME

class MaintainerDBusClient(object):

    def __init__(self, context):
        self.bus = SystemBus() if context.system else SessionBus()
        self.interface = self.bus.get(SERVICE_NAME, MaintainerInterface.OBJECT_PATH)

    def deploy(self, application_name):
        self.interface.Deploy(application_name)

    def run_ansible_playbook(self, playbook_name):
        self.interface.RunAnsiblePlaybook(playbook_name)

    def upgrade_system(self):
        self.interface.UpgradeSystem()
