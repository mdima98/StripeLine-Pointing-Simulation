import numpy as np
import matplotlib.pyplot as plt
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
    
    # Sort hist by bins
    hist_dict = dict(sorted(toml_dict["hist"].items()))
    
    bins = np.fromiter(hist_dict.keys(), dtype=int)
    freq = np.fromiter(hist_dict.values(), dtype=int)
    
    return specifics, bins, freq

# def combine_hist(nhist, start_days, ndays, pol_name):
    
    
    
    


def main():
    
    fpath = str(sys.argv[1])
    
    specifics, bins, freq = read_toml_hist(fpath)
    
    fig, ax = plt.subplots(figsize=(12, 4), tight_layout=True)
    
    bins_edges = np.append(bins-0.5, bins[-1]+0.5)
    ax.stairs(freq, bins_edges, edgecolor="b", linewidth=1.0, fill=False, label=specifics["pol_name"])
    
    
    ax.legend()
    ax.set_xlabel(f"Pointing Error [{specifics['units']}]")
    ax.set_yscale("log")
    ax.set_ylabel('Frequency')
    ax.legend()

    # plotdir = "hist_plots/"
    # s = fpath.split("/")
    # fname = s[-1].replace(".hist", ".png")
    # savepath = plotdir+fname
    # plt.savefig(savepath)
    plt.savefig("hist_plots/I0_I1_V4_0_10.png")

    plt.show()


if __name__ == "__main__":
    
    main()
    
