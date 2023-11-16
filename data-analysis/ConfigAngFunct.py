from PlotOptions import *

# A = 1
# phi = 1
# omega = 1

# def f(x):
#     return A*np.sin(omega*x + phi)

# x = np.arange(1,50, 0.1)

# plt.plot(x,f(x))


# x = np.arange(1,50, 1)
# centers = x[:-1] + np.diff(x) * (A)
# y = f(centers)
# plt.stairs(y-1, x, edgecolor="r", linewidth=1.0, fill=False, label="Step")

# plt.show()

bins = np.arange(14)
centers = bins[:-1] + np.diff(bins) / 2
y = np.sin(centers / 2)

plt.stairs(y - 1, bins, baseline=None, label='step')
plt.plot(centers, y - 1, 'o--', color='grey', alpha=0.3, label="Config Ang Function")
plt.plot(np.repeat(bins, 2), np.hstack([y[0], np.repeat(y, 2), y[-1]]) - 1,
         'o', color='red', alpha=0.2)

plt.legend()
plt.xlabel("Time [days]")
plt.ylabel("Config Angle [au]")
plt.show()
