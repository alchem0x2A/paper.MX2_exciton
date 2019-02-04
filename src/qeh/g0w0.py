import numpy
from ase.io import read
from gpaw import GPAW, FermiDirac, PW
from gpaw.response.g0w0 import G0W0
# from gpaw.response.gwqeh g0w0, gwqeh, qeh
import os, os.path

materials = ["MoS2", "MoSe2", "WS2", "WSe2"]
data_path = "/cluster/scratch/ttian/QEH"
nbs = 100
# Get ground state wfs
def traj(mater):
    return os.path.join(data_path, "{}/relax.traj".format(mater))

def gs_wfs(mater):
    return os.path.join(data_path, "{}/gs.gpw".format(mater))

def es_wfs(mater):
    return os.path.join(data_path, "{}/es.gpw".format(mater))

def calc_es(mater,
            dens=5,             # make sure high symmetry points contain
            ecut=800,
            nbands=nbs,
            vacuum=12):
    mol = read(traj(mater))
    mol.cell[-1][-1] = vacuum
    mol.center()
    calc = GPAW(mode=PW(ecut=ecut),
                xc="PBE",
                kpts=dict(gamma=True, density=dens),
                occupations=FermiDirac(0.01),
                poissonsolver=dict(dipolelayer="xy"))
    calc.atoms = mol
    calc.get_potential_energy()
    calc.write(gs_wfs(mater), mode="all")
    # ES
    calc = GPAW(restart=gs_wfs(mater),
                fixdensity=True,
                nbands=nbands,
                kpts=dict(gamma=True, density=dens),
                convergence=dict(bands=-5),
                parallel=dict(kpt=1))
    calc.get_potential_energy()
    calc.diagonalize_full_hamiltonian(nbands=nbands)
    calc.write(es_wfs(mater), mode="all")
    return True
            

def calc_gw(mater, band_num=3):
    if not os.path.exists(es_wfs(mater)):
        calc_es(mater)
    calc = GPAW(restart=gs_wfs(mater))
    ne = calc.get_number_of_electrons()
    nb = int(ne // 2)
    bands = (nb - band_num, nb + band_num)
    print(bands)
    del calc
    calc = G0W0(calc=es_wfs(mater),
                nbands=nbs,
                bands=bands,
                nblocksmax=True,
                # ecut_extrapolation=True,
                truncation="2D",
                q0_correction=True,
                filename=os.path.join(data_path, mater, "g0w0"),
                restartfile=os.path.join(data_path, mater, "g0w0.tmp"),
                savepckl=True)
    calc.calculate()


if __name__ == "__main__":
    import sys
    assert len(sys.argv) == 2
    mater = sys.argv[1]
    calc_gw(mater)
