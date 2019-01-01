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


.PHONY: ansible-galaxy-install-requirements
ansible-galaxy-install-requirements:
	$(call ansible-galaxy-install,requirements.yml,galaxy-roles,$(DOWNLOAD_ROLES))


.PHONY: bootstrap
bootstrap: #ansible-galaxy-install-requirements
	$(call ansible-playbook,bootstrap.yml,root,$(STEP),$(GROUP))


.PHONY: provision
provision: #ansible-galaxy-install-requirements
	$(call ansible-playbook,provision.yml,$(ANSIBLE_SSH_USER),$(STEP),$(GROUP))


APPLICATION =

.PHONY: deploy
deploy: #ansible-galaxy-install-requirements
	$(call ansible-playbook,deploy.yml,$(ANSIBLE_SSH_USER),$(APPLICATION),$(GROUP))

.PHONY: ansible-vault-edit
ansible-vault-edit:
	cd "./ansible" && \
	ansible-vault \
		edit \
		--vault-password-file="./.vault-password" \
		$(ANSIBLE_VERBOSE) \
			"./group_vars/all/vault.yml"

define knock
	$(call ansible-local-shell,all,"knock -d 1000 {{ knockd_host_name }} {{ $(1)_knockd_sequence | replace(',', ' ') }}")
endef

define open-ssh-port
	$(call knock,ssh_server)
endef

.PHONY: knock
knock:
	$(call knock,$(APPLICATION))

.PHONY: open-ssh-port
open-ssh-port:
	$(call open-ssh-port)


.PHONY: copy-to
copy-to:
	$(call ansible,$(GROUP),copy,'src="$(SRC)" dest="$(DEST)"')
