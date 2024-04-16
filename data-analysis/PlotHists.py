from PlotFunctions import *


def main():
    
    # Get data files
    args = parse_commandline_plots()
    dargs = {
        "datadir": args.datadir,
        "first_day": args.first_day,
        "last_day": args.last_day,
        "polarimeter": args.polarimeter
    }
    specifics, fhist, fhist2d = get_hist_files(dargs, args.combined)
    
    options = {  
        "ground": args.ground,
        "savefig": args.savefig,
        "both": args.both
    }
    # Plot data
    plot_hist(specifics, fhist, options)
    
    if args.both:
        plot_both(specifics, fhist2d, options)
    else:
        plot_hist2d(specifics, fhist2d, options)
    
    
    # fig, axs = plt.subplots(1,1)
    
    # time_range, sky_tod = np.loadtxt("tod_data.csv", unpack=True, delimiter=',')
    
    # axs.plot(time_range, np.rad2deg(sky_tod), color=COLORS["palatinate-blue"], linewidth=0.5)
    # axs.set_xlabel("Time [s]")
    # axs.set_ylabel(r"Signal [$\mu$K]")
    
    # plt.savefig(SAVEPATH+"signal_plot.pdf", format="pdf", dpi=600)
    
    # plt.show()


if __name__ == "__main__":
    
    main()
    

