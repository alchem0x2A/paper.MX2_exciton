import os, os.path
import shutil
from glob import glob

root_path = os.path.abspath("/cluster/scratch/ttian/QEH")
def mater_path(mater):
    return os.path.join(root_path, "{}".format(mater))

def main(mater):
    for f in glob(os.path.join(mater_path(mater), "gw*")):
        res = os.remove(f)
        print(f, res)
    for f in glob(os.path.join(mater_path(mater), "g0w0*")):
        res = os.remove(f)
        print(f, res)
    for f in glob(os.path.join(mater_path(mater), "*.gpw")):
        res = os.remove(f)
        print(f, res)
    return

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        mater = "MoS2"
    else:
        mater = sys.argv[1]
    main(mater)
        
