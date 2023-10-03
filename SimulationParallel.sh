#!/bin/bash

if [ "$1" == "" ]; then
    echo "Usage: $(basename $0) STARTDAY NDAYS POL"
    exit 1
fi

readonly STARTDAY = "$1"
readonly NDAYS = "$2"
readonly POL = "$3"

time julia Simulation.jl $STARTDAY $NDAYS $POL