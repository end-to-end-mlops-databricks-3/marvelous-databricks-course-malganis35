=========================
VS Code Environment Setup
=========================

:Authors:
    Cao Tri DO <cao-tri.do@keyrus.com>
:Version: 2025-04

.. admonition:: Objectives
    :class: important

    This article is intended to help you set up your local development environment for the project.

VS Code Settings
================

1. Create a .vscode directory in the root of your project.

.. code-block:: bash

   mkdir .vscode

2. Create a settings.json file in the .vscode directory.

.. code-block:: bash

   nano .vscode/settings.json

3. Add the following settings to the settings.json file:

.. code-block:: json

    {
        "jupyter.interactiveWindow.cellMarker.codeRegex": "^# COMMAND ----------|^# Databricks notebook source|^(#\\s*%%|#\\s*\\<codecell\\>|#\\s*In\\[\\d*?\\]|#\\s*In\\[ \\])",
        "jupyter.interactiveWindow.cellMarker.default": "# COMMAND ----------"
    }

This will allow you to run Databricks notebooks in VS Code.
You will need to use in your .py files the following command to run the cells:

.. code-block:: python

    # COMMAND ----------

Databricks Settings
===================

1. Create a databricks.yml file in the root of your project.

.. code-block:: bash

   nano databricks.yml

2. Add the following settings to the databricks.yml file:

.. code-block:: yaml

    # This is a Databricks asset bundle definition for course-code-hub.
    # The Databricks extension requires databricks.yml configuration file.
    # See https://docs.databricks.com/dev-tools/bundles/index.html for documentation.

    bundle:
    name: course-code-hub

    targets:
    dev:
        mode: development
        default: true
        workspace:
        host: https://dbc-c2e8445d-159d.cloud.databricks.com

    ## Optionally, there could be 'staging' or 'prod' targets here.
    #
    # prod:
    #   workspace:
    #     host: https://dbc-c2e8445d-159d.cloud.databricks.com

This will allow you to run Databricks notebooks in VS Code remotely
