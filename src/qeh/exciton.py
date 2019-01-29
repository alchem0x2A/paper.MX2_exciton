from gpaw.response.qeh import Heterostructure
import numpy
import os, os.path
import shutil

d_list = {"MoS2": 6.15,
          "MoSe2": 6.46,
          "WS2": 6.15,
          "WSe2": 6.49}

mu_dict = {"MoS2": 0.24,
           "MoSe2": 0.27,
           "WS2": 0.17,
           "WSe2": 0.19}

data_path = os.path.join(os.path.dirname(__file__), "../../data/chi/")

def construct(mat, n_layers):
    assert mat in d_list.keys()
    assert n_layers >= 1
    structure = ["{}{}".format(int(n_layers), mat)]
    distances = [d_list[mat] ] * (n_layers - 1)
    d0 = d_list[mat]
    cur_path = os.path.abspath(os.path.curdir)
    ch_file = os.path.join(data_path, "{}-chi.npz".format(mat))
    # ch_file_new = 
    ch_copied = shutil.copy(ch_file, cur_path)
    hs = Heterostructure(structure=structure,
                         d=distances,
                         d0=d0,
                         wmax=0,
                         qmax=1)
    os.remove(ch_copied)        # remove tmp file
    return hs


if __name__ == "__main__":
    hs = construct("MoS2", 3)
    e_dist = numpy.zeros(6)
    h_dist = numpy.zeros(6)
    e_dist[4] = 1
    h_dist[4] = 1
    print(e_dist)
    ee, ev = hs.get_exciton_binding_energies(eff_mass=mu_dict["MoS2"],
                                             e_distr=e_dist,
                                             h_distr=h_dist)
    print(ee[0])
