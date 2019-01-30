import numpy
import matplotlib.pyplot as plt
from gpaw.response.gw_bands import GWBands
import os, os.path


materials = ["MoS2", "MoSe2", "WS2", "WSe2"]
data_path = "/cluster/scratch/ttian/QEH"
def es_wfs(mater):
    return os.path.join(data_path, "{}/es.gpw".format(mater))
def g0w0_file(mater):
    return os.path.join(data_path, "{}/g0w0_results.pckl".format(mater))

def get_band(mater):
    K = numpy.array([1 / 3, 1 / 3, 0])
    G = numpy.array([0.0, 0.0, 0.0])
    kpoints = numpy.array([G, K, G])
    gw = GWBands(calc=es_wfs(mater),
                 gw_file=g0w0_file(mater),
                 kpoints=kpoints)
    res = gw.get_gw_bands(interpolate=True, vac=True)
    print(res.keys())
    xx = res["x_k"]
    ekn = res["e_kn"]
    return xx, ekn

def plot_band(mater):
    xx, ekn = get_band(mater)
    plt.figure()
    plt.plot(xx, ekn)
    plt.show()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        mater = "MoS2"
    else:
        mater = sys.argv[1]

    plot_band(mater)
