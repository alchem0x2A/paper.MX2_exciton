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
res_path = os.path.join(os.path.dirname(__file__), "../../results/")

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

def get_eb(mat, n_layers):
    hs = construct(mat, n_layers)
    mu = mu_dict[mat]
    e_distr = numpy.zeros(n_layers * 2)
    h_distr = numpy.zeros(n_layers * 2)
    index_center = n_layers // 2
    e_distr[(index_center - 1) * 2] = 1
    h_distr[(index_center - 1) * 2] = 1
    ee, ev = hs.get_exciton_binding_energies(eff_mass=mu,
                                             e_distr=e_distr,
                                             h_distr=h_distr)
    return ee[0].real
    

def main():
    mat_list = ["MoS2", "MoSe2", "WS2", "WSe2"]
    
    for mat in mat_list:
        results = []
        for i in range(1, 20):
            print(mat, i)
            eb = get_eb(mat, i)
            results.append((i, eb))
        results = numpy.array(results)
        f_name = os.path.join(res_path, "{}_eb.csv".format(mat))
        numpy.savetxt(f_name, X=results, delimiter=",", header="N, Eb(eV)")
    

if __name__ == "__main__":
    main()
    # hs = construct("MoS2", 3)
    # e_dist = numpy.zeros(6)
    # h_dist = numpy.zeros(6)
    # e_dist[4] = 1
    # h_dist[4] = 1
    # print(e_dist)
    # ee, ev = hs.get_exciton_binding_energies(eff_mass=mu_dict["MoS2"],
    #                                          e_distr=e_dist,
    #                                          h_distr=h_dist)
    # print(ee[0])
    
    
