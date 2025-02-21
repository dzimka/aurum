.SILENT:

SHELL=/bin/zsh

# Python version
PYTHON_VER=3.13
# Python version
# POETRY_VER=1.6.1
PYTHON_BIN=python$(PYTHON_VER)
PIP_BIN=pip$(PYTHON_VER)

# Python virtual environment name and location
VENV_DIR=venv-$(PYTHON_VER)-$(VENV)
VENVS=dev test

env: install-uv
	if [[ "$(VENV)" != "dev" && "$(VENV)" != "test" ]]; then \
		echo "Error: Invalid value for VENV. Available options: $(VENVS)"; \
		echo "Examples:"; \
		echo ">>> make env-dev"; \
		echo ">>> make env-test"; \
		exit 1; \
	fi
	echo "Checking for existing virtual environment in dir: `echo $(VENV_DIR)`"
	if [ -d "$(VENV_DIR)" ]; then \
		echo "Already exists, nothing to create."; \
		exit 0; \
	else \
		echo "Not detected, will create a new one"; \
		uv venv -p $(PYTHON_BIN) $(VENV_DIR); \
		. $(VENV_DIR)/bin/activate; \
		echo "Using `python -V` from `which python`"; \
		echo "Upgrading pip..."; \
		uv pip install --upgrade pip; \
		echo "Installing poetry"; \
		uv pip install poetry; \
	fi
	if [[ "$(VENV)" == "dev" ]]; then \
		echo "Installing development dependencies to `echo $(VENV_DIR)`"; \
		. $(VENV_DIR)/bin/activate; \
		echo "Using `python -V` from `which python`"; \
		uv pip install -r requirements.txt; \
		echo "Done!"; \
		echo "Command to activate >>> source `echo $(VENV_DIR)`/bin/activate"; \
	fi
	if [[ "$(VENV)" == "test" ]]; then \
		echo "Installing pytest dependencies"; \
		. $(VENV_DIR)/bin/activate; \
		uv pip install -r requirements.txt; \
		echo "Done!"; \
		echo "Command to activate >>> source `echo $(VENV_DIR)`/bin/activate"; \
	fi

env-dev:
	if [ -d "$(VENV_DIR)dev" ]; then \
		echo "Already exists, nothing to create."; \
		exit 0; \
	else \
		echo "Making development environment"; \
		make env VENV=dev; \
	fi

env-test:
	if [ -d "$(VENV_DIR)test" ]; then \
		echo "Already exists, nothing to create."; \
		exit 0; \
	else \
		echo "Making test environment"; \
		make env VENV=test; \
	fi

envs:
	echo "Creating virtual environments for all available options: $(VENVS)"
	make env-dev VENV=dev
	make env-test VENV=test
	echo "Done!"

install-uv:
	echo -n "Checking uv: "
	if [ -x "`command -v uv`" ]; then \
		echo "uv is already installed, updating..."; \
		uv self update; \
	else \
		echo "uv is not installed, installing..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh ; \
		echo "Please run 'source $$HOME/.cargo/env' or restart the terminal to use uv"; \
	fi
	echo "Done!"

install-pre-commit:
	echo "Installing pre-commit"
	pip install pre-commit
	pre-commit install
	echo "Done!"

# uninstall targets

uninstall-pre-commit:
	echo "Uninstalling pre-commit"
	pre-commit uninstall
	pip uninstall pre-commit
	echo "Done!"

uninstall-uv:
	echo -n "Uninstalling uv... "
	@if [ -x "`command -v uv`" ]; then \
		rm -rf $(HOME)/.cache/uv; \
		rm $(HOME)/.cargo/bin/uv; \
		echo "Done!"; \
	else \
		echo "uv is not installed"; \
	fi