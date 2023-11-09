import matplotlib
import numpy as np
from matplotlib.backends.backend_pgf import FigureCanvasPgf
matplotlib.backend_bases.register_backend('pdf', FigureCanvasPgf)
import matplotlib.pyplot as plt

def figsize(scale):
    fig_width_pt = 452.9679                         # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    golden_mean = (np.sqrt(5.0)-1.0)/2.0            # Aesthetic ratio (you could change this)
    fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
    fig_height = fig_width*golden_mean              # height in inches
    fig_size = [fig_width,fig_height]
    return fig_size


plt.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'text.usetex': True,         # use LaTeX to write all text
    'pgf.rcfonts': False,
    'font.family': 'serif',
    "font.serif": ["Latin Modern"],                   # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "axes.labelsize": 10,               # LaTeX default is 10pt font.
    "font.size": 10,
    "legend.fontsize": 8,               # Make the legend/label fonts a little smaller
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.figsize": figsize(0.9),     # default fig size of 0.9 textwidth
    "pgf.preamble": "\n".join([
        r"\usepackage[utf8x]{inputenc}",     # use utf8 fonts becasue your computer can handle it :)
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{lmodern}",
     ]),
})