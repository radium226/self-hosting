GROUP = odroid
INSTANCE = 01

.PHONY: ssh
ssh:
	$(call ssh,odroid,$(INSTANCE))
