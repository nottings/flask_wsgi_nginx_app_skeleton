NAME := app-name
SRC_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

all: rpm

venv:
	# Create the virtualenv
	$(eval VENV := $(DEST)/opt/$(NAME))

	mkdir -p $(VENV)
	virtualenv $(VENV)

	# Add the virtualenv's bin directory into our $PATH
	$(eval export PATH := $(VENV)/bin:$(PATH))

	# Install our dependencies
	pip install -U -r $(SRC_DIR)/requirements.txt

	# Install ourselves into the virtualenv
	pip install -U $(SRC_DIR)

	# We can only do this after everything is installed
	virtualenv --relocatable $(VENV)
	rm $(VENV)/bin/activate $(VENV)/bin/activate.*

	# Un-prelink the Python executable or else rpmbuild tries to do this twice, which breaks the resulting RPM
	prelink -u $(VENV)/bin/python

	# Remove unused symlink which breaks the RPM build
	rm $(VENV)/lib64

rpm:
	rpmbuild --define "srcdir $(SRC_DIR)" --define "_topdir $(SRC_DIR)" -bb support/$(NAME).spec
