============================
Django Card Primitives
============================

.. image:: https://img.shields.io/badge/license-BSD-red.svg
   :target: https://raw.githubusercontent.com/aubreystarktoller/django-babik-card-primitives/master/LICENSE

This module containts utilities, fields and validators for handling bank
card information in the Django framework. It also includes JavaScript
utilities for validating card data.

Contents
========

* `Installaion`
* `Testing`
* `Contributing`
* `Authors`
* `License`

INSTALLATION
============

Django Versions Supported:

* Django 1.8 with Python 2.7, 3.2, 3.3 and 3.4
* Django 1.9 with Python 2.7, 3.4 and 3.5

To install using pip:

::

    pip install git+https://github.com/aubreystarktoller/django-babik-card-primitives.git

You can obtain the source for ``django-babik-card-primitives`` from:

::

    https://github.com/aubreystarktoller/django-babik-card-primitives

TESTING
=======

To run the tests first clone the git repo:

    git clone https://github.com/aubreystarktoller/django-babik-card-primitives
  
To run the tests you'll require ``make``. 

TESTING PYTHON CODE
-------------------
It is recommended that use tox to run
the tests:
    
    tox

To run the tests in the current environment:

    make test

CONTRIBUTING
============

Contributions are welcome. Please ensure the any submitted code is well
tested.

If you think you have found a security venerability in the code please report
it **privately** by e-mailing Aubrey Stark-Toller at aubrey@deepearth.uk.

Please **do not** raise it on the issue tracker, or publicly at all, until I
have had a chance to look into it.

AUTHORS
=======
Aubrey Stark-Toller

LICENSE
=======
``django-babik-card-primitives`` is licensed under the BSD license. See
LICENSE for the full license.
