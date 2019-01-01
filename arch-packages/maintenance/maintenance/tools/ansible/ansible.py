#!/usr/bin/env python

from subprocess import Popen
import os
from pathlib import Path
from maintenance.context import Context
import shutil
class Ansible:

    def __init__(self, context):
        self.context = context

    def install_requirements(self, force=False):
        folder_path = Path(self.context.config["git"]["folder_path"])
        ansible_folder_path = Path(self.context.config["ansible"]["folder_path"])
        requirements_file_path = ansible_folder_path / self.context.config["ansible"]["requirements_file_path"]
        galaxy_roles_folder_path = ansible_folder_path / self.context.config["ansible"]["galaxy_roles_folder_path"]
        if force and (folder_path / galaxy_roles_folder_path).exists():
            shutil.rmtree(str(folder_path / galaxy_roles_folder_path))

        requirements_args = ["-r", str(requirements_file_path)]
        roles_path_args = ["-p", str(galaxy_roles_folder_path)]
        action_args = ["install"]
        command = ["ansible-galaxy", "-vvvv"] + action_args + requirements_args + roles_path_args
        #print(f"command={command}")
        env = os.environ.copy()
        env["GIT_SSH_COMMAND"] = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
        process = Popen(command, cwd=str(folder_path), env=env)
        return_code = process.wait()

    def run_playbook(self, playbook_file_path, limit=[], local=False, tags=[]):
        folder_path = Path(self.context.config["git"]["folder_path"])
        ansible_folder_path = Path(self.context.config["ansible"]["folder_path"])
        ssh_folder_path = Path(self.context.config["ssh"]["folder_path"])
        playbook_folder_path = ansible_folder_path/ self.context.config["ansible"]["playbook_folder_path"]
        inventory_file_path = ansible_folder_path / self.context.config["ansible"]["inventory_file_path"]
        vault_password_file_path = Context.path(ansible_folder_path, self.context.config["ansible"]["vault_password_file_path"])
        requirements_file_path = ansible_folder_path / self.context.config["ansible"]["requirements_file_path"]
        roles_folder_path = ansible_folder_path / self.context.config["ansible"]["galaxy_roles_folder_path"]
        config_file_path = ansible_folder_path / self.context.config["ansible"]["config_file_path"]
        ssh_config_file_path = Context.path(ssh_folder_path, self.context.config["ssh"]["config_file_path"])
        user = self.context.config["ansible"]["user"]
        galaxy_roles_folder_path = ansible_folder_path / self.context.config["ansible"]["galaxy_roles_folder_path"]

        inventory_args = [f"--inventory-file={str(inventory_file_path)}"]
        limit_args = [f"--limit={','.join(limit)}"] if len(limit) > 0 else []
        connection_args = ["--connection=local"] if local else []
        playbook_args = [str(playbook_file_path)]
        vault_password_args = [f"--vault-password-file={str(vault_password_file_path)}"] if vault_password_file_path else []
        ssh_extra_args = [] if local else ["--ssh-extra-args", f"-F {str(ssh_config_file_path)}"]
        extra_vars_args = ["--extra-vars", "system_maintenance='yes'"] + [] if local else ["--extra-vars", f"ansible_ssh_user='{user}'"]
        tags_args = ["--tags=" + ",".join(tags)] if len(tags) > 0 else []
        command = ["sudo", "--preserve-env=ANSIBLE_CONFIG,GIT_SSH_COMMAND", "-u", user] + ["ansible-playbook", "-vvv"] + inventory_args + playbook_args + extra_vars_args + tags_args + connection_args + vault_password_args + ssh_extra_args + limit_args
        print(f"command={command}")
        print((" ").join(command))

        env = os.environ.copy()
        env["ANSIBLE_CONFIG"] = str(config_file_path)
        env["GIT_SSH_COMMAND"] = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"

        process = Popen(command, env=env, cwd=str(folder_path))
        return_code = process.wait()
