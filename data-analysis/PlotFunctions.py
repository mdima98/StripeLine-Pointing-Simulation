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
    
    # title = f"Pointing Error Distribution"
    # ax.set_title(title)
    ax.set_xlabel(f"Pointing Error [{specifics['units']}]")
    ax.set_yscale("log")
    ax.set_ylabel('Count')
    ax.legend()
    
    if options["savefig"]:
        name = f"point_err_distr_{specifics['start_day']}_{specifics['start_day']+specifics['ndays']}_{specifics['polarimeter']}.svg"
        fname = SAVEPATH + name
        plt.savefig(fname, format='svg', dpi=600)
    
    
def plot_hist2d(specifics, fhist2d, options, fig=None, ax=None):

    usecols, coord_name = ([3,4,5], "GR") if options["ground"] else ([0,1,2], "EQ")
    # figsize = None if options["savefig"] else (8,6)
    figure_size = figsize(0.9)
    
    hist2d = pd.read_csv(fhist2d, names=["colat", "long", "freq"],
                         header=None, usecols=usecols).dropna()
    
    # # Apply azimuth correction (check if not already done in simulation)
    # if options["ground"]:
    #     hist2d["long"] *= np.sin(np.deg2rad(20.0 + hist2d.colat/3600.))
    #     hist2d = hist2d.astype("int")
    #     hist2d = hist2d.groupby(['colat', 'long'], as_index=False).sum()
    
    freq_max = hist2d["freq"].values.max()
    freq_min = hist2d["freq"].values.min()
    
    # Set plot axis limits
    colat_low = hist2d['colat'].values.min()
    colat_high = hist2d['colat'].values.max()
    long_low = hist2d['long'].values.min()
    long_high = hist2d['long'].values.max()
    
    colat_len = colat_high - colat_low
    long_len = long_high - long_low
    
    if options["ground"]:
        low_bound = 0.08
        high_bound = 0.08
    else:
        low_bound = 0.03
        high_bound = 0.03
    
    colat_low -= colat_len*low_bound
    colat_high += colat_len*high_bound
    long_low -= long_len*low_bound
    long_high += long_len*high_bound 
    
    r_colat = range(int(colat_low), int(colat_high))
    r_long = range(int(long_low), int(long_high))
    
    # Set hist2d as matrix for plotting
    hist2d = ( hist2d.pivot(index = 'long', columns = 'colat', values = 'freq')
            .reindex(index = r_long, columns = r_colat)
            .fillna(0)
            .rename_axis(columns = None,index = None).T )
    
    extent = [colat_low, colat_high, long_low, long_high]
    
    # Plot hist 2D
    if ax is None:
        fig = plt.figure(figsize=figure_size)
        ax = plt.gca()
    
    

    g = ax.imshow(hist2d, interpolation="none", aspect="auto", origin="lower",
                  extent=extent,
                  label=specifics["polarimeter"],
                  cmap='viridis',
                  norm=matplotlib.colors.LogNorm(vmin=freq_min, vmax=freq_max, clip=True))
    # formatter = matplotlib.ticker.LogFormatter(10, labelOnlyBase=True) 
    # tick = None
        
    cbar = fig.colorbar(g, label="Count")
    
    if options["ground"]:
        ax.set_aspect(1)

    # Set labels    
    if options["ground"]:
        title = f"Angular Error Distribution in ground coordinates ({specifics['polarimeter']})"
    else:
         title = f"Angular Error Distribution in sky coordinates ({specifics['polarimeter']})"
    # ax.set_title(title)
    
    # ylabel =  rf"$\delta \vartheta$ [{specifics['units']}]" if options["ground"] else f"Colatitude Error [{specifics['units']}]"
    # xlabel = rf"$\delta \varphi \times \sin(\vartheta)$ [{specifics['units']}]" if options["ground"] else f"Longitude Error [{specifics['units']}]"
   
    ylabel = f"Zenithal Distance Error [{specifics['units']}]" if options["ground"] else f"Colatitude Error [{specifics['units']}]"
    xlabel = rf"Azimuth Error $\times$ sin(Zen. Dist.) [{specifics['units']}]" if options["ground"] else f"Longitude Error [{specifics['units']}]"
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    if options["savefig"] and not options["both"]:
        # name = title.replace(" ", "_")
        name = f"hist2d_{coord_name}_{specifics['polarimeter']}_{specifics['start_day']}_{specifics['start_day'] + specifics['ndays']}"
        savefig(name)
        
        
        
