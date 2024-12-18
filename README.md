# SimSES
SimSES (Simulation of stationary energy storage systems) is an open source modeling framework for simulating stationary energy storage systems.
Further information can be found in the accompanying research article: https://doi.org/10.1016/j.est.2021.103743. If you are using SimSES, or plan to do so, please cite this work.

## Setup and installation

### 1. Create a virtual environment
Create a virtual environment, for example with either
[venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html), or directly through your IDE like [PyCharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#env-requirements) and [VS Code](https://code.visualstudio.com/docs/python/environments).

### 2. Install dependencies
Install `simses` and all other required python packages in your virtual environment. This can be done with a single command:
```
pip install -e .
```

### 3. Exemplary simulations
Visit [this page](simses/simulation/simulation_examples/readme.md) to read more about some exemplary simulations and setting up a simulation with pre-configured parameters.

### 4. Contributions
The contribution is made by extending the SimSES tool to include fast frequency response (FFR) and voltage regulation (VR) functionalities, enabling detailed simulations and analyses. The modifications cater to various application scenarios and enhance the tool's flexibility for techno-economic evaluations. Below are the key contributions and adjustments, along with their precise path links:

1) FFR and VR Functionalities
New scripts were developed to implement FFR and VR strategies:
- Files: Fast_Frequency_Response_FFR1.py, Fast_Frequency_Response_FFR2.py, Fast_Frequency_Response_FFR3.py, Fast_Frequency_Response_FFR4.py, and Voltage_Regulation_VR.py.
 Location: simses/logic/energy_management/strategy/basic.
- Note: Focus was placed on FFR1 for this thesis, while FFR2, FFR3, and FFR4 were implemented for potential future use.

2) Application Stacking and Scenario Creation
Additional scripts were developed to stack applications and create scenarios:
- Files: fcr_ffr1_idm_recharge_stacked.py, fcr_ffr2_idm_recharge_stacked.py, fcr_ffr3_idm_recharge_stacked.py, fcr_ffr4_idm_recharge_stacked.py, and fcr_ffr_VR_idm_recharge_stacked.py.
- Location: simses/logic/energy_management/strategy/stacked.
- Note: Similar to the basic strategy, FFR1 was the primary focus.
  
3) Energy Management Factory Adjustment
Adjustments were made to energy_management_factory.py to include FFR and VR functionalities and stacked applications:
- Location: freq_voltage_simses/simses/logic/energy_management/energy_management_factory.py.
- Approach: Existing logic for FCR and IDM was followed to ensure consistency and reliability.

4) Batch File Adjustments
Modifications to batch.py allow simultaneous scenario runs, with recommendations for sufficient computational resources:
- Files: simses/batch.py, simses/main.py.
- Note: For sequential runs, use main.py, which reads configurations from simses/analysis.defaults.ini.

5) Analysis Configuration
Updates to analysis.defaults.ini provide options to toggle technical and economic simulations and configure market prices:
- Location: simses/analysis.defaults.ini.
- Note: Fixed prices were used for FCR, FFR, and VR in this study, with the capability to input dynamic prices for future use.

6) Simulation Parameters
Simulation parameters were adjusted in simulation.local.ini:
- Location: simses/simulation.local.ini.
- Note: Configurations include simulation time, input frequency, and voltage data.

7) KPI Analysis and Revenue Calculation
A new script, analysis-final-script-new_final.ipynb, was created for Key Performance Indicators (KPIs) and revenue analysis
- Location: simses/analysis-final-script-new_final.ipynb.
- Note: Ensure the results folder is correctly configured for accurate data processing.
  
## Acknowlegdements
The tool, originally developed in MATLAB, was initiated by Maik Naumann and Nam Truong, transferred to Python by Daniel Kucevic and Marc Möller and now continuously improved at the Chair of Electrical Energy Storage of the Technical University of Munich.
#   f r e q _ v o l t a g e _ s i m s e s 
 
 
