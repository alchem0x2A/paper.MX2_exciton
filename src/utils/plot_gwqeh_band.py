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
    K = numpy.array([1 / 3, 1 / 3, 0])
    M = numpy.array([1 / 2, 0, 0])
    G = numpy.array([0.0, 0.0, 0.0])
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
    return xx, ekn, X

def plot_band_single(ax, mater, n_layers=1):
    xx, ekn, X = get_band(mater, n_layers)
    ax.plot(xx, ekn, color=get_color(n_layers),
            alpha=0.85)
    # K-path labeling
    if n_layers == 1:
        [ax.axvline(x=x_, ls="--", color="grey") for x_ in X]
        ax.set_xticks(X)
        ax.set_xticklabels(["$\\Gamma$", "M", "K", "$\\Gamma$"])  #

def main(mater, n_max=15):
    fig = plt.figure(figsize=(3.5, 2.8))
    plt.style.use("science")
    ax = fig.add_subplot(111)
    [plot_band_single(ax, mater, n) for n in range(n_max, 0, -1)]
    ax.set_title("{}-GWQEH".format(mater))
    ax.set_ylabel("$E$ (eV)")
    add_cbar(fig, ax)
    ax.set_ylim(-2, 4)
    plt.tight_layout()
    f_name = os.path.join(img_path, "{}-gwqeh-band.pdf".format(mater))
    fig.savefig(f_name)

if __name__ == "__main__":
    import sys
    for mater in materials:
        main(mater)
