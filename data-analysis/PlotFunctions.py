from scipy.sparse import csr_matrix, coo_matrix

from DataHandling import *
# from PlotOptions import *
import matplotlib.pyplot as plt




def plot_hist(specifics, fhist):
    
    fig, ax = plt.subplots(figsize=(8,6), tight_layout=True)
    
    hist = np.loadtxt(fhist, delimiter=',', unpack=False, dtype=int)
    
    # Sort (bins,freq) for hist plotting  
    hist = np.array(sorted(hist, key=lambda x: x[0]))
    bins = hist[:,0]
    freq = hist[:,1]

    bins_edges = np.append(bins-0.5, bins[-1]+0.5)
    
    ax.stairs(freq, bins_edges, edgecolor="b", linewidth=1.0, fill=False, label=specifics["pol_name"])
    
    title = f"Pointing Error Distribution (Days {specifics['start_day']} to {specifics['start_day']+specifics['ndays']} - {specifics['pol_name']})"
    ax.set_title(title)
    ax.set_xlabel(f"Pointing Error [{specifics['units']}]")
    ax.set_yscale("log")
    ax.set_ylabel('Count')
    ax.legend()
    
    
def plot_hist2d(specifics, fhist2d, ground):
    
    # fig, ax = plt.subplots(figsize=(8, 6), tight_layout=True)
    
    # (colat2d, long2d, freq2d) = np.loadtxt(fhist2d, delimiter=',', usecols=[0,1,2], unpack=True, dtype=int)
            
    
    # g = ax.scatter(colat2d,long2d,c=freq2d, marker='o', edgecolors='none', label=specifics["pol_name"], cmap='inferno')
    # cbar = fig.colorbar(g, label="Count")
    
    usecols, coord_name = ([3,4,5], "GR") if ground else ([0,1,2], "EQ")
    
    hist2d = pd.read_csv(fhist2d, names=["colat", "long", "freq"], header=None, usecols=usecols)
    hist2d = hist2d.dropna()
    
    # Set plot axis limits
    colat_low = hist2d['colat'].values.min()
    colat_high = hist2d['colat'].values.max()
    long_low = hist2d['long'].values.min()
    long_high = hist2d['long'].values.max()
    
    colat_len = colat_high - colat_low
    long_len = long_high - long_low
    
    low_bound = 0.05
    high_bound = 0.05
    
    colat_low -= colat_len*low_bound
    colat_high += colat_len*high_bound
    long_low -= long_len*low_bound
    long_high += long_len*high_bound 
    
    r_colat = range(int(colat_low), int(colat_high))
    r_long = range(int(long_low), int(long_high))
    
    # Set hist2d as matrix for plotting
    hist2d = ( hist2d.pivot(index = 'colat', columns = 'long', values = 'freq')
            .reindex(index = r_colat, columns = r_long)
            .fillna(0)
            .rename_axis(columns = None,index = None).T )
    
    extent = [colat_low, colat_high, long_low, long_high]
    
    # Plot hist 2D
    fig, ax = plt.subplots(figsize=(8,6), tight_layout=True)

    g = ax.imshow(hist2d, interpolation="none", aspect="auto", origin="lower", extent=extent, label=specifics["pol_name"], cmap='viridis')
    cbar = fig.colorbar(g, label="Count")

    # Set labels    
    title = f"Angular Error Distribution (Days {specifics['start_day']} to {specifics['start_day']+specifics['ndays']} - {specifics['pol_name']})"
    ax.set_title(title)
    
    xlabel = f"Colatitude Error ({coord_name}) [{specifics['units']}]"
    ax.set_xlabel(xlabel)

    ylabel = f"Longitude Error ({coord_name}) [{specifics['units']}]"
    ax.set_ylabel(ylabel)