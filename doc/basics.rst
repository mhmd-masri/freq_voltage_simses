Basic structure of SimSES
========================================
SimSES is object-oriented programmed, which allows a modular combination of various components.
The core if SimSES is the storage system,
which is divided into an AC system and a DC system (see figure :ref:`storage_system`). Each AC system
has one AC/DC converter at least one storage technology and one DC/DC converter. With SimSES
it is possible to simulate with more than one storage technology (AC coupled or DC coupled).
The selectable components a described in section configuration.


.. raw:: latex
    \newpage

.. _storage_system:
.. figure:: images/SimSES_storageSystem.*

    AC storage system and DC Storage system in SimSES.

Simulation Loop
=======================================
SimSES is a time continuous simulation, which means that the calculations are done step by step.
The simulation loop is showed in figure :ref:`SimSES_loop` Based on the selected
operation strategy (application) the energy management system (EMS) calculates the AC target power.
The AC target power is splitted into the various AC systems. Within each AC system the power is
converted by a AC/DC converter and splitted into the various DC systems.


.. _SimSES_loop:
.. figure:: images/SimSES_loop.*

    Simulation loop of SimSES.

Configuration
=======================================
