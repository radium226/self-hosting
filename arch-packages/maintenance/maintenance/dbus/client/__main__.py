#!/usr/bin/env python

import argparse
from maintenance.dbus.client import MaintainerDBusClient
from maintenance.context import Context

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--system", action="store_true", default=False)
    subparsers = parser.add_subparsers(dest="action")

    deploy_parser = subparsers.add_parser("deploy")
    deploy_parser.add_argument("--application-name", required=True)
    def deploy(client, args):
        client.deploy(args.application_name)

    run_ansible_playbook_parser = subparsers.add_parser("run-ansible-playbook")
    run_ansible_playbook_parser.add_argument("--playbook-name", required=True)
    def run_ansible_playbook(client, args):
        client.run_ansible_playbook(args.playbook_name)

    upgrade_system_parser = subparsers.add_parser("upgrade-system")
    def upgrade_system(client, args):
        client.upgrade_system()

    actions = {
        "deploy": deploy,
        "run-ansible-playbook": run_ansible_playbook,
        "upgrade-system": upgrade_system
    }

    args = parser.parse_args()
    context = Context(args.system)
    client = MaintainerDBusClient(context)
    actions[args.action](client, args)
