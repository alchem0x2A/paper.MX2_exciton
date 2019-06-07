import numpy
from gpaw import GPAW
from gpaw.response import g0w0, gwqeh, qeh
import os, os.path

materials = ["MoS2", "MoSe2", "WS2", "WSe2"]
data_path = "/cluster/scratch/ttian/cluster/scratch/ttian/QEH"
# Get ground state wfs
def gs_wfs(mater):
    return os.path.join(data_path, "{}/es.gpw".format(mater))

def calc_gw(mater, ecut=250, band_num=3):
    calc = GPAW(restart=gs_wfs(mater))
    ne = calc.get_number_of_electrons()
    nb = ne // 2
    bands = (nb - band_num, nb + band_num)
    del calc
    calc = G0W0(calc=gs_wfs(mater),
                bands=bands,
                ecut=ecut,
                ecut_extrapolation=True,
                truncation="2D",
                q0_correction=True,
                filename=os.path.join(data_path, mater, "g0w0"),
                restartfile=os.path.join(data_path, mater, "g0w0.tmp"),
                savepckl=True)
    calc.calculate()
