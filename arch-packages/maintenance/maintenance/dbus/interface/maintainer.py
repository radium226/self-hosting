#!/usr/bin/env python

class MaintainerInterface(object):
    """
        <node>
            <interface name='com.github.radium226.Maintainer'>
                <method name='Deploy'>
                    <arg name='application_name' type='s' direction='in'/>
                </method>
                <method name='RunAnsiblePlaybook'>
                    <arg name='playbook_name' type='s' direction='in'/>
                </method>
            </interface>
        </node>
    """

    OBJECT_PATH = "/Maintainer"

    def __init__(self, maintainer):
        self.maintainer = maintainer

    def Deploy(self, application_name):
        self.maintainer.deploy(application_name)

    def RunAnsiblePlaybook(self, playbook_name):
        self.maintainer.run_ansible_playbook(playbook_name)
