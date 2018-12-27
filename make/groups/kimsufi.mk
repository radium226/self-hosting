GROUP = kimsufi
INSTANCE = 01

.PHONY: ssh
ssh:
	$(call ssh,kimsufi,$(INSTANCE))
