import numpy
import matplotlib.pyplot as plt
from gpaw.response.gw_bands import GWBands
from ase.units import Ha
import os, os.path


materials = ["MoS2", "MoSe2", "WS2", "WSe2"]
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
    f_name = os.path.join(exp_path, "{}.csv".format(mater))
    data = numpy.genfromtxt(f_name, delimiter=",",
                            skip_header=1)
    n = data[:, 0]
    e_a = data[:, 1]
    return n, e_a

def main(mater, n_max=15):
    fig = plt.figure(figsize=(3.5, 2.5))
    plt.style.use("science")
    ax = fig.add_subplot(111)
    N1, Eb = get_exciton(mater)
    N2, Eg = get_gap(mater)
    cond1 = numpy.where(N1 <= n_max)
    cond2 = numpy.where(N2 <= n_max)
    N1 = N1[cond1];  N2 = N2[cond2]
    Eb= Eb[cond1];  Eg = Eg[cond2]
    Ea = Eg - Eb
    exp_n, exp_ea = get_exp(mater)
    ax.plot(N1, Eb, "-o", label="$E_{b}$")
    ax.plot(N2, Eg, "-o", label="$E_{g}$")
    ax.plot(N1, Ea, "-o", label="$E_{A}$")
    ax.set_xlabel("$N$")
    ax.set_ylabel("Energy level (eV)")
    ax.legend(loc=0)
    ax.set_title("{}".format(mater))
    fig.tight_layout()
    f_name = os.path.join(img_path, "{}-qeh-gap.svg".format(mater))
    fig.savefig(f_name)
    return

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        mater = "MoS2"
    else:
        mater = sys.argv[1]

    main(mater)
