ANSIBLE_SSH_USER = ansible
ANSIBLE_VERBOSE = -vv

define ansible-playbook
	ANSIBLE_CONFIG="./ansible/ansible.cfg" \
		ansible-playbook \
			$(ANSIBLE_VERBOSE) \
			-i "./ansible/inventory.ini" \
			"./ansible/playbooks/$(1)" \
				-e "ansible_ssh_user='$(2)'" \
				$(shell if [[ -z "$(3)" ]]; then echo ""; else echo "--tags=$(3)"; fi ) \
				--vault-password-file="./ansible/.vault-password" \
				--extra-vars="system_maintenance='no'" \
				--limit="$(shell if [[ -z "$(4)" ]] || [[ "$(4)" == "none "]]; then echo "all"; else echo "$(4)"; fi )" #FIXME == "none" is bad
endef

define ansible-local-shell
	ANSIBLE_CONFIG="./ansible/ansible.cfg" \
		ansible \
			$(1) \
			$(ANSIBLE_VERBOSE) \
			-m "shell" \
			-a $(2) \
			-i "./ansible/inventory.ini" \
				--connection="local" \
				--vault-password-file="./ansible/.vault-password"
endef

define ansible-galaxy-install
	cd "ansible" && \
	if [[ "$(3)" == "true" ]]; then rm -Rf "./$(2)" ; mkdir -p "./$(2)" ; fi && \
	ansible-galaxy \
		$(ANSIBLE_VERBOSE) \
		install \
		-r "./$(1)" \
		-p "./$(2)" \
		--force
endef
