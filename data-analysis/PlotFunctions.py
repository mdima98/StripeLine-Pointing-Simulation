from DataHandling import *


def plot_hist(specifics, fhist):
    
    fig, ax = plt.subplots(figsize=(8, 6), tight_layout=True)
    
    (bins, freq) = np.loadtxt(fhist, delimiter=',', unpack=True, dtype=int)
    
    if type(bins) == np.int64:
        bins= np.array([bins, bins+1])
        freq = np.array([freq, 0])
      
    # Sort for hist plotting  
    bins = np.sort(bins)
    freq = np.array([freq for _, freq in sorted(zip(bins, freq), key=lambda pair: pair[0])])
    
    bins_edges = np.append(bins-0.5, bins[-1]+0.5)
    
    ax.stairs(freq, bins_edges, edgecolor="b", linewidth=1.0, fill=False, label=specifics["pol_name"])
    
    ax.set_title("Pointing Error Distribution")
    ax.set_xlabel(f"Pointing Error [{specifics['units']}]")
    ax.set_yscale("log")
    ax.set_ylabel('Frequency')
    ax.legend()
    
    
def plot_hist2d(specifics, fhist2d):
    
    fig, ax = plt.subplots(figsize=(8, 6), tight_layout=True)
    
    (colat2d, long2d, freq2d) = np.loadtxt(fhist2d, delimiter=',', unpack=True, dtype=int)
    
    freq2d = np.ma.masked_where(freq2d < 35, freq2d)
            
    
    g = ax.scatter(colat2d,long2d,c=freq2d, marker='o', edgecolors='none', label=specifics["pol_name"], cmap='inferno')
    cbar = fig.colorbar(g, label="Frequency")

    
    ax.set_title("Colatitude and Longitude Error Distribution")
    ax.set_xlabel(f"Colatitude [{specifics['units']}]")
    ax.set_ylabel(f"Longitude [{specifics['units']}]")
    ax.legend()