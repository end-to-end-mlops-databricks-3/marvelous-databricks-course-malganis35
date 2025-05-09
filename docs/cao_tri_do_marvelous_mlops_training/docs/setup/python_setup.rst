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


Download and Install Pyenv

.. code:: bash

   curl -LsSf https://astral.sh/uv/install.sh | sh



Install cookiecutter
--------------------

Introduction to project squeleton
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

source: https://best-practice-and-impact.github.io/govcookiecutter/#govcookiecutter

Within the team, when you start a new Python Data Science project, you will always have to 
start with our squeleton.

.. note:: **What is a squeleton ?**
   
   A squeleton is a template of code with which by just answering to some questions, it will 
   automatically generates for you the folders, structure and initial code for you. With this,
   you can start your data science project in 2 min and have a code production ready from day 1 !
   Amazing, not ?

Within the team, we use the famous library ``cookiecutter`` (https://github.com/cookiecutter/cookiecutter)
as the framework for all our squeletons:

- Python Data Science Projects
- Sphinx Documentation

Example of structure created by our cookiecutter template:

.. code:: text

    ├── LICENSE
    ├── Makefile              <- Makefile with commands like `make data` or `make train`
    ├── README.md             <- The top-level README for developers using this project.
    ├── data
    │   ├── external          <- Data from third party sources.
    │   ├── interim           <- Intermediate data that has been transformed.
    │   ├── processed         <- The final, canonical data sets for modeling.
    │   └── raw               <- The original, immutable data dump.
    │
    ├── docs                  <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models                <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks             <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                            the creator's initials, and a short `-` delimited description, e.g.
    │                            `1.0-jqp-initial-data-exploration`.
    │
    ├── references            <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports               <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures           <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt      <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py              <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                   <- Source code for use in this project.
    │   ├── mypkg             <- Name of your package    
    │   │   ├── __init__.py   <- Makes src a Python module
    │   │   │
    │   │   ├── data          <- Scripts to download or generate data
    │   │   │   └── make_dataset.py
    │   │   │
    │   │   ├── features      <- Scripts to turn raw data into features for modeling
    │   │   │   └── build_features.py
    │   │   │
    │   │   ├── models        <- Scripts to train models and then use trained models to make
    │   │   │   │                 predictions
    │   │   │   ├── predict_model.py
    │   │   │   └── train_model.py
    │   │   │
    │   │   └── visualization <- Scripts to create exploratory and results oriented visualizations
    │   │       └── visualize.py
    │
    └── tox.ini               <- tox file with settings for running tox; see tox.readthedocs.io

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

