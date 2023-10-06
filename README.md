# StripeLine-Pointing-Simulation

This code simulate the poinitng of the LSPE/STRIP instrument to study its error in non ideal conditions

- The directory `pointing-simulation` contains all the Julia code that runs the simulation, and the it referes to a `.toml` file for the parameters, such as `sim_parameters.toml`.
- The directory `data-analysis` contains some Python code to perform analysis on the data produced by the simulation.
- The shell script `SimulationParallel.sh` is for running the simulation in parallel, using [GNU Parallel](https://www.gnu.org/software/parallel/).

The other directories contain some data made in test runs of the code.

