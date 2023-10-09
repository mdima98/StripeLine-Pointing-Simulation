import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import sys
import toml


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
    trim_data2d(hist2d_dict)

    colat2d, long2d = list(zip(*(list(map(int, s.split(','))) for s in list(hist2d_dict.keys())))) # Seprated values of keys as colat and long
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
    
    fpath = str(sys.argv[1])
    
    data_dict = read_toml_hist(fpath)
    
    # Hist
    fig, ax = plt.subplots(figsize=(12, 4), tight_layout=True)
    
    (bins, freq) = data_dict["hist"]
    bins_edges = np.append(bins-0.5, bins[-1]+0.5)
    ax.stairs(freq, bins_edges, edgecolor="b", linewidth=1.0, fill=False, label=data_dict["specifics"]["pol_name"])
    
    
    ax.legend()
    ax.set_xlabel(f"Pointing Error [{data_dict['specifics']['units']}]")
    ax.set_yscale("log")
    ax.set_ylabel('Frequency')
    ax.legend()
    
    # Hist2D
    fig, ax = plt.subplots(figsize=(12, 4), tight_layout=True)
    
    (colat2d, long2d, freq2d) = data_dict["hist2d"]
    
    g = ax.scatter(colat2d,long2d,c=freq2d, s=100, marker='s', edgecolors='none', label=data_dict["specifics"]["pol_name"])
    cbar = fig.colorbar(g, label="Frequency")

    
    ax.set_xlabel(f"Colatitude [{data_dict['specifics']['units']}]")
    ax.set_ylabel(f"Longitude [{data_dict['specifics']['units']}]")
    ax.legend()

    # plotdir = "hist_plots/"
    # s = fpath.split("/")
    # fname = s[-1].replace(".hist", ".png")
    # savepath = plotdir+fname
    # plt.savefig(savepath)










    plt.show()


if __name__ == "__main__":
    
    main()
    

