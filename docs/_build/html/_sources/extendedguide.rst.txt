.. _ref-to-extended:

Extended Guide
========================================

.. _ref-to-anaconda:

1 Create a Virtual Environment
------------------------------------------

It is recommended to install SimSES and third-party Python packages in a virtual environment isolated from the system Python distribution using Anaconda.
The Anaconda interpreter can be integrated into the IDE such as PyCharm and VS Code to optimize the development environment for your projects.
The following steps are necessary:

1. Get Anaconda https://www.anaconda.com/products/distribution.

2. Create a new environment in Anaconda:

To create a virtual environment for SimSES in **Anaconda Navigator** proceed with the following steps.
A more detailed documentation about
virtual environments and how to create them can be found in https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html.

    + run Anaconda
    + click **Environments**
    + click **Create**
    + name the new environment (i.e. SimSES) and choose a Python version ≥ Python 3.8
    + after confirming creating a new environment wait until all packages are loaded
    + click on **Play button** and **Open Terminal** to install dependencies in the created virtual environment

Alternatively, the new environment can be activated in a terminal by calling the command:
::
    conda activate <name of the new environment>

3.Install dependencies.
The following packages are required for SimSES:
    - scipy
    - numpy
    - numpy_financial
    - pandas
    - plotly
    - matplotlib
    - pytz
Install the packages using pip:
::
    pip install numpy-financial scipy numpy plotly matplotlib pytest pytz

After all packages have been installed you can close Anaconda.



.. _ref-to-modify-simulation:

2 Modify the Simulation File
------------------------------------------

In the *simulation.local.ini* file, the following options are available for customization:

**Section: GENERAL:**
    - `START`: Format: YYYY-MM-DD HH:MM:SS - Specifies the start time of the simulation.
    - `END`: Format: YYYY-MM-DD HH:MM:SS - Determines the end time of the simulation.
    - The duration of the simulation must align with the duration of the data profiles used.
    - `TIME_STEP`: The time step of the simulation in seconds, e.g. 1.
    - `LOOP`: The number of simulation cycles.

---


**Section: ENERGY MANAGEMENT:**
In this section, the operation strategy is defined, which can be either Single Use or Multi Use.
Please note that the necessity of these parameters varies depending on the selected operation strategy
and the specifics of the application case. Not every parameter must be filled out for each scenario.
For instance, FCR_RESERVE may not be relevant for scenarios focused purely on EV charging.
However, at least one of the available strategies must be selected for the simulation to proceed.
Also, ensure that the load, generation, and technical profiles match the requirements of the chosen strategy.


**Available Strategies in ENERGY MANAGEMENT Section:**

- **PowerFollower**: Simulates an AC power profile with the storage system, aiming to match the specified power profile.

- **SOCFollower**: Attempts to follow a specified State-of-Charge profile with the storage system.

- **ResidentialPvGreedy**: For residential storage with a PV system, employing a greedy strategy. The storage is charged whenever there's surplus generation from the PV.

- **ResidentialPvFeedInDamp**: Simulates residential storage with a PV system using a feed-in damp strategy, where the storage is charged one hour before sunset.

- **IntradayMarketRecharge**: Simulates recharging based on the intraday market.
    - `POWER_IDM`: Specifies the power available for IDM recharge in watts.

- **SimplePeakShaving**: Aims to reduce peak load.
        - `MAX_POWER`: Sets the peak-shaving limit for the entire year in watts.
        - `MAX_POWER_MONTHLY`: Defines monthly peak-shaving limits in watts. The first value is for January, the second for February, and so on.
        - `MAX_POWER_MONTHLY_MODE`: When set to True, uses the monthly peak-shaving limits from `MAX_POWER_MONTHLY`. If False, `MAX_POWER` is used as the limit for the entire simulation.

- **PeakShavingPerfectForesight**: Reduces peak load with perfect foresight of the load profile, maintaining a low SOC to minimize calendar aging.
      - `MAX_POWER`: Sets the yearly peak-shaving limit in watts.

- **FrequencyContainmentReserve (FCR)**: Participates in the FCR market without recharging. Adheres to German regulations.
        - `POWER_FCR`: Power offered to the FCR market in watts.
        - `SOC_SET`: Target SOC for FCR simulations.
        - `FCR_RESERVE`: Full power reserve for alert state in hours, defaulting to 0.25 (15-minute criterion).

