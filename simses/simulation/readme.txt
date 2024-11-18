Everyone should create an own folder within the processing directory for his/her batch processing simulations.
Those folders will be ignored by git.

If you want to take advantage of multiple core processing you have the following options:

Option 1

Use multiprocesssing as provided in example.py


Option 2

Use PyCharm with run configuration as follows:

0) Create python scripts for starting your batch, e.g. "example_run_1"

1) Create run configurations for "example_run_1" and "example_run_2"

2) In both configurations you need to "Allow parallel run" (top right corner)

3) Setup a new compound configuration

4) Add run configurations of "example_run_1" and "example_run_2" to the compound configuration

5) Run the compound configuration
