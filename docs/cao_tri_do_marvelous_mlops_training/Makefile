# Minimal makefile for Sphinx documentation

# Put it first so that "make" without argument is like "make help".
help_sphinx:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help_sphinx Makefile

#################################################################################
# GLOBALS                                                                       #
#################################################################################
# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

PYTHON_INTERPRETER = python3
PYTHON_VERSION = 3.12.0
PROJECT_NAME = cao_tri_do_marvelous_mlops_training

# Source for a good Python Makefile: https://gist.github.com/genyrosk/2a6e893ee72fa2737a6df243f6520a6d

# Colors for echos
ccend=$(shell tput sgr0)
ccbold=$(shell tput bold)
ccgreen=$(shell tput setaf 2)
ccred=$(shell tput setaf 1)
ccso=$(shell tput smso)

#################################################################################
# ENV CHECK                                                                     #
#################################################################################

# Check if Anaconda is present in the system
ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

# Check if Pyenv is present in the system
ifeq (,$(shell which pyenv))
HAS_PYENV=False
else
HAS_PYENV=True
endif

# Check if Poetry is present in the system
ifeq (,$(shell which poetry))
HAS_POETRY=False
else
HAS_POETRY=True
endif

# Check if the current directory if a git repo
IS_GIT_REPO := $(shell git rev-parse --is-inside-work-tree 2>/dev/null)

#################################################################################
# COMMANDS (GENERAL)                                                            #
#################################################################################

## Test python environment is setup correctly
test_environment:
	@echo "$(ccso)--> Test the local virtual env systems available$(ccend)"
ifeq (True,$(HAS_CONDA))
	@echo ">>> Conda is $(ccgreen)available$(ccend)"
else
	@echo ">>> Conda is $(ccred)not available$(ccend)"
endif
ifeq (True,$(HAS_PYENV))
	@echo ">>> Pyenv is $(ccgreen)available$(ccend)"
else
	@echo ">>> Pyenv is $(ccred)not available$(ccend)"
endif
ifeq (True,$(HAS_POETRY))
	@echo ">>> Poetry is $(ccgreen)available$(ccend)"
else
	@echo ">>> Poetry is $(ccred)not available$(ccend)"
endif

#################################################################################
# COMMANDS (SETUP)                                                            #
#################################################################################

## Install Python Dependencies (Dev)
dev_install:
	@echo "$(ccso)--> Install Python Dependencies (Dev)$(ccend)"
	pip install -r requirements.txt

## Install latex dependencies
latex_setup:
	sudo apt-get install texlive-xetex texlive-latex-base texlive-extra-utils
	sudo apt-get install texlive-fonts-extra

## Set up python interpreter environment (pyenv)
create_pyenv_env:
	@echo "$(ccso)--> Set up python interpreter environment (pyenv)$(ccend)"
ifeq (True,$(HAS_PYENV))
	@echo ">>> Detected pyenv, creating pyenv environment."
	pyenv virtualenv $(PYTHON_VERSION) $(PROJECT_NAME)
	@echo ">>> New pyenv created. Activate with: pyenv activate $(PROJECT_NAME)"
	pyenv local $(PROJECT_NAME)
	@echo ">>> By default, the pyenv is activated in the local folder"
else
	@echo ">>> No virtualenv packages installed. Please install one above first"
endif

## Delete pyenv environment
delete_pyenv_env:
	@echo "$(ccso)--> Delete pyenv environment$(ccend)"
	pyenv virtualenv-delete $(PROJECT_NAME)

#################################################################################
# COMMANDS (SPHINX)                                                         #
#################################################################################

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

## Delete all compiled _build/ folder
clean:
	@echo "Delete _build directory"
	rm -r "$(BUILDDIR)"

## Automatically generate HTML documentation
livehtml:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

## PDF Build with LateX
pdf_build:
	- make latexpdf LATEXMKOPTS="-interaction=nonstopmode"
	- make latexpdf LATEXMKOPTS="-interaction=nonstopmode"
	- cp ./_build/latex/keyrus_training.pdf ./_build/

## PDF Build with SimplePDF
simplepdf_build:
	- make simplepdf


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

## Initial setup to follow
help_setup:
	@echo "$(ccso)--> Initial setup to follow$(ccend)"
	@echo "1. (optional) install pyenv if not already installed: curl https://pyenv.run | bash"
	@echo "2. (optional) if python $(PYTHON_VERSION) is not your default env, we recommend to add it to your pyenv. Follow the guide on the knowledge center"
	@echo "3. (recommanded) test to see what python virtual environment manager is present in your system: make test_environment"
	@echo "4. create a pyenv environment with pyenv virtualenv system cao_tri_do_marvelous_mlops_training"
	@echo "5. activate your local environment with pyenv activate cao_tri_do_marvelous_mlops_training"
	@echo "**Note**: you can install step 4 and 5 using: make create_pyenv_env"
	@echo "6. install the requirements using: make dev-install"
	@echo "7. (optional) clean your environment using: pyenv virtualenv-delete cao_tri_do_marvelous_mlops_training"

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
	@echo
