#!/usr/bin/env python

from subprocess import Popen

class AnsibleGalaxy:

    def __init__(self):
        pass

    def install_requirements(self, requirements_file_path, roles_folder_path, force=False):
        requirements_args = ["-r", str(requirements_file_path)]
        roles_path_args = ["-p", str(roles_folder_path)]
        command = ["ansible-galaxy"] + requirements_args + roles_path_args
        #print(f"command={command}")
        process = Popen(command)
        return_code = process.wait()
