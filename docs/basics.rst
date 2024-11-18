.. _ref-to-basic_structure:

Basic structure of SimSES
========================================

1 Classes of SimSES
---------------------------

SimSES is object-oriented programmed, which allows a modular combination of various components.
The basic structure of the program can be seen in figure :ref:`class`
It shows the individual classes of SimSES in the different levels. For example, the *Commons* class has three subclasses:
*Profile*, *Data* and *State*. *Profile* in turn has the subclasses *Economic*, *Power* and *Technical*.

.. raw:: html

    <br>

.. _class:
.. figure:: images/class_diagramm_2.*

    Class diagram of SimSES.

2 Storage Systems
-------------------

The core of SimSES is the storage system, which is divided into an AC system and a DC system
(see figure :ref:`storage_system`). Each AC system has one AC/DC converter, at least one storage technology and
one DC/DC converter. With SimSES it is possible to simulate more than one storage technology (AC coupled or DC coupled).
The selectable components are described in the section configuration.

.. _storage_system:
.. figure:: images/SimSES_storageSystem.*

    AC storage system and DC Storage system in SimSES.

3 Simulation Loop
----------------------------------------
SimSES is a time continuous simulation, which means that the calculations are done step by step.
The simulation loop is shown in figure :ref:`SimSES_loop` Based on the selected
operation strategy (application) the energy management system (EMS) calculates the AC target power.
The AC target power is splitted into the various AC systems. Within each AC system the power is
converted by a AC/DC converter and splitted into the various DC systems.


.. _SimSES_loop:
.. figure:: images/SimSES_loop.*

    Simulation loop of SimSES.

4 Configuration
----------------------------------------
The configuration of the simulation can be created and changed in so-called config files.
Initially there is the default-config *simulation_defaults.ini*, which is used automatically at the start.
The simulation parameters can be changed on your own system using a local ini file, that should be named
*simulation.local.ini* and be inserted in the same folder as the default config file.
SimSES then takes all default parameters in the simulation and overwrites them, if defined, with values from the
local config file.
A description of the config files with examples can be found in the :ref:`Examples <ref-to-examples>` section.
