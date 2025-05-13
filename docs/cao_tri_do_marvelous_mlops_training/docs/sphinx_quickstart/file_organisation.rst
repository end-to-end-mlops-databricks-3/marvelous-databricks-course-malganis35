====================
Files organisation
====================

:Authors:
    Cao Tri DO <cao-tri.do@keyrus.com>
:Version: 2025-02

Main index.rst file
===================

The main ``index.rst`` file has a ``.. toctree::`` it point to all ``.rst`` and ``.md`` files.

.. code::

  # index.rst
  .. toctree::
     :maxdepth: 2
     :caption: Contents:

     /src/main.rst
     /src/sphinx_tutorial/index.rst
     /src/sphinx_tutorial/markdown.md

.. note::
  Our Sphinx documentation covered both ``.rst`` and ``.md`` files.

  We recommanded in general to use ``.rst`` as the language offered more possibility for documentation through the multiple directives.

Pointing to index.rst from toctree can be chained
=================================================

.. code::

  # /src/sphinx_tutorial/index.rst

  .. toctree::
     :maxdepth: 3
     :caption: RST syntaxe to document serious projects:

     /src/sphinx_tutorial/wiki_syntax_demo.rst
     /src/sphinx_tutorial/mermaid_syntax_demo.rst
     /src/sphinx_tutorial/file_organisation.rst


.. code::

  ├── index.rst      # main Table of Contents
  ├── src
  │   ├── images
  │   │   ├── betty_blocks.webp
  │   │   └── mendix_01.jpeg
  │   ├── bettyBlocks.rst          # subsections will be exposed
  │   ├── mendix.rst
  │   ├── powerPlatform.rst
  │   ├── contact.rst
  │   ├── commonTopics
  │   │   ├── Authentication.rst
  │   │   └── MultiTenancy.rst
  │   └── sphinx_tutorial
  │       ├── index.rst            # root index.rst will point to this one
  │       ├── mermaid_syntax_demo.rst
  │       ├── file_organisation.rst
  │       └── wiki_syntax_demo.rst
  └── ...



To add left menu sections that can be fold/unfold it's only matter to make the first
level of ``index.rst`` file to point to a submenu ``sphinx_tutorial/index.rst``:

.. mermaid::

   flowchart LR

     src(index.rst)
     main(src/main.rst)
     sp_index(src/sphinx_tutorial/index.rst)
     wiki_syntax_demo(src/sphinx_tutorial/wiki_syntax_demo.rst)
     file_organisation(src/sphinx_tutorial/file_organisation.rst)

     src --> main
     src --> sp_index
     sp_index --> wiki_syntax_demo
     sp_index --> file_organisation
