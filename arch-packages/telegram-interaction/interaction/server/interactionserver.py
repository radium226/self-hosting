#!/usr/bin/env python

from interaction.telegram import InteractionBot

from interaction.dbus import SERVICE_NAME
from interaction.dbus import InteractionInterface

from pydbus import SystemBus

from gi.repository import GLib


class InteractionServer(object):

    def __init__(self, context):
        self.context = context

        self.bus = SystemBus()
        self.loop = GLib.MainLoop()

        self.bus.publish(SERVICE_NAME)
        self.bus.register_object("/Interaction", InteractionInterface(self.bus, InteractionBot(context.config["telegram"]["token"], context.config["telegram"]["chat_id"])), None)

    def start(self):
        self.loop.run()

    def stop(self):
        self.loop.quit()
