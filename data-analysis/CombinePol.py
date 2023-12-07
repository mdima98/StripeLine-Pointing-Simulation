from DataHandling import *
import os

def main():
    
    datadir = "hist_tests"
    pols = ['V4', 'V4']
    pols_save = pols
    first_day = 0
    last_day = 6
    
    # Get first data
    pol = pols.pop(0)
    
    dargs = {
    "datadir": datadir,
    "first_day": first_day,
    "last_day": last_day,
    "polarimeter": pol
    }
    
    specifics_first, fhist_first, fhist2d_first = get_hist_files(dargs, comb=True)
    
    hist_comb = pd.read_csv(fhist_first, names=["point-err", "freq"], header=None).dropna()
    hist2d_eq_comb = pd.read_csv(fhist2d_first, names=["colat_eq", "long_eq", "freq_eq"], header=None, usecols=[0,1,2]).dropna()
    hist2d_gr_comb = pd.read_csv(fhist2d_first, names=["colat_gr", "long_gr", "freq_gr"], header=None, usecols=[3,4,5]).dropna()
    
    for pol in pols:
        
        dargs = {
        "datadir": datadir,
        "first_day": first_day,
        "last_day": last_day,
        "polarimeter": pol
        }
        
        specifics_first, fhist, fhist2d = get_hist_files(dargs, comb=True)
        
        hist = pd.read_csv(fhist, names=["point-err", "freq"], header=None).dropna()
        hist2d_eq = pd.read_csv(fhist2d, names=["colat_eq", "long_eq", "freq_eq"], header=None, usecols=[0,1,2]).dropna()
        hist2d_gr = pd.read_csv(fhist2d, names=["colat_gr", "long_gr", "freq_gr"], header=None, usecols=[3,4,5]).dropna()
    
        # Combine hist
        hist_comb = pd.concat([hist_comb, hist]).groupby('point-err', as_index=False).sum()
    
        # Combine hist2d
        hist2d_eq_comb = pd.concat([hist2d_eq_comb, hist2d_eq]).groupby(['colat_eq', 'long_eq'], as_index=False).sum()
        hist2d_gr_comb = pd.concat([hist2d_gr_comb, hist2d_gr]).groupby(['colat_gr', 'long_gr'], as_index=False).sum()
        
    hist2d_comb = hist2d_eq_comb.join(hist2d_gr_comb,lsuffix='_eq', rsuffix='_gr')
    
    save_hist_multipol(hist_comb, hist2d_comb, specifics_first, pols_save)
        
    


def save_hist_multipol(hist_comb, hist2d_comb, specifics_first, pols_save):
    
    if not path.isdir(specifics_first["datadir"]+"/multipolarimeter"):
        os.mkdir(path.join(specifics_first["datadir"],"multipolarimeter"))
    
    fhist = f"hist_multipolarimeter_{specifics_first['start_day']}_{specifics_first['start_day']+specifics_first['ndays']}.csv"
    hist_file = path.join(specifics_first["datadir"], "multipolarimeter",fhist)
    
    fhist2d = f"hist2d_multipolarimeter_{specifics_first['start_day']}_{specifics_first['start_day']+specifics_first['ndays']}.csv"
    hist2d_file = path.join(specifics_first["datadir"], "multipolarimeter",fhist2d)
    
    
    with open(hist_file, 'w') as file:
        file.write(f"# Polarimeters: {pols_save}\n")
        hist_comb.to_csv(hist_file, header=False, index=False)
    
    
    with open(hist2d_file, 'w') as file:
        file.write(f"# Polarimeters: {pols_save}\n")
        hist2d_comb.to_csv(hist2d_file, header=False, index=False)
    
    specifics_comb = {
        "units": specifics_first["units"],
        "datadir": specifics_first["datadir"],
        "first_day": specifics_first["first_day"],
        "last_day": specifics_first["last_day"],
        "result_hist": fhist,
        "polarimeter": pols_save,
        "result_hist2d": fhist2d,
        "start_day": specifics_first['start_day'],
        "ndays": specifics_first['ndays']
    }
    
    fspecifics = f"specifics__multipolarimeter_{specifics_first['start_day']}_{specifics_first['start_day']+specifics_first['ndays']}.toml"
    fpath_specifics =path.join(specifics_first["datadir"], "multipolarimeter", fspecifics)
    
    with open(fpath_specifics, 'w') as file:
        toml.dump(specifics_comb, file)
      
    
if __name__ == "__main__":
    
    main()