import numpy as np
import matplotlib.pyplot as plt
import sys
import toml
from os import path


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
    
    
    
    


def main():
    
    fpath_specifics = str(sys.argv[1])
    
    # data_dict = read_toml_hist(fpath)
    with open(fpath_specifics, 'r') as file:
          
         specifics = toml.load(file)
    
    fhist = path.join(specifics["datadir"], specifics["pol_name"], specifics["results_hist"])
    fhist2d = path.join(specifics["datadir"], specifics["pol_name"], specifics["results_hist2d"])
    
    # Hist
    fig, ax = plt.subplots(figsize=(8, 6), tight_layout=True)
    
    # (bins, freq) = data_dict["hist"]
    (bins, freq) = np.loadtxt(fhist, delimiter=',', unpack=True, dtype=int)
    bins_edges = np.append(bins-0.5, bins[-1]+0.5)
    ax.stairs(freq, bins_edges, edgecolor="b", linewidth=1.0, fill=False, label=specifics["pol_name"])
    
    
    ax.legend()
    ax.set_xlabel(f"Pointing Error [{specifics['units']}]")
    ax.set_yscale("log")
    ax.set_ylabel('Frequency')
    ax.legend()
    
    # Hist2D
    fig, ax = plt.subplots(figsize=(8, 6), tight_layout=True)
    
    # (colat2d, long2d, freq2d) = data_dict["hist2d"]
    (colat2d, long2d, freq2d) = np.loadtxt(fhist2d, delimiter=',', unpack=True, dtype=int)
    
    g = ax.scatter(colat2d,long2d,c=freq2d, s=100, marker='o', edgecolors='none', label=specifics["pol_name"], cmap='inferno')
    cbar = fig.colorbar(g, label="Frequency")

    
    ax.set_xlabel(f"Colatitude [{specifics['units']}]")
    ax.set_ylabel(f"Longitude [{specifics['units']}]")
    ax.legend()

    # plotdir = "hist_plots/"
    # s = fpath.split("/")
    # fname = s[-1].replace(".hist", ".png")
    # savepath = plotdir+fname
    # plt.savefig(savepath)










    plt.show()


if __name__ == "__main__":
    
    main()
    

