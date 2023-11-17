import numpy as np
import matplotlib.pyplot as plt
import sys
import toml

from DataHandling import *





def main():
    
    args = parse_commandline_combine()
    
    # Get first data 
    dargs1 = {
        "datadir": args.datadir,
        "first_day": args.first_day_1,
        "last_day": args.last_day_1,
        "polarimeter": args.polarimeter_1
    }
    specifics1, fhist1, fhist2d1 = get_hist_files(dargs1)
    
    # Get second data
    dargs2 = {
        "datadir": args.datadir,
        "first_day": args.first_day_2,
        "last_day": args.last_day_2,
        "polarimeter": args.polarimeter_2
    }
    specifics2, fhist2, fhist2d2 = get_hist_files(dargs2)
    
    combine_hist(dargs1, specifics1, fhist1, fhist2d1, dargs2, specifics2, fhist2, fhist2d2)
    
    


def print_warnings(specifics1, specifics2):
    
    first_last1 = (specifics1["first_day"], specifics1["last_day"])
    first_last2 = (specifics2["first_day"], specifics2["last_day"])
    polarimeter1 = specifics1["polarimeter"]
    polarimeter2 = specifics2["polarimeter"]
    
    
    
    
    # if (polarimeter_1 == polarimeter_2) and ( first_last_1 != first_last_2 ):
    #     print(colored(f"WARNING: combining hists of same polarimeter {polarimeter_1} in different time intervals.", "yellow"))
    



def combine_hist(dargs1, specifics1, fhist1, fhist2d1, dargs2, specifics2, fhist2, fhist2d2):
    
    print_warnings(specifics1, specifics2)
    
    hist_1 = pd.read_csv(fhist1, names=["point-err", "freq"], header=None).dropna()
    hist_2 = pd.read_csv(fhist2, names=["point-err", "freq"], header=None).dropna()
   
    hist2d_eq_1 = pd.read_csv(fhist2d1, names=["colat", "long", "freq"], header=None, usecols=[0,1,2]).dropna()
    hist2d_gr_1 = pd.read_csv(fhist2d1, names=["colat", "long", "freq"], header=None, usecols=[3,4,5]).dropna()
    
    hist2d_eq_2 = pd.read_csv(fhist2d2, names=["colat", "long", "freq"], header=None, usecols=[0,1,2]).dropna()
    hist2d_gr_2 = pd.read_csv(fhist2d2, names=["colat", "long", "freq"], header=None, usecols=[3,4,5]).dropna()
    
    # Combine hist
    hist_comb = pd.concat([hist_1, hist_2]).groupby('point-err', as_index=False).sum()
    
    # Combine hist2d
    hist2d_eq_comb = pd.concat([hist2d_eq_1, hist2d_eq_2]).groupby(['colat', 'long'], as_index=False).sum()
    hist2d_gr_comb = pd.concat([hist2d_gr_1, hist2d_gr_2]).groupby(['colat', 'long'], as_index=False).sum()
    
    hist2d_comb = hist2d_eq_comb.join(hist2d_gr_comb,lsuffix='_eq', rsuffix='_gr')
    
    

def save_hist(hist_comb, hist2d_comb,dargs1, dargs2):
    
    
    

if __name__ == "__main__":
    
    main()