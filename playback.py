# play the latest history file
import glob, os

exps = glob.glob(f"data/experiment_*")
exp = sorted(exps)[-1]
gens = glob.glob(f"{exp}/gene*")
gen = sorted(gens)[-2]
history = f"{gen}/bestfit/bestfit.history"

os.system(f"./VoxCAD {history}&")
