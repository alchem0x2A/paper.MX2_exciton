import numpy
import matplotlib.pyplot as plt
from gpaw.response.gw_bands import GWBands
from ase.units import Ha
import os, os.path
from scipy.optimize import curve_fit


materials = ["MoS2", "MoSe2", "WS2", "WSe2"]
colors = dict(MoS2="r",
              MoSe2="g",
              WS2="k",
              WSe2="b")
# symbols = ["^", "v"]
curdir = os.path.dirname(__file__)
res_path = os.path.join(curdir, "../../results")
exp_path  = os.path.join(curdir, "../../data/exp/")
img_path = os.path.join(os.path.dirname(__file__), "../../img")


def compare_n(ax):
    data = numpy.genfromtxt(os.path.join(exp_path, "N_fit.csv"),
                            delimiter=",", skip_header=1)
    ea = data[:, 1]
    N0_exp = data[:, 2]
    err_l = data[:, 3]
    err_h = data[:, 4]
    Ng = data[:, -3]
    Nb = data[:, -2]
    Na = data[:, -1]
    ax.errorbar(ea, N0_exp, yerr=[err_h - N0_exp,
                                  N0_exp - err_l],
                fmt="s",
                label="Exp")
    ax.plot(ea, Ng, "o", label="from Eg")
    ax.plot(ea, Nb, "^", label="from Eb")
    ax.plot(ea, Na, "*", label="from Ea")
    ax.set_xlim(1.5, 2.0)
    ax.set_ylim(1.5, 10)
    ax.set_xlabel("$E_{\\rm{A}}$ (eV)")
    ax.set_ylabel("$N_0$ from Fitting")
    ax.legend()
    return

def compare_delta(ax):
    data = numpy.genfromtxt(os.path.join(exp_path, "fitting_comparison.csv"),
                            delimiter=",", skip_header=1)
    delta = data[:, 1]
    err = data[:, 2]
    delta_model = data[:, 3]
    wd = 0.5
    ax.bar(numpy.array([1, 2, 3, 4]) - wd / 2, delta_model, width=wd,
           alpha=0.5, label="Model")
    ax.bar(numpy.array([1, 2, 3, 4]) - wd / 2, delta, yerr=err,
           width=wd,
           label="Exp", alpha=0.5)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(["", ] * 4)
    ax.set_ylabel("$E_{\\rm{A, ML}} - E_{\\rm{A, Bulk}}$ (meV)")
    ax.legend(loc=0)
    ax.set_ylim(0, 200)
    
    

def main(n_max=15):
    fig = plt.figure(figsize=(5.6, 2.8))
    plt.style.use("science")

    
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    compare_n(ax1)
    compare_delta(ax2)
        # ax.set_ylim(0, 200)
        # ax.set_ylabel()
        
        
    
    # exp_n, exp_ea = get_exp(mater)
    # ax.set_xlabel("$N$")
    # ax.set_ylabel("Energy (eV)")
    # ax.legend(loc=0)
    fig.tight_layout()
    f_name = os.path.join(img_path, "compare_exp.svg")
    fig.savefig(f_name)
    return

if __name__ == "__main__":
    main()
