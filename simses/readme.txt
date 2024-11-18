In *.defaults.ini are the default configs for simulation, analysis, logger and data. These config files are tracked in git.

If you would like to have untracked local changes please create a *.local.ini file for the respective config. You have to copy
necessary config options you would to overwrite into that file. This file will be ignored by git. The local config needs to
be in the same folder as the defaults config file.

Example: Changing timestep for simulation in local config

1) Create 'simulation.local.ini'

2) Copy options into 'simulation.local.ini':
    [GENERAL]
    TIME_STEP = 60

3) If you run a simulation, it will overwrite the timestep from default config with this value in cache. The defaults
    file remains same.
