import numpy
import matplotlib.pyplot as plt
from gpaw.response.gw_bands import GWBands
import os, os.path


materials = ["MoS2", "MoSe2", "WS2", "WSe2"]
data_path = os.path.join(os.path.dirname(__file__), "../../results")

def es_wfs(mater):
    return os.path.join(data_path, "gw_bs/{}/es.gpw".format(mater))

def g0w0_file(mater):
    return os.path.join(data_path, "gw_bs/{}/g0w0_results.pckl".format(mater))

def get_band(mater):
    K = numpy.array([1 / 3, 1 / 3, 0])
    M = numpy.array([1 / 2, 0, 0])
    G = numpy.array([0.0, 0.0, 0.0])
<<<<<<< HEAD
=======
    M = numpy.array([1 / 2, 0, 0])
>>>>>>> dd4da4870227272bd74c7549f581c3fece8bffcf
    kpoints = numpy.array([G, M, K, G])
    gw = GWBands(calc=es_wfs(mater),
                 gw_file=g0w0_file(mater),
                 kpoints=kpoints)
    res = gw.get_gw_bands(interpolate=True, vac=True)
    print(res.keys())
    xx = res["x_k"]
    ekn = res["e_kn"]
    X = res["X"]
    return xx, ekn, X

def plot_band(mater):
    xx, ekn, X = get_band(mater)
    plt.figure()
    plt.plot(xx, ekn, color="b")
    # K-path labeling
    [plt.axvline(x=x_, ls="--", color="grey") for x_ in X]
    plt.xticks(X, ["G", "M", "K", "G"])  #
    plt.show()
    # plt.save("{}.png".format(mater))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        mater = "MoS2"
    else:
        mater = sys.argv[1]

    plot_band(mater)
