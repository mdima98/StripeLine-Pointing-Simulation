from scipy.sparse import csr_matrix, coo_matrix

from DataHandling import *
from PlotOptions import *





def plot_hist(specifics, fhist, options):
    
    figsize = None if options["savefig"] else (8,6)
    
    fig = plt.figure(figsize=figsize)
    ax = plt.gca()
    
    hist = np.loadtxt(fhist, delimiter=',', unpack=False, dtype=int)
    
    # Sort (bins,freq) for hist plotting  
    hist = np.array(sorted(hist, key=lambda x: x[0]))
    bins = hist[:,0]
    freq = hist[:,1]

    bins_edges = np.append(bins-0.5, bins[-1]+0.5)
    
    ax.stairs(freq, bins_edges, edgecolor=COLORS["palatinate-blue"], linewidth=1.0, fill=False, label=specifics["polarimeter"])
    
    title = f"Pointing Error Distribution"
    ax.set_title(title)
    ax.set_xlabel(f"Pointing Error [{specifics['units']}]")
    ax.set_yscale("log")
    ax.set_ylabel('Count')
    ax.legend()
    
    if options["savefig"]:
        name = f"point_err_distr_{specifics['start_day']}_{specifics['start_day']+specifics['ndays']}_{specifics['polarimeter']}.svg"
        fname = SAVEPATH + name
        plt.savefig(fname, format='svg', dpi=600)
    
    
def plot_hist2d(specifics, fhist2d, options):

    usecols, coord_name = ([3,4,5], "GR") if options["ground"] else ([0,1,2], "EQ")
    figsize = None if options["savefig"] else (8,6)
    
    hist2d = pd.read_csv(fhist2d, names=["colat", "long", "freq"],
                         header=None, usecols=usecols).dropna()
    
    # Apply azimuth correction (check if not already done in simulation)
    if options["ground"]:
        hist2d["long"] *= np.sin(np.deg2rad(20.0 + hist2d.colat/3600.))
        hist2d = hist2d.astype("int")
        hist2d = hist2d.groupby(['colat', 'long'], as_index=False).sum()
    
    freq_max = hist2d["freq"].values.max()
    freq_min = hist2d["freq"].values.min()
    
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
    fig = plt.figure(figsize=figsize)
    ax = plt.gca()

    g = ax.imshow(hist2d, interpolation="none", aspect="auto", origin="lower",
                  extent=extent,
                  label=specifics["polarimeter"],
                  cmap='viridis',
                  norm=matplotlib.colors.LogNorm(vmin=freq_min, vmax=freq_max, clip=True))
    # formatter = matplotlib.ticker.LogFormatter(10, labelOnlyBase=True) 
    # tick = None
    cbar = fig.colorbar(g, label="Count")

    # Set labels    
    if options["ground"]:
        title = f"Angular Error Distribution in ground coordinates ({specifics['polarimeter']})"
    else:
         title = f"Angular Error Distribution in sky coordinates ({specifics['polarimeter']})"
    ax.set_title(title)
    
    xlabel =  f"Zenithal Distance Error [{specifics['units']}]" if options["ground"] else f"Colatitude Error [{specifics['units']}]"
    ax.set_xlabel(xlabel)

    ylabel = f"Azimuth Error [{specifics['units']}]" if options["ground"] else f"Longitude Error [{specifics['units']}]"
    ax.set_ylabel(ylabel)
    
    if options["savefig"]:
        name = title.replace(" ", "_")
        savefig(name)