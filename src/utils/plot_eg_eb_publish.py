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

def get_exciton(mater):
    f_name = os.path.join(res_path,
                          "exciton/{}_eb.csv".format(mater))
    data = numpy.genfromtxt(f_name, delimiter=",")
    N = data[:, 0]
    Eb = data[:, 1]
    return N, Eb

def get_gap(mater):
    f_name = os.path.join(res_path,
                          "gw_gap/{}-gwqeh-gap.csv".format(mater))
    data = numpy.genfromtxt(f_name, delimiter=",")
    N = data[:, 0]
    Eg = data[:, 1]
    return N, Eg

def get_exp(mater):
    f_name = os.path.join(exp_path, "{}_new.csv".format(mater))
    data = numpy.genfromtxt(f_name, delimiter=",",
                            skip_header=1)
    n = data[:, 0]
    e_a = data[:, 1]
    return n, e_a

def fit_fun(n, E_1, E_inf, N_0):
    return E_inf + (E_1 - E_inf) * numpy.exp(-(n-1)/N_0)
    

def main(n_max=15):
    fig = plt.figure(figsize=(2.8, 2.8))
    plt.style.use("science")
    
    ax = fig.add_subplot(111)
    for i, mater in enumerate(materials):
        N1, Eb = get_exciton(mater)
        N2, Eg = get_gap(mater)
        N_exp, Ea_exp = get_exp(mater)
        cond1 = numpy.where(N1 <= n_max)
        cond2 = numpy.where(N2 <= n_max)
        N1 = N1[cond1];  N2 = N2[cond2]
        Eb = Eb[cond1];  Eg = Eg[cond2]
        Ea = Eg - Eb
        # ax.plot(N1, Eg, "-o", label=mater)
        # ax.plot(N2, Eg, "-o")
        p = curve_fit(fit_fun, N1, Ea, p0=(Ea[0], Ea[-1], 3))
        p1, *_ = curve_fit(fit_fun, N1, Eb, p0=(Eb[0], Eb[-1], 3))
        p2, *_ = curve_fit(fit_fun, N2, Eg, p0=(Eg[0], Eg[-1], 3))
        p3, *_ = curve_fit(fit_fun, N_exp, Ea_exp, p0=(Ea_exp[0], Ea_exp[-1], 3))
        print(mater, "Eb", p1)
        print(mater, "Eg", p2)
        
        E_inf = fit_fun(100, *p2) - fit_fun(100, *p1)
        l, = ax.plot(N1, Eb, "^", label="Eb " + mater, color=colors[mater],
                     markersize=5)
        l2, = ax.plot(N2, Eg, "o", label="Eg", color=colors[mater],
                      markersize=5)
        # ax.plot(N_exp, (Ea_exp - p3[1]) * 1000, "s", label="Experiment")
        nn = numpy.linspace(1, 15)
        ax.plot(nn, fit_fun(nn, *p1),
                color=l.get_c())
        ax.plot(nn, fit_fun(nn, *p2),
                color=l2.get_c())
    ax.legend()
        # ax.set_ylim(0, 200)
        # ax.set_ylabel()
        
        
    
    # exp_n, exp_ea = get_exp(mater)
    ax.set_xlabel("$N$")
    ax.set_ylabel("Energy (eV)")
    # ax.legend(loc=0)
    fig.tight_layout()
    f_name = os.path.join(img_path, "all-eg-vs-eb.svg")
    fig.savefig(f_name)
    return

if __name__ == "__main__":
    main()
