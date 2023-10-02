import numpy as np
import matplotlib.pyplot as plt
import sys



def read_hist_file(fname):
    
    with open(fname, "r") as hfile:
        
        nbins, step, outliers = hfile.readline().split("\t")
        
    freq, bins = np.loadtxt(fname, delimiter="\t", skiprows=1, unpack=True)
  
    return int(nbins), float(step), int(outliers), freq.astype(int), bins.astype(float)



def main():
    
    fpath = str(sys.argv[1])
    nbins, step, outliers, freq, bins = read_hist_file(fpath)
    
    fig, ax = plt.subplots(figsize=(12, 4), tight_layout=True)
    bins_width = step

    # ax.bar(bins, freq, width=step, edgecolor='crimson', fill=False)
    ax.step(bins, freq, where="mid", c="blue")
    ax.set_xlabel("Pointing Error [arcsec]")
    ax.set_yscale("log")
    ax.set_ylabel('Frequency')

    plotdir = "hist_plots/"
    s = fpath.split("/")
    fname = s[-1].replace(".hist", ".png")
    savepath = plotdir+fname
    plt.savefig(savepath)

    plt.show()


if __name__ == "__main__":
    
    main()
    
