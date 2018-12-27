ANSIBLE_SSH_USER = ansible
ANSIBLE_VERBOSE = -vv


define ansible-playbook
	ANSIBLE_CONFIG="./ansible/ansible.cfg" \
		ansible-playbook \
			$(ANSIBLE_VERBOSE) \
			-i "./ansible/inventory.ini" \
			"./ansible/playbooks/$(1)" \
				-e "ansible_ssh_user='$(2)'" \
				$(shell if [[ -z "$(3)" ]]; then echo ""; else echo "--tags=$(3)"; fi )
endef


define ansible-galaxy-install
	cd "ansible" && \
	if $(3); then rm -Rf "./$(2)" ; mkdir -p "./$(2)" ; fi && \
	ansible-galaxy \
		$(ANSIBLE_VERBOSE) \
		install \
		-r "./$(1)" \
		-p "./$(2)" \
		--force
endef
