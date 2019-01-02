#!/usr/bin/env python

from gi.repository import GLib
from pydbus import SessionBus, SystemBus
from maintenance.dbus.interface import MaintainerInterface
from maintenance.maintainer import Maintainer
from maintenance.dbus import SERVICE_NAME

class MaintainerDBusServer(object):

    def __init__(self, context):
        self.context = context
        self.main_loop = GLib.MainLoop()
        self.bus = SystemBus() if context.system else SessionBus()
        self.bus.publish(SERVICE_NAME)

        maintainer = Maintainer(self.context)
        interface = MaintainerInterface(maintainer)
        self.bus.register_object(MaintainerInterface.OBJECT_PATH, interface, None)

    @classmethod
    def start(cls, context):
        return MaintainerDBusServer(context)

    def idle(self):
        self.main_loop.run()

    def stop(self):
        self.main_loop.quit()
