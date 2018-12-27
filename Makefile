include ./make/ansible.mk
include ./make/ssh.mk

GROUP = none
include ./make/groups/$(GROUP).mk

.PHONY: ssh-keygen
ssh-keygen:
	yes | ssh-keygen \
		-b "2048" \
		-t "rsa" \
		-f "./ssh/id_rsa" \
		-N "" \
		-C "self-hosting"


ANSIBLE_GALAXY_INSTALL_REQUIREMENTS_PURGE = true

.PHONY: ansible-galaxy-install-requirements
ansible-galaxy-install-requirements:
	$(call ansible-galaxy-install,requirements.yml,galaxy-roles,$(ANSIBLE_GALAXY_INSTALL_REQUIREMENTS_PURGE))


.PHONY: bootstrap
bootstrap: ansible-galaxy-install-requirements
	$(call ansible-playbook,bootstrap.yml,root,)


.PHONY: provision
provision: ansible-galaxy-install-requirements
	$(call ansible-playbook,provision.yml,$(ANSIBLE_SSH_USER),)


APPLICATION =

.PHONY: deploy
deploy: ansible-galaxy-install-requirements
	$(call ansible-playbook,deploy.yml,$(ANSIBLE_SSH_USER),$(APPLICATION))
