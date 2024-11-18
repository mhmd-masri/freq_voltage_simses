.. _ref-to-examples:

Examples
==============================

In this section you can find several examples of how to use SimSES for different use cases.
The corresponding configuration files can be found in *“simses\\simulation\\simulation_examples”*,
which can be adapted and rename to *simulation.local.ini* in the main directory *“simses”*.

1 Power Follower/SoC Follower
--------------------------------

1.1 Exemplary file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    *power_soc_follower.ini*

1.2 Operation Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In this strategy, the Energy Management System (EMS) follows a given AC power profile with the **PowerFollower** or
a given State of Charge (SoC) profile with the **SocFollower**. If the **SocFollower** is used, SimSES calculates
the required power to reach the desired SoC in each timestep.

1.3	Relevant Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The options that might be important regarding this strategy are chosen and explained in the ini-file.

    - Section **[GENERAL]**: time properties (start time, end time, timesetp, etc.), which will be neglected for simplicity in other examples.
    - Section **[ENERGY_MANAGEMENT]**: **STRATEGY = PowerFollower** or **STRATEGY = SocFollower**.
    - Section **[BATTERY]**: here, lithium-ion batteries (LIBs) are chosen as storage technology: lower SoC limit, upper SoC limit, start State of Health (SoH) and End of Life (EoL) based on the remaining capacity, etc.
    - Section **[STORAGE_SYSTEM]** configures AC and DC system. Note that one AC system must be assigned with at least one DC system.
    - Section **[PROFILE]**: name of the power profile should be attributed to parameter **LOAD_PROFILE** when using **PowerFollower**, while name of the SoC profile should be assigned to parameter **SOC_PROFILE**.

1.4 Input Profiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When **PowerFollower** is applied, the power profile should be droped in the default directory *“\\simses\\data\\profile\\power”*.
In the case of **SocFollower**, the SoC profile is to be provided in *“\\simses\\data\\profile\\technical”*.
If other directories are desired, they should be stated in the parameter **POWER_PROFILE_DIR** and **TECHNICAL_PROFILE_DIR**, respectively.

2 Residential Photovoltaic Battery Storage System
--------------------------------------------------------
In this example, the operation of a residential storage system with PV as well as its thermal behavior can be simulated.

2.1 Exemplary file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    *thermal_simulation_residential_storage.ini*

2.2 Operation Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
There are currently two operation strategies available in SimSES: greedy and feed-in damping.
A more detailed description of the two strategies can be found in the publication: Kucevic, D.; Tepe, B.;
Englberger, S.; Parlikar, A.; Muehlbauer, M.; Bohlen, O.; Jossen, A.; Hesse, H. (2020);
*Standard Battery Energy Storage System Profiles: Analysis of various Applications for Stationary Lithium-Ion Battery Energy Storage Systems using a Holistic Simulation Framework*,
`doi:10.1016/j.est.2019.101077 <https://www.sciencedirect.com/science/article/pii/S2352152X19309016?via%3Dihub>`_.

2.3	Relevant Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The options that might be important regarding this strategy are chosen and explained in the ini-file.

    - Section **[ENERGY_MANAGEMENT]**: **STRATEGY = ResidentialPvGreedy** or **STRATEGY = ResidentialPvFeedInDamp**.
    - Section **[STORAGE_SYSTEM]**: here, the Battery Energy Stationary System (BESS) consists of 1 AC system with a power rating of 5 kW, an intermediate DC voltage of 333 V. No housing type or a dedicated Heating, Ventilation und Air Conditioning (HVAC) system connected to the BESS is specified. In this case, the system is installed indoors, where a constant room temperature (= 25 °C) is assumed to be maintained and meanwhile the BESS is not exposed to direct sunlight. As the temperature evolution of our battery cells is of interest, the thermal simulation is enabled by setting **THERMAL_SIMULATION** to **True**.
    - Section **[PROFILE]**: the household load profile is assigned to parameter **LOAD_PROFILE**. Besides, by choosing Energy for parameter **LOAD_PROFILE_SCALING** and giving a value of 3.5e6 to parameter **LOAD_SCALING_FACTOR** we scale the load profile to meet an annual energy consumption of 3.5 MWh. Furthermore, for the simulation of residential storage system with PV the PV generation profile should be specified, which is in this example scaled to a peak power of 10 kW (see **GENERATION_PROFILE_SCALING** and **GENERATION_SCALING_FACTOR**).

2.4 Input Profiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The input profiles include the household load profile and PV generation profile, both of which should be placed by default
in *“\\simses\\data\\profile\\power”*.

3 Peak Shaving (PS)
--------------------------------
This example demonstrates how to setup a simulation for a stationary storage system with peak shaving function in industrial applications.

