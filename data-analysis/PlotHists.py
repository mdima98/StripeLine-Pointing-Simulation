from PlotFunctions import *


def main():
    
    # Get data files
    args = parse_commandline()
    specifics, fhist, fhist2d = get_data(args)
    ground = args.ground
    
    # Plot data
    plot_hist(specifics, fhist)
    plot_hist2d(specifics, fhist2d, ground)
    
    plt.show()


if __name__ == "__main__":
    
    main()
    

