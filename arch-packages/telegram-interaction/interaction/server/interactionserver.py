#!/usr/bin/env python

from interaction.telegram import InteractionBot

from interaction.dbus import SERVICE_NAME
from interaction.dbus import InteractionInterface

from pydbus import SystemBus, SessionBus

from gi.repository import GLib


class InteractionServer(object):

    def __init__(self, context):
        self.context = context

        self.bus = SystemBus() if context.system else SessionBus()
        self.loop = GLib.MainLoop()

        telegram_chat_id = context.config["telegram"]["chat_id"]
        telegram_token = context.config["telegram"]["token"]
        print(f"telegram_chat_id={telegram_chat_id} / telegram_token={telegram_token}")
        self.bus.publish(SERVICE_NAME)
        self.bus.register_object("/Interaction", InteractionInterface(self.bus, InteractionBot(telegram_token, telegram_chat_id)), None)

    def start(self):
        self.loop.run()

    def stop(self):
        self.loop.quit()
