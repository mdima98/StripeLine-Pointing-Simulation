from scipy.sparse import csr_matrix
from DataHandling import *




def plot_hist(specifics, fhist):
    
    fig, ax = plt.subplots(figsize=(8, 6), tight_layout=True)
    
    hist = np.loadtxt(fhist, delimiter=',', unpack=False, dtype=int)
    
    # Sort (bins,freq) for hist plotting  
    hist = np.array(sorted(hist, key=lambda x: x[0]))
    bins = hist[:,0]
    freq = hist[:,1]

    bins_edges = np.append(bins-0.5, bins[-1]+0.5)
    
    ax.stairs(freq, bins_edges, edgecolor="b", linewidth=1.0, fill=False, label=specifics["pol_name"])
    
    ax.set_title("Pointing Error Distribution")
    ax.set_xlabel(f"Pointing Error [{specifics['units']}]")
    ax.set_yscale("log")
    ax.set_ylabel('Count')
    ax.legend()
    
    
def plot_hist2d(specifics, fhist2d):
    
    # fig, ax = plt.subplots(figsize=(8, 6), tight_layout=True)
    
    # (colat2d, long2d, freq2d) = np.loadtxt(fhist2d, delimiter=',', unpack=True, dtype=int)
            
    
    # g = ax.scatter(colat2d,long2d,c=freq2d, marker='o', edgecolors='none', label=specifics["pol_name"], cmap='inferno')
    # cbar = fig.colorbar(g, label="Count")
    
    # hist2d = np.loadtxt(fhist2d, delimiter=',', usecols=(0,1), dtype=int)
    # freq2d = np.loadtxt(fhist2d, delimiter=',', usecols=2, dtype=int)
    
    # colat_min, colat_max = np.min(hist2d[:,1]), np.max(hist2d[:,1])
    # long_min, long_max = np.min(hist2d[:,2]), np.max(hist2d[:,2])

    
    
    
    hist2d = pd.read_csv(fhist2d, names=["Colatitude", "Longitude", "Count"], header=None, usecols=[0,1,2])
    hist2d = hist2d.dropna()
    
    # Set plot axis limits
    if specifics["units"] == "arcsec":
        low_bound = 0.03
        high_bound = 0.03
    elif specifics["units"] == "arcmin":
        low_bound = 0.20
        high_bound = 0.20
    else:
        low_bound = 0.03
        high_bound = 0.03
        
    low_extent = int(hist2d[['Colatitude', 'Longitude']].values.min()*(1+low_bound))
    high_extent = int(hist2d[['Colatitude', 'Longitude']].values.max()*(1+high_bound))
    extent = [low_extent, high_extent, low_extent, high_extent]
    
    r = range(low_extent, high_extent)
    hist2d = (hist2d.set_index(['Colatitude','Longitude'])['Count']
        .unstack(fill_value=0)
        .reindex(index=r, columns=r, fill_value=0)
        .rename_axis(None)
        .rename_axis(None, axis=1)
        .T)
    
    # hist2d = csr_matrix(hist2d.values, dtype=int)


    fig, ax = plt.subplots(figsize=(8, 6), tight_layout=True)

    g = ax.imshow(hist2d, interpolation="none", aspect="auto", origin="upper", extent=extent, label=specifics["pol_name"], cmap='viridis')
    cbar = fig.colorbar(g, label="Count")
    
    title = f"Angular Error Distribution (Days {specifics['start_day']} to {specifics['start_day']+specifics['ndays']} - {specifics['pol_name']})"
    ax.set_title(title)
    ax.set_xlabel(f"Colatitude Error [{specifics['units']}]")
    ax.set_ylabel(f"Longitude Error [{specifics['units']}]")