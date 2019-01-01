#!/usr/bin/env python

from maintenance.dbus.server import MaintainerDBusServer
from maintenance.http.server import MaintainerHTTPServer
from threading import Thread

class MaintainerDaemon(object):

    def __init__(self, context):
        self.context = context

        self.dbus_server = MaintainerDBusServer.start(context)
        def dbus_server_thread_target():
            self.dbus_server.idle()

        self.dbus_server_thread = Thread(target=dbus_server_thread_target)
        self.dbus_server_thread.start()

        self.http_server = MaintainerHTTPServer.start(context)
        def http_server_thread_target():
            self.http_server.idle()

        self.http_server_thread = Thread(target=http_server_thread_target)
        self.http_server_thread.start()

    @classmethod
    def start(cls, context):
        return MaintainerDaemon(context)

    def stop(self):
        self.dbus_server.stop()
        self.http_server.stop()

    def idle(self):
        self.dbus_server_thread.join()
        self.http_server_thread.join()