def plot_both(specifics, fhist2d, options):
    
    fig, axs = plt.subplots(1,2)
    
    
    #############################
    # Get colorbar limits
    hist2d_gr = pd.read_csv(fhist2d, names=["colat", "long", "freq"],
                         header=None, usecols=[3,4,5]).dropna()
    hist2d_eq = pd.read_csv(fhist2d, names=["colat", "long", "freq"],
                         header=None, usecols=[0,1,2]).dropna()
    
    
    freq_max = np.maximum(hist2d_eq["freq"].values.max(), hist2d_gr["freq"].values.max())
    freq_min = np.minimum(hist2d_eq["freq"].values.min(), hist2d_gr["freq"].values.min())
    
    norm = matplotlib.colors.LogNorm(vmin=freq_min, vmax=freq_max, clip=True)


    #################### GR ################################

    usecols = [3,4,5]
    hist2d = pd.read_csv(fhist2d, names=["colat", "long", "freq"],
                         header=None, usecols=usecols).dropna()
    
    # Set axes limits
    colat_high, colat_low, long_high, long_low = set_axes_lim(hist2d, 0.08, 0.08)
    r_colat = range(int(colat_low), int(colat_high))
    r_long = range(int(long_low), int(long_high))
    
    # Set hist2d as matrix for plotting
    hist2d = ( hist2d.pivot(index = 'long', columns = 'colat', values = 'freq')
            .reindex(index = r_long, columns = r_colat)
            .fillna(0)
            .rename_axis(columns = None,index = None).T )
    extent = [colat_low, colat_high, long_low, long_high]

    g = axs[0].imshow(hist2d, interpolation="none", aspect="auto", origin="lower",
                  extent=extent,
                  label=specifics["polarimeter"],
                  cmap='viridis',
                  norm=norm)
    
    #################### EQ ################################

    usecols = [0,1,2]
    hist2d = pd.read_csv(fhist2d, names=["colat", "long", "freq"],
                         header=None, usecols=usecols).dropna()
    
    # Set axes limits
    colat_high, colat_low, long_high, long_low = set_axes_lim(hist2d, 0.03, 0.03)
    r_colat = range(int(colat_low), int(colat_high))
    r_long = range(int(long_low), int(long_high))
    
    # Set hist2d as matrix for plotting
    hist2d = ( hist2d.pivot(index = 'long', columns = 'colat', values = 'freq')
            .reindex(index = r_long, columns = r_colat)
            .fillna(0)
            .rename_axis(columns = None,index = None).T )
    extent = [colat_low, colat_high, long_low, long_high]

    g = axs[1].imshow(hist2d, interpolation="none", aspect="auto", origin="lower",
                  extent=extent,
                  label=specifics["polarimeter"],
                  cmap='viridis',
                  norm=norm)
    
    #########################################################

    xlabel = f"Azimuth Error [{specifics['units']}]" if options["ground"] else f"Longitude Error [{specifics['units']}]"
    ylabel =  f"Zenithal Distance Error [{specifics['units']}]" if options["ground"] else f"Colatitude Error [{specifics['units']}]"
    axs[0].set_xlabel(xlabel)
    axs[0].set_ylabel(ylabel)
    
    axs[1].set_xlabel(xlabel)
    axs[1].set_ylabel(ylabel)
    
    cbar = fig.colorbar(g, ax=axs, label="Count")
    
    if options["savefig"]:
        # name = title.replace(" ", "_")
        name = f"hist2d_{specifics['polarimeter']}_{specifics['start_day']}_{specifics['start_day'] + specifics['ndays']}"
        savefig(name)
        



















    
    # options = {  
    #     "ground": True,
    #     "savefig": options["savefig"],
    #     "both": options["both"]
    # }
    # plot_hist2d(specifics, fhist2d, options, fig, axs[0])
    
    # options = {  
    #     "ground": False,
    #     "savefig": options["savefig"],
    #     "both": options["both"]
    # }
    # plot_hist2d(specifics, fhist2d, options, fig, axs[1])




def set_axes_lim(hist2d, low_bound, high_bound):
    # Set plot axis limits
    colat_low = hist2d['colat'].values.min()
    colat_high = hist2d['colat'].values.max()
    long_low = hist2d['long'].values.min()
    long_high = hist2d['long'].values.max()
    
    colat_len = colat_high - colat_low
    long_len = long_high - long_low
    
    colat_low -= colat_len*low_bound
    colat_high += colat_len*high_bound
    long_low -= long_len*low_bound
    long_high += long_len*high_bound 
    
    return colat_high, colat_low, long_high, long_low