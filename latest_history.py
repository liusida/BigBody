# show the latest history file
# and 
# ./VoxCAD `python latest_history.py`
#
import glob, os
abs_path = os.path.dirname(os.path.abspath(__file__))
exps = glob.glob(f"{abs_path}/data/experiment_*")
exp = sorted(exps)[-1]
gens = glob.glob(f"{exp}/gene*")
gen = sorted(gens)[-2]
history = f"{gen}/bestfit/bestfit.history"
print(history)