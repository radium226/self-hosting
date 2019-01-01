#!/usr/bin/env python

from maintenance.logging import info
from pathlib import Path
from maintenance.tools.ansible import Ansible
from maintenance.tools.git import Git
from maintenance.logging import info

from interaction.client import InteractionClient

class Maintainer(object):

    def __init__(self, context):
        self.context = context
        self.interaction_client = InteractionClient()
        print(context)

    def deploy(self, application_name):
        if self.interaction_client.ask(f"Est-ce que tu veux déployer l'application {application_name} ?", keyboard=["Oui", "Non"]) == "Oui":
            info(f"deploy({application_name})")

            folder_path = Path(self.context.config["git"]["folder_path"])
            git = Git(self.context)
            ansible = Ansible(self.context)
            if folder_path.exists():
                info("Pulling repo")
                git.pull()
            else:
                folder_path.mkdir()
                info("Cloning repo")
                git.clone()

            host_name = self.context.config["host"]["name"]
            playbook_file_path = Path(self.context.config["ansible"]["folder_path"]) / self.context.config["ansible"]["playbook_folder_path"] / "deploy.yml"
            info("Installing requirements")
            ansible.install_requirements(force=True)
            info("Running playbook")
            ansible.run_playbook(playbook_file_path, local=True, limit=[host_name], tags=[application_name])


    def run_ansible_playbook(self, playbook_name):
        info(f"run_ansible_playbook({playbook_name})")
        #AnsibleGalaxy().install_requirements(requirements_file_path, roles_folder_path)
        playbook_file_path = Path(self.context.config["ansible"]["folder_path"]) / self.context.config["ansible"]["playbook_folder_path"] / f"{playbook_name}.yml"
        Ansible(self.context).run_playbook(playbook_file_path)