3.1 Exemplary file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    *thermal_simulation_peak_shaving.ini*

3.2 Operation Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
There are several peak shaving strategies available in *“simses\\logic\\energy_management\\strategy\\basic”*.
Here the **SimplePeakShaving** algorithm is chosen for simplicity, i.e., in case of exceeding a power limit
defined in **MAX_POWER** in section **[ENERGY_MANAGEMENT]**, the BESS will be activated to provide the extra
amount of electricity above the power limit until the minimum allowed SoC is reached. When the load power drops
below the power limit, the BESS will be charged with a power of **MAX_POWER** – load power at the current timestamp
to the upper SoC limit.

3.3	Relevant Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The options that might be important regarding this strategy are chosen and explained in the ini-file.

    - Section **[ENERGY_MANAGEMENT]**: **STRATEGY = SimplePeakShaving**, **MAX_POWER = 2.5e6** indicating a power limit of 2.5 MW.
    - Section **[STORAGE_SYSTEM]** specifies here the configuration for a 1 MW / 1.25 MWh BESS with a 20 ft. container as housing. The system is installed outdoors, where location-dependent ambient temperature as well as solar irradiance is present. In order to control the temperature of BESS and reduce the aging effect, a HVAC unit with constant Coefficient of Performance (COP) for cooling and constant energy efficiency for heating is applied. As the temperature evolution of our battery cells is again of interest, the **THERMAL_SIMULATION** is set to **True**.
    - Section **[PROFILE]**: the industry load profile is assigned to parameter **LOAD_PROFILE**, with Power as the type of scaling and peak power scaled to 3.5 MW. Since the location-dependent ambient temperature and solar irradiance are specified, the ambient temperature profile and global horizontal irradiance profile are provided (see **AMBIENT_TEMPERATURE_PROFILE** and **GLOBAL_HORIZONTAL_IRRADIATION_PROFILE**).

3.4 Input Profiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The necessary profile for simulation with peak shaving strategies is load profile in *“\\simses\\data\\profile\\power”*. In this very example, ambient temperature profile and irradiance profile should be given in “\\simses\\data\\profile\\thermal” according to the desired **AMBIENT_TEMPERATURE_MODEL** and **SOLAR_IRRADIATION_MODEL** in Section **[STORAGE_SYSTEM]**.

4 Frequency Containment Reserve (FCR)
----------------------------------------
This example gives insight into a multi-use application Frequency Containment Reserve (FCR) combined with participation in the Intraday Market (IDM).

4.1 Exemplary file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    *thermal_simulation_fcr_idm_stacked.ini*

4.2 Operation Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A detailed introduction to the FCR can be referred to in article: Kucevic, D.; Tepe, B.; Englberger, S.; Parlikar, A.;
Muehlbauer, M.; Bohlen, O.; Jossen, A.; Hesse, H. (2020); *Standard Battery Energy Storage System Profiles:
Analysis of various Applications for Stationary Lithium-Ion Battery Energy Storage Systems using a Holistic Simulation
Framework*, `doi:10.1016/j.est.2019.101077 <https://www.sciencedirect.com/science/article/pii/S2352152X19309016?via%3Dihub>`_.

4.3	Relevant Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The options that might be important regarding this strategy are chosen and explained in the ini-file.

    - Section **[ENERGY_MANAGEMENT]**: **STRATEGY = FcrIdmRechargeStacked**, power to be delivered to the FCR market (**POWER_FCR**) and IDM (**POWER_IDM**) are assigned with 1.1 MW and 0.25 MW, respectively. Parameters **SOC_SET** and **FCR_RESERVE** are elucidated in the above-mentioned article.
    - Section **[STORAGE_SYSTEM]**: a 1.35 MW / 1.35 MWh BESS with a 40 ft. container as housing is designed. As in the example of peak shaving, the location-dependent ambient temperature model as well as solar irradiation model is chosen, and the HVAC system is set to **FixCOPHeatingVentilationAirConditioning**.
    - Section **[PROFILE]**: the frequency profile of the grid defined in **FREQUENCY_PROFILE** is needed to generate the storage profile. In accordance with the chosen thermal model, the location temperature and solar irradiation profiles are required for the thermal simulation.
    - Section **[MARKET_PROFILE]** in *analysis.defaults.ini*: apart from the options in the exemplary file, the FCR and IDM price profile can be provided via parameters **FCR_PRICE_PROFILE** and **INTRADAY_PRICE_PROFILE**.

