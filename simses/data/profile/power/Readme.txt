This file gives instructions on how to provide a load or generation file (e.g. PV) for the simulation.

1. The load file should satisfy the following conditions, otherwise it will raise errors during the preprossing of the given profile.

I.   It should in the format of *.csv or *.gz.
II.  The header to specify the unit of the power should be given in the first twenty lines.
III. The standard format of header:
	"""
	# Source: \n
	# Unit: W\n
      # Time: s\n
	# Sampling in s: 1\n
	# Timezone: Berlin\n
	# Origin: Measured\n
	# Datasets: 1\n
	# Publishable: Yes\n
	# Annual load consumption in kWh: 182\n
	"""
   Default values:
	# Unit: W
      # Time: s
	# Sampling in s: time step in simulation configuration
	# Timezone: UTC

   When no time series are given, the time series will be generated according to the start time and time step defined in the simulation configuration.

   The location can be given in two ways:
	'Continent/City'. e.g. 'Europe/Berlin'
	the longitude and the latitude -> not further implemented

IV. The time and power value should be separated with "," and the format should be kept as:
   	time,power
   instead of the other round, i.e. "power, time", otherwise it will cause identification error. 

2. The load file should be put in the folder "simses/data/profile/power". which can also be changed in the simulation configuration file (simulation.*.ini) in the main directory.
   Dfault is: POWER_PROFILE_DIR = profile/power/

3. Finally, the name of the file without file type like ".csv" or "csv.gz" should be set to "LOAD_PROFILE" in the case of load profile or
   "GENERATION_PROFILE" in the case of generation profile in the simulation configuration file (simulation.*.ini) in the main directory.
