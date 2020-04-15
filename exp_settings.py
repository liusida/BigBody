import random
import numpy as np
from voxelyze.helper import cprint

seed = 1010
random.seed(seed)
np.random.seed(seed)

# ============== should be able to change during evolution: ================
#  Plan: evolve a 100x100x100 body
#  target generation = 500
# 1. effect at this generation:
# only if fitness score pass new height multiple times, increase body dimension
# otherwise, keep adapting.

best_last_round = 0
body_dimension_n = 30
fitness_score_surpass_time = 0

def init_body_dimension_n(n):
    global body_dimension_n
    body_dimension_n = n

def body_dimension(generation=0, fitness_scores=[0]):
    return [6,6,6]

# 2. effect between this generation and the next:
def mutation_rate(generation=0):
    # every 10 time, change activation function 1 time.
    # weight change std 0.1
    ret = [20, 0.1]
    return ret

# 3. effect at next generation:
def target_population_size(generation=0):
    return 10

# =================== cannot change during evolution: =======================
experiment_name = f"BB{seed}"
hidden_layers = [10,10,10]
