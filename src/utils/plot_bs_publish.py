import numpy
import matplotlib.pyplot as plt
from gpaw.response.gw_bands import GWBands
from ase.units import Ha
import os, os.path


materials = ["MoS2", "MoSe2", "WS2", "WSe2"]
# materials = ["MoS2", "MoSe2", "WS2",]
data_path = os.path.join(os.path.dirname(__file__), "../../results")
img_path = os.path.join(os.path.dirname(__file__), "../../img")

def get_color(i, n_max=15):
    color = plt.cm.rainbow(numpy.linspace(0, 1, n_max + 1))
    return color[i]

def add_cbar(fig, ax, n_max=15):
    xlim = ax.get_xlim()
    sc = ax.scatter([-100, -100], [-100, -100], c=[1, n_max],
                    cmap="rainbow")
    cb = fig.colorbar(sc)
    cb.set_ticks([1, 5, 10, 15])
    cb.ax.set_title("$N$")
    ax.set_xlim(*xlim)
    return

def es_wfs(mater):
    return os.path.join(data_path, "gw_bs/{}/es.gpw".format(mater))

def g0w0_file(mater):
    return os.path.join(data_path, "gw_bs/{}/g0w0_results.pckl".format(mater))

def get_band(mater, n_layers=1):
    npz_file = os.path.join(data_path,
                            "{}_{}.npz".format(mater, n_layers))
    if not os.path.exists(npz_file):
        K = numpy.array([1 / 3, 1 / 3, 0])
        M = numpy.array([1 / 2, 0, 0])
        G = numpy.array([0.0, 0.0, 0.0])
        # P1 = K * 0.8
        # P2 = K + (M - K) * 0.4
        # kpoints = numpy.array([P1, K, P2])
        kpoints = numpy.array([G, M, K, G])
        gw = GWBands(calc=es_wfs(mater),
                     gw_file=g0w0_file(mater),
                     kpoints=kpoints)
        # Use QP energy from GWQEH
        if n_layers > 1:
            f_qeh = os.path.join(data_path,
                                 "gw_bs/{0}/gwqeh_{1}_qeh.npz".format(mater, n_layers))
            gw.gw_file["qp"] = numpy.load(f_qeh)["Qp_sin"] * Ha
        res = gw.get_gw_bands(nk_Int=120,
                              interpolate=True, vac=True)
        print(res)
        xx = res["x_k"]
        ekn = res["e_kn"]
        X = res["X"]
        # Now shift ekn to VBM
        ekn -= numpy.max(ekn[:, 2])
        numpy.savez(npz_file,
                    xx=xx,
                    ekn=ekn,
                    X=X)
    else:
        data = numpy.load(npz_file)
        xx = data["xx"]
        ekn = data["ekn"]
        X = data["X"]
    return xx, ekn, X

def plot_band_single(ax, mater, n_layers=1):
    xx, ekn, X = get_band(mater, n_layers)
    ax.plot(xx, ekn, color=get_color(n_layers),
            alpha=0.85)
    # K-path labeling
    xx = numpy.arange(-1, 1.1, 0.5)
    GG = (X[1] - X[0]) * 2
    ticks = xx / (2 * numpy.pi) * GG + X[2]

    # Get Ea plot
    # span = numpy.array([-0.3, 0.3]) / (2 * numpy.pi) * GG + X[2]
    # data = numpy.genfromtxt(os.path.join(data_path, "exciton/{}_eb.csv".format(mater)))
    # n = data[:, 0]; Eb = data[:, 1]
    # eb = Eb[n == n_layers]
    # ax.plot(span, numpy.ones_like(span) * (ekn))
    
    ax.set_xlim(ticks[0], ticks[-1])
    if n_layers == 1:
        # [ax.axvline(x=x_, ls="--", color="grey") for x_ in X]
        # xx = numpy.arange(-1, 1.01, 0.2)
        ax.set_xticks(ticks)  # Offset with K point
        ax.set_xticklabels(map(lambda x: "{:.1f}".format(abs(x)), xx))
        
        # ax.set_xticklabels(["", "K", ""])  #

def plot_ea(ax, mater):
    xx, ekn, X = get_band(mater, 1)
    GG = (X[1] - X[0]) * 2
    span = numpy.array([-0.2, 0.2]) / (2 * numpy.pi) * GG + X[2]
    data = numpy.genfromtxt(os.path.join(data_path,
                                         "exciton/{}_eb.csv".format(mater)),
                            delimiter=",")
    data_eg = numpy.genfromtxt(os.path.join(data_path,
                                            "gw_gap/{}-gwqeh-gap.csv".format(mater)),
                               delimiter=",")
    n_eb = data[:, 0]; eb = data[:, 1]
    n_eg = data_eg[:, 0]; eg = data_eg[:, 1]
    for i in range(1, 16):
        if (i in n_eb) and (i in n_eg):
            ea = eg[n_eg == i] - eb[n_eb == i]
            print(i, ea)
            ax.plot(span, numpy.ones_like(span) * ea, linewidth=0.5,
                    color=get_color(i))
    return
    
def main(n_max=15):
    fig = plt.figure(figsize=(9, 3))
    plt.style.use("science")
    for i, mater in enumerate(materials):
        ax = fig.add_subplot("14{}".format(i+1))
        [plot_band_single(ax, mater, n) for n in range(n_max, 0, -1)]
        plot_ea(ax, mater)
        ax.set_title("{}-GWQEH".format(mater))
        ax.set_ylabel("$E$ (eV)")
        add_cbar(fig, ax)
        ax.set_ylim(-1, 4)
    plt.tight_layout()
    f_name = os.path.join(img_path, "gwqeh_all.svg")
    fig.savefig(f_name)

if __name__ == "__main__":
    import sys
    main()
