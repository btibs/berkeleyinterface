SHELL := /bin/sh

LOCALPATH := $(CURDIR)
TESTPATH := $(LOCALPATH)/tests

.PHONY: test

test:
	nosetests -v --with-coverage --cover-package=BerkleyInterface --cover-inclusive --cover-erase tests
