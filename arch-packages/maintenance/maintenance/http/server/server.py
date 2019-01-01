#!/usr/bin/env python

from maintenance.dbus.client import MaintainerDBusClient
import cherrypy

class RootController(object):

    def __init__(self, token, client):
        self.client = client
        self.token = token

    @cherrypy.expose
    def deploy(self, application_name, token):
        if token == self.token:
            self.client.deploy(application_name)
            cherrypy.response.status = "202 Accepted"
            return None
        else:
            cherrypy.response.status = "401 Unauthorized"
            return None

    @cherrypy.expose
    def run_ansible_playbook(self, playbook_name, token):
        if token == self.token:
            self.client.run_ansible_playbook(playbook_name)
            cherrypy.response.status = "202 Accepted"
            return None
        else:
            cherrypy.response.status = "401 Unauthorized"
            return None

class MaintainerHTTPServer(object):

    def __init__(self, context):
        self.context = context

    @classmethod
    def start(self, context):
        client = MaintainerDBusClient()
        token = context.config["http"]["token"]
        root_controller = RootController(token, client)
        cherrypy.config.update({
            "global": {
                "engine.autoreload.on" : False,
                "server.socket_port": 8080,
                "server.socket_host": "0.0.0.0"
            }
        })
        cherrypy.tree.mount(root_controller, "", config={
            "/": {
                #"request.dispatch": cherrypy.dispatch.MethodDispatcher(),
                "tools.trailing_slash.on": False,
            }
        })
        cherrypy.engine.start()
        return MaintainerHTTPServer(context)

    def idle(self):
        cherrypy.engine.block()

    def stop(self):
        cherrypy.engine.exit()
