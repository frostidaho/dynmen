mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
project_dir := $(dir $(mkfile_path))

.PHONY: all
all: uninstall install_user

.PHONY: install_develop
install_develop:
	@echo "----------------------------------------"
	@echo -e "Installing dynmen in development mode from\n\t" $(project_dir)
	@echo "----------------------------------------"
	pip3 install --user -e $(project_dir)
	pip2 install --user -e $(project_dir)

.PHONY: install_user
install_user:
	@echo "----------------------------------------"
	@echo -e "Installing dynmen into home directory from\n\t" $(project_dir)
	@echo "----------------------------------------"
	pip3 install --user $(project_dir)
	pip2 install --user $(project_dir)

.PHONY: install
install:
	@echo "----------------------------------------"
	@echo -e "Installing dynmen - may need root\n\t" $(project_dir)
	@echo "----------------------------------------"
	pip3 install $(project_dir)
	pip2 install $(project_dir)

.PHONY: uninstall
uninstall:
	-pip3 uninstall dynmen
	-pip2 uninstall dynmen

.PHONY: tests
tests:
	@echo "----------------------------------------"
	@echo "Running tests for python3"
	@echo "----------------------------------------"
	py.test "$(project_dir)tests/"
	py.test2 "$(project_dir)tests/"