- **FcrIdmRechargeStacked**: A multi-use strategy for FCR market participation with IDM recharge.
     - `POWER_IDM`: Power available for Intraday Market participation in watts.
     - `AUTOMATED_FCR_IDM_ALLOCATION`: Enables automated power allocation for FCR with IDM recharge according to current German TSO requirements.

- **ElectricVehicle**: Simulates the load on EV batteries during driving and recharges using a power profile and a binary profile.
     - `EV_CHARGING_STRATEGY`: Selects the charging strategy, such as Uncontrolled.
     - `MAX_POWER`: Sets the maximum AC charging power in watts.

- **ElectricVehicleSOC**: Simulates the load on EV batteries during driving and recharges using an SOC profile and a binary profile.
        - `EV_CHARGING_STRATEGY`: Options include Original, Uncontrolled, Mean_power, Paused.
        - `MAX_POWER`: Maximum AC charging power in watts.

- **EvChargerWithBuffer**: Simulates buffer storage for EV charging stations.
    - `MAX_POWER`: Maximum AC grid power in watts.

**SOC Limits**: `MIN_SOC` and `MAX_SOC` in p.u [0,1[ and ]0,1] respectively, set the lower and upper SOC limits of the storage system. Adjust these values if the technology's SOC range differs from [0;1].




**Storage Technology:**


Available storage technologies within the system include batteries, redox-flow cells, and hydrogen-based systems which encompass both electrolyzers for hydrogen production and fuel cells for energy conversion.

For these technologies, you can define various parameters such as:
    - `MIN_SOC`: x.x [Number between 0.0 and 1.0 indicating the minimum state of charge]
    - `MAX_SOC`: x.x [Number between 0.0 and 1.0 indicating the maximum state of charge]
    - `EOL`: x.x [Number between 0.0 and 1.0 indicating the end of life criteria]
    - `START_SOH`: x.x [Number between 0.0 and 1.0 indicating the initial state of health]
    - Other parameters like START_SOH_SHARE, START_RESISTANCE_INC, and EXACT_SIZE can be set to [True/False], alongside PRESSURE_CATHODE, PRESSURE_ANODE, and TEMPERATURE.
Please remember that not every parameter is applicable to all storage technologies.


---

**Section: STORAGE SYSTEM:**


In this section the structural framework of the storage system will be established by detailing the AC-DC system topology,
as well as the housing and HVAC setup.
Each storage system must include a minimum of one AC storage system paired with a corresponding AC-DC converter.
One AC storage system can be connected to multiple DC storage systems and must be connected to at least one DC system.
When configuring, ensure that the names you choose for the ACDC converter, housing, HVAC system, DCDC converter and storage technology are consistent with the definitions provided
in later sections of your configuration document.
These names serve as identifiers that link the physical components of the storage system to their operational characteristics within the simulation environment.
For the respective types such as converter type or housing type, a name that aligns with one of the listed
types available in the configuration options must be selected.
This name matching is critical to ensure that the selected converter's specifications are recognized by the system.





- **STORAGE_SYSTEM_AC**: format:
    - `AC-system name, max AC power in W, DC voltage level in V, ACDC converter name, housing name, HVAC name`

- **ACDC_CONVERTER**: format:
    - `ACDC Converter name, converter type, [optional: number of converters]`
    - ACDC converter types available for selection: `NottonAcDcConverter`, `FixEfficiencyAcDcConverter`, (additional types: `BonfiglioliAcDcConverter`, `Sinamics120AcDcConverter`, `SungrowAcDcConverter`, `M2bAcDcConverter`).

- **HOUSING**: format:
     - `housing name, housing type, [optional: high cube [True/False], housing azimuth in °, housing absorptivity, ground albedo]`
     - Available options for housing type are: `NoHousing`, `TwentyFtContainer`, `FortyFtContainer`.
     - Default values for the optional parameters are `False` for high cube, `0` for azimuth, `0.15` for absorptivity, and `0.2` for ground albedo.
     - If you want to set specific optional parameters while leaving others at their default values, only fill in the fields you wish to change.

- **HVAC**: format:
    - `HVAC system name, HVAC system type, [optional: heating/cooling power in W, set-point temperature in °C]`
    - HVAC system type options: `NoHeatingVentilationAirConditioning` or `FixCOPHeatingVentilationAirConditioning`.

