import numpy as np
import pandas as pd
import sys
import toml
from os import path
import argparse
from termcolor import colored

polarimeters = ["I0", "I1", "V4"]

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
    
    fhist = path.join(specifics["datadir"], specifics["pol_name"], specifics["results_hist"])
    fhist2d = path.join(specifics["datadir"], specifics["pol_name"], specifics["results_hist2d"])
    
    return specifics, fhist, fhist2d

def get_data(args):
    
    fspecifics = f"specifics_{args.polarimeter}_{args.first_day}_{args.last_day}.toml"
    fpath_specifics = path.join(args.datadir, "specifics", args.polarimeter,fspecifics)
    
    try:
        with open(fpath_specifics, 'r') as file:
            specifics = toml.load(file)
    except FileNotFoundError:
        print(colored("Error: The simulation data does not exist.", "red"))
        print(f"Data in '{args.datadir}' must be in '{colored('hist', 'yellow')}', '{colored('hist2d', 'yellow')}' and '{colored('specifics', 'yellow')}' directories.")
        sys.exit()
    
    fhist = f"hist_{args.polarimeter}_{args.first_day}_{args.last_day}.csv"
    hist_file = path.join(args.datadir, "hist", args.polarimeter, fhist)
    
    fhist2d = f"hist2d_{args.polarimeter}_{args.first_day}_{args.last_day}.csv"
    hist2d_file = path.join(args.datadir, "hist2d", args.polarimeter, fhist2d)
    
    return specifics, hist_file, hist2d_file


def parse_commandline():
    
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
    
    args = parser.parse_args()

    return args
    