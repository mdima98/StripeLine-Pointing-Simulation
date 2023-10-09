#!/bin/bash

# Simulation starting values
readonly PARAMFILE="sim_params.toml"
readonly NCORES=5
readonly FIRSTDAY=0
readonly LASTDAY=10
readonly POL="I0 Y4 V4 G5 R2"
readonly NPOL=5

readonly NDAYS=$(((LASTDAY-FIRSTDAY)*NPOL/NCORES))
readonly STARTDAY
STARTDAY=$(seq $FIRSTDAY $NDAYS $LASTDAY)


parallel -j $NCORES julia pointing-simulation/Simulation.jl '{1}' '{2}' '{3}' '{4}' ::: $PARAMFILE ::: $STARTDAY ::: $NDAYS ::: $POL