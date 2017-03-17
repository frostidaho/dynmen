mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
project_dir := $(dir $(mkfile_path))

.PHONY: all
all: uninstall install_user

.PHONY: user_reqs
user_reqs:
	@echo "----------------------------------------"
	@echo -e "Installing dynmen depdencies for $$USER from\n\t" $(project_dir)requirements.txt
	@echo "----------------------------------------"
	python -m pip install --user -r $(project_dir)requirements.txt

.PHONY: install-develop
install-develop: user_reqs
	@echo "----------------------------------------"
	@echo -e "Installing dynmen in development mode from\n\t" $(project_dir)
	@echo "----------------------------------------"
	python -m pip install --user -e $(project_dir)

.PHONY: install-user
install-user: user_reqs
	@echo "----------------------------------------"
	@echo -e "Installing dynmen into home directory from\n\t" $(project_dir)
	@echo "----------------------------------------"
	python -m pip install --user $(project_dir)

.PHONY: install
install:
	@echo "----------------------------------------"
	@echo -e "Installing dynmen - may need root\n\t" $(project_dir)
	@echo "----------------------------------------"
	python -m pip install -r $(project_dir)requirements.txt
	python -m pip install $(project_dir)

.PHONY: uninstall
uninstall:
	-python -m pip uninstall dynmen

.PHONY: tests
tests:
	@echo "----------------------------------------"
	@echo "Running tests for $$(python --version)" 
	@echo "----------------------------------------"
	python -m pytest "$(project_dir)tests/"

.PHONY: generate-options
generate-options:
	mkdir -p "$(project_dir)src/dynmen/data/"
	sh -c "$(project_dir)utils/gen_dmenu.py" > "$(project_dir)src/dynmen/dmenu.py"
	sh -c "$(project_dir)utils/gen_rofi.py" > "$(project_dir)src/dynmen/rofi.py"

.PHONY: build
build: generate-options
	python "$(project_dir)setup.py" sdist
	python "$(project_dir)setup.py" bdist_wheel

.PHONY: clean
clean:
	git clean -dxf


.PHONY: generate-test-data
generate-test-data:
	sh -c "$(project_dir)utils/gen_test_data.py" > "$(project_dir)tests/data.json"
