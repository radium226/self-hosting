VERSION = $(shell git rev-list --count HEAD)
NAME =  $(shell basename "$(PWD)")

./dist/$(NAME)-$(VERSION).tar.gz
	VERSION=$(VERSION) \
		python "./setup.py" sdist \
			--format="gztar"

./$(NAME)-$(VERSION).tar.gz:
	cp "./dist/$(NAME)-$(VERSION).tar.gz" "./$(NAME)-$(VERSION).tar.gz"

.PHONY: build
build: ./$(NAME)-$(VERSION).tar.gz
	PKGVER=$(VERSION) \
		makepkg \
			--force \
			--syncdeps \
			--skipchecksums \
			--noconfirm \
			--clean \
			--cleanbuild
