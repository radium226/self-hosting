#!/usr/bin/env python

from gi.repository import GLib
from maintenance.dbus import SERVICE_NAME, BUS
from maintenance.dbus.interface import MaintainerInterface
from maintenance.maintainer import Maintainer

class MaintainerDBusServer(object):

    def __init__(self, context):
        self.context = context
        self.main_loop = GLib.MainLoop()
        self.bus = BUS
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
