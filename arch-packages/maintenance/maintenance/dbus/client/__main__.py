#!/usr/bin/env python

import argparse
from maintenance.dbus.client import MaintainerDBusClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action") # this line changed

    deploy_parser = subparsers.add_parser("deploy")
    deploy_parser.add_argument("--application-name", required=True)
    def deploy(client, args):
        client.deploy(args.application_name)

    run_ansible_playbook_parser = subparsers.add_parser("run-ansible-playbook")
    run_ansible_playbook_parser.add_argument("--playbook-name", required=True)
    def run_ansible_playbook(client, args):
        client.run_ansible_playbook(args.playbook_name)

    actions = {
        "deploy": deploy,
        "run-ansible-playbook": run_ansible_playbook
    }

    args = parser.parse_args()
    client = MaintainerDBusClient()
    actions[args.action](client, args)