4.4 Input Profiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Prerequisites for the simulation with FCR are frequency profile of the grid in *“\\simses\\data\\profile\\technical”* and FCR market price profile in *“\\simses\\data\\profile\\economic”*. When IDM is involved in the economic analysis, IDM price profile should be dropped in *“\\simses\\data\\profile\\economic”* as well. Similar to the example of peak shaving, the ambient temperature profile and irradiance profile are placed in *“\\simses\\data\\profile\\thermal”*.

..
    needs to be checked

5 Electric Vehicle Simulation
----------------------------------------

5.1 Exemplary file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    *thermal_simulation_fcr_idm_stacked.ini*

5.2 Operation Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Charging Strategy
    As of March 2023, three charging strategies are available:

    - uncontrolled charging -> **Uncontrolled**
    - charging with medium power to reach 100% SoC at departure -> **Mean_power**
    - paused charging: the paused charging strategy means that after arrival, the vehicle is charged to a threshold SoC. Afterwards, the charging is paused until shortly before the departure. The vehicle is then charged to 100% SoC. The threshold SoC has to be defined after the name of the charging strategy, e.g., **Paused, 0.6** -> 60% or **Paused, 0.85** -> 85%.

* Availability of EV
    However, unlike the stationary storage systems, the EVs are not always available for charging or discharging. The information on the availability of the EVs will be transformed into a binary profile, where 0 represents the case whenever the vehicle is on the road or anywhere else other than at home or at depot or plugged in, and 1, on the other hand, implies that the EV is plugged in. During the time 	period when the binary profile is 1, the charging strategy is applied in SimSES.

5.3	Relevant Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The options that might be important regarding this strategy are chosen and explained in the ini-file.

    - Section **[ENERGY_MANAGEMENT]**: **STRATEGY = ElectricVehicle**, **EV_CHARGING_STRATEGY = Uncontrolled**.
    - Section **[STORAGE_SYSTEM]**: an EV with 93 kW / 45 kWh battery system is configured.
    - Section **[PROFILE]**: load profile of the vehicle is specified in **LOAD_PROFILE** and the above-mentioned binary profile is assigned to **BINARY_PROFILE**.

5.4 Input Profiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In comparison with stationary storage systems, EVs are not always available. Thus, SimSES requires two profiles to simulate operation of EV:

    - either a load profile containing the load power of all driving processes in *“\\simses\\data\\profile\\power”* or a SoC profile of the vehicle in *“\\simses\\data\\profile\\technical”*,
    - a binary profile containing the information on the availability should be prepared and put in *“\\simses\\data\\profile\\technical”*, The binary profile variable is BINARY_PROFILE.

..
    TODO: needs to be checked
If the load profile contains charging processes of the EV, i.e., the sign of the power is negative, SimSES neglects them and applies the chosen charging strategy,
when the value of the binary vector is 1. On the other hand, when the value of the binary vector is 0, the PowerFollower operation strategy will be adopted.
If only SoC profile of the vehicle exists, the operation strategy **ElectricVehicleSOC** should be chosen for **STRATEGY** in section **[ENERGY_MANAGEMENT]**, instead.
..
    TODO: needs to be checked

6 Multi-Use Simulation
----------------------------------------

6.1 Exemplary file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    *semi_dynamic_multi_use.ini*

6.2 Operation Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The simulation procedure is that the individual applications are called up and the power required to be charged or discharged is determined in each case.
At the same time, power and energy limitations are considered depending on the allocation. The power is then allocated in order of priority,
as a result of which the application of lower priority may not achieve the desired power. The simulation also automatically differentiates between
Behind the Meter (BTM) and in Front of the Meter (FTM) applications. A BTM application of higher priority can thus draw power from the subsystem of
a BTM application of lower priority. This is not possible between BTM and FTM subsystems.

6.3 Relevant Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The options that might be important regarding this strategy are chosen and explained in the ini-file.

    - Section **[ENERGY_MANAGEMENT]**: **STRATEGY = SemiDynamicMultiUse**, list the operation strategies by **MULTI_USE_STRATEGIES = ResidentialPvGreedy, SimplePeakShaving**, allocate the proportions by **ENERGY_ALLOCATION = 0.7, 0.3** and **POWER_ALLOCATION = 0.7, 0.3**, define the priorities by **RANKING = 2, 1**. In addition, the peak shaving limit is set to 80 kW by **MAX_POWER = 80e3**.
    - Section **[STORAGE_SYSTEM]**: an EV with 300 kW / 600 kWh battery system is configured.
    - Section **[PROFILE]**: household load profile is specified in **LOAD_PROFILE** and the generation profile is declared in **GENERATION_PROFILE**.

6.4 Input Profiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The input profiles are in the multi-use case a collection of the profile files required for the individual use cases,
here, i.e., household load profile for residential storage system with PV and peak shaving, and PV generation profile for residential storage system with PV.
