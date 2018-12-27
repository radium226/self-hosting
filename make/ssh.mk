SSH_USER = root

define ssh
	ssh \
		-F "./ssh/config" \
		-tt \
		$(SSH_USER)@$(1)-$(2) \
		bash -i
endef
