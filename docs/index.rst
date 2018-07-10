.. Bookied documentation master file, created by
   sphinx-quickstart on Thu Nov  9 12:48:47 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BookieSports's documentation!
========================================

`BookieSports` is a module that contains the management information for
BOS. This management information describes which sports are supported,
which leagues and participants are available and how and what betting
markets are created and resolved.

Structure
---------

This repository contains

* the sports with emta data supported by bookied
* schema files for validation of the provided data
* a python module to facilitate loading of the data

Folders:
* `bookiesports/`: Contains the module that can be loaded from python to obtain the sports data.
* `bookiesports/bookiesports`: Each sport has it's own folder which carries the most important information in a sports-specific `index.yaml` file.
* `bookiesports/schema/`: Contains the yaml formated json schemata for validation of the bookie sports files.

Outline
-------
.. toctree::
   :maxdepth: 3

   installation
   bookiesports
   schema
   namingscheme

API
---

.. toctree::
   :maxdepth: 3

   bookiesports

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
