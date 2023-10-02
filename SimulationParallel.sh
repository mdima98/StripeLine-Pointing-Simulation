#!/bin/bash

parallel -j 3 julia Simulation.jl 0 10 '{1}' ::: I0 I1 V4