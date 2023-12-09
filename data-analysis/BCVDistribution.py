from DataHandling import *
from PlotOptions import *

fname = "data-analysis/bcv_angles_all_arcsec.csv"

df = pd.read_csv(fname, names=["ang", "freq"], header=None).dropna()
df.ang =  pd.to_numeric(df.ang)

# df = df.astype({"ang": "int", "freq": "int"})
df = df.groupby(['ang'], as_index=False).sum()

plt.hist(df.ang, bins=20, histtype="step", color=COLORS["palatinate-blue"])

# hist = df.to_numpy()

# # Sort (bins,freq) for hist plotting  
# hist = np.array(sorted(hist, key=lambda x: x[0]))
# bins = hist[:,0]
# freq = hist[:,1]

# bins_edges = np.append(bins-0.5, bins[-1]+0.5)

# fig = plt.figure(figsize=(8,6))
# ax = plt.gca()


# ax.stairs(freq, bins_edges, edgecolor=COLORS["palatinate-blue"], linewidth=1.0, fill=False, label="BCV Angles")
    
# title = f"BCV Flexures Angles Distribution"
# ax.set_title(title)
# ax.set_xlabel(f"Angle [arcsec]")
# ax.set_ylabel('Count')
# ax.legend()

plt.show()