- **STORAGE_SYSTEM_DC**: format:
    - `AC-system name, DCDC converter name, storage technology name`

- **DCDC_CONVERTER**: format:
    - `DCDC converter name, converter type, power in W, [optional: Efficiency in p.u.]`
    - Available DCDC converter types: `NoLossDcDcConverter`, `FixEfficiencyDcDcConverter`.

- **STORAGE_TECHNOLOGY**: format:
    - `storage technology name, energy in Wh, technology type, [optional: technology specific parameters]`
    - Lithium-ion: Select from cell types: `SonyLFP, LTOLMO, LTONMC, PanasonicNCA, MolicelNMC, AkasolAkmNMC, AkasolOemNMC, SanyoNMC, GenericCell, Samsung78AhNMC, DaimlerLMO, Samsung94AhNMC, Samsung94AhNMCLabtests, Samsung94AhNMCHybrid, Samsung120AhNMC, LGMJ1_NMC`
    - Optionally, set the Start SOC and Start SOH for these cells. For a GenericCell, it's possible to configure the degradation model in the [BATTERY] section.
    - Redox-Flow: Specify the stack type and nominal power of the stack module, with an optional pump algorithm.
    - Available cell stack types are `CellDataStack5500W, DummyStack3000W, IndustrialStack1500W`.
    - Hydrogen: This type encompasses the entire hydrogen energy chain, including fuel cells, electrolyzers, and storage components. Specification options:
        - fuel_cell: Choose from types `PemFuelCell, JupiterFuelCell`.
        - fuel_cell_nominal_power: The nominal power output of the fuel cell.
        - electrolyzer: Types are `PemElectrolyzerMultiDimAnalytic, PemElectrolyzer, AlkalineElectrolyzer`.
        - electrolyzer_nominal_power: The nominal power rating of the electrolyzer.
        - storage: Available types of hydrogen storage `PressureTank, SimplePipeline`.
        - max_pressure: The maximum pressure for hydrogen storage.

---

Configuration of power distributor logic between AC systems as well as between DC systems.
Available distribution options: `EqualPowerDistributor, SocBasedPowerDistributor`.

- **Temperature:** Temperature setting can be specified in this section. If no temperature is specified, the default value is 25 °C.
    - AMBIENT_TEMPERATURE_MODEL: format:
    - `model type [ConstantAmbientTemperature/ UserDefinedTemperatureValue/ LocationAmbientTemperature], temperature in °C`
    - If you opt for `LocationAmbientTemperature`, the default location set is Berlin, but you can define a different one if necessary.
    - For `UserDefinedTemperatureValue`, input your desired temperature.

- **SOLAR_IRRADIATION_MODEL:**
    - Available options: `NoSolarIrradiationModel, LocationSolarIrradiationModel`

- **THERMAL_SIMULATION:**
    - If False: NoHeatingVentilationAirConditioning and NoHousing must be selected
    - If True: supports all Housing, HVAC, Ambient Temperature, and Solar Irradiation (LocationSolarIrradiationModel incompatible with NoHousing)

- **CYCLE_DETECTOR:**
    - Available options: `RainflowCycleDetector, NoCycleDetector, HalfCycleDetector`

---

**Section: PROFILE**

The following types of profiles are available. The user can also upload own data (see :ref:`ref-to-profiles`).

- **Power profiles:**
    - LOAD_PROFILE = name of your load profile in the specified path
    - Random Profile generates a profile for plug and play simulations
    - GENERATION_PROFILE = name of your PV generation profile in the specified path

- **Technical profiles:**
    - FREQUENCY_PROFILE = name of your frequency profile in the specified path
    - SOC_PROFILE = name of your Soc profile in the specified path

- **Thermal profiles:**
    - AMBIENT_TEMPERATURE_PROFILE = name of your location ambient temperature profile in the specified path
    - GLOBAL_HORIZONTAL_IRRADIATION_PROFILE = name of your location GHI profile in the specified path

