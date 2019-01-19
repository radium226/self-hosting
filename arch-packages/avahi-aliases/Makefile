VERSION = $(shell git rev-list --count HEAD)
NAME =  $(shell basename "$(PWD)")

./dist/$(NAME)-$(VERSION).tar.gz:
	VERSION=$(VERSION) \
		python "./setup.py" sdist \
			--format="gztar"

./$(NAME)-$(VERSION).tar.gz: ./dist/$(NAME)-$(VERSION).tar.gz
	cp "./dist/$(NAME)-$(VERSION).tar.gz" "./$(NAME)-$(VERSION).tar.gz"

.PHONY: build
build: ./$(NAME)-$(VERSION).tar.gz
	VERSION=$(VERSION) \
	NAME=$(NAME) \
		makepkg \
			--force \
			--syncdeps \
			--skipchecksums \
			--noconfirm \
			--clean \
			--cleanbuild

./.venv:
	virtualenv \
		--system-site-packages \
		"./.venv"

.PHONY: install
install: install-requirements
	VERSION="$(VERSION)" \
		pip install --editable "."

.PHONY: install-requirements
install-requirements:
	if ! yay -Q "python-gobject"; then \
		yay -S "python-gobject" --noconfirm ; \
	fi
	pip install --requirement "./requirements.txt"

.PHONY: clean
clean:
	rm -Rf "./.venv" || true
	NAME="$(NAME)" \
	VERSION="$(VERSION)" \
		python "./setup.py" clean
	rm -Rf "./dist" || true
	rm -Rf "./$(NAME)-$(VERSION).tar.gz" || true
	rm -Rf "./pkg" || true
	find . -name "*.pkg.tar.xz" | xargs -I {} rm "{}" || true
	rm -Rf "./src" || true
	find . -name "*.tar.gz" | xargs -I {} rm "{}"
	find . -name "*.tar.xz" | xargs -I {} rm "{}"
	find . -name "*.egg-info" -type "d" | xargs -I {} rm -Rf "{}"

.PHONY: develop
develop: ./.venv
	bash \
		--rcfile "./.bashrc" \
		-i

.PHONY: test
test:
	cd "../.." && \
	scp -F "ssh/config" "arch-packages/maintenance/$(shell find . -name "*.tar.xz")" "ansible@kimsufi-01:/tmp/maintenance.tar.xz" && \
	ssh -F "ssh/config" -tt "ansible@kimsufi-01" "yay -U '/tmp/maintenance.tar.xz' --noconfirm --force && sudo -u 'maintenance' maintenanced"
