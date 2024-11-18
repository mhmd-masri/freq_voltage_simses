Quickstart
========================================
.. note::
    Installation is only tested on Microsoft Windows 10 Enterprise.
.. note::
    We plan to provide SimSES by PyPi package management in the future


We recommend installing SimSES (and in general third-party) python packages in a
virtual environment, encapsulated from the system python distribution.
This is optional. To install SimSES in windows, it is currently recommended to use
`Anaconda <https://www.anaconda.com/distribution/>`_
and create a virtual environment (Python 3.6 or 3.7) with Anaconda. Creating a virtual environment with
Anaconda can be done within the Anaconda Navigator (Environments | Create) or via terminal.
A more deailed deocumentaion about virtual environment and how to create them can be found
`here <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_.

Download and Configure SimSES Project
------------------------------------------
After creating an virtula environment you can clone SimSES from servers hosted by the 'leibniz rechenzentrum'.
You can easily clone (git) SimSES via: https://gitlab.lrz.de/ees-ses/opensimses. After cloning SimSES you can
open the project within a Python IDE (e.g. `PyCharm <https://www.jetbrains.com/pycharm/>`_).
As project interpreter please select the before created virtual environment. In Pycharm this
can be done in Settings | ProjectInterpreter.

To start SimSES you have to install some required packages. This can be done by executing setup.py.
This installs the following packages:

- scipy
- numpy
- pandas
- matplotlib

SimSES can be simply start with executing the main.py. This script starts the simulation as well as the
analysis with some basic settings. All possible settings as well as the code structure will be explained
in the following chapter. 



