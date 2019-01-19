#!/usr/bin/env python

import subprocess
import avahi, dbus
import os
from time import sleep
from gi.repository import GLib
from encodings.idna import ToASCII


class Settings:
    # Got these from /usr/include/avahi-common/defs.h
    TTL = 60
    CLASS_IN = 0x01
    TYPE_CNAME = 0x05


class AvahiAliasPublisher:

    def __init__(self):
        self.main_loop = GLib.MainLoop()

    def encode(self, name):
        """ convert the string to ascii
            copied from https://gist.github.com/gdamjan/3168336
        """
        return '.'.join(ToASCII(p).decode("utf-8") for p in name.split('.') if p)

    def publish(self, cname):
        bus = dbus.SystemBus()
        server = dbus.Interface(bus.get_object(avahi.DBUS_NAME, avahi.DBUS_PATH_SERVER),
                avahi.DBUS_INTERFACE_SERVER)
        group = dbus.Interface(bus.get_object(avahi.DBUS_NAME, server.EntryGroupNew()),
                avahi.DBUS_INTERFACE_ENTRY_GROUP)

        cname = self.encode(cname)
        rdata = self.encode_rdata(server.GetHostNameFqdn())
        rdata = avahi.string_to_byte_array(rdata)

        group.AddRecord(avahi.IF_UNSPEC, avahi.PROTO_UNSPEC, dbus.UInt32(0),
            cname, Settings.CLASS_IN, Settings.TYPE_CNAME, Settings.TTL, rdata)
        group.Commit()

    def encode_rdata(self, name):
        """
            copied from https://gist.github.com/gdamjan/3168336
        """
        def enc(part):
            a = ToASCII(part).decode("utf-8")
            return chr(len(a)), a

        rdata = ''.join('%s%s' % enc(p) for p in name.split('.') if p) + '\0'
        return rdata

    def idle(self):
        self.main_loop.run()
