<h1 align="center">
Marvelous MLOps End-to-end MLOps with Databricks course

## Cao Tri DO Marvelous MLOps Training

[![Keyrus Badge](https://img.shields.io/badge/COMPANY-KEYRUS-003189?style=for-the-badge&logo=Keyrus&logoColor=00A3E0)](https://www.keyrus.com)
[![KeyrusFR Badge](https://img.shields.io/badge/COUNTRY-FR-28C6FF?style=for-the-badge&logo=Keyrus&logoColor=00A3E0)](https://www.keyrus.com)
[![KeyrusTeam Badge](https://img.shields.io/badge/TEAM-DATA--SCIENCE-FF9810?style=for-the-badge&logo=Keyrus&logoColor=00A3E0)](https://www.keyrus.com)

This repository contains all the training from Cao Tri DO, alias malganis35 on Discord for Cohort 3 of Marvelous MLOps End-to-end MLOps with Databricks course

## Practical information
- Weekly lectures on Wednesdays 16:00-18:00 CET.
- Code for the lecture is shared before the lecture.
- Presentation and lecture materials are shared right after the lecture.
- Video of the lecture is uploaded within 24 hours after the lecture.

- Every week we set up a deliverable, and you implement it with your own dataset.
- To submit the deliverable, create a feature branch in that repository, and a PR to main branch. The code can be merged after we review & approve & CI pipeline runs successfully.
- The deliverables can be submitted with a delay (for example, lecture 1 & 2 together), but we expect you to finish all assignments for the course before the 15th of June.


## Set up your environment
In this course, we use Databricks 15.4 LTS runtime, which uses Python 3.11.
In our examples, we use UV. Check out the documentation on how to install it: https://docs.astral.sh/uv/getting-started/installation/

Install task: https://taskfile.dev/installation/

Update .env file with the following:
```
GIT_TOKEN=<your github PAT>
```

To create a new environment and create a lockfile, run:
```
task dev-install
source .venv/bin/activate
```

Or, alternatively:
```
export GIT_TOKEN=<your github PAT>
uv venv -p 3.11 .venv
source .venv/bin/activate
uv sync --extra dev
```

## Technological Stack

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![docker](https://img.shields.io/badge/docker-257bd6?style=for-the-badge&logo=docker&logoColor=white)
![databricks](https://img.shields.io/badge/databricks-%23f4cccc.svg?style=for-the-badge&logo=databricks&logoColor=red)
![mlflow](https://img.shields.io/badge/mlflow-%23d9ead3.svg?style=for-the-badge&logo=numpy&logoColor=blue)

![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![GitLab](https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white)
[![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=fff)](#)

![sphinx](https://img.shields.io/badge/Sphinx-F7C942?style=flat&logo=sphinx&logoColor=white)

![vscode](https://img.shields.io/badge/vscode-%23cfe2f3.svg?style=for-the-badge&logo=visualstudiocode&logoColor=007ACC)

## Project Organization

    ├── Taskfile              <- Taskfile with commands
    ├── README.md             <- The top-level README for developers using this project.
    │
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
    ├── pyproject.toml        <- Project configuration file with package metadata for
    │                            cao_tri_do_marvelous_mlops_training and configuration for tools like ruff
    │
    ├── references            <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports               <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures           <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt      <- The requirements file for reproducing the analysis environment, e.g.
    │                            generated with `pipreqs`
    │
    ├── src                   <- Source code for use in this project.
    │   │
    │   ├──mlops_course       <- Name of your package
    │   │   ├── __init__.py   <- Makes the package a Python module
    │   │   │
    │   │   ├── data          <- Module to extract / transform / load data
    │   │   │
    │   │   ├── features      <- Module to turn raw data into features for modeling
    │   │   │
    │   │   ├── models        <- Module to train models and then use trained models to make
    │   │   │                    predictions
    │   │   │
    │   │   ├── utils         <- Module for utility functions
    │   │   │
    │   │   └── visualization <- Module to create exploratory and results oriented visualizations
    │
    ├── .env.template         <- .env file template for credentials
    ├── .gitignore            <- Standard gitignore file for DS project
    └── .pre-commit-config.yaml <- pre-commit config file

--------

<p><small>Project based on the <a target="_blank" href="https://github.com/end-to-end-mlops-databricks-3/cookiecutter-mlops-course">cookiecutter-mlops-course template</a>. #cookiecutter</small></p>

## Setup

1. Create a personnal token on Github

2. Setup your linux environment variable
EXPORT GITHUB_TOKEN = "xxxx"

3. Install Databricks extension

- Databricks
- Databricks Power Tools
