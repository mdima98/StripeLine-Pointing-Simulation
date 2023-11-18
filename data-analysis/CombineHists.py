import numpy as np
import matplotlib.pyplot as plt
import sys
import toml
from datetime import datetime, timedelta

from DataHandling import *





def main():
    
    args = parse_commandline_combine()
    
    # Get first hist
    dargs = {
    "datadir": args.datadir,
    "first_day": args.first_day,
    "last_day": args.first_day + 1,
    "polarimeter": args.polarimeter
    }
    
    specifics_first, fhist_first, fhist2d_first = get_hist_files(dargs, comb=False)
    
    hist_comb = pd.read_csv(fhist_first, names=["point-err", "freq"], header=None).dropna()
    hist2d_eq_comb = pd.read_csv(fhist2d_first, names=["colat_eq", "long_eq", "freq_eq"], header=None, usecols=[0,1,2]).dropna()
    hist2d_gr_comb = pd.read_csv(fhist2d_first, names=["colat_gr", "long_gr", "freq_gr"], header=None, usecols=[3,4,5]).dropna()
    
    days = np.arange(args.first_day + 1, args.last_day, 1)
     
    for day in days:
        
        dargs = {
        "datadir": args.datadir,
        "first_day": day,
        "last_day": day + 1,
        "polarimeter": args.polarimeter
        }
        
        _, fhist, fhist2d = get_hist_files(dargs, comb=False)
        
        hist = pd.read_csv(fhist, names=["point-err", "freq"], header=None).dropna()
        hist2d_eq = pd.read_csv(fhist2d, names=["colat_eq", "long_eq", "freq_eq"], header=None, usecols=[0,1,2]).dropna()
        hist2d_gr = pd.read_csv(fhist2d, names=["colat_gr", "long_gr", "freq_gr"], header=None, usecols=[3,4,5]).dropna()
    
        # Combine hist
        hist_comb = pd.concat([hist_comb, hist]).groupby('point-err', as_index=False).sum()
    
        # Combine hist2d
        hist2d_eq_comb = pd.concat([hist2d_eq_comb, hist2d_eq]).groupby(['colat_eq', 'long_eq'], as_index=False).sum()
        hist2d_gr_comb = pd.concat([hist2d_gr_comb, hist2d_gr]).groupby(['colat_gr', 'long_gr'], as_index=False).sum()
        
    hist2d_comb = hist2d_eq_comb.join(hist2d_gr_comb,lsuffix='_eq', rsuffix='_gr')
    
    save_hist_comb(hist_comb, hist2d_comb, args, days, specifics_first)
    
    
    
    


def print_warnings(specifics1, specifics2):
    
    first_last1 = (specifics1["first_day"], specifics1["last_day"])
    first_last2 = (specifics2["first_day"], specifics2["last_day"])
    polarimeter1 = specifics1["polarimeter"]
    polarimeter2 = specifics2["polarimeter"]
    
    
    
    
    # if (polarimeter_1 == polarimeter_2) and ( first_last_1 != first_last_2 ):
    #     print(colored(f"WARNING: combining hists of same polarimeter {polarimeter_1} in different time intervals.", "yellow"))
    



def combine_hist(fhist1, fhist2d1, fhist2, fhist2d2):
    
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
    
    return hist_comb, hist2d_comb
    
    

def save_hist_comb(hist_comb, hist2d_comb, args, days, specifics_first):
    
    fhist = f"hist_comb_{args.polarimeter}_{days[0] - 1}_{days[-1] + 1}.csv"
    hist_file = path.join(args.datadir, "hist", args.polarimeter,fhist)
    
    fhist2d = f"hist2d_comb_{args.polarimeter}_{days[0] - 1}_{days[-1] + 1}.csv"
    hist2d_file = path.join(args.datadir, "hist2d", args.polarimeter,fhist2d)
    
    hist_comb.to_csv(hist_file, header=False, index=False)
    hist2d_comb.to_csv(hist2d_file, header=False, index=False)
    
    specifics_comb = {
        "units": specifics_first["units"],
        "datadir": args.datadir,
        "first_day": specifics_first["first_day"],
        "last_day": specifics_first["first_day"] + timedelta(days=int(days[-1])),
        "result_hist": fhist,
        "result_hist2d": fhist2d,
        "polarimeter": args.polarimeter,
        "start_day": args.first_day,
        "ndays": len(days)
    }
    
    fspecifics = f"specifics_comb_{args.polarimeter}_{days[0] - 1}_{days[-1] + 1}.toml"
    fpath_specifics = path.join(args.datadir, "specifics", args.polarimeter,fspecifics)
    

    with open(fpath_specifics, 'w') as file:
        toml.dump(specifics_comb, file)
    
    
    

if __name__ == "__main__":
    
    main()