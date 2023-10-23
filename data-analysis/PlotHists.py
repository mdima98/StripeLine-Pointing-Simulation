from PlotFunctions import *


def main():
    
    # Get data files
    args = parse_commandline()
    specifics, fhist, fhist2d = get_data(args)
    
    # Plot data
    plot_hist(specifics, fhist)
    plot_hist2d(specifics, fhist2d)
    
    plt.show()


if __name__ == "__main__":
    
    main()
    

