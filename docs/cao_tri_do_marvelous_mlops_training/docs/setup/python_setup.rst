Python Setup
=========================

:Authors:
    Cao Tri DO <cao-tri.do@keyrus.com>
:Version: 2025-05

.. admonition:: Pre-requiresites

   - ``curl`` package is installed
   - ``git`` package is installed


Setup Python with ``uv``
---------------------------

Installing python 3 and utils:

.. code:: bash

    sudo apt-get update  # to update the local DB with the available remote ubuntu software
    sudo apt-get install python3-pip python-is-python3 make build-essential python3-venv


Download and Install uv

.. code:: bash

   curl -LsSf https://astral.sh/uv/install.sh | sh



Install cookiecutter
--------------------

Introduction to project squeleton
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

source: https://best-practice-and-impact.github.io/govcookiecutter/#govcookiecutter

Within the course, when you start a new Python Data Science project, you will always have to
start with our squeleton.

.. note:: **What is a squeleton ?**

   A squeleton is a template of code with which by just answering to some questions, it will
   automatically generates for you the folders, structure and initial code for you. With this,
   you can start your data science project in 2 min and have a code production ready from day 1 !
   Amazing, not ?

Within the course, we use the famous library ``cookiecutter`` (https://github.com/cookiecutter/cookiecutter)
as the framework for all our squeletons and those for Python Data Science Projects

Installation of cookiecutter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``cookiecutter`` can be installed in 2 ways:

- using **Python** : ``pip install cookiecutter`` (do not forget to install it within a pyenv environment). This is not recommended because you will have
- using **apt** : ``sudo apt-get install cookiecutter``

Be careful, even if the last way seems more confortable because it is not attached to a virtual environment, we have observe that the apt package version is not the latest.

.. code-block:: bash

   sudo apt-get install cookiecutter

After, you can add some aliases to your ``.bashrc``. For example : **marvelous-make**: This alias will allow you to create a Keyrus Data Science Project

.. code-block:: bash

   alias marvelous-make='cookiecutter git@git_repo_url'
