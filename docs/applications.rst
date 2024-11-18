.. _ref-to-applications:

Applications
==============================
In general, applications for SimSES are distinguished between Front-of-the-Meter (FTM) and Behind-the-Meter (BTM) applications.
FTM applications include solutions like Frequency Containment Reserve (FCR), storage-assisted renewable energy time shift,
and participation in the intraday continuous market. BTM applications focus on more distributed and locally coordinated power supply strategies,
such as peak shaving for industrial applications or at electric vehicle charging stations, and bill-saving at residential sites through increased self-consumption with local photovoltaic generation (residential battery storage).
For the self-consumption increase scenario, two distinct strategies are identified: "Residential PV Greedy" and "Residential PV Feed-in Damp".
Additionally, applications designed for validation purposes have been implemented, including the "Power Follower" and "State of Charge Follower" strategies.
The following sections briefly explain each application.


The Power Follower strategy is an operational approach designed to align the activity of a storage system with a predefined power profile. This strategy ensures that the storage system mimics a specific power output pattern over time.
Similarly, the State of Charge Follower strategy transforms a set SOC profile into a corresponding power output profile, with the objective of having the storage system match this derived power demand at every time step.


Frequency Regulation
------------------------------------------

Frequency Containment Reserve is a critical service in power system management designed to counteract deviations in the system frequency.
FCR responds to frequency changes by requiring full activation within 30 seconds and must be provided symmetrically,
i.e. there's no distinction between positive and negative FCR. Activation is frequency dependent,
with suppliers measuring the grid frequency locally at the point of generation or consumption and responding immediately to any changes.
This mechanism stops and stabilises frequency fluctuations, regardless of where in the European interconnected grid the deviation occurs.
To restore the frequency to the standard 50 hertz and replace FCR, the Frequency Restoration Reserve is used in the control area causing the imbalance. The energy activated by the FCR contributes to the unintentional exchange and is settled monthly between the Transmission System Operators.

In SimSES, FCR is implemented according to German regulatory criteria.
The system adjusts the charging and discharging power in proportion to the frequency deviation.
If the frequency falls below 49.8 Hz or rises above 50.2 Hz, the system delivers power at the pre-qualified level.
Within a dead band around 50 Hz (plus/minus 10 mHz) the output power is set to 0 watts. The strategy includes the flexibility to exceed the output power by up to 20% to bring the state of charge back to a pre-defined set point.

.. figure:: images/Applications_images/FCR_expl.*
    :name: fcr_appl
    :width: 50%

    Frequency Containment Reserve in European Countries


Intraday Continuous Market
------------------------------------------

The Intraday Continuous Market is an essential part of energy trading that complements
the Day-Ahead Market. Intraday trading allows for the buying and selling of electricity on the same
day as delivery, helping to balance supply and demand by allowing adjustments close to the time of energy
consumption. This capability is increasingly vital with the growth of intermittent renewable energy sources,
such as wind and solar, which can lead to unpredictable power outputs. The intraday market helps participants
manage these fluctuations and maintain balance after the day-ahead market predictions have been realized.
Intraday power trading is facilitated by exchanges like EPEX Spot in Paris and Nord Pool, where participants can trade electricity in real time, responding to changes in power production and consumption.


The IDM operation strategy in SimSES involves charging or discharging the ESS by trading energy on the electricity market,
specifically on the IDM, based on whether the SOC falls below a predefined lower limit or exceeds an upper limit.



Peak-Shaving
------------------------------------------

Peak Shaving (PS) is a strategy used by consumers to reduce their electricity consumption during periods of high demand
to avoid causing a demand peak. This can be achieved through temporarily reducing production, activating on-site generation resources,
or utilizing a battery storage system.
Using self-generated electricity to offset a potential peak in demand helps in managing energy costs effectively,
especially since charges are often based on the highest power peak recorded during a billing cycle (usually monthly or annually).


Peak shaving is often used in industrial settings due to the significant cost implications associated with peak power demands.
Industries often face substantial electricity costs that are not just based on the total energy consumed,
but also on the maximum rate of power usage recorded during the billing period.
This maximum rate, or peak load, can substantially increase utility bills because many electricity tariffs
include demand charges, which are costs applied based on the highest level of power drawn during any interval
in the billing cycle.

