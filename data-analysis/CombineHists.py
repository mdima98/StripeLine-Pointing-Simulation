import numpy as np
import matplotlib.pyplot as plt
import sys
import toml

from DataHandling import *





def main():
    
    args = parse_commandline_combine()
    
    # Get first data 
    dargs_1 = {
        "datadir": args.datadir_1,
        "first_day_1": args.first_day_1,
        "last_day_1": args.last_day_1,
        "polarimeter_1": args.polarimeter_1
    }
    specifics_1, fhist_1, fhist2d_1 = get_hist_files(dargs_1)
    
    # Get second data
    dargs_2 = {
        "datadir": args.datadir,
        "first_day_2": args.first_day_2,
        "last_day_2": args.last_day_2,
        "polarimeter_2": args.polarimeter_2
    }
    specifics_2, fhist_2, fhist2d_2 = get_hist_files(dargs_2)
    
    


def print_warnings(specifics_1, specifics_2):
    
    first_last_1 = (specifics_1["first_day"], specifics_1["last_day"])
    first_last_2 = (specifics_2["first_day"], specifics_2["last_day"])
    polarimeter_1 = specifics_1["pol_name"]
    polarimeter_2 = specifics_2["pol_name"]
    
    
    
    
    # if (polarimeter_1 == polarimeter_2) and ( first_last_1 != first_last_2 ):
    #     print(colored(f"WARNING: combining hists of same polarimeter {polarimeter_1} in different time intervals.", "yellow"))
    



def combine_hist(dargs_1, specifics_1, fhist_1, fhist2d_1, dargs_2, specifics_2, fhist_2, fhist2d_2):
    
    print_warnings(specifics_1, specifics_2)
    
    hist_1 = pd.read_csv(fhist_1, names=["point-err", "freq"], header=None).dropna()
    hist_2 = pd.read_csv(fhist_2, names=["point-err", "freq"], header=None).dropna()
   
    hist2d_eq_1 = pd.read_csv(fhist2d_1, names=["colat", "long", "freq"], header=None, usecols=[0,1,2]).dropna()
    hist2d_gr_1 = pd.read_csv(fhist2d_1, names=["colat", "long", "freq"], header=None, usecols=[3,4,5]).dropna()
    
    hist2d_eq_2 = pd.read_csv(fhist2d_2, names=["colat", "long", "freq"], header=None, usecols=[0,1,2]).dropna()
    hist2d_gr_2 = pd.read_csv(fhist2d_2, names=["colat", "long", "freq"], header=None, usecols=[3,4,5]).dropna()



if __name__ == "__main__":
    
    main()