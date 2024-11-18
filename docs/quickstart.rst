.. _ref-to-quickstart:

Quick Start Guide
========================================

1 Installation
------------------------------------------
To install SimSES, a Python version of 3.8 or higher is required, along with an IDE such as PyCharm (https://www.jetbrains.com/pycharm/) or VS Code (https://code.visualstudio.com/).
It is recommended to install SimSES, as well as other third-party Python packages, within a virtual environment that is separate from the system's Python distribution.
The current recommendation, for Windows installations, is to use Anaconda to create a virtual environment.
For more comprehensive documentation on virtual environments and how to set them up, please refer see :ref:`ref-to-anaconda`.
Utilizing a virtual environment ensures that all necessary dependencies are installed.
The dependencies required for SimSES include scipy, numpy, numpy_financial, pandas, plotly, matplotlib, and pytz.

1.1 Download SimSES Project from Git
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
After setting up your virtual environment, you can proceed to clone SimSES from Git.

1. To clone the SimSES repository, if PyCharm is newly installed, launch PyCharm and select **Get from VCS** (which can also be found under *Git* --> *Clone*). Next, click on **Download and Install Git**.
Once the Git installation is complete, copy the link https://gitlab.lrz.de/open-ees-ses/simses.git and paste it into the **Repository URL** field. Confirm to start the cloning process.
You will be prompted to log in to your GitLab profile; proceed with the login and then select **Trust project**.
If the virtual environment was already created in the previous step, cancel the creation of a virtual environment for the prompted window in PyCharm.

2. For the project interpreter, make sure to select the virtual environment you created earlier. To do this, follow these steps:

    a. click **No Interpreter** in the lower right corner
    b. select **Add New Interpreter**
    c. select **Add Local Interpreter…**
    d. click **Conda Environment** on the left
    e. select **'…'** for **Interpreter** and choose the Python Interpreter in the local preinstalled Conda-Environment, which can usually be found in e.g. *'Users\\NAME\\anaconda3\\envs\\<name of the new environment>\\python.exe'*.

1.2	Test SimSES with Default Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
After having completed the previous steps you can start SimSES for the first time.
This can be done by running the main function of the system, which can be found under *simses* --> *main.py*. This starts SimSES with the default settings.
The simulation name is by default *simses_1*, but can be newly defined in the *main.py* by specifying the value of *simulation_name* at the bottom of the code.


1.3	Results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
After having run the main, SimSES creates a folder with the results. The default result path is *'\\results\\simses_1\\'*, which can also be modified in *main.py* by specifying the value of *result_path* and *simulation_name*.
Each new simulation result will then be summarized in a new subfolder of *'results\\<simulation_name>\\'* with the folder name revealing the start time of the simulation.
After completing the simulation, a HTML file should open automatically in your Browser, if not it can be opened by clicking on the *Results.html* file in the results folder.
This website contains a graphical analysis including a *System Technical Evaluation*
such as system power and system SOC as well as as the power losses.
Further included are a thermal analysis and the Site Level Evaluation and the Economic Evaluation as well as the Technical Evaluation for the storage technology,
here the Lithium Ion Technical Evaluation.

The pictures below show a few examples of the results html file.
The first image :ref:`system-power-analysis`, presents an analysis of the system’s AC and DC power,
which includes the DC power of the storage system and the intermediate circuit.
All values are measured in watts (W). The data also provide a more detailed analysis, such as the power losses illustrated in the second image :ref:`power-losses`.
Additionally, the results include an in-depth evaluation of the system's components, for example, the current and voltage of the lithium-ion system, as shown in :ref:`libsystem`.

.. figure:: images/SystemPowerAnalysis_SimSES.*
    :name: system-power-analysis

    System power analysis

.. figure:: images/PowerLosses_SimSES.*
    :name: power-losses

    Power losses of the system

.. figure:: images/CurrentandVoltage_LIB_SimSES.*
    :name: libsystem

    Current and voltage for the lithium-ion system


2 Explanation of Default Simulation
------------------------------------------

SimSES operates by leveraging specific files that are provided to its constructor.
These files contain configuration parameters with detailed descriptions and are essential for the simulation and analysis.
There are four categories of files: simulation, data, analysis and logger.
Within the main SimSES folder, you'll find four *.defaults.ini* files corresponding to these categories.
These are: *simulation.defaults.ini*, *data.defaults.ini*, *analysis.defaults.ini* and *logger.defaults.ini*.
They are used to create the aforementioned results with the *simulation.defaults.ini* being the most important one.

The *simulation.defaults.ini* is divided into sections: General, Energy Management, Battery, Storage System and Profile.

In the **General** section, the timing of the simulation is set.
For this particular example, the simulation spans from 00:00:00 on January 1, 2014, to 03:59:59 on January 1, 2014.

In the **Energy Management** section, the operation strategy or application is specified.
In this instance, the *PowerFollower* strategy is utilized, aiming to replicate a given AC power profile using the storage system.
It's also here where you can set the minimum and maximum State of Charge (SOC) for the storage, with our example storage system ranging from a minimum SOC of 0 to a maximum SOC of 1.
Subsequently, specific storage parameters are detailed in the **Battery** section.

Following this, the **Storage System** is outlined, which primarily defines the power electronics of the system.
It involves setting up the AC-storage system configuration, the ACDC-converter, as well as any optional components such as housing and a HVAC system.
In the default scenario, no housing or climate control system is included. Finally, the DC-storage system and the DCDC-converter are delineated.
Here also the specific storage technology can be defined, using a lithium-ion generic cell in the default case.
The ambient temperature profile can be chosen with a constant ambient temperature of 25° C as a default setting.

In the **Profile** section, specific data files are referenced for the program to run simulations.
Three profile types can be integrated into the simulation file: a Power profile, a Technical profile, and a Thermal profile.
By default, a random power profile is selected. To simulate specific application cases, custom data can be input and utilized as profiles.
Detailed instructions on how to implement own data files will be provided in the :ref:`ref-to-extended`



3 Configuration of Simulation
------------------------------------------

To use your own data and values or to modify the simulation, the *(simulation/analysis/data/logger).defaults.ini* files must be copied into the same folder and named *(simulation/analysis/data/logger).local.ini*.
The local configurations/values defined in the *.local.ini* file will override the values specified in the *.defaults.ini*.
For the values that have not been overwritten, the values from the *.defaults.ini* will be used.
This has the advantage that not all parameters need to be reconfigured every time, as many parameters often remain the same.
The overwritten data in the *.defaults.ini* file will be ignored by SimSES.
There is always only one *.local.ini* file for each of the four segments.
SimSES uses the local file for the simulation. There is more detailed description how to :ref:`to-modify-simulation`.


4 Next Steps
------------------------------------------
The :ref:`ref-to-extended` explains
    + how to create a virtual environment in anaconda
    + how to modify the *simulation.ini*
    + how to upload own user specific files
    + detailed description of the results



