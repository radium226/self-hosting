#!/usr/bin/env python

from subprocess import Popen
import os

class Git:

    def __init__(self, context):
        self.context = context

    def clone(self):
        env = os.environ.copy()
        env["GIT_SSH_COMMAND"] = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
        process = Popen(["git", "clone", self.context.config["git"]["repo_url"], "."], cwd=str(self.context.config["git"]["folder_path"]), env=env)
        process.wait()

    def pull(self):
        env = os.environ.copy()
        env["GIT_SSH_COMMAND"] = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
        process = Popen(["git", "pull"], cwd=str(self.context.config["git"]["folder_path"]), env=env)
        process.wait()
