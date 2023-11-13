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
    specifics, fhist, fhist2d = get_hist_files(dargs)
    
    options = {  
        "ground": args.ground,
        "savefig": args.savefig
    }
    # Plot data
    plot_hist(specifics, fhist, options)
    plot_hist2d(specifics, fhist2d, options)
    
    plt.show()


if __name__ == "__main__":
    
    main()
    

