import numpy as np
import pandas as pd
import sys
import toml
from os import path
import argparse
from termcolor import colored

POLARIMETERS = [
    "I0", "I1", "I2", "I3", "I4", "I5", "I6",
    "B0", "B1", "B2", "B3", "B4", "B5", "B6",
    "V0", "V1", "V2", "V3", "V4", "V5", "V6",
    "R0", "R1", "R2", "R3", "R4", "R5", "R6",
    "O0", "O1", "O2", "O3", "O4", "O5", "O6",
    "Y0", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6",
    "G0", "G1", "G2", "G3", "G4", "G5", "G6"
]

def read_hist_file(fname):
    
    with open(fname, "r") as hfile:
        
        nbins, step, outliers = hfile.readline().split("\t")
        
    freq, bins = np.loadtxt(fname, delimiter="\t", skiprows=1, unpack=True)
  
    return int(nbins), float(step), int(outliers), freq.astype(int), bins.astype(float)
    
def read_toml_hist(fpath):
    
    with open(fpath, 'r') as file:
          
         toml_dict = toml.load(file)
    
    specifics = toml_dict["specifics"]
    
    # Get hist sorted by bins
    hist_dict = dict(sorted(toml_dict["hist"].items()))
    
    bins = np.fromiter(hist_dict.keys(), dtype=int)
    freq = np.fromiter(hist_dict.values(), dtype=int)
    
    # Get hist2D
    hist2d_dict = toml_dict["hist2d"]
    #trim_data2d(hist2d_dict)

    colat2d, long2d = list(zip(*(list(map(int, s.split(','))) for s in list(hist2d_dict.keys())))) # Separate values of keys as colat and long
    freq2d = np.fromiter(hist2d_dict.values(), dtype=int)
    
    data_dict = {
        "specifics": specifics,
        "hist": (bins, freq),
        "hist2d": (colat2d, long2d, freq2d)
    }
    
    return data_dict

def trim_data2d(hist2d_dict):
    
    threshold = 0.05
    maxfreq = max(hist2d_dict.values())
    
    for key in list(hist2d_dict.keys()):
        if hist2d_dict[key] < threshold*maxfreq:
            del hist2d_dict[key]
    
def read_specifics(fpath_specifics):
    
    with open(fpath_specifics, 'r') as file:
        specifics = toml.load(file)
    
    fhist = path.join(specifics["datadir"], specifics["polarimeter"], specifics["results_hist"])
    fhist2d = path.join(specifics["datadir"], specifics["polarimeter"], specifics["results_hist2d"])
    
    return specifics, fhist, fhist2d

def get_hist_files(dargs, comb):
    
    comb = "comb_" if comb else "" 
    fspecifics = f"specifics_{comb}{dargs['polarimeter']}_{dargs['first_day']}_{dargs['last_day']}.toml"
    fpath_specifics = path.join(dargs['datadir'], "specifics", dargs['polarimeter'],fspecifics)
    
    try:
        with open(fpath_specifics, 'r') as file:
            specifics = toml.load(file)
    except FileNotFoundError:
        print(colored("ERROR: The simulation data does not exist.", "red"))
        print(f"Data in '{dargs['datadir']}' must be in '{colored('hist', 'yellow')}', '{colored('hist2d', 'yellow')}' and '{colored('specifics', 'yellow')}' directories.")
        print(f"To plot combined histograms, launch the program '{colored('PlotHists.py', 'yellow')}' with '{colored('-c', 'yellow')}' option")
        sys.exit()
    
    fhist = specifics["results_hist"]
    hist_file = path.join(dargs['datadir'], "hist", dargs['polarimeter'],fhist)
    
    fhist2d = specifics["results_hist2d"]
    hist2d_file = path.join(dargs['datadir'], "hist2d", dargs['polarimeter'],fhist2d)
    
    return specifics, hist_file, hist2d_file


def parse_commandline_plots():
    
    parser = argparse.ArgumentParser(description="Plot hist and hist2d data from StripeLine Pointing Simulation")
    
    parser.add_argument("datadir",
                        type=str,
                        help="Data directories.")
    
    parser.add_argument("first_day",
                        type=int,
                        help="First day of simulation data.")
    
    parser.add_argument("last_day",
                        type=int,
                        help="Last day of simulation data.")
    
    parser.add_argument("polarimeter",
                        type=str,
                        help="Polarimeter name.")

    parser.add_argument("-g", "--ground",
                        action="store_true",
                        help="Plot the 2D histogram using ground coordinates instead of Equatorial ones."
                        )
    
    parser.add_argument("-s", "--savefig",
                        action="store_true",
                        help="Save the plots to disk."
                        )
    
    parser.add_argument("-c", "--combined",
                        action="store_true",
                        help="Enable this option to plot combined histograms."
                        )
    
    args = parser.parse_args()

    return args

def parse_commandline_combine():
    
    parser = argparse.ArgumentParser(description="Combine two hist and hist2d from StripeLine Pointing Simulation in a single file.")
    
    parser.add_argument("datadir",
                        type=str,
                        help="Data directories.")
    
    parser.add_argument("first_day",
                        type=int,
                        help="First day of simulation data.")
    
    parser.add_argument("last_day",
                        type=int,
                        help="Last day of simulation data.")
    
    parser.add_argument("polarimeter",
                        type=str,
                        help="Polarimeter name.")
    
    args = parser.parse_args()

    return args