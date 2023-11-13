from PlotFunctions import *


def main():
    
    # Get data files
    args = parse_commandline()
    specifics, fhist, fhist2d = get_data(args)
    
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
    