In the context of SimSES, the Peak Shaving application is designed to mitigate high power demands from the distribution grid.
This is economically beneficial as the highest power peak per billing period is multiplied by a power-related price;
capping these peaks with an Energy Storage System can lead to substantial cost savings.
The system provides the necessary power from the ESS to keep demand below a critical threshold,
thereby reducing the financial impact of peak power charges.


1. The **Simple Peak Shaving Strategy** operates by maintaining power usage below a specified threshold.
When the target power exceeds this threshold, the ESS supplies the required additional power.
Conversely, when the power demand falls below this threshold, the ESS recharges.
This strategy is particularly effective in managing energy costs and enhancing grid stability.


2. A more advanced strategy called the **PS Perfect Foresight Strategy** assumes perfect knowledge
of future load profiles. This strategy charges the ESS only with the amount of energy anticipated to be
necessary for managing the next peak demand. This approach not only helps in effectively managing demand
peaks but also minimizes the calendar aging of lithium-ion based ESS by reducing unnecessary charge cycles.
By charging the ESS strategically just before anticipated demand peaks, this strategy ensures optimal use of
the storage system, prolonging its lifespan and increasing efficiency.

.. figure:: images/Applications_images/Peakshaving.*
    :name: ps_appl
    :width: 70%

    Peak Shaving Mechanism



Self-Consumption Increase
------------------------------------------
Self-Consumption Increase (SCI) is a strategy aimed at increasing the use of energy produced by PV systems
for personal consumption, rather than selling it back to the grid.
This approach has become increasingly important as the financial benefits of selling energy have declined,
making self-consumption more economically attractive. Key metrics for this strategy include the Self-Consumption Rate (SCR),
which measures the proportion of PV-generated energy that is consumed on site, and the Self-Sufficiency Rate (SSR), which measures the proportion of total energy demand that is met by self-generation.


In SimSES, two operational strategies have been implemented for residential SCI in combination with PV units:

1. **Residential PV Greedy Operation Strategy**: This strategy prioritises charging the Energy Storage System
as quickly as possible when PV energy exceeds household demand, regardless of grid conditions.
When PV generation is less than demand, the ESS is discharged to cover the shortfall.
This approach generally achieves the highest SCR and SSR, resulting in significant cost savings.
However, it can have a negative impact on the electrical grid due to high fluctuations in power flow, which can lead to grid congestion and voltage instability.
In addition, frequent high states of charge and high power throughput can accelerate battery ageing.


2. **Residential PV Feed-In Damp Operation Strategy**: This method schedules ESS charging based on PV power
forecasts and aims to maintain constant charging power, ideally fully charging the ESS by sunset.
This strategy fills the storage one hour before sunset and limits power output based on remaining energy capacity and time to sunset.
It results in longer battery life by avoiding high SOC levels and facilitates the integration of more solar installations by smoothing the power fed into the grid.
By limiting potential excess PV generation, it reduces the likelihood of generating excess energy that the grid cannot absorb.


.. figure:: images/Applications_images/PV_HSS.*
    :name: pv_appl
    :scale: 50%

    Usage of a Home Storage System with PV


Vehicle-to-Grid
------------------------------------------

Vehicle-to-Grid (V2G) technology enables electric vehicles to interact with the power grid
by allowing energy stored in the EV’s battery to be fed back into the grid.
This capability can help manage energy demand, stabilize the grid, and facilitate the integration of
renewable energy sources. V2G systems take advantage of bi-directional charging infrastructure,
which allows EV batteries not only to charge from the grid but also to discharge energy back to it.
The technology turns EVs into mobile energy storage units that can provide grid services, such as peak load shaving,
frequency regulation, and emergency power supply.

In the SimSES framework, V2G implementation is modeled by tracking the availability of EVs for charging and discharging
using a binary profile, where '0' means the EV is unavailable and '1' indicates it is ready and connected to the grid.
When available, SimSES simulates various charging strategies to assess V2G's role in grid management,
factoring in the intermittent presence of EVs to determine the system's effectiveness and economic feasibility.
