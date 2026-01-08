Installation
============

Prerequisites
-------------

Zuspec requires Python 3.8 or later. We recommend using Python 3.10 or newer.

Installing with pip
-------------------

The core Zuspec language package can be installed via pip:

.. code-block:: bash

   pip install zuspec-dataclasses

Installing Backend Packages
----------------------------

Depending on your use case, you may want to install additional backend packages:

SystemVerilog Backend
~~~~~~~~~~~~~~~~~~~~~

For generating SystemVerilog RTL:

.. code-block:: bash

   pip install zuspec-be-sv

Software Backend
~~~~~~~~~~~~~~~~

For generating C/C++ software models:

.. code-block:: bash

   pip install zuspec-be-sw

HDL Simulation Backend
~~~~~~~~~~~~~~~~~~~~~~

For HDL cosimulation:

.. code-block:: bash

   pip install zuspec-be-hdlsim

Trace Backend
~~~~~~~~~~~~~

For generating execution traces:

.. code-block:: bash

   pip install zuspec-be-trace

Formal Verification Backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For formal verification:

.. code-block:: bash

   pip install zuspec-be-fv

Development Installation
------------------------

To install Zuspec packages from source for development:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/zuspec/zuspec.github.io.git
   cd zuspec.github.io
   
   # Install using ivpm
   python3 -m pip install ivpm
   python3 -m ivpm update

Verifying Installation
----------------------

To verify your installation:

.. code-block:: python

   import zuspec_dataclasses as zdc
   print(zdc.__version__)

Next Steps
----------

After installation, check out the Zuspec Dataclasses
documentation to learn about the core language features.
