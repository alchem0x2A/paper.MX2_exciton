import numpy
from ase.io import read
from gpaw import GPAW, FermiDirac, PW
# from gpaw.response.g0w0 import G0W0
from gpaw.response.df import DielectricFunction
from gpaw.response.qeh import BuildingBlock
from gpaw.response.gwqeh import GWQEHCorrection
from gpaw.response.gw_bands import GWBands
from ase.parallel import parprint, world
import shutil
import glob
from ase.units import Ha
import pickle

import os, os.path

materials = ["MoS2", "MoSe2", "WS2", "WSe2"]

d_list = {"MoS2": 6.15,
          "MoSe2": 6.46,
          "WS2": 6.15,
          "WSe2": 6.49}

mu_dict = {"MoS2": 0.24,
           "MoSe2": 0.27,
           "WS2": 0.17,
           "WSe2": 0.19}

data_path = "/cluster/scratch/ttian/QEH"
# Get ground state wfs
# def traj(mater):
    # return os.path.join(data_path, "{}/relax.traj".format(mater))

def gs_wfs(mater):
    return os.path.join(data_path, "{}/gs.gpw".format(mater))

def es_wfs(mater):
    return os.path.join(data_path, "{}/es.gpw".format(mater))

def g0w0_file(mater):
    return os.path.join(data_path, "{}/g0w0_results.pckl".format(mater))

def bb_file(mater):
    f_name = os.path.join(os.path.curdir, "{}-chi.npz".format(mater))
    if os.path.exists(f_name):
        return f_name
    else:                       # Calculate the BB
        parprint("Chi matrix not calculated, build for now!")
        df = DielectricFunction(calc=es_wfs(mater),
                                eta=0.1,
                                intraband=False,
                                truncation="2D")
        bb = BuildingBlock(mater, df, qmax=3.0)
        bb.calculate_building_block()
        return f_name

def gwqeh(mater, n_layers, band_num=3):
    parprint("Calculate QP correction for {} with {} layers".format(mater, n_layers))
    assert mater in d_list.keys()
    assert n_layers >= 2
    structure = ["{}{}".format(int(n_layers), mater)]
    distances = [d_list[mater] ] * (n_layers - 1)
    d0 = d_list[mater]
    f_out = os.path.join(data_path,
                         "{}/gwqeh_{}".format(mater, n_layers))
    # The GWQEH calculation
    calc = GPAW(restart=gs_wfs(mater))
    ne = calc.get_number_of_electrons()
    nb = int(ne // 2)
    bands = (nb - band_num, nb + band_num)
    del calc
    # Calc GWQEH
    qeh_corr = GWQEHCorrection(calc=es_wfs(mater),
                               gwfile=g0w0_file(mater),
                               filename=f_out,
                               structure=structure,
                               d=distances,
                               layer=int(n_layers // 2),
                               bands=bands,
                               include_q0=True  # Why?
    )
    qeh_corr.calculate_qp_energies()
    # parprint(corr)
    qeh_corr.save_state_file()

def get_gap(mater, n, band_num=3):
    K = numpy.array([1 / 3, 1 / 3, 0])
    G = numpy.array([0.0, 0.0, 0.0])
    kpoints = numpy.array([G, K, G])
    # Some tricks
    if n == 1:
        gw = GWBands(calc=es_wfs(mater),
                     gw_file=g0w0_file(mater),
                     kpoints=kpoints)
        ekn = gw.gw_file["qp"][0]
    else:
        gwqeh_ = os.path.join(data_path,
                              "{}/gwqeh_{}_qeh.npz".format(mater, n))
        ekn = numpy.load(gwqeh_)["Qp_sin"][0] * Ha

    gap = numpy.min(ekn[:, band_num] - ekn[:, band_num - 1])  # band do not shift
    # if n > 1:
        # f = numpy.load(gwqeh_)
        # gw.gw_file["qp"] = f["Qp_sin"] * Ha  # Try to replace!

    # res = gw.get_gw_bands(interpolate=True, vac=True)  # No gwqeh file
    return gap

def main(mater, n_max=10):
    # Delete all previous files
    if world.rank == 0:
        for f in glob.glob(os.path.join(data_path, "{}/gwqeh*".format(mater))):
            os.remove(f)
    world.barrier()
    for n in range(2, n_max):
        parprint(n)
        gwqeh(mater, n_layers=n)    # Just try!
    res = []
    for n in range(1, n_max):
        print(n)
        gap = get_gap(mater, n)
        res.append((n, gap))
    res = numpy.array(res)
    parprint(res)
    return

if __name__ == "__main__":
    import sys
    assert len(sys.argv) == 2
    mater = sys.argv[1]
    main(mater)