- **Scaling:**
    - LOAD_PROFILE_SCALING = The input load profile is scaled to energy or power or no scaling at all (False)
    - LOAD_SCALING_FACTOR = If LOAD_PROFILE_SCALING = Energy --> Annual energy in Wh
    - LOAD_SCALING_FACTOR = If LOAD_PROFILE_SCALING = Power --> Peak power in W
    - GENERATION_PROFILE_SCALING = The generation profile is scaled to power or no scaling at all (False)
    - GENERATION_SCALING_FACTOR = If GENERATION_PROFILE_SCALING = Power --> Peak power in W











.. _ref-to-profiles:
3 Supply own Profile Files
------------------------------------------

Users have the option to upload their own profile files. An example could be load or generation profiles, such as those for photovoltaic (PV) systems.
In the absence of user-uploaded profiles, example files provided by SimSES are available for use.

The *simulation.ini* file allows for the uploading of three distinct types of profiles: *power*, *technical*, and *thermal*.
Additionally, the *analysis.ini* file supports the uploading of a *market profile*.

For organization and accessibility, profiles used in simulations and analyses should be stored and categorized within the *simses\\data\\profile* directory.
Each file must be placed in a folder that matches its type (for example, a Power Profile should be located in *"simses\\data\\profile\\power"*.).
Subsequently, these profiles need to be correctly referenced in the simulation or analysis configuration files.
To do this, the filename should be updated in the **[PROFILE]** section of *simulation.local.ini* for simulation profiles, and in the **[MARKET_PROFILE]** section of *analysis.local.ini* for market profiles.


This is what an example for the Power Profile in the *simulation.local.ini* could look like:
    - section: [PROFILE]
    - directory of the power profile: POWER_PROFILE_DIR = profile/power/
    - specific power profile file: LOAD_PROFILE = *Name of the respective Power Profile*


3.1 Format of Profile Files in SimSES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The supported formats for all types of profiles are either *.csv* or *.csv.gz*.
For power profiles specifically, they must meet certain criteria to avoid errors during preprocessing:

1. The file is expected to present time series data in the first column and power values in the second column, with time represented in the "Unix-Timestamp" format.

2. The sampling interval must match the **TIME_STEP** value set in the **[GENERAL]** section of the *simulation.local.ini* file.

3. In cases where time series data are not provided, the system will generate them based on the start time and time step defined in the simulation configuration.

4. The file must include a header within the first twenty lines. The header must contain the unit of the power [W].

4 Results
------------------------------------------

Apart from the HTML file, SimSES creates multiple files in the respective folder. These files are:

1.	Generated *csv* files to record simulation: *SystemState.csv*, *EnergyManagementState.csv* and *LithiumIonState.csv*
    + The *SystemState.csv* provides an overview of the power management system such as the AC and DC power, the temperature (i.e. ambient temperature), different kinds of power losses, thermal power (i.e. of the HVAC) and many more
    + The EnergyManagementState.csv file delivers insights into the power dynamics controlled by the Energy Management System (EMS). It records the demand for power, the availability of electric vehicles (EVs) for charging, reserves set aside for Frequency Containment Reserve (FCR), and the defined limits for peak shaving. Additional data encompasses photovoltaic (PV) power generation and corresponding timestamps.
    + The LithiumIonState.csv file is captures the performance characteristics of the lithium-ion battery system. It includes metrics on total capacity, degradation impacts on capacity over time, electric current, internal resistance, voltage, state of health, temperature, and time. It also provides the open-circuit voltage and further details pertinent to battery state analysis.

2.	*csv* files containing evaluation results generated after simulation: *SystemTechnicalEvaluation0.0.csv*, *SiteLevelEvaluation0.0.csv*, *EconomicEvaluation0.0.csv*, *LithiumIonTechnicalEvaluation1.1.csv*
    + The *SystemTechnicalEvaluation0.0.csv* contains information such as the round trip efficiency, max/min/mean state of charge, AC/DC charging/discharging efficiency and other information
    + The  *SiteLevelEvaluation0.0.csv* refers to data such as maximum grid power, self-consumption-rate, self-sufficiency-rate and more
    + The *EconomicEvaluation0.0.csv* contains the investment cost, NPV, ROI, Profitability Index, Levelized Cost of Storage and more
    + The *LithiumIonTechnicalEvaluation1.1.csv* contains information on the round trip efficiency, max/min/mean state of charge, energy throughput, full equivalent circles and more
Please note that the information generated by SimSES depends on the use case.


