#!/usr/bin/env python

from functools import reduce
import os
import toml
from pathlib import Path
import socket
from pathlib import Path
from deepmerge import Merger
from copy import deepcopy

class Context:

    DEFAULT_CONFIG = {
        "git": {
            "folder_path": "/var/lib/maintenance/self-hosting",
            "repo_url": "CHANGME"
        },
        "ansible": {
            "folder_path": "ansible",
            "playbook_folder_path": "playbooks",
            "inventory_file_path": "inventory.ini",
            "vault_password_file_path": "/etc/maintenance/vault-password",
            "requirements_file_path": "requirements.yml",
            "galaxy_roles_folder_path": "galaxy-roles",
            "config_file_path": "ansible.cfg",
            "user": "ansible"
        },
        "host": {
            "name": socket.gethostname()
        },
        "ssh": {
            "folder_path": "/etc/maintenance/ssh",
            "config_file_path": "config"
        },
        "http": {
            "token": "CHANGEME"
        }
    }

    def __init__(self, system):
        self.system = system
        self.config = Context._read_config(system)

    def __str__(self):
        return f"Context(config={self.config})"

    def __repr__(self):
        return str(self)

    @staticmethod
    def _merge_config(left_config, right_config):
        merger = Merger(
            [
                (list, ["append"]),
                (dict, ["merge"])
            ],
            ["override"],
            ["override"]
        )
        merged_config = deepcopy(left_config)
        merger.merge(merged_config, right_config)
        return merged_config

    @staticmethod
    def _read_config(system):
        def read_toml(file_path):
            try:
                return toml.loads(file_path.read_text())
            except:
                return {}

        file_paths = [
            Path("/etc/maintenance/config.toml") if system else Path.home() / ".config/maintenance/config.toml",
            Path(os.getcwd()) / "maintenance.toml"
        ]
        config = reduce(
            Context._merge_config,
            map(read_toml, file_paths),
            Context.DEFAULT_CONFIG
        )
        return config

    @staticmethod
    def path(*args):
        if str(args[-1]).startswith("/"):
            return Path(str(args[-1]))
        else:
            return Path("/".join(map(str, args)))

if __name__ == "__main__":
    context = Context()
    print(context)
